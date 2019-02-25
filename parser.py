import argparse, sys, os, subprocess

# declare a global dictionary to match genOutput and genExecutable to generator row
genOutput= {'clasdis': 'sidis.dat', 'dvcs': 'dvcs.dat','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}

# Proper configuration of scard:
scard_key = ['project_group','user','nevents','generator', 'genOptions',  'gcards', 'jobs',  'project', 'luminosity', 'tcurrent',  'pcurrent']


# from https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712
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
        self.validate_scard_line(linenum, line) # 1st validating
        pos_delimeter_colon = line.find(":")
        pos_delimeter_hash = line.find("#")
        key =   line[:pos_delimeter_colon].strip()
        value=  line[pos_delimeter_colon+1:pos_delimeter_hash].strip()
        if key != scard_key[linenum]:
            print "ERROR: The " + ordinal(linenum+1) +" line of steering card starts with "+ key +"."
            print "That line must have the key " + scard_key[linenum] +"."
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
            print "# can be only used for a delimeter and for once. Stopped."
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
        self.project_group = self.data.get("project_group")
        self.user = self.data.get("user")
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

def write_clas12_condor(project, jobs):
    file = open("clas12.condor","w")
    file.write("# The UNIVERSE defines an execution environment. You will almost always use vanilla.\n")
    file.write("Universe = vanilla\n\n")
    file.write("+SINGULARITY_JOB = true\n")
    file.write("+SINGULARITY_SHELL = csh\n\n")
    file.write("# singularity image\n\n")
    file.write("Requirements  = (GLIDEIN_Site == \"MIT_CampusFactory\" && BOSCOGroup == \"bosco_lns\")\n")
    file.write("+SingularityImage = \"/cvmfs/singularity.opensciencegrid.org/jeffersonlab/clas12simulations:production\"\n")
    file.write("+SingularityBindCVMFS = True\n\n")
    file.write("request_cpus = 2\n")
    file.write("request_memory = 2 GB\n\n")
    file.write("# EXECUTABLE is the program your job will run It\'s often useful\n")
    file.write("# to create a shell script to \"wrap\" your actual work.\n")
    file.write("Executable = run_job.sh\n\n")
    file.write("# Error and Output are the error and output channels from your job\n")
    file.write("# Log is job\'s status, success, and resource consumption.\n")
    file.write("Error  = log/job.$(Cluster).$(Process).err\n")
    file.write("Output = log/job.$(Cluster).$(Process).out\n")
    file.write("Log    = log/job.$(Cluster).$(Process).log\n\n")
    file.write("# Send the job to Held state on failure.\n")
    file.write("# on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)\n\n")
    file.write("# Periodically retry the jobs every 1 hour, up to a maximum of 5 retries.\n")
    file.write("# periodic_release =  (NumJobStarts < 5) && ((CurrentTime - EnteredCurrentStatus) > 60*60)\n\n")
    file.write("# default CLAS12 project\n")
    file.write("+ProjectName = \""+project+"\"\n\n\n")
    file.write("# Input files. Do not add comments after the file list\n")
    file.write("# transfer_input_files = cook.csh\n\n")
    file.write("# output\n")
    file.write("should_transfer_files = YES\n")
    file.write("when_to_transfer_output = ON_EXIT\n")
    file.write("transfer_input_files=runscript.sh,condor_wrapper\n")
    file.write("transfer_output_files = out_dir$(Cluster)\n\n")
    file.write("# QUEUE is the \"start button\" - it launches any jobs that have been\n")
    file.write("# specified thus far. 1 means launch only 1 job\n")
    file.write("Queue "+jobs+"\n")
    file.close()

def write_runscirpt_sh(genExecutable, nevents, genOptions, genOutput, gcards, tcurrent, pcurrent):
    file = open("runscript.sh","w")
    file.write("#!/bin/csh\n\n")
    file.write("set script_start  = `date`\n\n")
    file.write("# source /cvmfs/cms.cern.ch/cmsset_default.csh\n\n")
    file.write("echo \"XXXXXXXXXXXX\"\n")
    file.write("#cat $PWD/.job.ad\n")
    file.write("echo \"XXXXXXXXXXXX\"\n\n\n")
    file.write("uname -a\n\n")
    file.write("echo \" ==== PWD\"\n")
    file.write("pwd\n\n")
    file.write("echo \" ==== ./\"\n")
    file.write("ls -lhrt ./\n\n")
    file.write("echo \" ==== /etc/profile.d/\"\n")
    file.write("ls -lhrt /etc/profile.d/\n\n")
    file.write("echo \" ==== ENV\"\n")
    file.write("env\n\n")
    file.write("source /etc/profile.d/environmentB.csh\n")
    file.write("cd /tmp\n\n")
    file.write("#set ClusterId = `sed -n \'0,/ClusterId = \"\([^\"]*\)\"/\\1/p\' $PWD/.job.ad`\n\n")
    file.write("set ClusterId = ` awk -F \'=\' \'/^ClusterId/ {print $2}\' $PWD/.job.ad`\n")
    file.write("echo ClusterId $ClusterId\n\n\n")
    file.write("set ProcId = ` awk -F \'=\' \'/^ProcId/ {print $2}\' $PWD/.job.ad`\n")
    file.write("echo ProcId $ProcId\n\n\n")
    file.write("printf \"Start time: \"; /bin/date\n")
    file.write("printf \"Job is running on node: \"; /bin/hostname\n")
    file.write("printf \"Job running as user: \"; /usr/bin/id\n")
    file.write("printf \"Job is running in directory: \"; /bin/pwd\n\n")
    file.write("echo\n")
    file.write("echo JLAB_ROOT: $JLAB_ROOT\n")
    file.write("echo\n\n")
    file.write("echo starting files\n")
    file.write("ls -l\n")
    file.write("set generator_start  = `date`\n")
    file.write(genExecutable+" --trig "+nevents+" --docker "+genOptions+"\n")
    file.write("#dvcsgen --trig 71 --docker\n\n")
    file.write("echo after generator\n")
    file.write("echo test finish\n")
    file.write("ls -l\n")
    file.write("set gemc_start = `date`\n")
    file.write("gemc -USE_GUI=0 -N="+nevents+" -INPUT_GEN_FILE=\"lund, "+genOutput +"\"  "+gcards+"\n\n")
    file.write("echo after gemc\n")
    file.write("ls -l\n\n\n")
    file.write("set evio2hipo_start = `date`\n")
    file.write("evio2hipo -r 11 -t "+tcurrent+" -s "+pcurrent+" -i out.ev -o gemc.hipo\n\n")
    file.write("echo after decoder\n")
    file.write("ls -l\n\n")
    file.write("set notsouseful_start = `date`\n")
    file.write("notsouseful-util -i gemc.hipo -o out_gemc.hipo -c 2\n\n")
    file.write("echo after cooking\n")
    file.write("ls -l\n\n\n")
    file.write("echo Moving file\n")
    file.write("echo $ClusterId\n")
    file.write("mv out.ev out.$ProcId.ev\n")
    file.write("echo File moved\n")
    file.write("echo `basename out.$ProcId.ev`\n\n")
    file.write("echo creating directory\n")
    file.write("mkdir out_dir$ClusterId\n")
    file.write("echo moving file\n")
    file.write("mv out.$ProcId.ev out_dir$ClusterId\n")
    file.write("mv out_gemc.hipo out_gemc.$ProcId.hipo\n")
    file.write("mv out_gemc.$ProcId.hipo out_dir$ClusterId\n\n")
    file.write("#final job log\n")
    file.write("printf \"Job finished time: \"; /bin/date\n\n")
    file.write("echo \"script started at\" $script_start\n")
    file.write("echo \"generator started at\" $generator_start\n")
    file.write("echo \"gemc started at\" $gemc_start\n")
    file.write("echo \"evio2hipo started at\" $evio2hipo_start\n")
    file.write("echo \"notsouseful started at\" $notsouseful_start\n")
    file.close()
def condor_submit():
    subprocess.call(["condor_submit","clas12.condor"])
