#!/bin/bash

# Instructions: 
# 1. First create a new repo on GitHub at https://github.com/new
#    - Name it: medical-rag-chatbot
#    - Choose public or private
#    - DON'T initialize with README
# 2. Replace YOUR_USERNAME below with your GitHub username
# 3. Run this script: bash push_to_github.sh

echo "🚀 Pushing Medical Chatbot to GitHub..."
echo ""

# Replace YOUR_USERNAME with your actual GitHub username
GITHUB_USERNAME="YOUR_USERNAME"
REPO_NAME="medical-rag-chatbot"

echo "Step 1: Adding remote repository..."
git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git

echo "Step 2: Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub."
echo "🔗 Repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
echo "Next step: Deploy to Render.com using this repo!"

