#!/bin/bash
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

# Setup the Lambda code

cd globalserverless/lambdacode/
npm install
zip -r Archive.zip .

rm -rf node_modules/
rm event.json
rm exports.js
rm package-lock.json
rm package.json

# Deploy stacks

cd ../../globalserverless
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -e .
cdk bootstrap
cdk deploy GlobalServerlessPrimaryStack
STREAMARN=$(aws dynamodbstreams list-streams --region ap-southeast-2 --table-name GlobalDDBTableForAppSync --limit 1 | grep -oP '(?<="StreamArn": ")[^"]*')
cdk deploy GlobalServerlessSecondaryStack --parameters globalStreamARN=$STREAMARN
deactivate

# Finish

echo "Code Setup Completed"