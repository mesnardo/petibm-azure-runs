#!/usr/bin/env bash
# Provision a pool, ingress data, run a job,
# and delete job and pool once the job is completed.
# cli: ./shipyard-driver.sh

#read -p "Enter configuration directory: " configdir
configdir="config_shipyard"
export SHIPYARD_CONFIGDIR=$configdir
#echo -n "Password:"
#read -s password
password="\$BDolv381738"
export SHIPYARD_AAD_PASSWORD=$password
#echo
#read -p "Enter directory for log files (press enter to use ./log_shipyard): " logdir
#logdir=${logdir:-"log_shipyard"}
logdir="log_shipyard"
mkdir -p $logdir

shipyard --version > $logdir/version.log 2>&1
echo "Provisioning pool of compute nodes..."
shipyard pool add --yes > $logdir/pool-add.log 2>&1
echo "Ingressing input data..."
shipyard data ingress > $logdir/data-ingress.log 2>&1
echo "Submitting job..."
shipyard jobs add > $logdir/jobs-add.log 2>&1
echo "Polling job until task is complete..."
shipyard jobs tasks list --poll-until-tasks-complete > $logdir/jobs-monitor.log 2>&1
###
echo "Checking if task succeeded..."
shipyard jobs tasks list --jobid "job-snake3d2k45" 2>info.txt
python $HOME/tmp/checkexitcode.py info.txt > errorcode.txt
rc=$(<errorcode.txt)
if [ $rc != 0 ]; then
	exit $rc
fi
###
echo "Deleting pool..."
shipyard pool del --yes > $logdir/pool-del.log 2>&1

unset SHIPYARD_CONFIGDIR
unset SHIPYARD_AAD_PASSWORD
echo "Done."
