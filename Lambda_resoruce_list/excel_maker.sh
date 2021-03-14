#!/bin/bash


echo Hotel shilla auto Asset management Start
sleep 3;

echo Start t-project

python ./main.py ap-northeast-2 AKIAW5AWKLRSKCYKOLGX iRkrTVWVzfFaTeeuR1kRgx6oPw5XNo3W4CsIwTtJ

sleep 5;
echo Done t-project

sed 's/t-project/shilla-cicd/' main.py > main.temp
mv main.temp main.py

sleep 2;
echo Start shilla-cicd
python ./main.py ap-northeast-2 AKIAYCFSYGR6UOPBFDHO Wj45h0PHbTG5JE0wJpLN7w+3aXQuVXstDE46HcPV

sleep 5;
echo Done shilla-cicd

sed 's/shilla-cicd/shilla-poc/' main.py > main.temp
mv main.temp main.py

sleep 2;
echo Start shilla-poc

python ./main.py ap-northeast-2 AKIA5RGSB2EBU7JL23MX tE8cyF4z2xydQiFseSiBHOmbHDUlF/HYQceEEYat

sleep 5;
echo Done shilla-poc

sed 's/shilla-poc/shilla-translate/' main.py > main.temp
mv main.temp main.py

sleep 2;
echo Start shilla-translate

python ./main.py ap-northeast-2  AKIAYIP5QHOYEPVVVKER bq+p+2/BFlloX/ia2GX6iGBqaqJChfdCsPNdFni/

sleep 5;
echo Done shilla-translate

sed 's/shilla-translate/cms-project/' main.py > main.temp
mv main.temp main.py

sleep 2;
echo Start cms-project

python ./main.py ap-northeast-2 AKIAYWVSS4LN3DQPJKYD PbfGR5R6Z2rZSL6qgFJ8lQwx2YfxX553iU3cP9I5

sleep 5;
echo Done cms-project

sed 's/cms-project/t-project-prd/' main.py > main.temp
mv main.temp main.py

sleep 2;
echo Start t-project-prd

python ./main.py ap-northeast-2 AKIATQXXR5YUNVGKTYQ4 97+XIjHiqJMV5mmToxNFPpDIAxGXqzzjoPAo12ce

sleep 5;
echo Done t-project-prd

sed 's/t-project-prd/t-project/' main.py > main.temp
mv main.temp main.py

aws s3 mv ./t-project.xlsx s3://private.source/xlsx/
aws s3 mv ./shilla-cicd.xlsx s3://private.source/xlsx/
aws s3 mv ./shilla-poc.xlsx s3://private.source/xlsx/
aws s3 mv ./shilla-translate.xlsx s3://private.source/xlsx/
aws s3 mv ./cms-project.xlsx s3://private.source/xlsx/
aws s3 mv ./t-project-prd.xlsx s3://private.source/xlsx/
