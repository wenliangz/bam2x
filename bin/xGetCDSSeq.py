#!/usr/bin/env python
# Programmer : zhuxp
# Date: 
# Last-modified: 01-27-2013, 21:19:43 EST
VERSION="0.1"
import os,sys,argparse
from xplib.Annotation import Bed
from xplib import TableIO
import signal
signal.signal(signal.SIGPIPE,signal.SIG_DFL)
import gzip
import time
from xplib.DBI.DB import GenomeI
from xplib.Tools import seq_wrapper
def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency : xplib')
    p.add_argument('-v','--version',action='version',version='%(prog)s '+VERSION)
    p.add_argument('-i','--input',dest="input",default="stdin",type=str,help="input annotation file in gene table format or bed DEFAULT: STDIN")
    p.add_argument('-g','--genome',dest="genome",type=str,help="chromosome.2bit file")
    p.add_argument('-o','--output',dest="output",type=str,default="stdout",help="output file DEFAULT: STDOUT")
    
    if len(sys.argv)==1:
        print >>sys.stderr,p.print_help()
        exit(0)
    return p.parse_args()
def Main():
    '''
    IO TEMPLATE
    '''
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
    if args.input=="stdin":
        fin=sys.stdin
    else:
        try:
            x=args.input.split(".")
            if x[-1]=="gz":
                fin=gzip.open(args.input,"r")
            else:
                fin=open(args.input,"r")
        except IOError:
            print >>sys.stderr,"can't read file",args.input
            fin=sys.stdin
    '''
    END OF IO TEMPLATE 
    '''
    print >>out,"# This data was generated by program ",sys.argv[0]," (version: %s)"%VERSION,
    print >>out,"in bam2x ( https://github.com/nimezhu/bam2x )"
    print >>out,"# Date: ",time.asctime()
    print >>out,"# The command line is :"
    print >>out,"#\t"," ".join(sys.argv)
    genome=GenomeI(args.genome)
    for i in TableIO.parse(fin,"genebed"):
            print >>out,">",i.id+"_CDS"
            print >>out,seq_wrapper(genome.get_cds_seq(i))




    
if __name__=="__main__":
    Main()





