#!/bin/bash

S3BUCKET=$1

aws s3 sync . s3://$S3BUCKET/cloudformation --delete