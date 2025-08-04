#!/bin/bash
# Run tests for this project only

# Set locale to avoid git warnings
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧪 Running tests for Ics Calendar Utils...${NC}"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run tests
if [ -d "tests" ]; then
    pytest tests/ -v
else
    echo -e "${BLUE}💡 No tests directory found${NC}"
fi
