#!/usr/bin/env sh

at_sig() {
  echo "Kill $pid1"
  # kill -15 $pid1
  kill -15 $pid2
  # kill -15 $pid3
  exit 0
}

trap at_sig TERM
trap at_sig INT

# mongod &
# pid1=$!
# sleep 3
cd app && npm start &
pid2=$!
# cd app/server && node watchdog.js &
# pid3=$!

while true; do sleep 1; done;
