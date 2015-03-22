#!/bin/sh

CWD="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

line="*/10 * * * * ${CWD}/runtest"
(crontab -u root -l; echo "$line" ) | crontab -u root -
