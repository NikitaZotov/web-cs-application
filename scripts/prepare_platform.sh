#!/bin/bash

echo -en "Install OSTIS platform\n"
git clone "${PLATFORM_REPO}"
cd "${PLATFORM_PATH}" || { echo "OSTIS web platform wasn't installed"; exit 1; }
git checkout minimum_required
cd "${APP_ROOT_PATH}" || { echo "Submodules wasn't installed"; exit 1; }
git submodule update --init --recursive

cd "${PLATFORM_PATH}"/scripts || { echo "OSTIS web platform was incorrectly installed. Scripts not found"; exit 1; }
./prepare.sh no_build_kb no_build_sc_machine

if ! grep -q "${INTERFACE_PATH}" "${PLATFORM_PATH}/sc-machine/config/config.ini.in";
        then
            INTERFACE_PATH_ESCAPED="$(echo "${INTERFACE_PATH}" | sed -e 's/[/]/\\&/g')"
            sed -i "s/^path.*=.*/path = ${INTERFACE_PATH_ESCAPED}/" "${PLATFORM_PATH}/sc-machine/config/config.ini.in"
fi

if ! grep -q "${PYTHON_PATH}" "${PLATFORM_PATH}/sc-machine/config/config.ini.in";
        then
            PYTHON_PATH_ESCAPED="$(echo "${PYTHON_PATH}" | sed -e 's/[/]/\\&/g')"
            sed -i "/modules_path/ s/$/;${PYTHON_PATH_ESCAPED}/" "${PLATFORM_PATH}/sc-machine/config/config.ini.in"
fi
if ! grep -q "${CONNECTED_TOOLS_PATH}" "${PLATFORM_PATH}/sc-machine/config/config.ini.in";
        then
            CONNECTED_TOOLS_PATH_ESCAPED="$(echo "${CONNECTED_TOOLS_PATH}" | sed -e 's/[/]/\\&/g')"
            sed -i "/modules_path/ s/$/;${CONNECTED_TOOLS_PATH_ESCAPED}/" "${PLATFORM_PATH}/sc-machine/config/config.ini.in"
fi

cd "${PLATFORM_PATH}" || { echo "OSTIS web platform was removed"; exit 1; }
rm -rf ./kb/menu

cd "${APP_ROOT_PATH}"
# remove blank lines
awk 'NF' "${PLATFORM_PATH}"/"${REPO_PATH_FILE}" > "${PLATFORM_PATH}"/prepared"${REPO_PATH_FILE}"
# add ostis-web-platform/ to beginning of lines that don't contain #
sed -i -E '/(#)/!s/^/ostis-web-platform\//' "${PLATFORM_PATH}"/prepared"${REPO_PATH_FILE}"
cat "${APP_ROOT_PATH}"/"${REPO_PATH_FILE}" >> "${PLATFORM_PATH}"/prepared"${REPO_PATH_FILE}"
cat "${PLATFORM_PATH}"/prepared"${REPO_PATH_FILE}" > "${APP_ROOT_PATH}"/"${REPO_PATH_FILE}"
rm "${PLATFORM_PATH}"/prepared"${REPO_PATH_FILE}"

cd "${PLATFORM_PATH}"/scripts || { echo "OSTIS web platform scripts was removed"; exit 1; }
python3 kb_scripts/prepare_kb.py
