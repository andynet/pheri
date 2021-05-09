#!/bin/sh
set -e

mkdir -p          "${PREFIX}/bin"
mv ./data        "${PREFIX}/"
mv ./bin/pheri   "${PREFIX}/bin/"
mv ./bin/main.py "${PREFIX}/bin/"

