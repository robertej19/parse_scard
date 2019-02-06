import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument('filename', default='scard.txt',help='file name of scard')
parser.add_argument('key', default=None,help='key of each line')
# parser.add_argument('-v','--verbose', action='store_true', help='file name e.g. rss.xml')

args = parser.parse_args()
filename = args.filename
specific_key = args.key
if ':' in specific_key:
    specific_key=specific_key[:-1]
file = open(filename,'r')
comments=['# number of events each job',\
'# one of clasdis, dvcs, disrad', '# generator option',\
'# gcard', '# number of jobs', '# OSG project',\
'# percent of 10^35 luminosity from 0 to 100',\
'# percent of torus current from -100 to 100',\
'# percent of solenoid current from -100 to 100']
data_scard={} # declare a dictionary
genOutput= {'clasdis': 'sidis.data', 'dvcs': 'dvcs.data','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}

for i,line in enumerate(file):
    pos_delimeter_colon = line.find(":")
    pos_delimeter_comment = line.find(comments[i])
    if pos_delimeter_colon <0:
        print "Invalid scard. No colon detected in %d-th line. Stopped."%i
        exit()
    if pos_delimeter_comment <0:
        print "Invalid scard. Don't edit the comments starting #. Stopped."
        exit()
    key = line[:pos_delimeter_colon].strip()
    value= line[pos_delimeter_colon+1:pos_delimeter_comment].strip()
    data_scard[key] = value

if data_scard.get(specific_key) != None:
    print data_scard.get(specific_key)
elif specific_key == "genOutput":
    print genOutput.get(data_scard.get("generator"))
elif specific_key == "genExecutable":
    print genExecutable.get(data_scard.get("generator"))
else:
    print "Improper Usage: correct usage is 'python [script_location/parser.py] [(scard_filename)] [key_to_lookup]"
    print "The key " + specific_key + " is not among the possible keys:"
    print '\"jobs\"', '\"generator\"', '\"genOptions\"', '\"luminosity\"', '\"gcards\"', '\"pcurrent\"', '\"project\"', '\"nevents\"', 'and \"tcurrent\"'
    print "e.g.) python parser.py scard.txt  genOptions:"
    print exit()
