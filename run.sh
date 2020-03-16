#!/bin/bash
find /tmp -maxdepth 1 -name 'output-*.xml' -delete
BUCKET=my-versioning-app python3.6 ap/main.py
