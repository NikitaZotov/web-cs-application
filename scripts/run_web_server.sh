#!/bin/bash

run_server()
{
  fi=${ip:-127.0.0.1}
  fp=${port:-7050}
  si=${server_ip:-127.0.0.1}
  sp=${server_port:-7040}
  python3 -m py-scripts.web.__main__ --ip "$fi" --port "$fp" --server_ip "$si" --server_port "$sp"
}

help()
{
   echo "i     ip address of a flask web-server (default value is 127.0.0.1)"
   echo "p     port of a flask web-server (default value is 7050)"
   echo "s     ip address of a flask REST-server (default value is 127.0.0.1)"
   echo "c     port of a flask REST-server (default value is 7040)"
   echo ""
   echo "h     print this help"
   echo
}

while getopts "i:p:s:c:h" option; do
   case $option in
      i)
         ip=$OPTARG;;
      p)
         port=$OPTARG;;
      s)
         server_ip=$OPTARG;;
      c)
         server_port=$OPTARG;;
      h)
         help
         exit;;
      \?) # incorrect option
         echo "Error: Invalid option"
         help
         exit;;
   esac
  done

set -eo pipefail

cd ../src
run_server
