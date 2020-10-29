#!/usr/bin/env bash
set -e

function updaterc() {
    echo "Updating /etc/bash.bashrc"
    echo -e "$1" | tee -a /etc/bash.bashrc
}

DEFAULT_UTILS="\
    yapf\
    pre-commit"

export PIPX_HOME="/usr/local/py-utils"
export PIPX_BIN_DIR=${PIPX_HOME}/bin
export PATH=${PIPX_BIN_DIR}:${PATH}

# Update pip
echo "Updating pip..."
python3 -m pip install --no-cache-dir --upgrade pip

# Install tools
mkdir -p ${PIPX_BIN_DIR}

echo "Installing Python tools..."

# Installs pipx with pip into a tmp location, then reinstalls pipx with pipx and
# deletes the tmp

# PYTHONUSERBASE is used by pip with the --user option
export PYTHONUSERBASE=/tmp/pip-tmp
pip3 install --disable-pip-version-check --no-warn-script-location  --no-cache-dir --user pipx
$PYTHONUSERBASE/bin/pipx install --pip-args=--no-cache-dir pipx
echo "${DEFAULT_UTILS}" | xargs -n 1 $PYTHONUSERBASE/bin/pipx install --system-site-packages --pip-args '--no-cache-dir --force-reinstall'
rm -rf $PYTHONUSERBASE

updaterc "export PIPX_HOME=${PIPX_HOME}\nexport PIPX_BIN_DIR=${PIPX_BIN_DIR}\nexport PATH=\${PATH}:\${PIPX_BIN_DIR}"
