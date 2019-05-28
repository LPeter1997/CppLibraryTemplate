#!/bin/bash

echoerr() { echo "$@" 1>&2; }

warn_cnt=$(grep -c "warning: " $1)
err_cnt=$(grep -c "error: " $1)

echoerr "Warnings: ${warn_cnt}"
echoerr "Errors: ${err_cnt}"

if [ "$warn_cnt" -gt 0 ] || [ "$err_cnt" -gt 0 ]; then
    echoerr "Warnings or errors in the output!"
    exit -1;
fi;
