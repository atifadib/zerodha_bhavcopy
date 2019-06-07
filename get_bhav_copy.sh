#!/bin/bash -x
wget --server-response https://www.bseindia.com/download/BhavCopy/Equity/EQ$1_CSV.ZIP 2>&1 | awk '/^  HTTP/{print $2}' > bse_response.txt
unzip EQ$1_CSV.ZIP
rm EQ$1_CSV.ZIP
mv EQ$1.CSV ./BHAV_DATA/
