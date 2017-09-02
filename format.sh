#----------------------------#
# A script for formatting csv#
#----------------------------#

#!/bin/bash

data_dir="~/projects/SodaFountain/data/rnb-blues-jazz/"
csv_dir="~/projects/SodaFountain/data/rnb-blues-jazz/csv/" 

cd ~/projects/SodaFountain/data/rnb-blues-jazz/ 


for filename in ./*.mid; do 
    midicsv $filename ${filename%.*} #converts to csv
    midicsv $filename | perl exchannel.pl
    
done 

