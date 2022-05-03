#!/bin/bash

cd ../
git submodule update --init --recursive

cd src/
pip3 install --upgrade pip -r dev.txt
cd ../scripts/
