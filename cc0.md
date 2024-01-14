# 50.043 Cohort class 0 (e-learning)

# Learning Objectives

By this end of this cohort class you should be able to 

1. Launch an ubuntu instance on AWS educate using from the Web UI
2. Connect to the Ubuntu instance on AWS educate using SSH
3. Install and use MySQL on Ubuntu
4. Launch an ubuntu instance on AWS educate using Python and BOTO3


# Launch an ubuntu instance on AWS educate

1. You should have received an email from AWS educate
2. Register/login to your AWS educate account
3. Go to the AWS Academy Learner Lab
4. Follow the video instructions given on eDimension -> information -> AWS Educate


# SSH into the launched Ubuntu instance
In case you want to remote login to the AWS instance directly from you laptop,
run the following on your Mac / Linux / Windws( Ubuntu subsystem)

```bash
ssh -i .ssh/aws_edu.pem ubuntu@3.102.45.7 
```
You may need to change the ip address accordingly.

if an error saying the permission of the pem file is too open, run the following then re-run the previous command

```bash
chmod 400 .ssh/aws_edu.pem
```

