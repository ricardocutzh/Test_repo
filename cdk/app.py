#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack
from modules.aurora.aurora import AuroraServerlessStack

env_USA = cdk.Environment(account="695292474035", region="us-east-1")


app = cdk.App()

#CdkStack(app, "cdk")

AuroraServerlessStack(
    app,
    "ricardo",
    "dev",
    "vpc-53ed4929",
    ["subnet-05663e4f", "subnet-3f8b1c11"],
    env=env_USA
)

app.synth()
