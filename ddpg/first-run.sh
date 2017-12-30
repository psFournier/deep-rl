#!/usr/bin/env bash

NAMES=(a b c d e f)
FORCE="true"

for NAME in ${NAMES[*]}
do
  export LOGS=logs/perf/$NAME
  rm -rf $LOGS
  mkdir -p $LOGS
  (
    export LOGS
    export NAME
    export FORCE
    export PERF_STUDY="xperf_$NAME"
    rm -f $LOGS/${PERF_STUDY}.e* $LOGS/${PERF_STUDY}.o* ${PERF_STUDY}.e* ${PERF_STUDY}.o*
    qsub -N ${PERF_STUDY} -o "$LOGS/${PERF_STUDY}.out" -b "$LOGS/${PERF_STUDY}.err" -d . first-submit.sh
  )
done
