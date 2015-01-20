#!/bin/bash

# Define a timestamp function
timestamp() {
	date +"%H:%M:%S [Import]"
}

# Count how often we have tried to connect to Virtuoso
TIMEOUT_COUNTER=0

echo "$(timestamp) Connecting to Virtuoso ..."
sleep 3

while ! isql-vt exec='select 1;' &> /dev/null; do
	if ((TIMEOUT_COUNTER == 0)); then
		echo "$(timestamp) Waiting for Virtuoso ..."
	elif ((TIMEOUT_COUNTER < 10)); then
		echo "$(timestamp) Still waiting for Virtuoso ..."
	elif ((TIMEOUT_COUNTER == 10)); then
		echo "$(timestamp) Virtuoso failed to respond, giving up." >&2
		exit 1
	fi

	((TIMEOUT_COUNTER++))
	sleep 3
done

echo "$(timestamp) Select the files to import"
isql-vt exec="ld_dir('./output', '*.nt.gz', 'http://wikidata.org');"

echo "$(timestamp) Start the import"
isql-vt exec="rdf_loader_run();" &

# Remember the process ID of the import
pid=$!

# If this script is killed, kill the import
trap "kill $pid 2> /dev/null" EXIT

# While the import ir running ...
while kill -0 $pid 2> /dev/null; do
		# ... print the status
		echo "$(timestamp) Current import status:"
		isql-vt exec="select * from DB.DBA.load_list;"
		sleep 10
done

# Disable the trap on a normal exit
trap - EXIT
