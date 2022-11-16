# ATOP binary log parser for forensic purposes
This is a partial implementation of parsing ATOP binary log files with python. It uses the `dissect.cstruct` library which makes life worth living for if you want to work with C structures in python.

Feel free to add example data and update the code. Only reason this is licensed as AGPL is due to the original license of `dissect.cstruct`. Do let me know if it is NOT necessary to license this code as AGPL, since I'm not a big fan of this license.

Companion blog: https://diablohorn.com/2022/11/17/parsing-atop-files-with-python-dissect-cstruct/
# Examples
You run this with the assumption that you know the version that created the file. you can easily adapt the code to just guess the version number.

Command: 

`python atopdump.py 27 example_data/v2.7/atop_20221111` 

Output (line breaks for clarity only): 

`{"rawheader": {"magic": 4276993775, "aversion": 33287, "future1": 0, "future2": 0, "rawheadlen": 480, "rawreclen": 96, "hertz": 100, "sfuture": [0, 0, 0, 0, 0,} 

{"rawrecord": {"curtime": 1668196310, "flags": 49, "sfuture": [0, 0, 0], "scomplen": 1520, "pcomplen": 6786, "interval": 66, "ndeviat": 174, "nactproc": 134, "} 

{"tstat": {"gen": {"tgid": 1, "pid": 1, "ppid": 0, "ruid": 0, "euid": 0, "suid": 0, "fsuid": 0, "rgid": 0, "egid": 0, "sgid": 0, "fsgid": 0, "nthr": 1, "name":} 

{"tstat": {"gen": {"tgid": 2, "pid": 2, "ppid": 0, "ruid": 0, "euid": 0, "suid": 0, "fsuid": 0, "rgid": 0, "egid": 0, "sgid": 0, "fsgid": 0, "nthr": 1, "name":} 

{"tstat": {"gen": {"tgid": 3, "pid": 3, "ppid": 2, "ruid": 0, "euid": 0, "suid": 0, "fsuid": 0, "rgid": 0, "egid": 0, "sgid": 0, "fsgid": 0, "nthr": 1, "name":}
`