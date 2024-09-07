#! /bin/bash

set -x

cd $(dirname $(realpath "$0"))

JAVA_FLAGS=(
	-Xmx4G
	-Xms1G
	-XX:+UnlockExperimentalVMOptions
	-XX:+UseZGC
	-XX:-ZProactive
	-XX:SoftMaxHeapSize=3G
)

MINE_FLAGS=(
	--nogui
	--bonusChest
	--port=1337 
)

while [ true ]; do
	java ${JAVA_FLAGS[@]} -jar server.jar ${MINE_FLAGS[@]}
	echo "Server restarting..."
	echo "Press CTRL + C to stop."
done
