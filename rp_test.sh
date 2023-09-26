#!/bin/bash

echo "Starting readiness probe"
curl -I http://0.0.0.0:3001
echo ""
echo "readiness probe started"