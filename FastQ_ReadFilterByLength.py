#!/usr/bin/env python

import sys
import os
import getopt
from Bio.SeqIO.QualityIO import FastqGeneralIterator

OPT_INPUT_FILE=""
OPT_OUTPUT_FILE=False
OPT_MIN_LENGTH=0
OPT_MAX_LENGTH=False

def Usage():
    print "\nFastQ_ReadFilterByLength.py is a program that read a FASTQ file and filter the sequences according to their length. \n"
    print "Usage:"
    print "\tFastQ_ReadFilterByLength.py -i [FASTQ file]\n"
    print "\nMandatory options:"
    print "\t-i, --input=FILE"
    print "\t\tThe input FASTQ file to be filtered."
    print "\nOther options:"
    print "\t-h, --help"
    print "\t\tShow the options of the program."
    print "\t-m, --minimum=THRESHOLD"
    print "\t\tThis option set the minimum length that all sequences must have. By default is 0."
    print "\t-M, --maximum=THRESHOLD"
    print "\t\tThis option set the maximum length that all sequences must have. By default is not defined which means that the is not an upper length limit."
    print "\t-o, --output=FILE"
    print "\t\tWrite the output to the given file in FASTQ format. By default this option is not set and the ouput is written to the STDOUT."
    print "\n"
    sys.exit(1)

# Function that read and parse the command line arguments.
def SetOptions(argv):
    if len(argv) == 0:
        Usage()
    options, remaining = getopt.getopt(argv, 'i:m:M:o:h', ['input=','minimum=','maximum=','output=','help'])
    opt_flag = {'i': False, 'm':False, 'M':False, 'o':False}
    global OPT_INPUT_FILE, OPT_OUTPUT_FILE, OPT_MIN_LENGTH, OPT_MAX_LENGTH
    for opt, argu in options:
        if opt in ('-i', '--input'):
            if not opt_flag['i']:
                if os.path.exists(argu):
                    OPT_INPUT_FILE = argu
                    opt_flag['i'] = True
                else:
                    print >> sys.stderr , "\n[ERROR]: File or path of the input file does not exist. ", argu, "\n"
                    sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the input file. Option -i / --input was already set.\n"
                sys.exit(1)
        elif opt in ('-o', '--output'):
            if not opt_flag['o']:
                if not os.path.dirname(argu): # Empty path means the current directory.
                    OPT_OUTPUT_FILE = argu
                    opt_flag['o'] = True
                else:
                    if os.path.exists(os.path.dirname(argu)):
                        OPT_OUTPUT_FILE = argu
                        opt_flag['o'] = True
                    else:
                        print >> sys.stderr , "\n[ERROR]: Path to write the output does not exist. ", os.path.dirname(argu), "\n"
                        sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the output file. Option -o / --output was already set.\n"
                sys.exit(1)
        elif opt in ('-h', '--help'):
            Usage()
        elif opt in ('-m', '--minimum'):
            if not opt_flag['m']:
                OPT_MIN_LENGTH = int(argu)
                opt_flag['m'] = True
                if OPT_MIN_LENGTH < 0:
                    print >> sys.stderr , "\n[ERROR]: The minimum sequence length must be an integer greater or equal than 0. See option -m / --minimum.\n"
                    sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the minimum sequence length. Option -m / --minimum was already set.\n"
                sys.exit(1)
        elif opt in ('-M', '--maximum'):
            if not opt_flag['M']:
                OPT_MAX_LENGTH = int(argu)
                opt_flag['M'] = True
                if OPT_MAX_LENGTH < 0:
                    print >> sys.stderr , "\n[ERROR]: The maximum sequence length must be an integer greater or equal than 0. See option -M / --maximum.\n"
                    sys.exit(1)
            else:
                print >> sys.stderr , "\n[ERROR]: Trying to redefine the maximum sequence length. Option -M / --maximum was already set.\n"
                sys.exit(1)
    if not opt_flag['i']:
        print >> sys.stderr , "\n[ERROR]: Input file not defined. Option -i / --input.\n"
        sys.exit(1)
    if opt_flag['M'] and (OPT_MAX_LENGTH < OPT_MIN_LENGTH):
        print >> sys.stderr , "\n[ERROR]: The threshold for the maximum sequence length must be greater or equal than the threshold for the minimum sequence length. (max >= min): "+str(OPT_MAX_LENGTH)+" >= "+str(OPT_MIN_LENGTH)+"\n"
        sys.exit(1)

# Parse command line
SetOptions(sys.argv[1:])

# Setting the output
if OPT_OUTPUT_FILE:
    OPT_OUTPUT_FILE=open(OPT_OUTPUT_FILE,"w")
else:
    OPT_OUTPUT_FILE=sys.stdout

# The option -M / --maximum was not set
if not OPT_MAX_LENGTH:
    for read in FastqGeneralIterator(open(OPT_INPUT_FILE)): # Reading the FASTQ.
        if len(read[1]) >= OPT_MIN_LENGTH:
            print >> OPT_OUTPUT_FILE , "@"+read[0]
            print >> OPT_OUTPUT_FILE , read[1]
            print >> OPT_OUTPUT_FILE , "+"
            print >> OPT_OUTPUT_FILE , read[2]
else:
    for read in FastqGeneralIterator(open(OPT_INPUT_FILE)): # Reading the FASTQ.
        if (len(read[1]) >= OPT_MIN_LENGTH) and (len(read[1]) <= OPT_MAX_LENGTH):
            print >> OPT_OUTPUT_FILE , "@"+read[0]
            print >> OPT_OUTPUT_FILE , read[1]
            print >> OPT_OUTPUT_FILE , "+"
            print >> OPT_OUTPUT_FILE , read[2]


