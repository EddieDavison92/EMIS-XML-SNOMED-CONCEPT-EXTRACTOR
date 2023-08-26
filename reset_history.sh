#!/bin/bash

# Reset the History for main
git checkout main
git checkout --orphan tempmain
git add -A  
git commit -m "Initial commit for main"

# Replace main with Clean History
git branch -D main
git branch -m main
git push -f origin main

# Reset the History for stage
git checkout stage
git checkout --orphan tempstage
git add -A  
git commit -m "Initial commit for stage"

# Replace stage with Clean History
git branch -D stage
git branch -m stage
git push -f origin stage

echo "Commit histories for main and stage have been reset."
