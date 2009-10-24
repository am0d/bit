#!/bin/bash

for file in `ls | grep test.py`
do
    echo -e "\033[1;35mRunning $file\033[0m"
    python $file
done
