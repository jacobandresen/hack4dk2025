#!/bin/bash

echo "Testing Filmkassen setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Build and start services
echo "Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "Checking service health..."

# Check database
if docker-compose exec -T database pg_isready -U postgres -d filmkassen > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database is not ready"
    docker-compose logs database
    exit 1
fi

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is ready"
else
    echo "❌ Backend is not ready"
    docker-compose logs backend
    exit 1
fi

# Check frontend
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is ready"
else
    echo "❌ Frontend is not ready"
    docker-compose logs frontend
    exit 1
fi

echo ""
echo "🎉 All services are running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/swagger"
echo ""
echo "To run E2E tests:"
echo "cd tests/e2e && npm install && npx playwright test"
echo ""
echo "To stop services:"
echo "docker-compose down"
