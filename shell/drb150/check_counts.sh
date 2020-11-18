#! /bin/bash

product=dd


#for i in {1950..1980} ; do echo $i; aws s3 ls dev-et-data/enduser/DelawareRiverBasin/drb150/$i/ | grep $product | wc ; done
#for i in `seq 1950 10 2100`; do echo $i; done
#for i in  `seq 1950 10 2100`; do echo $i; aws s3 ls dev-et-data/enduser/DelawareRiverBasin/drb150/$i/ | grep $product | wc ; done
for i in {1950..2099} ; do echo $i; aws s3 ls dev-et-data/enduser/DelawareRiverBasin/drb150_nofunswitch/$i/ | grep $product | wc ; done
#dev-et-data/enduser/DelawareRiverBasin/drb150_nofunswitch/
