#!/bin/bash
echo -en '\E[47;31m'"\033[1mBuild sc-machine\033[0m\n"
tput sgr0

if [ "$1" != "-ci" ];
	then
			source set_vars.sh
	fi

set -eo pipefail


cd "${PLATFORM_PATH}"/sc-machine
if [ "$1" == "--full" ] || [ "$1" == "-f" ];
	then
		rm -rf build
		rm -rf bin
fi

if [ ! -d "./build" ];
	then
		mkdir build
fi
cd build
# check last argument
if [ "${!#}" == "--debug" ] || [ "${!#}" == "-d" ];
	then
		cmake "${APP_ROOT_PATH}" -DCMAKE_BUILD_TYPE=Debug
	else
		cmake "${APP_ROOT_PATH}"
fi

make

cd "${WORKING_PATH}"
echo "${PLATFORM_PATH}"
