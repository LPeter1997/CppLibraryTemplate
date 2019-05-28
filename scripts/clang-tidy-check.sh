#!/bin/bash

set -e

warn_cnt=$(grep -c "warning: " $1)
err_cnt=$(grep -c "error: " $1)

echo "Warnings: ${warn_cnt}"
echo "Errors: ${err_cnt}"

if [ "$warn_cnt" -gt 0 ] || [ "$err_cnt" -gt 0 ]; then
    echo "Warnings or errors in the output!"
    exit -1;
fi;
