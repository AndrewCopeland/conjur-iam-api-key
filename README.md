# conjur-iam-api-key
Get an iam api key used by conjur, get a sdk client using iam authentication.


## Installing the code

### From source
```bash
$ git clone https://github.com/AndrewCopeland/conjur-iam-api-key.git
$ cd conjur-iam-api-key; pip3 install .
```

## Usage

#### Setting environment variables
```bash
$ export CONJUR_APPLIANCE_URL=https://conjur.yourorg.com
$ export AUTHN_IAM_SERVICE_ID=dev
$ export CONJUR_AUTHN_LOGIN=host/cust-portal/<aws-account-id>/<iam-role-name>
$ export CONJUR_CERT_FILE=./conjur-dev.pem
$ export CONJUR_ACCOUNT=dev
```

#### create_conjur_iam_api_key

This function will return a json formatted header used as an api key to authenticate to conjur when using authn-iam.

```python
>>> from conjur_iam_client import *
>>> conjur_api_key = create_conjur_iam_api_key()
```

#### get_conjur_iam_session_token

This function will retrieve the api key from the method above and then will authenticate to the conjur API and obtain a session token which can be used in subsquent calls to interact with the conjur api.

```python
>>> from conjur_iam_client import *
>>> appliance_url = 'https://conjur.yourorg.com'
>>> service_id = 'dev'
>>> username = 'host/cust-portal/<aws-account-id>/<iam-role-name>'
>>> cert_file = 'conjur-cert.pem'
>>> conjur_account = 'dev'
>>> conjur_session_token = get_conjur_iam_session_token(appliance_url, conjur_account, service_id, username, cert_file)
```

#### create_conjur_iam_client

This function will retrieve the session token from the method above and will initiate a conjur client for you. The conjur client returned can be found https://github.com/cyberark/conjur-api-python3. The token will not be refreshed within the client so the client can only be used for 5-8 min. After this time another client must be initiliazed with this method

```python
>>> from conjur_iam_client import *
>>> appliance_url = 'https://conjur.yourorg.com'
>>> service_id = 'dev'
>>> username = 'host/cust-portal/<aws-account-id>/<iam-role-name>'
>>> cert_file = 'conjur-cert.pem'
>>> conjur_account = 'dev'
>>> conjur_client = create_conjur_iam_client(appliance_url, conjur_account, service_id, username, cert_file)
>>> conjur_client.list() # This will return a list of all the resource you have access to. See https://github.com/cyberark/conjur-api-python3 for all of the methods this client supports.
```

#### create_conjur_iam_client_from_env

This function returns a client exactly like the function above. However instead of providing all of the parameters within the function it will read the parameters from the environment variables mentioned in the 'Setting environment variables' section.

```python
>>> from conjur_iam_client import *
>>> conjur_client = create_conjur_iam_client_from_env()
>>> conjur_client.list() # This will return a list of all the resource you have access to. See https://github.com/cyberark/conjur-api-python3 for all of the methods this client supports.
```

## EC2 Usage
In this example we will be using the `create_conjur_iam_client_from_env()` function. It is assumed an IAM role is already associated with the ec2 instance.

#### Setting the environment variables
```bash
$ export CONJUR_APPLIANCE_URL=https://conjur.yourorg.com
$ export AUTHN_IAM_SERVICE_ID=dev
$ export CONJUR_AUTHN_LOGIN=host/cust-portal/<aws-account-id>/<iam-role-name>
$ export CONJUR_CERT_FILE=./conjur-dev.pem
$ export CONJUR_ACCOUNT=dev
```

#### Executing python script from the ec2 instance
```python3
from conjur import Client
from conjur_iam_client import create_conjur_iam_client_from_env

conjur_client = create_conjur_iam_client_from_env()
conjur_list = conjur_client.list()
```

## Lambda Usage
Since lambda cannot reach out to the AWS metadata url we have to slightly modify how we execute `create_conjur_iam_client_from_env()`. It is assumed an IAM role is already associated with the lambda function.

#### Lambda environment variables
```
CONJUR_APPLIANCE_URL=https://conjur.yourorg.com
AUTHN_IAM_SERVICE_ID=dev
CONJUR_AUTHN_LOGIN=host/cust-portal/<aws-account-id>/<iam-role-name>
CONJUR_CERT_FILE=./conjur-dev.pem
CONJUR_ACCOUNT=dev
IAM_ROLE_NAME=<iam-role-name>
```

#### Executing python script
The difference here is instead of having the client reach out to the metadata url and automatically obtain the keys and tokens required to authenticate. We are fetching these and pushing them into the `create_conjur_iam_client_from_env()` function.
```python3
from conjur import Client
from conjur_iam_client import create_conjur_iam_client_from_env
import os

def lambda_handler(event, context):
    iam_role_name=os.environ['IAM_ROLE_NAME']
    access_key=os.environ['AWS_ACCESS_KEY_ID']
    secret_key=os.environ['AWS_SECRET_ACCESS_KEY']
    token=os.environ['AWS_SESSION_TOKEN']
    conjur_client = create_conjur_iam_client_from_env(iam_role_name, access_key, secret_key, token)
    conjur_list = conjur_client.list()
    return {
        "list": conjur_list
    }
```
