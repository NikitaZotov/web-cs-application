#!/bin/bash
source set_vars.sh

run_sctp()
{
  cd "${PLATFORM_PATH}"/scripts
  ./run_sctp.sh
}

set -eo pipefail

cd "${APP_ROOT_PATH}"
if [ -d "${PLATFORM_PATH}" ];
	then
	  run_sctp
	else
	  echo -en "Install project first\n"
fi

cd "${WORKING_PATH}"
