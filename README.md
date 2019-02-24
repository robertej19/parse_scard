# parse_scard
python submit.py 'scard.txt' [-s]
(or alternatively, ./submit.py scard.txt)

if -s turned on, submit.py will call clas12.condor job
if not, clas12.condor and runscript.sh are refreshed without job submission.

submit.py will call parser.py which has parser class.