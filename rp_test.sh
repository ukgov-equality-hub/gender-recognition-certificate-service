#!/bin/bash

echo "Starting readiness probe"
echo "curl admin"
curl -I http://0.0.0.0:3001
echo "curl app"
curl -I http://0.0.0.0:3000
echo "curl dashboard"
curl -I http://0.0.0.0:3002
echo ""
echo "readiness probe started"