#!/usr/bin/env bash

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
simudir=$scriptdir

source /opt/intel/compilers_and_libraries/linux/mpi/intel64/bin/mpivars.sh

# get number of nodes
IFS=',' read -ra HOSTS <<< "$AZ_BATCH_HOST_LIST"
nodes=${#HOSTS[@]}
echo "Number of nodes: $nodes"
echo "Hosts: $AZ_BATCH_HOST_LIST"
# number of processes per node
ppn=12
echo "Number of processes per node to use: $ppn"
# number of processes
np=$(($nodes * $ppn))
echo "Total number of processes: $np"

# get number of GPUs on machine
ngpusmax=`nvidia-smi -L | wc -l`
echo "Number of GPU devices available on each node: $ngpusmax"
# number of GPUs to use per node
CUDA_VISIBLE_DEVICES=0,1
IFS=',' read -ra GPUS <<< "$CUDA_VISIBLE_DEVICES"
ngpus=${#GPUS[@]}
echo "Number of GPU devices per node to use: $ngpus ($CUDA_VISIBLE_DEVICES)"

echo "PATH: $PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

cp $AZ_BATCH_TASK_DIR/stdout.txt $simudir
cp $AZ_BATCH_TASK_DIR/stderr.txt $simudir

mpirun -np $np -ppn $ppn -host $AZ_BATCH_HOST_LIST \
  -genv CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
  petibm-decoupledibpm \
  -directory $simudir \
  -log_view ascii:$simudir/view.log \
  -malloc_log \
  -memory_view \
  -options_left >> $simudir/stdout.txt 2> $simudir/stderr.txt

rc=$?
if [ $rc != 0 ]; then
	storageaccountname="<storage-account-name>"
	sharename="<storage-share-name>"
	mountpoint="/mnt/$sharename"
	mkdir -p $mountpoint
	storageaccountkey="<storage-account-key>"
	mount -t cifs //$storageaccountname.file.core.windows.net/$sharename $mountpoint -o vers=3.0,username=$storageaccountname,password=$storageaccountkey,dir_mode=0777,file_mode=0777,sec=ntlmssp
	cp -r $simudir $mountpoint
fi
exit $rc
