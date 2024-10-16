#!/bin/bash

# Navigate to your project directory if you're not already there
cd /path/to/youtube-transcribe-service # Update this path accordingly

# Add all changes to the staging area
git add .

# Commit the changes with a timestamp
git commit -m "Update: $(date +'%Y-%m-%d %H:%M:%S')"

# Push the changes to the main branch on GitHub
git push origin main

echo "Changes pushed to GitHub successfully!"
