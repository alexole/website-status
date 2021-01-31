#!/usr/bin/env bash

export $(grep -v '^#' .env | xargs)

python ./src/status/write.py
