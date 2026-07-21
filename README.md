# 🧹 Automated Cloud Janitor & Environment Lifecycle Engine

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DevSecOps](https://img.shields.io/badge/DevSecOps-Ready-brightgreen?style=for-the-badge)
![FinOps](https://img.shields.io/badge/FinOps-Cost_Optimized-blue?style=for-the-badge)

An event-driven AWS governance project that combines FinOps, DevSecOps, and cloud automation into a practical, testable solution. It helps teams enforce tagging rules, identify expired resources by TTL, and notify stakeholders when non-compliant infrastructure is detected.

## 📖 Overview

Cloud environments often accumulate forgotten or over-provisioned resources, causing unnecessary spend and security drift. This project provides a lightweight governance layer that can:

- enforce required tags for EC2 resources
- identify instances that have exceeded their TTL
- publish compliance alerts through SNS
- support deployment through AWS Lambda, CloudFormation, and GitHub Actions

## ✨ Core Features

1. Real-Time Compliance Checks
   - Evaluates EC2 launch events and flags instances missing required tags such as Owner, Environment, and TTL.
2. TTL-Based Janitor Logic
   - Detects expired instances based on the TTL tag and launch time.
3. AWS-Friendly Automation
   - Includes Lambda handlers, CloudFormation resources, and CI/CD deployment workflow.
4. Test Coverage
   - Includes automated pytest tests for the core compliance and janitor behaviors.

## 🛠️ Tech Stack

- Python 3.13
- boto3 for AWS SDK integration
- pytest for automated validation
- GitHub Actions for CI/CD
- AWS Lambda and CloudFormation for deployment

## 🚀 Local Setup

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## ☁️ Deployment

1. Create the AWS resources with CloudFormation:

```bash
aws cloudformation deploy \
  --template-file deploy/aws-resources.yaml \
  --stack-name cloud-janitor-stack \
  --capabilities CAPABILITY_IAM
```

2. Add the following GitHub repository secrets:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY

3. Push to the main branch to trigger the deployment workflow.

## 📁 Project Structure

- compliance_checker.py — Lambda handler for compliance enforcement
- janitor.py — TTL-based cleanup logic
- tests/test_lambda_handlers.py — automated tests
- deploy/aws-resources.yaml — AWS infrastructure template
- .github/workflows/deploy.yml — GitHub Actions deployment pipeline

## 🔗 Repository

https://github.com/shatteredcode69/Automated-Cloud-Janitor-Environment-Lifecycle-Engine