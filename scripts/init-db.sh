#!/bin/bash
set -e

# Script to initialize PostgreSQL databases and users
# This script runs on the host and uses docker compose exec to run commands in the postgres container

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment variables from .env file
if [ -f .env ]; then
    echo -e "${GREEN}Loading environment variables from .env file...${NC}"
    export $(grep -v '^#' .env | xargs)
else
    echo -e "${YELLOW}Warning: .env file not found, using environment variables${NC}"
fi

# Ensure required environment variables are set
if [ -z "$DJANGO_DB_NAME" ] || [ -z "$DJANGO_DB_USER" ] || [ -z "$DJANGO_DB_PASSWORD" ]; then
    echo -e "${RED}Error: Required environment variables are not set${NC}"
    echo "Required variables: DJANGO_DB_NAME, DJANGO_DB_USER, DJANGO_DB_PASSWORD"
    exit 1
fi

if [ -z "$DB_USERNAME" ]; then
    echo -e "${RED}Error: DB_USERNAME is not set${NC}"
    exit 1
fi

echo -e "${GREEN}Starting database initialization...${NC}"
echo ""

# Check if postgres container is running
if ! docker compose ps postgres | grep -q "Up"; then
    echo -e "${RED}Error: postgres container is not running${NC}"
    echo "Please start the postgres container with: docker compose up -d postgres"
    exit 1
fi

echo -e "${GREEN}=== Creating Django Database ===${NC}"

# Check if database exists
DB_EXISTS=$(docker compose exec -T postgres psql -U "$DB_USERNAME" -lqt | cut -d \| -f 1 | grep -w "$DJANGO_DB_NAME" | wc -l)

if [ "$DB_EXISTS" -eq 1 ]; then
    echo -e "${GREEN}Database '${DJANGO_DB_NAME}' already exists${NC}"
else
    echo -e "${YELLOW}Creating database '${DJANGO_DB_NAME}'...${NC}"
    docker compose exec -T postgres psql -U "$DB_USERNAME" -c "CREATE DATABASE ${DJANGO_DB_NAME};"
    echo -e "${GREEN}Database '${DJANGO_DB_NAME}' created successfully${NC}"
fi

echo ""
echo -e "${GREEN}=== Creating Django User ===${NC}"

# Check if user exists
USER_EXISTS=$(docker compose exec -T postgres psql -U "$DB_USERNAME" -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DJANGO_DB_USER}'" | grep -c 1 || true)

if [ "$USER_EXISTS" -eq 1 ]; then
    echo -e "${GREEN}User '${DJANGO_DB_USER}' already exists${NC}"
    echo -e "${YELLOW}Updating password for user '${DJANGO_DB_USER}'...${NC}"
    docker compose exec -T postgres psql -U "$DB_USERNAME" -c "ALTER USER ${DJANGO_DB_USER} WITH PASSWORD '${DJANGO_DB_PASSWORD}';"
    echo -e "${GREEN}Password updated successfully${NC}"
else
    echo -e "${YELLOW}Creating user '${DJANGO_DB_USER}'...${NC}"
    docker compose exec -T postgres psql -U "$DB_USERNAME" -c "CREATE USER ${DJANGO_DB_USER} WITH PASSWORD '${DJANGO_DB_PASSWORD}';"
    echo -e "${GREEN}User '${DJANGO_DB_USER}' created successfully${NC}"
fi

echo ""
echo -e "${GREEN}=== Granting Privileges ===${NC}"

echo -e "${YELLOW}Granting all privileges on database '${DJANGO_DB_NAME}' to user '${DJANGO_DB_USER}'...${NC}"

# Grant database privileges
docker compose exec -T postgres psql -U "$DB_USERNAME" -c "GRANT ALL PRIVILEGES ON DATABASE ${DJANGO_DB_NAME} TO ${DJANGO_DB_USER};"

# Grant schema privileges
docker compose exec -T postgres psql -U "$DB_USERNAME" -d "$DJANGO_DB_NAME" -c "GRANT ALL ON SCHEMA public TO ${DJANGO_DB_USER};"

# Grant privileges on all existing tables
docker compose exec -T postgres psql -U "$DB_USERNAME" -d "$DJANGO_DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${DJANGO_DB_USER};"

# Grant privileges on all existing sequences
docker compose exec -T postgres psql -U "$DB_USERNAME" -d "$DJANGO_DB_NAME" -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${DJANGO_DB_USER};"

# Set default privileges for future tables
docker compose exec -T postgres psql -U "$DB_USERNAME" -d "$DJANGO_DB_NAME" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO ${DJANGO_DB_USER};"

# Set default privileges for future sequences
docker compose exec -T postgres psql -U "$DB_USERNAME" -d "$DJANGO_DB_NAME" -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO ${DJANGO_DB_USER};"

echo -e "${GREEN}All privileges granted successfully${NC}"

echo ""
echo -e "${GREEN}Database initialization completed successfully!${NC}"
echo ""
echo "Summary:"
echo "  - Database: $DJANGO_DB_NAME"
echo "  - User: $DJANGO_DB_USER"
echo "  - Privileges: ALL on database $DJANGO_DB_NAME"
