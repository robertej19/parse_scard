#!/usr/bin/env python
from parser import *

# define program's arguments
argparser = argparse.ArgumentParser()
argparser.add_argument('steering_card', default='scard.txt', help='file name of scard')
argparser.add_argument('key', nargs='?', default=None, help='each column item name. If called, print correspinding item\'s value. If omitted, s')
argparser.add_argument('-s', '--submit', help= 'submit.',action="store_true")
args = argparser.parse_args()

# rename variables for human-readability
filename = args.steering_card
specific_key = args.key

# Collecting info from scard
# If scard is not in a proper format, the class scard_parser should stop the script.
scard = scard_parser(filename) # parse scard. scard is called only once at this line.
data_scard = scard.data # This is dictionary which has every data from scard.
project_group = scard.project_group  # Alternatively, they can be called in single name.
user = scard.user
nevents = scard.nevents
generator = scard.generator
genOptions = scard.genOptions
gcards = scard.gcards
jobs = scard.jobs
project = scard.project
luminosity = scard.luminosity
tcurrent = '%1.2f'%(float(scard.tcurrent)/100.)
if float(scard.tcurrent)%10==0:
    tcurrent = '%1.1f'%(float(scard.tcurrent)/100.)
pcurrent = '%1.2f'%(float(scard.pcurrent)/100.)
if float(scard.pcurrent)%10==0:
    pcurrent = '%1.1f'%(float(scard.pcurrent)/100.)
genOutput = scard.genOutput
genExecutable = scard.genExecutable

# #remove existing clas12.condor
# os.remove("clas12.condor")
#write new clas12.condor from scard.txt
write_clas12_condor(project,jobs)
# #remove existing runscript.sh
# os.remove("runscript.sh")
#write new runscript.sh
write_runscirpt_sh(genExecutable, nevents, genOptions, genOutput, gcards, tcurrent, pcurrent)

#if submit flag turned on, submit
if args.submit:
    condor_submit()
