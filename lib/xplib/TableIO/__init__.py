# Programmer : zhuxp
# Date: 
# Last-modified: 09-11-2013, 14:22:15 EDT
import BedIO
import GeneBedIO
import SimpleIO
import TransIO
import OddsRatioSNPIO
import BamIO
import VCFIO
import RepeatIO
import MetaBedIO
import gtfIO
import IO
FormatToIterator = { "bed":BedIO.BedIterator,
                     "genebed":GeneBedIO.GeneBedIterator,
                     "genepred":GeneBedIO.GeneBedIterator,
                     "simple":SimpleIO.SimpleIterator,
                     "transunit":TransIO.TransUnitIterator,
                     "oddsratiosnp":OddsRatioSNPIO.OddsRatioSNPIterator,
                     "aps":OddsRatioSNPIO.OddsRatioSNPIterator,
                     "bam":BamIO.BamIterator,
                     "sam":BamIO.SamIterator,
                     "bam2bed":BamIO.BamToBedIterator,
                     "vcf":VCFIO.VCFIterator,
                     "repeat":RepeatIO.RepeatIterator,
                     "metabed":MetaBedIO.MetaBedIterator,
                     "gtf":gtfIO.GTFIterator,
                     "fimo":IO.FimoIterator,
                     "bam2bed12":BamIO.BamToBed12Iterator,
                     "bam2fragment":BamIO.BamToFragmentIterator,
                   }
def parse(handle,format="simple",**dict):
    """
    - handle  - handle to the file, or the filename
    - format  - lower case string describing the file format
                example 'bed' 'genebed' 'bam' 'sam' 'vcf' 'gtf'
    Example:
        from xplib import TableIO
        for i in TableIO.parse(file or filename,"bed"):
            print i

    """
    mode='rU'
    if format in FormatToIterator:
        iterator_generator=FormatToIterator[format]
        i=iterator_generator(handle,**dict)
    for r in i:
        yield r
def convert(item,format="bam2bed12",**dict):
    items=[item]
    a=parse(items,format,**dict)
    try:
        b=a.next()
        a.close()
        return b
    except:
        return None

def format_string(x):
    s=""
    for i in x:
        s+=str(i)+"\t"
    s=s.strip("\t")
    return s
