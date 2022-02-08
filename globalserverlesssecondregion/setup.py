# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="globalserverlesssecondregion",
    version="0.0.1",
    description="CDK Stack for the Second Region",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ralph Richards",
    package_dir={"": "globalserverlesssecondregion"},
    packages=setuptools.find_packages(where="globalserverlesssecondregion"),

    install_requires=[
        "aws-cdk.core==1.119.0",
        "aws-cdk.aws_iam==1.119.0",
        "aws-cdk.aws_sqs==1.119.0",
        "aws-cdk.aws_sns==1.119.0",
        "aws-cdk.aws_sns_subscriptions==1.119.0",
        "aws-cdk.aws_s3==1.119.0",
        "aws-cdk.aws_dynamodb==1.119.0",
        "aws-cdk.aws_lambda_event_sources==1.119.0",
        "aws-cdk.aws_appsync==1.119.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
