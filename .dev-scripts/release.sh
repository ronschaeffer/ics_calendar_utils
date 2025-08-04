#!/bin/bash
# Semantic versioning release script

# Set locale to avoid git warnings
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}❌ Uncommitted changes detected. Please commit or stash changes first.${NC}"
    exit 1
fi

# Get current version from pyproject.toml
get_current_version() {
    if command -v poetry >/dev/null 2>&1; then
        poetry version --short 2>/dev/null
    else
        grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'
    fi
}

# Increment version based on type
increment_version() {
    local version=$1
    local type=$2
    
    # Parse version (assuming semantic versioning: MAJOR.MINOR.PATCH)
    local major=$(echo "$version" | cut -d. -f1)
    local minor=$(echo "$version" | cut -d. -f2)
    local patch=$(echo "$version" | cut -d. -f3)
    
    case "$type" in
        "major")
            echo "$((major + 1)).0.0"
            ;;
        "minor")
            echo "${major}.$((minor + 1)).0"
            ;;
        "patch")
            echo "${major}.${minor}.$((patch + 1))"
            ;;
        *)
            echo "$version"
            ;;
    esac
}

# Parse command line arguments
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}Usage: $0 <version|--major|--minor|--patch>${NC}"
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  $0 1.2.3        # Set specific version"
    echo -e "  $0 --major      # Increment major version (1.0.0 -> 2.0.0)"
    echo -e "  $0 --minor      # Increment minor version (1.0.0 -> 1.1.0)"
    echo -e "  $0 --patch      # Increment patch version (1.0.0 -> 1.0.1)"
    exit 1
fi

CURRENT_VERSION=$(get_current_version)
if [ -z "$CURRENT_VERSION" ]; then
    echo -e "${RED}❌ Could not determine current version${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Current version: ${YELLOW}$CURRENT_VERSION${NC}"

# Determine new version
case "$1" in
    "--major")
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "major")
        ;;
    "--minor")
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "minor")
        ;;
    "--patch")
        NEW_VERSION=$(increment_version "$CURRENT_VERSION" "patch")
        ;;
    *)
        NEW_VERSION="$1"
        ;;
esac

echo -e "${BLUE}🎯 New version: ${GREEN}$NEW_VERSION${NC}"
echo ""

# Confirm release
echo -e "${YELLOW}This will:${NC}"
echo -e "  1. Update version in pyproject.toml to $NEW_VERSION"
echo -e "  2. Update version in source code (__init__.py)"
echo -e "  3. Commit changes with message: 'Release v$NEW_VERSION'"
echo -e "  4. Create and push git tag: v$NEW_VERSION"
echo -e "  5. Trigger GitHub Actions for build/publish"
echo ""

read -p "Continue with release? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🚫 Release cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🚀 Starting release process...${NC}"

# Update version in pyproject.toml using Poetry if available
if command -v poetry >/dev/null 2>&1; then
    echo -e "${BLUE}📝 Updating version with Poetry...${NC}"
    poetry version "$NEW_VERSION"
else
    echo -e "${BLUE}📝 Updating version in pyproject.toml...${NC}"
    sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
fi

# Update version in source code (__init__.py files)
echo -e "${BLUE}📝 Updating version in source code...${NC}"
find . -name "__init__.py" -path "./src/*" -exec sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" {} \;

# Commit changes
echo -e "${BLUE}📝 Committing changes...${NC}"
git add pyproject.toml
find . -name "__init__.py" -path "./src/*" -exec git add {} \;
git commit -m "Release v$NEW_VERSION"

# Create and push tag
echo -e "${BLUE}🏷️ Creating and pushing tag...${NC}"
git tag "v$NEW_VERSION"
git push origin main --tags

echo ""
echo -e "${GREEN}✅ Release v$NEW_VERSION completed successfully!${NC}"
echo -e "${BLUE}📦 Check GitHub Actions for build progress:${NC}"
echo -e "${BLUE}   https://github.com/ronschaeffer/ics_calendar_utils/actions${NC}"

