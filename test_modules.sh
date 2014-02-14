#!/usr/bin/env sh

for module in $(ls ./modules/); do
  ./test_module.py $module;
  read;
done;
