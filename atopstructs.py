"""Store C structures for atop"""
# Make sure you add your class here
__all__ = ['V27', 'V26']

## TEMPLATE CLASS
## Copy this template to add new structures for other versions
# class VXX:
#     """atop structures"""
#     VERSIONMIN = XX
#     VERSIONMAX = XX
#     DOCS = """
#     """

#     TYPEDEFS = """
#     typedef unsigned long long time_t;
#     typedef long long count_t;
#     """
#     UTSNAME = """
#     #define _UTSNAME_LENGTH 65
#     struct utsname {
#         /* Name of the implementation of the operating system.  */
#         char sysname[_UTSNAME_LENGTH];

#         /* Name of this node on the network.  */
#         char nodename[_UTSNAME_LENGTH];

#         /* Current release level of this implementation.  */
#         char release[_UTSNAME_LENGTH];
#         /* Current version level of this release.  */
#         char version[_UTSNAME_LENGTH];

#         /* Name of the hardware type the system is running on.  */
#         char machine[_UTSNAME_LENGTH];

#         /* Name of the domain of this node on the network.  */
#         char domainname[_UTSNAME_LENGTH];
#     };
#     """ 
#     RAWHEADER = """
#     """
#     RAWRECORD = """
#     """
#     PROCS = """
#     """

