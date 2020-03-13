import os

#-----------------------------------------------------------------------------
# You need to edit these for your use case!
#
# The source EP is where the data is coming. Your provider will give you that
SOURCE_ENDPOINT_ID      = 'ddb59aef-6d04-11e5-ba46-22000b92c6ec'
PATH = '/share/godata'
# Create your own EP using the globus CLI
DESTINATION_ENDPOINT_ID = 'a7552630-d2a3-11e9-98e2-0a63aa6b37da'
# How many concurrent jobs at a time. Test with a small value then increase.
# Bear in mind that more jobs will make recovery more complex in the event
# of a failure.
NUM_JOBS = 2
# Working directory where the script is expected to be located and
# where the script will run (may not be where the files are).
# Note: Probably should be absolute path.
WORKING_DIR = os.getcwd()
# Resources for your job in qstat format
RESOURCES = '-l nodes=1:ppn=1,mem=1gb,walltime=01:00:00'
#-----------------------------------------------------------------------------