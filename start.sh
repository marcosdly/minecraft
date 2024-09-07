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

java ${JAVA_FLAGS[@]} -jar server-1.21.1.jar ${MINE_FLAGS[@]}