class V27:
    """atop structures"""
    VERSIONMIN = 27
    VERSIONMAX = 27
    DOCS = """
    From the original file: https://github.com/Atoptool/atop/blob/master/rawlog.h
    ** structure describing the raw file contents
    **
    ** layout raw file:    rawheader
    **
    **                     rawrecord                           \
    **                     compressed system-level statistics   | sample 1
    **                     compressed process-level statistics /
    **
    **                     rawrecord                           \
    **                     compressed system-level statistics   | sample 2
    **                     compressed process-level statistics /
    **
    ** etcetera .....
    """

    TYPEDEFS = """
    typedef unsigned long long time_t;
    typedef long long count_t;
    """
    UTSNAME = """
    #define _UTSNAME_LENGTH 65
    struct utsname {
        /* Name of the implementation of the operating system.  */
        char sysname[_UTSNAME_LENGTH];

        /* Name of this node on the network.  */
        char nodename[_UTSNAME_LENGTH];

        /* Current release level of this implementation.  */
        char release[_UTSNAME_LENGTH];
        /* Current version level of this release.  */
        char version[_UTSNAME_LENGTH];

        /* Name of the hardware type the system is running on.  */
        char machine[_UTSNAME_LENGTH];

        /* Name of the domain of this node on the network.  */
        char domainname[_UTSNAME_LENGTH];
    };
    """ 

    RAWHEADER = """
    struct rawheader {
        unsigned int	magic;

        unsigned short	aversion;	/* creator atop version with MSB */
        unsigned short	future1;	/* can be reused 		 */
        unsigned short	future2;	/* can be reused 		 */
        unsigned short	rawheadlen;	/* length of struct rawheader    */
        unsigned short	rawreclen;	/* length of struct rawrecord    */
        unsigned short	hertz;		/* clock interrupts per second   */
        unsigned short	sfuture[6];	/* future use                    */
        unsigned int	sstatlen;	/* length of struct sstat        */
        unsigned int	tstatlen;	/* length of struct tstat        */
        struct utsname	utsname;	/* info about this system        */
        char		cfuture[8];	/* future use                    */

        unsigned int	pagesize;	/* size of memory page (bytes)   */
        int		supportflags;  	/* used features                 */
        int		osrel;		/* OS release number             */
        int		osvers;		/* OS version number             */
        int		ossub;		/* OS version subnumber          */
        int		ifuture[6];	/* future use                    */
    };
    """
    RAWRECORD = """
    struct rawrecord {
        time_t		curtime;	/* current time (epoch)         */

        unsigned short	flags;		/* various flags                */
        unsigned short	sfuture[3];	/* future use                   */

        unsigned int	scomplen;	/* length of compressed sstat   */
        unsigned int	pcomplen;	/* length of compressed tstat's */
        unsigned int	interval;	/* interval (number of seconds) */
        unsigned int	ndeviat;	/* number of tasks in list      */
        unsigned int	nactproc;	/* number of processes in list  */
        unsigned int	ntask;		/* total number of tasks        */
        unsigned int    totproc;	/* total number of processes	*/
        unsigned int    totrun;		/* number of running  threads	*/
        unsigned int    totslpi;	/* number of sleeping threads(S)*/
        unsigned int    totslpu;	/* number of sleeping threads(D)*/
        unsigned int	totzomb;	/* number of zombie processes   */
        unsigned int	nexit;		/* number of exited processes   */
        unsigned int	noverflow;	/* number of overflow processes */
        unsigned int	ifuture[6];	/* future use                   */
    };
    """
    PROCS = """
    #define	PNAMLEN		15
    #define	CMDLEN		255
    
    /* 
    ** structure containing only relevant process-info extracted 
    ** from kernel's process-administration
    */
    struct tstat {
        /* GENERAL TASK INFO 					*/
        struct gen {
            int	tgid;		/* threadgroup identification 	*/
            int	pid;		/* process identification 	*/
            int	ppid;           /* parent process identification*/
            int	ruid;		/* real  user  identification 	*/
            int	euid;		/* eff.  user  identification 	*/
            int	suid;		/* saved user  identification 	*/
            int	fsuid;		/* fs    user  identification 	*/
            int	rgid;		/* real  group identification 	*/
            int	egid;		/* eff.  group identification 	*/
            int	sgid;		/* saved group identification 	*/
            int	fsgid;		/* fs    group identification 	*/
            int	nthr;		/* number of threads in tgroup 	*/
            char	name[PNAMLEN+1];/* process name string       	*/
            char 	isproc;		/* boolean: process level?      */
            char 	state;		/* process state ('E' = exited)	*/
            int	excode;		/* process exit status		*/
            time_t 	btime;		/* process start time (epoch)	*/
            time_t 	elaps;		/* process elaps time (hertz)	*/
            char	cmdline[CMDLEN+1];/* command-line string       	*/
            int	nthrslpi;	/* # threads in state 'S'       */
            int	nthrslpu;	/* # threads in state 'D'       */
            int	nthrrun;	/* # threads in state 'R'       */

            int	ctid;		/* OpenVZ container ID		*/
            int	vpid;		/* OpenVZ virtual PID		*/

            int	wasinactive;	/* boolean: task inactive	*/

            char	container[16];	/* Docker container id (12 pos)	*/
        } gen;

        /* CPU STATISTICS						*/
        struct cpu {
            count_t	utime;		/* time user   text (ticks) 	*/
            count_t	stime;		/* time system text (ticks) 	*/
            int	nice;		/* nice value                   */
            int	prio;		/* priority                     */
            int	rtprio;		/* realtime priority            */
            int	policy;		/* scheduling policy            */
            int	curcpu;		/* current processor            */
            int	sleepavg;       /* sleep average percentage     */
            int	ifuture[4];	/* reserved for future use	*/
            char	wchan[16];	/* wait channel string    	*/
            count_t	rundelay;	/* schedstat rundelay (nanosec)	*/
            count_t	cfuture[1];	/* reserved for future use	*/
        } cpu;

        /* DISK STATISTICS						*/
        struct dsk {
            count_t	rio;		/* number of read requests 	*/
            count_t	rsz;		/* cumulative # sectors read	*/
            count_t	wio;		/* number of write requests 	*/
            count_t	wsz;		/* cumulative # sectors written	*/
            count_t	cwsz;		/* cumulative # written sectors */
                        /* being cancelled              */
            count_t	cfuture[4];	/* reserved for future use	*/
        } dsk;

        /* MEMORY STATISTICS						*/
        struct mem {
            count_t	minflt;		/* number of page-reclaims 	*/
            count_t	majflt;		/* number of page-faults 	*/
            count_t	vexec;		/* virtmem execfile (Kb)        */
            count_t	vmem;		/* virtual  memory  (Kb)	*/
            count_t	rmem;		/* resident memory  (Kb)	*/
            count_t	pmem;		/* resident memory  (Kb)	*/
            count_t vgrow;		/* virtual  growth  (Kb)    	*/
            count_t rgrow;		/* resident growth  (Kb)     	*/
            count_t vdata;		/* virtmem data     (Kb)     	*/
            count_t vstack;		/* virtmem stack    (Kb)     	*/
            count_t vlibs;		/* virtmem libexec  (Kb)     	*/
            count_t vswap;		/* swap space used  (Kb)     	*/
            count_t	vlock;		/* virtual locked   (Kb) 	*/
            count_t	cfuture[3];	/* reserved for future use	*/
        } mem;

        /* NETWORK STATISTICS						*/
        struct net {
            count_t tcpsnd;		/* number of TCP-packets sent	*/
            count_t tcpssz;		/* cumulative size packets sent	*/
            count_t	tcprcv;		/* number of TCP-packets recved	*/
            count_t tcprsz;		/* cumulative size packets rcvd	*/
            count_t	udpsnd;		/* number of UDP-packets sent	*/
            count_t udpssz;		/* cumulative size packets sent	*/
            count_t	udprcv;		/* number of UDP-packets recved	*/
            count_t udprsz;		/* cumulative size packets sent	*/
            count_t	avail1;		/* */
            count_t	avail2;		/* */
            count_t	cfuture[4];	/* reserved for future use	*/
        } net;

        struct gpu {
            char	state;		// A - active, E - Exit, '\0' - no use
            char	cfuture[3];	//
            short	nrgpus;		// number of GPUs for this process
            int32_t	gpulist;	// bitlist with GPU numbers

            int	gpubusy;	// gpu busy perc process lifetime      -1 = n/a
            int	membusy;	// memory busy perc process lifetime   -1 = n/a
            count_t	timems;		// milliseconds accounting   -1 = n/a
                        // value 0   for active process,
                        // value > 0 after termination

            count_t	memnow;		// current    memory consumption in KiB
            count_t	memcum;		// cumulative memory consumption in KiB
            count_t	sample;		// number of samples
        } gpu;
    """
