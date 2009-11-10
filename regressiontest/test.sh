#!/bin/bash

for dir in `ls | grep test.py`
do
    echo -e "\033[1;35mRunning $file\033[0m"
    python2.6 $file
done
