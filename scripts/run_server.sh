#!/bin/bash
source set_vars.sh

run_server()
{
  fi=${flask_ip:-127.0.0.1}
  fp=${flask_port:-5000}
  pi=${platform_ip:-127.0.0.1}
  pp=${platform_port:-8090}
  cd "${APP_ROOT_PATH}"
  python3 src/__main__.py --flask_ip "$fi" --flask_port "$fp" --platform_ip "$pi" --platform_port "$pp"
}

help()
{
   echo "i     ip address of a flask server (default value is 127.0.0.1)"
   echo "p     port of a flask server (default value is 5000)"
   echo "s     ip address of a platform sc-server (default value is 127.0.0.1)"
   echo "c     port of a platform sc-server(default value is 8090)"
   echo ""
   echo "h     print this help"
   echo
}

while getopts "i:p:s:c:h" option; do
   case $option in
      i)
         flask_ip=$OPTARG;;
      p)
         flask_port=$OPTARG;;
      s)
         platform_ip=$OPTARG;;
      c)
         platform_port=$OPTARG;;
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

cd "${APP_ROOT_PATH}"
if [ -d "${PLATFORM_PATH}" ];
	then
	  run_server
	else
	  echo -en "Install project first\n"
fi

cd "${WORKING_PATH}"
