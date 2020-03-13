from helper import WehiGlobusApiHelper
import globus_sdk as globus
from config import SOURCE_ENDPOINT_ID, DESTINATION_ENDPOINT_ID

def main():
  helper = WehiGlobusApiHelper()
  tc = helper.get_transfer_client()

  # Find the files that are available at the source end point.
  files = [e['name'] for e in tc.operation_ls(SOURCE_ENDPOINT_ID, path="/share/godata")]

  # Create TransferData that will describe the operation to Globus
  tdata = globus.TransferData(tc, SOURCE_ENDPOINT_ID, DESTINATION_ENDPOINT_ID, sync_level="checksum")

  # add the files that are to be downloaded
  for file in files:
    tdata.add_item("/share/godata/"+file, file)

  # Submit the transfer. This happens independently of the current script.
  # You could finish at the point and query the task later
  transfer_result = tc.submit_transfer(tdata)
  print("task_id =", transfer_result["task_id"])

  # Wait for the transfer to complete.
  completed = tc.task_wait(transfer_result["task_id"], timeout=60, polling_interval=15)
  if completed:
      print("Task finished!")
      rc = 0
  else:
      print("Task still running after timeout reached.")
      rc = 1

  # Print details of the task execution
  r = tc.get_task(transfer_result['task_id'])
  print(r)

  return rc

if __name__ == '__main__':
  quit(main())
