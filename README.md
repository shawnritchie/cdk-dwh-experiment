###Depolyment instructions
- Setup you `aws configure` to your account
- Bootstrap environment using `cdk bootstrap`
- Deploy the stacks
`cdk deploy vpc-stack bastion-stack redshift-stack kinesis-stream-stack kinesis-firehose-stack compute-stack flink-stack --require-approval never`
- Firehouse logging need to be turned on manually
- Redshift needs to be enabled publicly manually
- Redshift Schema needs to be created Manually 
```
create table payments (
  event_created timestamp not null,
  event_dw_regdate timestamp default GETDATE(),
  event_type varchar(200) not null,
  event_json_data varchar(65535) not null
);
```
- Turn on the Kinesis Data Analytics App
- Once everything in place deploy the lambda `cdk deploy payment-simulation-lambda-stack --require-approval never`

# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


## Deployment

###Bastion Connection
- Add cloud_user to the HostAdmins group
- Generate a new ssh key
```
ssh-keygen -t rsa -f mynew_key
```
- Propogate the ssh key to the new bastion host
```
aws ec2-instance-connect send-ssh-public-key --region ${REGION} --instance-id ${INSTANCE_ID} --availability-zone ${INSTANCE_AZ} --instance-os-user ec2-user --ssh-public-key file://mynew_key.pub
```
- Connect to the bastion host
```
ssh -i mynew_key ec2-user@ec${IP}.compute-1.amazonaws.com
```

