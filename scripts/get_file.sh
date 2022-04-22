#!/bin/bash

file="$1"
http GET "127.0.0.1:5000/download?file=$file"
