#!/bin/bash

# Hospital LOS Dashboard Setup Script
# This script sets up the project environment and gets it ready to run

echo "🏥 Hospital Length of Stay Prediction Dashboard"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Step 1: Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if (( python_major < 3 )) || (( python_major == 3 && python_minor < 9 )); then
    echo -e "${RED}✗ Python 3.9+ required. Found: $python_version${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Python $python_version found${NC}"
fi

# Create virtual environment
echo ""
echo -e "${BLUE}Step 2: Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo -e "${BLUE}Step 3: Activating virtual environment...${NC}"
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo -e "${BLUE}Step 4: Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install requirements
echo ""
echo -e "${BLUE}Step 5: Installing dependencies...${NC}"
echo "This may take 2-3 minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Create required directories
echo ""
echo -e "${BLUE}Step 6: Creating project directories...${NC}"
mkdir -p data models utils pages

if [ -d "data" ] && [ -d "models" ]; then
    echo -e "${GREEN}✓ Directories created${NC}"
else
    echo -e "${YELLOW}✗ Failed to create some directories${NC}"
fi

# Check for dataset
echo ""
echo -e "${BLUE}Step 7: Checking for dataset...${NC}"
if [ -f "data/LengthOfStay.csv" ]; then
    lines=$(wc -l < data/LengthOfStay.csv)
    echo -e "${GREEN}✓ Dataset found (${lines} lines)${NC}"
else
    echo -e "${YELLOW}⚠ Dataset not found (data/LengthOfStay.csv)${NC}"
    echo -e "${YELLOW}  Please place LengthOfStay.csv in the data/ folder${NC}"
fi

# Check for model
echo ""
echo -e "${BLUE}Step 8: Checking for trained model...${NC}"
if [ -f "models/best_model.pkl" ]; then
    echo -e "${GREEN}✓ Pre-trained model found${NC}"
else
    echo -e "${YELLOW}⚠ Model not found (models/best_model.pkl)${NC}"
    echo -e "${YELLOW}  Model will be created when needed${NC}"
fi

# Final summary
echo ""
echo "=================================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Ensure 'LengthOfStay.csv' is in data/ folder"
echo "2. Run: streamlit run app.py"
echo "3. Open browser to: http://localhost:8501"
echo ""
echo "📚 Documentation: See README.md"
echo "🏛️ Architecture: See DASHBOARD_MASTER_PLAN.md"
echo ""
