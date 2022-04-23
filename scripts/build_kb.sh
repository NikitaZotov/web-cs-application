#!/bin/bash
PREPARED_KB="prepared_kb"

if [[ -z ${PLATFORM_PATH+1} ]];
then
  source set_vars.sh
fi

ERRORS_FILE="${PLATFORM_PATH}/scripts/prepare.log"
if [[ -e  ${ERRORS_FILE} ]]; then
    rm "$ERRORS_FILE"
fi
touch "$ERRORS_FILE"

python3 "${PLATFORM_PATH}"/scripts/kb_scripts/prepare_kb.py "${PWD%/[^/]*}" $PREPARED_KB $REPO_PATH_FILE "$ERRORS_FILE"
cd ..


if [[ -f ${ERRORS_FILE} && ! ( -s ${ERRORS_FILE} )]]; then
  set -e -o pipefail
  "${PLATFORM_PATH}"/sc-machine/bin/sc-builder -f -c -i $PREPARED_KB/$REPO_PATH_FILE -o "${PLATFORM_PATH}"/kb.bin -s "${PLATFORM_PATH}"/config/sc-web.ini -e "${PLATFORM_PATH}"/sc-machine/bin/extensions
  rm "$ERRORS_FILE"
fi