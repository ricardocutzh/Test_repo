#!/bin/bash

S3BUCKET=$1

echo ">> changing directory "
cd slack_lambda/

echo ">> ziping files"
zip -r ../zip/slack_lambda2.zip *

echo ">> going back..."
cd ..

echo ">> showing directory zip/"
ls -la zip/

echo ">> uploading to s3"

aws s3 sync zip/ s3://$S3BUCKET/zip --delete