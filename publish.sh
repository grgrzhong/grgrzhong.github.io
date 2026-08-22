#!/bin/bash


# rm -rf .git
# git init
# git remote remove origin
# git checkout -b main
# git branch -M main
# git remote add origin https://github.com/grgrzhong/grgrzhong.github.io.git

# Create the envrionment
# conda create -n renv \
#     r=4.5 \
#     python \
#     jupyter \
#     r-languageserver \
#     r-tidyverse \
#     r-irkernel \
#     r-httpgd \
#     r-downlit \
#     r-xml2

source $(conda info --base)/etc/profile.d/conda.sh

conda activate renv

quarto render

git add .
git commit -m "Update notes"
git push -u origin main --force
