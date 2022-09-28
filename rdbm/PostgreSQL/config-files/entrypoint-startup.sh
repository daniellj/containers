#!/bin/sh

echo "#################################"
echo "stop ssh service"
sudo systemctl stop postgresql.service

echo "start ssh service"
sudo systemctl start postgresql.service

echo "restart ssh service"
sudo systemctl restart postgresql.service
echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";