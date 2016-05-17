#!/bin/bash

/bin/bash -c "/usr/bin/mysqld_safe &" && \
  sleep 5 && \
  mysql -u root -e "CREATE DATABASE sea"

mysql -u root sea < /tmp/sea.sql

echo -e "\nc.NotebookApp.password = u'sha1:f417260a6112:16bc4218d93ec8fb6043c80d2498c9c4084a9df3'" >> /home/pa/.jupyter/jupyter_notebook_config.py

# Handle special flags if we're root
if [ $UID == 0 ] ; then
    # Change UID of NB_USER to NB_UID if it does not match
    if [ "$NB_UID" != $(id -u $NB_USER) ] ; then
        usermod -u $NB_UID $NB_USER
        chown -R $NB_UID $CONDA_DIR
    fi

    # Enable sudo if requested
    if [ ! -z "$GRANT_SUDO" ]; then
        echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
    fi

    # Start the notebook server
    exec su $NB_USER -c "env PATH=$PATH jupyter notebook $*"
else
    # Otherwise just exec the notebook
    exec jupyter notebook $*
fi


