#!/bin/sh

echo "#################################"
echo "stop ssh service"
sudo systemctl stop postgresql

echo "start ssh service"
sudo systemctl start postgresql

echo "restart ssh service"
sudo systemctl restart postgresql

echo "status ssh service"
sudo systemctl status postgresql
echo "#################################"
#Extra line added in the script to run all command line arguments
exec "$@";