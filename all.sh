#!/bin/bash

# Run every step.

./clean.sh

./install-deps.sh

./generate.py

./build.sh

./test.sh

./deploy.sh
