#! /bin/bash

 aws s3 ls dev-et-data/enduser/DelawareRiverBasin/Run09_13_2020/ward_sandford_customer/2000/ | grep dd | wc

 for i in {2000..2019} ; do echo $i; aws s3 ls dev-et-data/enduser/DelawareRiverBasin/Run09_13_2020/ward_sandford_customer/$i/ | grep dd | wc ; done
