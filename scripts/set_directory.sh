#!/bin/bash

dir="$1"
http POST "127.0.0.1:5000/set?directory=$dir"
