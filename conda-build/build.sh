#!/bin/sh
set -e

mkdir -p   "${PREFIX}/bin"
mv data    "${PREFIX}/"
mv run.sh  "${PREFIX}/bin/"
mv main.py "${PREFIX}/bin/"

