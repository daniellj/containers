#!/bin/bash

echo "export environment variables"
sudo export PATH=$PATH

echo "#################################"
echo 'start the jupyterhub'
sudo nohup /srv/jupyterhub/bin/jupyterhub -f /etc/jupyterhub/jupyterhub_config.py &>/dev/null &

echo 'try to access the portal jupyterhub: yourdomain:5858/lab'

#Extra line added in the script to run all command line arguments
exec "$@";