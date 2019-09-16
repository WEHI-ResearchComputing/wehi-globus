from helper import WehiGlobusApiHelper
import globus_sdk as globus
from argparse import ArgumentParser
from config import SOURCE_ENDPOINT_ID, DESTINATION_ENDPOINT_ID
import sys

def build_parser():
  parser = ArgumentParser()
  parser.add_argument('--globus-path',
                      help='the directory of the file in the globus source end point',
                      dest='globus_path',
                      required=True)
  parser.add_argument('--file',
                      dest='file',
                      help='file name',
                      required=True)
  return parser

def main(argv):
  parser = build_parser()
  options = parser.parse_args(args=argv)

  helper = WehiGlobusApiHelper()

  file = options.file
  path = options.globus_path
  if not path.endswith('/'):
    path = path + '/'

  tc = helper.get_transfer_client()

  # Create TransferData that will describe the operation to Globus
  tdata = globus.TransferData(tc, SOURCE_ENDPOINT_ID, DESTINATION_ENDPOINT_ID, sync_level="checksum")

  # add the files that are to be downloaded
  tdata.add_item(path+file, file)

  # Submit the transfer. This happens independently of the current script.
  # You could finish at the point and query the task later
  transfer_result = tc.submit_transfer(tdata)
  print('Downloading: {fn}  task id: {task_id}'.format(fn=path+file, task_id=transfer_result["task_id"]))

  # Wait for the transfer to complete.
  completed = tc.task_wait(transfer_result["task_id"], timeout=sys.maxsize, polling_interval=60)
  if completed:
      print("Task finished!")
      rc = 0
  else:
      print("Task failed.")
      rc = 1

  # Print details of the task execution
  r = tc.get_task(transfer_result['task_id'])
  print(r)

  return rc

if __name__ == '__main__':
  quit(main(sys.argv[1:]))