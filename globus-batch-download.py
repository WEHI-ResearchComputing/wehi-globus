from helper import WehiGlobusApiHelper
import drmaa
from multiprocessing.pool import Pool
from config import *

"""
This is a template for building a system that will list files in a globus endpoint
and submit jobs to the batch system. You need to
1. Edit config.py
2. Login using the globus-login.py script
3. Start the globus personal client. The first time, this needs to be done manually but subsequently
   could also run as a batch job.
5. Fill in the is_file_needed function (this determines whether the file should be downloaded
6. Adapt the get_file_list function for your use case
7. Provide a process.sh bash script that takes source endpoint file name as argument. You will need
   to know where the file is located based on your endpoint configuration.

Good luck!
"""
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
"""
The file might have already been downloaded and processed, in which
return False and that will be skipped
"""
def is_file_needed(fn):
  return True
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
"""
During testing, just return a single file, then scale up
"""
def get_file_list():
  print('Starting file listing')

  helper = WehiGlobusApiHelper()
  tc = helper.get_transfer_client()

  # Find the files that are available at the source end point.
  files = [e['name'] for e in tc.operation_ls(SOURCE_ENDPOINT_ID, path=PATH)]
  print('{n} files found.'.format(n=len(files)))

  return files
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
"""
 This class builds and manages a batch job
"""
class Job:
  def __init__(self, fn):
    self.fn = fn

  def __call__(self, *args, **kwargs):
    fn = self.fn

    print('Building job for {fn}'.format(fn=fn))
    s = drmaa.Session()
    s.initialize()

    try:
      jt = s.createJobTemplate()
      jt.workingDirectory = WORKING_DIR
      jt.outputPath = WORKING_DIR
      jt.joinFiles = True
      jt.jobName = fn
      jt.remoteCommand = os.path.join(os.getcwd(), 'wrapper.sh')
      jt.args = [PATH, fn]
      jt.nativeSpecification = RESOURCES
      job_id = s.runJob(jt)

      print('Submitted job: {job_id}'.format(job_id=job_id))
      info = s.wait(job_id, drmaa.Session.TIMEOUT_WAIT_FOREVER)
      print('Completed job: {job_id}'.format(job_id=job_id))
      print("""\
      id:                        %(jobId)s
      exited:                    %(hasExited)s
      signaled:                  %(hasSignal)s
      with signal (id signaled): %(terminatedSignal)s
      dumped core:               %(hasCoreDump)s
      aborted:                   %(wasAborted)s
      resource usage:
      %(resourceUsage)s
      """ % info._asdict())
    finally:
      s.exit()

#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def main():
  # Get the file list and filter for the ones we want to process
  files = get_file_list()
  files = filter(is_file_needed, files)

  # A pool of workers. Each worker will manage a job in the batch system
  p = Pool(NUM_JOBS)
  # Create jobs for each file
  jobs = [Job(fn) for fn in files]
  # Submit them to the pool
  submitted_jobs = [p.apply_async(job) for job in jobs]

  # Wait for them to finish
  for submitted_job in submitted_jobs:
    submitted_job.get()
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
if __name__ == '__main__':
  main()
#-----------------------------------------------------------------------------
