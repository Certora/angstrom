#!/bin/bash

# run from root directory certora/scripts/certoraRunScript <conf_file_name> 

set -e

CONF_FILE=$1

if [ -z "$CONF_FILE" ]; then
  echo "Error: No conf file provided."
  echo "Usage: $0 <conf_file_name>"
  exit 1
fi

# Run Munge.sh
./certora/scripts/Munge.sh

# Run certoraRun with the provided conf file
if ! certoraRun certora/confs/$CONF_FILE --server production --prover_version master; then
  echo "certoraRun failed, continuing to Unmunge."
fi

# Run Unmunge.sh
./certora/scripts/Unmunge.sh
