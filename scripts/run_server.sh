#!/bin/bash

run_server()
{
  fi=${flask_ip:-127.0.0.1}
  fp=${flask_port:-5000}
  cd "${APP_ROOT_PATH}"
  python3 src/__main__.py --flask_ip "$fi" --flask_port "$fp"
}

help()
{
   echo "i     ip address of a flask server (default value is 127.0.0.1)"
   echo "p     port of a flask server (default value is 5000)"
   echo ""
   echo "h     print this help"
   echo
}

while getopts "i:p:h" option; do
   case $option in
      i)
         flask_ip=$OPTARG;;
      p)
         flask_port=$OPTARG;;
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

cd ../
run_server
