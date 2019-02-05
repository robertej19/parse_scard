import argparse, re

parser = argparse.ArgumentParser()
# parser.add_argument('-s','--scard', action='store_const', dest='mode_val',const='initialize', help='initialize an rss feed')
parser.add_argument('-f','--filename', action='store', default='scard.txt',help='file name e.g. rss.xml')
# parser.add_argument('-v','--verbose', action='store_true', help='file name e.g. rss.xml')

args = parser.parse_args()
filename = args.filename
file = open(filename,'r')
comments=['# number of events each job',\
'# one of clasdis, dvcs, disrad', '# generator option',\
'# gcard', '# number of jobs', '# OSG project',\
'# percent of 10^35 luminosity from 0 to 100',\
'# percent of torus current from -100 to 100',\
'# percent of solenoid current from -100 to 100']
data_scard={} # declare a dictionary

for i,line in enumerate(file):
    pos_delimeter_colon = line.find(":")
    pos_delimeter_comment = line.find(comments[i])
    if pos_delimeter_colon <0:
        print "Invalid scard. No colon detected. Halt"
        exit()
    if pos_delimeter_comment <0:
        print "Invalid scard. Don't edit the comments starting #. Halt."
        exit()
    key = line[:pos_delimeter_colon].strip()
    value= line[pos_delimeter_colon+1:pos_delimeter_comment].strip()
    data_scard[key] = value
