#!/usr/bin/env python3

from aws_cdk import core
from globalserverlesssecondregion.globalserverlesssecondregion_stack import GlobalserverlesssecondregionStack

app = core.App()

secondary_stack = GlobalserverlesssecondregionStack(
    app, 
    "GlobalServerlessSecondaryStack", 
    env=core.Environment(region='ap-southeast-2')
)

app.synth()