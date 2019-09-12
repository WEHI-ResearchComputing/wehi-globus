from tokens import WehiGlobusApiHelper
import globus_sdk as globus

#-------------------------------------------
# You need to edit these for your use case.
#-------------------------------------------
# The source EP is where the data is coming. Your provider will give you that
SOURCE_ENDPOINT_ID      = 'ddb59aef-6d04-11e5-ba46-22000b92c6ec'
# Create your own EP using the globus CLI
DESTINATION_ENDPOINT_ID = 'a7552630-d2a3-11e9-98e2-0a63aa6b37da'

def main():
  helper = WehiGlobusApiHelper()
  tc = helper.get_transfer_client()

  files = [e['name'] for e in tc.operation_ls(SOURCE_ENDPOINT_ID, path="/share/godata")]

  tdata = globus.TransferData(tc, SOURCE_ENDPOINT_ID, DESTINATION_ENDPOINT_ID, sync_level="checksum")

  for file in files:
    print(file)
    tdata.add_item("/share/godata/"+file, file)

  transfer_result = tc.submit_transfer(tdata)
  print("task_id =", transfer_result["task_id"])

  completed = tc.task_wait(transfer_result["task_id"], timeout=60, polling_interval=15)
  if completed:
      print("Task finished!")
  else:
      print("Task still running after timeout reached.")

  r = tc.get_task(transfer_result['task_id'])
  print(r)

if __name__ == '__main__':
  main()
