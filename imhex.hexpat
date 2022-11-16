#define _UTSNAME_LENGTH 65
struct utsname_s
  {
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
  
#define	MYMAGIC		0xfeedbeef

struct rawheader {
	u32	magic;

	u16	aversion;	/* creator atop version with MSB */
	u16	future1;	/* can be reused 		 */
	u16	future2;	/* can be reused 		 */
	u16	rawheadlen;	/* length of struct rawheader    */
	u16	rawreclen;	/* length of struct rawrecord    */
	u16	hertz;		/* clock interrupts per second   */
	u16	pidwidth;	/* number of digits for PID/TID  */
	u16	sfuture[5];	/* future use                    */
	u32	sstatlen;	/* length of struct sstat        */
	u32	tstatlen;	/* length of struct tstat        */
	utsname_s	utsname;	/* info about this system        */
	char		cfuture[8];	/* future use                    */

	u32	pagesize;	/* size of memory page (bytes)   */
	s32		supportflags;  	/* used features                 */
	s32		osrel;		/* OS release number             */
	s32		osvers;		/* OS version number             */
	s32		ossub;		/* OS version subnumber          */
	s32		ifuture[6];	/* future use                    */
	padding[2];
};

struct rawrecord {
	//time_t		curtime;	/* current time (epoch)         */
    u64 curtime;
	u16	flags;		/* various flags                */
	u16	sfuture[3];	/* future use                   */

	u32	scomplen;	/* length of compressed sstat   */
	u32	pcomplen;	/* length of compressed tstat's */
	u32	interval;	/* interval (number of seconds) */
	u32	ndeviat;	/* number of tasks in list      */
	u32	nactproc;	/* number of processes in list  */
	u32	ntask;		/* total number of tasks        */
	u32    totproc;	/* total number of processes	*/
	u32    totrun;		/* number of running  threads	*/
	u32    totslpi;	/* number of sleeping threads(S)*/
	u32    totslpu;	/* number of sleeping threads(D)*/
	u32	totzomb;	/* number of zombie processes   */
	u32	nexit;		/* number of exited processes   */
	u32	noverflow;	/* number of overflow processes */
	u32	ifuture[6];	/* future use                   */
};

rawheader header @ 0x00;
rawrecord record @ sizeof(rawheader);
