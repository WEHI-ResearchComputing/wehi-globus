#!/bin/bash

#
# This runs in the batch system:
# - calls a python script to download the file
# - calls the process.sh script to actually process the file.

# Setup your python enviroment. This may be a virtual env or a conda
module load python/3.7.0

python globus-single-file-download.py --globus-path $1 --file $2

if [ $? == "0" ]
then
  ./process.sh $2
fi