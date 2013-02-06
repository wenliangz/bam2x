#!/usr/bin/env python
# Programmer : zhuxp
# Date: 
# Last-modified: 02-05-2013, 20:33:04 EST
VERSION="0.1"
'''
'''
import os,sys,argparse
from xplib.Annotation import Bed
from xplib import TableIO
import pysam
from xplib import DBI
import signal
signal.signal(signal.SIGPIPE,signal.SIG_DFL)
import time

def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -i file.snp -a file.vcf.gz -A tabix -o output.file', epilog='Library dependency : pysam xplib')
    p.add_argument('-v','--version',action='version',version='%(prog)s '+VERSION)
    p.add_argument('-i','--input',dest="input",type=str,default="stdin",help="input file")
    p.add_argument('-I','--format',dest="input_format",type=str,help="input file format",default="bed")
    p.add_argument('-o','--output',dest="output",type=str,default="stdout",help="output file")
    p.add_argument('-b','--bam',dest="bam",type=str,default="",required=True,help="bam file")
    if len(sys.argv)==1:
        print >>sys.stderr,p.print_help()
        exit(0)
    return p.parse_args()


def Main():
    global args,out
    args=ParseArg()
    if args.output=="stdout":
        out=sys.stdout
    else:
        try:
            out=open(args.output,"w")
        except IOError:
            print >>sys.stderr,"can't open file ",args.output,"to write. Using stdout instead"
            out=sys.stdout
    argv=sys.argv
    argv[0]=argv[0].split("/")[-1]
    print >>out,"# This data was generated by program ",argv[0],"(version %s)"%VERSION,
    print >>out,"in bam2x ( https://github.com/nimezhu/bam2x )"
    print >>out,"# Date: ",time.asctime()
    print >>out,"# The command line is :\n#\t"," ".join(argv)
   
    dbi=DBI.init(args.bam,"bam")
    if args.input=="stdin":
        input=sys.stdin
    else:
        input=args.input

    for x in TableIO.parse(input,args.input_format):
        promoter=x.core_promoter(1000,1000)
        print >>out,x
        print >>out,promoter
        retv=[]
        for (i,r) in enumerate(dbi.query(promoter)):
            retv.append(sum(r))
        if x.strand=="-":
            retv=retv[::-1]
        for i in retv:
            print >>out,i,
        print >>out,""
       


    
if __name__=="__main__":
    Main()




