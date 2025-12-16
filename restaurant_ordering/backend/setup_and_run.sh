#!/bin/bash

# Remove existing virtual environment
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Start the server on port 8002 to avoid conflicts
uvicorn app.main:app --reload --port 8002
