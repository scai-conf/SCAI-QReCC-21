#!/bin/bash

# KPQA
git clone git@github.com:hwanheelee1993/KPQA.git
pushd KPQA
git checkout bb4b0a5
git apply ../KPQA.diff
echo "Download the cpt.zip from https://drive.google.com/file/d/1pHQuPhf-LBFTBRabjIeTpKy3KGlMtyzT/view?usp=sharing and extract it here"
popd

