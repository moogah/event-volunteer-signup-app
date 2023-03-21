#!/usr/bin/env bash

python3 unit_tests.py || { echo 'Failed Unit Tests' ; exit 1; } 

python3 runner.py
