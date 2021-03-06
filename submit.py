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
group = scard.group  # Alternatively, they can be called in single name.
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

# overwrite clas12.condor
write_clas12_condor(project,jobs)
#overwrite runscript.sh
write_runscirpt_sh(group,user,genExecutable, nevents, genOptions, genOutput, gcards, tcurrent, pcurrent)

#if submit flag turned on, submit
if args.submit:
    condor_submit()
#if not, print some messages
else:
    print "The scripts \'clas12.condor\' and \'runscript.sh\' are updated based on \'"+filename+".\'"
    print "Please turn on -s flag for job submission e.g.) python submit.py -s scard.txt\n"
