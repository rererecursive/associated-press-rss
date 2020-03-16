#!/bin/bash
set -e

TEMPLATE="template.out.yaml"

echo "Generating: $TEMPLATE ..."
python3 generate.py > $TEMPLATE

echo "Deploying: $TEMPLATE ..."
sam deploy \
    --stack-name AssociatedPress \
    --capabilities CAPABILITY_IAM \
    --s3-bucket my-versioning-app \
    --template $TEMPLATE

rm $TEMPLATE
