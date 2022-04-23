#!/bin/bash

echo "$1"

APP_ROOT_PATH=$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && cd .. && pwd)

if [ "$1" == "-ci" ];
    then
      {
        echo PLATFORM_PATH="${APP_ROOT_PATH}/ostis-web-platform"
        echo WORKING_PATH="$(pwd)"
        echo PYTHON_PATH="${APP_ROOT_PATH}"/problem-solver/py/services
        echo PLATFORM_REPO="https://github.com/ostis-ai/ostis-web-platform.git"
        echo REPO_PATH_FILE="repo.path"
      } >> "$GITHUB_ENV"
        cd ..
        echo APP_ROOT_PATH="$(pwd)" >> "$GITHUB_ENV"
    else 
        export PLATFORM_PATH="${APP_ROOT_PATH}/ostis-web-platform"
        export IMS_KB_FILE_PATH="${PLATFORM_PATH}/ims.ostis.kb/ims/knowledge_base_IMS.scs"
        WORKING_PATH="$(pwd)"
        export WORKING_PATH
        export PYTHON_PATH="${APP_ROOT_PATH}"/problem-solver/py/services
        export PLATFORM_REPO="https://github.com/ostis-ai/ostis-web-platform.git"
        export APP_ROOT_PATH
        export REPO_PATH_FILE="repo.path"
    fi    
