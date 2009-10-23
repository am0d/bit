#!/bin/bash

for file in `ls | grep test.py`
do
    python $file
done
