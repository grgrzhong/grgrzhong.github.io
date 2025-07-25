#!/bin/bash

### completely remove git
# rm -rf .git
# git init

# git remote remove origin
# git checkout -b main 
# git branch -M main

# git remote add origin https://github.com/grgrzhong/grgrzhong.github.io.git

conda activate quarto

### render site files to docs
quarto render

### add to the local git repository
git add .
# git add docs

git commit -m "update blogs"

### push to the remote repository
git push -u origin main --force
