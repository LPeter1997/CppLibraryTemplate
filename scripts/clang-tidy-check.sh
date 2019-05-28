#!/bin/bash

echoerr() { echo "$@" 1>&2; }

if [[ -n $(grep "warning: " $1) ]] || [[ -n $(grep "error: " $1) ]]; then
    echoerr "You must pass the clang tidy checks before submitting a pull request!"
    echoerr ""
    (grep --color -E '^|warning: |error: ' $1) 1>&2
    # Because travis...
    sleep 1
    exit -1;
else
    echoerr -e "\033[1;32m\xE2\x9C\x93 passed:\033[0m $1";
fi;
