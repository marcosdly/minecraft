#! /bin/bash

set -x

for pair in $(cat ../plugins/download-urls.txt); do
	NAME="$(printf "$pair" | awk -F'=' '{print $1}')"
	LINK="$(printf "$pair" | awk -F'=' '{print $2}')"

	# URLs should be direct so no -L (follow redirects)
	curl -o "../plugins/$NAME" "$LINK"
done

sha256sum --check ../plugins/sha256sum.txt
