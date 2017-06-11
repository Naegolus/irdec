#!/bin/sh

cat mode2-output.txt | paste -s | tr '\t' ' ' | tr -s ' '
