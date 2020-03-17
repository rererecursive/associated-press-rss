#!/bin/bash

sam local invoke ApScraperTopNews \
    --region ap-southeast-2 \
    -e event.json
