

rc=$?
if [ $rc != 0 ]; then
	mountpoint="$AZ_BATCH_NODE_ROOT_DIR/mounts"
	accountname="<storage-account-name>"
	fileshare="<storage-share-name>"
	rm -rf core.*
	cp -r $simudir $mountpoint/azfile-$accountname-$fileshare
fi
exit $rc
