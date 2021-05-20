#!/bin/bash
set -ve

cd payload; zip ../payload.zip *; cd ..
inputJobId=7
inputFPGA="xc7a100tcsg324-1"
inputZipFile=$(python3 encode.py)

curl --data "inputJobId=$inputJobId&inputFPGA=$inputFPGA&inputZipFile=$inputZipFile&XdcFileName=&inputXdcFile=&SrcFileName1=&inputFile1=&SrcFileName2=&inputFile2=" http://localhost:18888/submit
