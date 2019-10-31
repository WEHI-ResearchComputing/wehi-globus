# WEHI Globus Downloads

This a lightweight skeleton project for programmatic Globus downloads.

## Prerequisite tasks
1. Create a python environment and install the prequisites. Only a couple of packages are required so installing in your user area is fine. Otherwise use a virtual environment. Python 3.7 or higher is required.
2. Setup [Globus Connect Personal](https://www.globus.org/globus-connect-personal) (GCP) to service your endpoint. This needs to be done interactively the first time but can there after run in the background or even in the batch system.
3. Login using the `globus-login.py` script. This also needs to be done interactively the login tokens should last 6 months. Look in `helper.py` for more details. This is different to the Globus CLI in that different authorisation tokens are acquired. These tokens should be kept confidential.
4. Edit the `config.py` to match your requirements.

## Simple downloads
The `globus-simple-download.py` script
1. Lists the files in the source endpoint
2. Builds a single transfer request
3. Submits the request
4. Waits for completion
5. Prints the result.

This is likely to be adequate for small downloads. For larger downloads you may prefer to split it into batches so that the GCP is not overwhelmed.

## Complex of large downloads
If you have a lot of files or more data than can be stored concurrently, you may prefer to trickle the data down, process it then delete. The `globus-batch-download.py` will build and submit jobs to the batch system that then download a single file and call a script, that you provide, to process the file. It works as follows:
1. Run the `globus-batch-download.py` script from the login node or even as another batch job.
2. This script lists files in the source end point
3. Filters the files using a function that you write. If the file has already been processed (an output exists) or doesn't match your criteria then the function should return false. This provides some ability to restart failed processing.
4. A batch job is build and submitted to the batch system which:
    1. The job script is `wrapper.sh`.
    2. This calls `globus-single-file-download.py` to download a single file.
    4. If successful, the script `process.sh` is called with the file passed as an argument.
5. The `globus-batch-download.py` script maintains a used defined number of jobs in the system at a time.

## Notes.
The software has not been tested in anger. There may be scaling issues. Many failure modes will not be handled correctly. Please open issues or, even better, submit pull requests.

