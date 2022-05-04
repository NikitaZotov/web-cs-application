#!/bin/bash

run_server()
{
  fi=${ip:-127.0.0.1}
  fp=${port:-7040}
  pi=${server_ip:-127.0.0.1}
  pp=${server_port:-8090}
  python3 "$PWD"/py-scripts/rest/__main__.py --ip "$fi" --port "$fp" --server_ip "$pi" --server_port "$pp"
}

help()
{
   echo "i     ip address of a flask REST-server (default value is 127.0.0.1)"
   echo "p     port of a flask REST-server (default value is 7040)"
   echo "s     ip address of a platform sc-server (default value is 127.0.0.1)"
   echo "c     port of a platform sc-server (default value is 8090)"
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
