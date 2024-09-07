#! /bin/bash

set -x

for pair in $(cat ../bin/download-urls.txt); do
	NAME="$(printf "$pair" | awk -F'=' '{print $1}')"
	LINK="$(printf "$pair" | awk -F'=' '{print $2}')"

	# URLs should be direct so no -L (follow redirects)
	curl -o "../bin/$NAME" "$LINK"
done

sha256sum --check ../bin/sha256sum.txt
