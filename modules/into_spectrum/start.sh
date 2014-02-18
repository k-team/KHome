#!/usr/bin/env sh

at_sig() {
  echo "Kill $pid1"
  kill -15 $pid1
  kill -15 $pid2
  kill -15 $pid3
  exit 0
}

trap at_sig TERM
trap at_sig INT

mongod --dbpath ./db &
pid1=$!
[ -z "$(ls db)" ] && sleep 60 || sleep 3
cd IntoSpectrum && npm start &
pid2=$!
cd IntoSpectrum/server && node watchdog.js &
pid3=$!

while true; do sleep 1; done;
