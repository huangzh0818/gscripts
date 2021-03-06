__author__ = 'gpratt'

__author__ = 'gpratt'
import argparse
import subprocess
import os


def wrap_wait_error(wait_result):
    if wait_result != 0:
        raise NameError("Failed to execute command correctly {}".format(wait_result))

def pre_process_bam(bam, bam01, bam02, bam03, bam04, bam05, bam06, bam07, bam08, bam09):
    #split bam file into two, return file handle for the two bam files
    p = subprocess.Popen("samtools view {} | wc -l".format(bam), shell=True, stdout=subprocess.PIPE) # Number of reads in the tagAlign file
    stdout, stderr = p.communicate()
    nlines = int(stdout)
    shuffled_bam = os.path.splitext(os.path.basename(bam))[0]
    
    p = subprocess.Popen("samtools bamshuf {0} {1}".format(bam, shuffled_bam), shell=True) # This will shuffle the lines in the file and split it into two parts
    wrap_wait_error(p.wait())

    bam_and_percent = [(bam01, int(nlines * .1)),
                       (bam02, int(nlines * .2)),
                       (bam03, int(nlines * .3)),
                       (bam04, int(nlines * .4)),
                       (bam05, int(nlines * .5)),
                       (bam06, int(nlines * .6)),
                       (bam07, int(nlines * .7)),
                       (bam08, int(nlines * .8)), 
                       (bam09, int(nlines * .9)),]

    cmds = []
    for bam_file, percent in bam_and_percent:
        p1 = subprocess.Popen("samtools view -h {0}.bam | head -n {1} | samtools view -bS - | samtools sort - {2}".format(shuffled_bam, percent, os.path.splitext(bam_file)[0]), shell=True)
        wrap_wait_error(p1.wait())

    
    p1 = subprocess.Popen("rm {0}.bam".format(shuffled_bam), shell=True)
    wrap_wait_error(p1.wait())

    return bam01, bam02

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Downsamples bam to a given number of reads')
    parser.add_argument(
        '--bam', required=True, help='bam file to split')


    parser.add_argument(
        '--bam01', required=True, help='name of first output bam')
    parser.add_argument(
        '--bam02', required=True, help='name of second output bam')

    parser.add_argument(
        '--bam03', required=True, help='name of third output bam')

    parser.add_argument(
        '--bam04', required=True, help='name of fourth output bam')

    parser.add_argument(
        '--bam05', required=True, help='name of fith output bam')

    parser.add_argument(
        '--bam06', required=True, help='name of sixth output bam')

    parser.add_argument(
        '--bam07', required=True, help='name of seventh output bam')

    parser.add_argument(
        '--bam08', required=True, help='name of eighth  output bam')

    parser.add_argument(
        '--bam09', required=True, help='name of ninth output bam')




    args = parser.parse_args()

    bam01, bam02 = pre_process_bam(args.bam, args.bam01, args.bam02, args.bam03,
                                   args.bam04, args.bam05, args.bam06, args.bam07,
                                   args.bam08, args.bam09)
