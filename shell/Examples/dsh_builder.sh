#! /bin/bash

for i in {2004..2019}; do echo docker run -i tbutzer/etm_docker_image python3 api_etm.py -i out/DelawareRiverBasin/Run09_13_2020/ -o enduser/DelawareRiverBasin/Run09_13_2020/ward_sandford_customer/ -y $i dd netet \&; done
