#!/bin/bash
set -e

TEMPLATE="template.out.yaml"
echo "Building: $TEMPLATE ..."

sam build \
    --template $TEMPLATE \
