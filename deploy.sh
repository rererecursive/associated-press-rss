#!/bin/bash
set -e

TEMPLATE=".aws-sam/build/template.yaml"

echo "Deploying: $TEMPLATE ..."
sam deploy \
    --stack-name AssociatedPress \
    --capabilities CAPABILITY_IAM \
    --s3-bucket my-versioning-app \
    --template $TEMPLATE