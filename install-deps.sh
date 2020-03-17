#!/bin/bash
mkdir -p dependencies/python
pip3 install \
    -r ap/requirements.txt \
    -t dependencies/python/ \
    --system
