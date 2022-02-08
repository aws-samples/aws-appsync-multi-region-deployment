#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import core
from globalserverless.globalserverless_stack import GlobalserverlessStack

appRegions = ['eu-west-1', 'ap-southeast-2']

app = core.App()

primary_stack = GlobalserverlessStack(
    app, 
    "GlobalServerlessPrimaryStack", 
    env=core.Environment(region='eu-west-1'), 
    primary=True, 
    primary_region='eu-west-1', 
    secondary_region='ap-southeast-2'
)

app.synth()
