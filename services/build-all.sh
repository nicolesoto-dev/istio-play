#!/bin/bash
# Build and load all service images into Kind cluster
# Usage: ./build-all.sh [registry]
# Example: ./build-all.sh  (uses default: cloudmart)

REGISTRY="${1:-cloudmart}"
SERVICES=(product-svc order-svc payment-svc user-svc inventory-svc)

set -e

cd "$(dirname "$0")"

for svc in "${SERVICES[@]}"; do
  echo "==> Building ${svc}..."
  docker build -t "${REGISTRY}/${svc}:v1" "${svc}/"
  echo "==> Loading ${svc}:v1 into Kind..."
  kind load docker-image "${REGISTRY}/${svc}:v1" --name cloudmart
done

# Build product-svc v2 with VERSION=v2
echo "==> Building product-svc v2..."
docker build -t "${REGISTRY}/product-svc:v2" product-svc/
kind load docker-image "${REGISTRY}/product-svc:v2" --name cloudmart

echo ""
echo "All images built and loaded into Kind cluster 'cloudmart'."
echo "Images:"
for svc in "${SERVICES[@]}"; do
  echo "  - ${REGISTRY}/${svc}:v1"
done
echo "  - ${REGISTRY}/product-svc:v2"
