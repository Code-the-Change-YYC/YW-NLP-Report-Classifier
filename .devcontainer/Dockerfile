FROM python:3.8

# Install the Spacy model ASAP to maximize the possibility of the install being
# cached
ENV SPACY_MODEL_URL="https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.3.1/en_core_web_lg-2.3.1.tar.gz"
# Ideally the install will be cached, but use this to ensure the model is not
# being installed
ARG INSTALL_SPACY_MODEL="true"
RUN if [ "$INSTALL_SPACY_MODEL" = "true" ]; then pip3 --no-cache-dir install $SPACY_MODEL_URL; fi

# From
# https://code.visualstudio.com/docs/remote/containers-advanced#_persist-bash-history-between-runs
# for persisting bash history
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo $SNIPPET >> "/root/.bashrc"

# Setup global Python stuff
COPY .devcontainer/scripts/python-debian.sh /tmp/scripts/
RUN bash /tmp/scripts/python-debian.sh && rm -rf /tmp/scripts
   
# Setup node, nvm
ENV NVM_DIR=/usr/local/share/nvm
ENV NVM_SYMLINK_CURRENT=true \
    PATH=${NVM_DIR}/current/bin:${PATH}
COPY .devcontainer/scripts/node-debian.sh /tmp/scripts/
RUN bash /tmp/scripts/node-debian.sh && rm -rf /tmp/scripts
    
# Install project python dependencies
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

# Install project node dependencies
ENV PROJECT_NODE_MODULES=/usr/local/project_node_modules/
COPY client/package.json $PROJECT_NODE_MODULES
COPY client/package-lock.json $PROJECT_NODE_MODULES
WORKDIR $PROJECT_NODE_MODULES
RUN [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" \
    && nvm exec default npm install --global \