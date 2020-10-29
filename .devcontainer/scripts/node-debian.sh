#!/bin/bash

export NODE_VERSION="lts/*"

set -e

# Ensure apt is in non-interactive to avoid prompts
export DEBIAN_FRONTEND=noninteractive

# Install the specified node version if NVM directory already exists, then exit
if [ -d "${NVM_DIR}" ]; then
    echo "NVM already installed."
    if [ "${NODE_VERSION}" != "" ]; then
       su ${USERNAME} -c "source $NVM_DIR/nvm.sh && nvm install ${NODE_VERSION} && nvm clear-cache"
    fi
    exit 0
fi


# Run NVM installer if needed
mkdir -p ${NVM_DIR}

# Do not update profile - we'll do this manually
export PROFILE=/dev/null

curl -so- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash 
source ${NVM_DIR}/nvm.sh
nvm alias default ${NODE_VERSION}
nvm clear-cache 

echo "Updating /etc/bash.bashrc and /etc/zsh/zshrc with NVM scripts..."
(cat <<EOF
export NVM_DIR="${NVM_DIR}"
[ -s "\$NVM_DIR/nvm.sh" ] && . "\$NVM_DIR/nvm.sh"
[ -s "\$NVM_DIR/bash_completion" ] && . "\$NVM_DIR/bash_completion"
EOF
) | tee -a /etc/bash.bashrc



echo "Done!"