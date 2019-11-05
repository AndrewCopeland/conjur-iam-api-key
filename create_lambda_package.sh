CWD=$(pwd)
cd $HOME/venv/getConjurSecret
source bin/activate

cd lib/python3.7/site-packages

rm -rf conjur-iam-api-key
git clone https://github.com/AndrewCopeland/conjur-iam-api-key.git
cd conjur-iam-api-key
pip3 install .

cd ..
zip -r function.zip ./

mv function.zip $CWD/lambda_function_package.zip

