# Programmer : zhuxp
# Date:  Sep 2012
# Last-modified: 08-27-2013, 11:20:33 EDT

hNtToNum={'a':0,'A':0,
          'c':1,'C':1,
          'g':2,'G':2,
          't':3,'T':3
         }
Nt=['A','C','G','T']

    
def rc(seq):
   comps = {'A':"T", 'C':"G", 'G':"C", 'T':"A",
           'B':"V", 'D':"H", 'H':"D", 'K':"M",
           'M':"K", 'R':"Y", 'V':"B", 'Y':"R",
           'W':'W', 'N':'N', 'S':'S'}
   return ''.join([comps[x] for x in seq.upper()[::-1]])
def shuffle(seq):
   import random
   a=list(seq)
   random.shuffle(a)
   return "".join(a)

def seq_wrapper(seq,width=60):
    s=""
    seqlen=len(seq)
    for i in range(0,seqlen,width):
        stop=i+width
        if stop>seqlen:stop=seqlen
        s+=seq[i:stop]+"\n"
    return s
def distance(A,B):
    if A.chr!=B.chr: return None
    if overlap(A,B): return 0
    m=abs(A.start-B.start)
    if( m > abs(A.start-B.stop)): m = abs(A.start-B.stop)
    if( m > abs(A.stop-B.stop)): m = abs(A.stop-B.stop)
    if( m > abs(A.stop-B.start)): m = abs(A.stop-B.start)
    return m
def translate_coordinate(A,B):
    '''
    translate B's coordiante based on A
    '''
    if A.chr!=B.chr: return None
    if A.strand=="+" or A.strand==".":
        return (B.start-A.start,B.stop-A.start,B.strand)
    if A.strand=="-":
        strand="."
        if B.strand=="-":strand="+"
        if B.strand=="+":strand="-"
        return (A.stop-B.stop,A.stop-B.start,strand)

def overlap(A,B):
    '''
    if A is overlapping with B.
    A and B are ? extends Bed class.
    '''
    if(A.chr != B.chr) : return 0
    if (A.stop < B.start) : return 0
    if (B.stop < A.start) : return 0
    return 1
from xplib.Annotation import Bed
def find_nearest(bed,dbi,extends=50000,**dict):
    start=bed.start-extends
    stop=bed.stop+extends
    chr=bed.chr
    if start<0: start=0
    new_bed=Bed([chr,start,stop])

    results=dbi.query(new_bed,**dict)
    d=2*extends
    flag=0
    
    for result in results:
        if distance(bed,result)<d:
            d=distance(bed,result)
            nearest=result
            if  result.strand=="." or bed.strand==".":
                strand="."
            elif result.strand==bed.strand:
                strand="+"
            else:
                strand="-"
                
            flag=1
    if flag==0:
        return (None,None,None)
    else:
        return (d,nearest,strand)


def compatible(a,b):
    '''
    VERSION: TEST
    if a and b are compatible return true
    a and b are BED12 class or GENEBED 
    definition of compatible
       the overlap region should be same transcript structure.
    '''
    if (not overlap(a,b)): return True; 
    '''
    if two bed is not overlap, they are compatible.
    '''
    start=a.start;
    if (start < b.start): start=b.start 
    '''
    start is the max start of a.start and b.start 
    '''
    stop=a.stop
    if (stop > b.stop): stop=b.stop
    '''
    stop is the min stop of a.stop and b.stop
    find the overlap region from [start,stop)
    '''
    a_starts_slice=[];
    
    for i in a.exon_starts:
        if i>start and i<stop:
            a_starts_slice.append(i); 
    j=0;
    l=len(a_starts_slice);
    for i in b.exon_starts:
        if i>start and i<stop:
            if (j>l-1 or a_starts_slice[j]!=i) : return False
            j+=1
    if j!=l-1 : return False
    
    
    a_stops_slice=[];
    for i in a.exon_stops:
        if i>start and i<stop:
            a_stops_slice.append(i); 
    
    j=0;
    l=len(a_stops_slice);
    for i in b.exon_stops:
        if i>start and i<stop:
            if (j>l-1 or a_stops_slice[j]!=i) : return False
            j+=1
    if j!=l-1 : return False
    return True 


def cigar_to_coordinates(cigar,offset=0):
    '''
    demo version
    need to test
    
    deletion from genome (case 3) now consider as exon indel. 
    '''
    exon_starts=[offset]
    exon_lengths=[0]
    state=0
    for i in cigar:
        if i[0]==0 or i[0]==7 or i[0]==8:  # match
           exon_lengths[-1]+=i[1] 
           state=1 
        if i[0]==2:  # deletion from genome , need to consider this should be exon or intron? now count as exon. 
           exon_lengths[-1]+=i[1] 
           state=1 
        if i[0]==3:  # skipped region from the reference 
           if state==1:
               exon_starts.append(exon_starts[-1]+exon_lengths[-1]+i[1]);
               exon_lengths.append(0);
           else:
               exon_starts[-1]+=i[1]
           state=0
    return (exon_starts,exon_lengths)