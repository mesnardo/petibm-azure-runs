

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
