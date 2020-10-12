#! /bin/bash

product=etasw


for i in {1960..1970} ; do echo $i; aws s3 ls dev-et-data/enduser/DelawareRiverBasin/drb150/$i/ | grep $product | wc ; done
