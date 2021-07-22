#!/bin/bash
cat /dev/stdin | grep -o "[^,]*@[^,]*"
