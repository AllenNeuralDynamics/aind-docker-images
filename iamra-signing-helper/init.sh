#!/bin/bash

if [[ -f .env ]]; then
    source .env
fi

if [[ -z "$TRUST_ANCHOR_ARN" ]]; then
  echo "Must provide TRUST_ANCHOR_ARN environment variable." 1>&2
  exit 1
fi

if [[ -z "$PROFILE_ARN" ]]; then
  echo "Must provide PROFILE_ARN environment variable." 1>&2
  exit 1
fi

if [[ -z "$ROLE_ARN" ]]; then
  echo "Must provide ROLE_ARN environment variable." 1>&2
  exit 1
fi

echo "Updating AWS credentials for default profile..."
/aws_signing_helper update \
  --certificate /iamra/client_chain.pem \
  --private-key /iamra/client_private.key \
  --trust-anchor-arn $TRUST_ANCHOR_ARN \
  --profile-arn $PROFILE_ARN \
  --role-arn $ROLE_ARN
