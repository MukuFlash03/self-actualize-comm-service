#!/bin/bash

# Get DATABASE_URL from SSM Parameter Store
DATABASE_URL=$(aws ssm get-parameter \
    --name "/prod/comm-service-backend/DATABASE_URL" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)

# Stop and remove existing container if it exists
docker stop communication-backend || true
docker rm communication-backend || true

# Run new container with DATABASE_URL
docker run -d \
    -p 5000:5000 \
    -e DATABASE_URL="$DATABASE_URL" \
    --name communication-backend \
    116981800049.dkr.ecr.us-east-1.amazonaws.com/self-actualize/comm-service:v1.1.0

echo "Container started with DATABASE_URL from SSM"
