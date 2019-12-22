#!/bin/bash
sam build && sam local invoke ApScraper --region ap-southeast-2 -e event.json
