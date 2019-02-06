import argparse

# define program's arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', default='scard.txt',help='file name of scard')
parser.add_argument('key', default=None,help='key of each line')
args = parser.parse_args()

# rename variables
filename = args.filename
specific_key = args.key
# for someone who prefers the style like "genOptions:"" to the style like "genOptions"
if ':' in specific_key:
    specific_key=specific_key[:-1]

# declare a global dictionary
genOutput= {'clasdis': 'sidis.data', 'dvcs': 'dvcs.data','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}

# #from https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
def ordinal(n):
    return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

class scard_parser:
# Default Constructor: a = scard_parser();  a.parse_scard("scard.txt")
# Parametrized Constructor:  a = scard_parser("scard.txt")
    def __init__(self, scard_filename=None):
        self.type ='scard parser'
        self.data = {}
        if scard_filename != None:
            self.parse_scard(scard_filename)

# void function for saving line into a dictionary
    def parse_scard_line(self, linenum, line):
        self.validate_scard_line(linenum, line)
        pos_delimeter_colon = line.find(":")
        pos_delimeter_hash = line.find("#")
        key =   line[:pos_delimeter_colon].strip()
        value=  line[pos_delimeter_colon+1:pos_delimeter_hash].strip()
        self.data[key] = value

# voild function for parsing scard.txt into a dictionary
    def parse_scard(self, filename, store=True):
        scard=open(filename, "r")
        for linenum, line in enumerate(scard):
            self.parse_scard_line(linenum,line)
        if store == True:
            self.store()

#void function for validating s_card
    def validate_scard_line(self, linenum, line):
        if line.count("#") ==0:
            print "Warning: No comment in "+ ordinal(linenum+1) + " line."
        elif line.count("#")>1:
            print "ERROR: number of hashes>1 at "+ordinal(linenum+1)+" line."
            print "# can be only used for adelimeter and for once. Stopped."
            exit()
        if line.count(":") ==0:
            print "ERROR: No colon in "+ ordinal(linenum+1) + " line."
            print "The data cannot be interpreted. Stopped."
            exit()
        elif line.count(":")>1:
            print "ERROR: number of colons>1 at "+ordinal(linenum+1)+" line."
            print "\':\' can be only used for a delimeter and for once. Stopped."
            exit()
# store info's in dictionary into single variables
    def store(self):
        self.nevents = self.data.get("nevents")
        self.generator = self.data.get("generator")
        self.genOptions = self.data.get("genOptions")
        self.gcards = self.data.get("gcards")
        self.jobs = self.data.get("jobs")
        self.project = self.data.get("project")
        self.luminosity = self.data.get("luminosity")
        self.tcurrent = self.data.get("tcurrent")
        self.pcurrent = self.data.get("pcurrent")
        self.genOutput = genOutput.get(self.data.get("generator"))
        self.genExecutable = genExecutable.get(self.data.get("generator"))

# Uncomment below to test
# a = scard_parser()
# a.parse_scard("scard.txt")
# print a.nevents

scard = scard_parser("scard.txt")
data_scard = scard.data
if data_scard.get(specific_key) != None:
    print data_scard.get(specific_key)
elif specific_key == "genOutput":
    print genOutput.get(data_scard.get("generator"))
elif specific_key == "genExecutable":
    print genExecutable.get(data_scard.get("generator"))
else:
    print "Improper Usage: correct usage is\npython [script_location/parser.py] [(scard_filename)] [key_to_lookup]"
    print "The key " + specific_key + " is not among the possible keys:"
    print '\"jobs\"', '\"generator\"', '\"genOptions\"', '\"luminosity\"', '\"gcards\"', '\"pcurrent\"', '\"project\"', '\"nevents\"', 'and \"tcurrent\"'
    print "e.g.) python parser.py scard.txt  genOptions:"
    print exit()

# Future works will be changing csh files not to call scard.txt everytime
# import os,sys, subprocess ...
