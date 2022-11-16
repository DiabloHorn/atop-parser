#!/usr/bin/env
"""dump atop information from binary log files"""
import json
import sys
import zlib
from io import BufferedReader, BytesIO

from dissect import cstruct
from dissect.cstruct.types import Instance

import atopstructs


def get_version(version_raw: bytes) -> str:
    """Retrieve version from binary log file

    Args:
        version_raw (any): The binary packed version

    Returns:
        str: The version number of atop that created the file
    """
    version_mayor = (version_raw >> 8) & 0x7F
    version_minor = version_raw & 0xFF
    return f"{version_mayor}.{version_minor}"


def struct2json(structobj: Instance) -> str:
    """Convert a structure instance to a json

    Args:
        structobj (Instance): The structure instance that we want to convert to json

    Returns:
        str: json with the full structure
    """
    # structure including the structure name
    fullstruct = {}
    # structure with just the content, not the name
    outputstruct = {}
    structname = structobj._type.name # pylint: disable=protected-access

    # Use original dissect.cstruct as a reference
    # https://github.com/fox-it/dissect.cstruct/blob/5b290b26db8f1e498c152703c151c156225f4594/dissect/cstruct/utils.py#L117
    for field in structobj._type.fields: # pylint: disable=protected-access
        value = getattr(structobj, field.name)
        # json doesn't allow bytes to be serialized
        # convert process name/cmdline into ascii
        # convert bytes type to their hex representation
        # we can convert back by using bytes.fromhex()
        if isinstance(value, bytes):
            value = value.hex()

        # Do a 1 layer deep check for nested structure instances
        if isinstance(value, Instance):
            outputstruct[field.name] = {}
            for ifield in value._type.fields: # pylint: disable=protected-access
                ivalue = getattr(value, ifield.name)
                # of cours we need to repeat the conversion to ascii/hex
                if isinstance(ivalue, bytes):
                    if ifield.name == "name":
                        ivalue = ivalue.decode("ascii").strip("\x00")
                    elif ifield.name == "cmdline":
                        ivalue = ivalue.decode("ascii").strip("\x00")
                    else:
                        ivalue = ivalue.hex()
                # nest the nested structure field under the original name
                outputstruct[field.name][ifield.name] = ivalue
        else:
            outputstruct[field.name] = value
    # inefficient, but readable merge the name and content of the structure
    fullstruct[structname] = outputstruct
    return json.dumps(fullstruct)


def atop_header(fbinfile: BufferedReader) -> Instance:
    """Retrieves the parsed atop rawheader

    Args:
        fbinfile (BufferedReader): A file handle to the binary log file

    Returns:
        Instance: The rawheader data parsed as the correct structure
    """
    rawheader_len = len(cparser.rawheader)

    rawheader_data = fbinfile.read(rawheader_len)
    rawheader_parsed = cparser.rawheader(rawheader_data)
    return rawheader_parsed


def atop_records_compressed(fbinfile: BufferedReader, rawheader: any) -> dict:
    """Returns the rawrecord, compressed system, compressed process data

    Args:
        fbinfile (BufferedReader): A file handle to the binary log file
        rawheader (any): The parsed rawheader data

    Returns:
        dict: None when EOF is encountered

    Yields:
        Iterator[dict]: Contains the parsed rawrecord, compressed system data,
                        compressed process data
    """
    # trust the header record len instead of our own structure
    rawrecord_len = rawheader.rawreclen
    while True:
        rawrecord_data = fbinfile.read(rawrecord_len)
        if not rawrecord_data:
            # EOF
            return
        rawrecord_parsed = cparser.rawrecord(rawrecord_data)
        systemlevel_data_len = rawrecord_parsed.scomplen
        processlevel_data_len = rawrecord_parsed.pcomplen
        systemlevel_data_compressed = fbinfile.read(systemlevel_data_len)
        processlevel_data_compressed = fbinfile.read(processlevel_data_len)
        # we could also decompress, but we want to decouple decompression from parsing
        # this helps in also having the raw data available for debug/verification purposes
        yield {
            "rawrecord": rawrecord_parsed,
            "systemlevel_compressed": systemlevel_data_compressed,
            "processlevel_compressed": processlevel_data_compressed,
        }


def decompress_systemlevel() -> NotImplemented:
    """Not implemented

    Returns:
        NotImplemented: Not implemented
    """
    # Feel free to add parsing for this.
    raise NotImplementedError


def decompress_processlevel(rawrecord: Instance, process_compressed: bytes) -> Instance:
    """Decompress the process information & parse into correct structure

    Args:
        rawrecord (Instance): rawrecord that comes before the system/process level compressed data
        process_compressed (bytes): the raw bytes that are compressed with zlib

    Returns:
        Instance: an instance of the tstat structure
    """
    processlevel_data = BytesIO(zlib.decompress(process_compressed))
    for _ in range(rawrecord.ndeviat):
        try:
            task_parsed = cparser.tstat(processlevel_data)
        except EOFError as eof_error:
            print(f"[!] {eof_error}", file=sys.stderr)
            continue
        yield (task_parsed)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"{sys.argv[0]} <version> <atop binary file>")
        sys.exit()

    atopversion = int(sys.argv[1]) # pylint: disable=invalid-name
    cparser = None # pylint: disable=invalid-name
    # https://stackoverflow.com/a/70967367
    for cls in map(atopstructs.__dict__.get, atopstructs.__all__):
        if atopversion >= cls.VERSIONMIN and atopversion <= cls.VERSIONMAX:
            cparser = cstruct.cstruct()
            cparser.load(cls.TYPEDEFS)
            cparser.load(cls.UTSNAME, align=True)
            cparser.load(cls.RAWHEADER, align=True)
            cparser.load(cls.RAWRECORD, align=True)
            cparser.load(cls.PROCS, align=True)

    if cparser is None:
        print("[!] Failed to find structs", file=sys.stderr)
        sys.exit()

    atopbinfile = open(sys.argv[2], "rb")
    atop_rheader = atop_header(atopbinfile)

    # ensure we are parsing the right version
    # you can skip this if you just want to yolo
    atopbinfile_version = int(get_version(atop_rheader.aversion).replace(".", ""))
    if atopversion != atopbinfile_version:
        print(
            f"[!] Version mismatch file:{atopbinfile_version} arg:{atopversion}",
            file=sys.stderr,
        )
        sys.exit()

    print(struct2json(atop_rheader))
    atop_rcompressed = atop_records_compressed(atopbinfile, atop_rheader)
    for record_compressed in atop_rcompressed:
        print(struct2json(record_compressed["rawrecord"]))
        for process_entry in decompress_processlevel(
            record_compressed["rawrecord"], record_compressed["processlevel_compressed"]
        ):
            print(struct2json(process_entry))
    atopbinfile.close()