class V26:
    """atop structures"""
    VERSIONMIN = 26
    VERSIONMAX = 26
    DOCS = """
    From the original file: https://github.com/Atoptool/atop/blob/master/rawlog.h
    ** structure describing the raw file contents
    **
    ** layout raw file:    rawheader
    **
    **                     rawrecord                           \
    **                     compressed system-level statistics   | sample 1
    **                     compressed process-level statistics /
    **
    **                     rawrecord                           \
    **                     compressed system-level statistics   | sample 2
    **                     compressed process-level statistics /
    **
    ** etcetera .....
    """
    TYPEDEFS = """
    typedef unsigned long long time_t;
    typedef long long count_t;
    """
    UTSNAME = """
    #define _UTSNAME_LENGTH 65
    struct utsname {
        /* Name of the implementation of the operating system.  */
        char sysname[_UTSNAME_LENGTH];

        /* Name of this node on the network.  */
        char nodename[_UTSNAME_LENGTH];

        /* Current release level of this implementation.  */
        char release[_UTSNAME_LENGTH];
        /* Current version level of this release.  */
        char version[_UTSNAME_LENGTH];

        /* Name of the hardware type the system is running on.  */
        char machine[_UTSNAME_LENGTH];

        /* Name of the domain of this node on the network.  */
        char domainname[_UTSNAME_LENGTH];
    };
    """ 

    RAWHEADER = """
    struct rawheader {
        unsigned int	magic;

        unsigned short	aversion;	/* creator atop version with MSB */
        unsigned short	future1;	/* can be reused 		 */
        unsigned short	future2;	/* can be reused 		 */
        unsigned short	rawheadlen;	/* length of struct rawheader    */
        unsigned short	rawreclen;	/* length of struct rawrecord    */
        unsigned short	hertz;		/* clock interrupts per second   */
        unsigned short	sfuture[6];	/* future use                    */
        unsigned int	sstatlen;	/* length of struct sstat        */
        unsigned int	tstatlen;	/* length of struct tstat        */
        struct utsname	utsname;	/* info about this system        */
        char		cfuture[8];	/* future use                    */

        unsigned int	pagesize;	/* size of memory page (bytes)   */
        int		supportflags;  	/* used features                 */
        int		osrel;		/* OS release number             */
        int		osvers;		/* OS version number             */
        int		ossub;		/* OS version subnumber          */
        int		ifuture[6];	/* future use                    */
    };
    """
    RAWRECORD = """
    struct rawrecord {
        time_t		curtime;	/* current time (epoch)         */

        unsigned short	flags;		/* various flags                */
        unsigned short	sfuture[3];	/* future use                   */

        unsigned int	scomplen;	/* length of compressed sstat   */
        unsigned int	pcomplen;	/* length of compressed tstat's */
        unsigned int	interval;	/* interval (number of seconds) */
        unsigned int	ndeviat;	/* number of tasks in list      */
        unsigned int	nactproc;	/* number of processes in list  */
        unsigned int	ntask;		/* total number of tasks        */
        unsigned int    totproc;	/* total number of processes	*/
        unsigned int    totrun;		/* number of running  threads	*/
        unsigned int    totslpi;	/* number of sleeping threads(S)*/
        unsigned int    totslpu;	/* number of sleeping threads(D)*/
        unsigned int	totzomb;	/* number of zombie processes   */
        unsigned int	nexit;		/* number of exited processes   */
        unsigned int	noverflow;	/* number of overflow processes */
        unsigned int	ifuture[6];	/* future use                   */
    };
    """
    PROCS = """
    #define	PNAMLEN		15
    #define	CMDLEN		255

    /* 
    ** structure containing only relevant process-info extracted 
    ** from kernel's process-administration
    */
    struct tstat {
        /* GENERAL TASK INFO 					*/
        struct gen {
            int	tgid;		/* threadgroup identification 	*/
            int	pid;		/* process identification 	*/
            int	ppid;           /* parent process identification*/
            int	ruid;		/* real  user  identification 	*/
            int	euid;		/* eff.  user  identification 	*/
            int	suid;		/* saved user  identification 	*/
            int	fsuid;		/* fs    user  identification 	*/
            int	rgid;		/* real  group identification 	*/
            int	egid;		/* eff.  group identification 	*/
            int	sgid;		/* saved group identification 	*/
            int	fsgid;		/* fs    group identification 	*/
            int	nthr;		/* number of threads in tgroup 	*/
            char	name[PNAMLEN+1];/* process name string       	*/
            char 	isproc;		/* boolean: process level?      */
            char 	state;		/* process state ('E' = exited)	*/
            int	excode;		/* process exit status		*/
            time_t 	btime;		/* process start time (epoch)	*/
            time_t 	elaps;		/* process elaps time (hertz)	*/
            char	cmdline[CMDLEN+1];/* command-line string       	*/
            int	nthrslpi;	/* # threads in state 'S'       */
            int	nthrslpu;	/* # threads in state 'D'       */
            int	nthrrun;	/* # threads in state 'R'       */

            int	ctid;		/* OpenVZ container ID		*/
            int	vpid;		/* OpenVZ virtual PID		*/

            int	wasinactive;	/* boolean: task inactive	*/

            char	container[16];	/* Docker container id (12 pos)	*/
        } gen;

        /* CPU STATISTICS						*/
        struct cpu {
            count_t	utime;		/* time user   text (ticks) 	*/
            count_t	stime;		/* time system text (ticks) 	*/
            int	nice;		/* nice value                   */
            int	prio;		/* priority                     */
            int	rtprio;		/* realtime priority            */
            int	policy;		/* scheduling policy            */
            int	curcpu;		/* current processor            */
            int	sleepavg;       /* sleep average percentage     */
            int	ifuture[4];	/* reserved for future use	*/
            char	wchan[16];	/* wait channel string    	*/
            count_t	rundelay;	/* schedstat rundelay (nanosec)	*/
            count_t	cfuture[1];	/* reserved for future use	*/
        } cpu;

        /* DISK STATISTICS						*/
        struct dsk {
            count_t	rio;		/* number of read requests 	*/
            count_t	rsz;		/* cumulative # sectors read	*/
            count_t	wio;		/* number of write requests 	*/
            count_t	wsz;		/* cumulative # sectors written	*/
            count_t	cwsz;		/* cumulative # written sectors */
                        /* being cancelled              */
            count_t	cfuture[4];	/* reserved for future use	*/
        } dsk;

        /* MEMORY STATISTICS						*/
        struct mem {
            count_t	minflt;		/* number of page-reclaims 	*/
            count_t	majflt;		/* number of page-faults 	*/
            count_t	vexec;		/* virtmem execfile (Kb)        */
            count_t	vmem;		/* virtual  memory  (Kb)	*/
            count_t	rmem;		/* resident memory  (Kb)	*/
            count_t	pmem;		/* resident memory  (Kb)	*/
            count_t vgrow;		/* virtual  growth  (Kb)    	*/
            count_t rgrow;		/* resident growth  (Kb)     	*/
            count_t vdata;		/* virtmem data     (Kb)     	*/
            count_t vstack;		/* virtmem stack    (Kb)     	*/
            count_t vlibs;		/* virtmem libexec  (Kb)     	*/
            count_t vswap;		/* swap space used  (Kb)     	*/
            count_t	vlock;		/* virtual locked   (Kb) 	*/
            count_t	cfuture[3];	/* reserved for future use	*/
        } mem;

        /* NETWORK STATISTICS						*/
        struct net {
            count_t tcpsnd;		/* number of TCP-packets sent	*/
            count_t tcpssz;		/* cumulative size packets sent	*/
            count_t	tcprcv;		/* number of TCP-packets recved	*/
            count_t tcprsz;		/* cumulative size packets rcvd	*/
            count_t	udpsnd;		/* number of UDP-packets sent	*/
            count_t udpssz;		/* cumulative size packets sent	*/
            count_t	udprcv;		/* number of UDP-packets recved	*/
            count_t udprsz;		/* cumulative size packets sent	*/
            count_t	avail1;		/* */
            count_t	avail2;		/* */
            count_t	cfuture[4];	/* reserved for future use	*/
        } net;

        struct gpu {
            char	state;		// A - active, E - Exit, '\0' - no use
            char	cfuture[3];	//
            short	nrgpus;		// number of GPUs for this process
            int32_t	gpulist;	// bitlist with GPU numbers

            int	gpubusy;	// gpu busy perc process lifetime      -1 = n/a
            int	membusy;	// memory busy perc process lifetime   -1 = n/a
            count_t	timems;		// milliseconds accounting   -1 = n/a
                        // value 0   for active process,
                        // value > 0 after termination

            count_t	memnow;		// current    memory consumption in KiB
            count_t	memcum;		// cumulative memory consumption in KiB
            count_t	sample;		// number of samples
        } gpu;
    };
    """