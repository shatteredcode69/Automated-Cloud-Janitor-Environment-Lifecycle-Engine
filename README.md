# 🧹 Automated Cloud Janitor & Environment Lifecycle Engine

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DevSecOps](https://img.shields.io/badge/DevSecOps-Ready-brightgreen?style=for-the-badge)
![FinOps](https://img.shields.io/badge/FinOps-Cost_Optimized-blue?style=for-the-badge)

An event-driven automated governance system built on AWS. This project enforces tagging compliance, automatically cleans up orphaned/expired infrastructure to optimize cloud spend, and instantly remediates security misconfigurations (e.g., unauthorized open ports).

## 📖 Overview

In modern cloud environments, resources are frequently spun up and forgotten, leading to runaway costs ("cloud waste") and expanded attack surfaces. This project acts as an automated governance layer that spans three distinct disciplines:

*   **FinOps:** Automatically terminates resources that have exceeded their Time-To-Live (TTL).
*   **DevSecOps:** Detects and remediates dangerous security group drifts (like open SSH to `0.0.0.0/0`).
*   **Cloud Automation:** Enforces strictly tagged environments using event-driven architectures.

## 🏗️ Architecture 

    ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
    │ User Action     │  ──>  │ AWS CloudTrail  │  ──>  │ Amazon EventBridge│
    └─────────────────┘       └─────────────────┘       └─────────────────┘
                                         │
             ┌───────────────────────────┼───────────────────────────┐
             ▼                           ▼                           ▼
    [ Event: RunInstances ]     [ Event: Daily Cron ]       [ Config: Rule Breach ]
             │                           │                           │
    ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
    │ Compliance      │         │ FinOps Janitor  │         │ AWS Config &    │
    │ Lambda (Python) │         │ Lambda (Python) │         │ SSM Automation  │
    └─────────────────┘         └─────────────────┘         └─────────────────┘
             │                           │                           │
    Checks for Tags:            Checks 'TTL' Tag:           Auto-Remediates:
    Owner, Env, TTL             If Expired ──┐              Removes 0.0.0.0/0
             │                           │                  from Port 22
             ▼                           ▼                           │
    ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
    │ Amazon SNS      │         │ Amazon EC2      │         │ Secure State    │
    └─────────────────┘         └─────────────────┘         └─────────────────┘
             │
       Alerts Engineer

## ✨ Core Features

1. **Real-Time Compliance Enforcement:** Intercepts `RunInstances` API calls. If an instance lacks mandatory tags (`Owner`, `Environment`, `TTL`), it alerts the responsible team via SNS.
2. **Automated Cost Optimization:** A scheduled EventBridge cron job triggers a Lambda function daily to assess the `TTL` tag on all instances. Expired instances are automatically terminated.
3. **Security Drift Remediation:** AWS Config continuously monitors Security Groups. If an engineer accidentally opens port 22 or 3306 to the public, an SSM Automation document instantly reverts the rule to a secure state.

## 🛠️ Technologies Used
*   **Compute & Automation:** AWS Lambda (Python/Boto3), AWS Systems Manager (SSM)
*   **Event Routing:** Amazon EventBridge, AWS CloudTrail
*   **Governance & Security:** AWS Config, IAM
*   **Notifications:** Amazon SNS

## 🚀 How to Deploy

1. Enable **AWS CloudTrail** to log Management Events.
2. Create an **SNS Topic** for compliance alerts and subscribe your email.
3. Deploy the `compliance_checker.py` and `janitor.py` scripts to **AWS Lambda** with an IAM execution role granting EC2 and SNS permissions.
4. Configure **EventBridge** rules:
   * Rule 1 (Event Pattern): Triggers the Compliance Lambda on EC2 `RunInstances`.
   * Rule 2 (Schedule): Triggers the Janitor Lambda on a daily `cron()` schedule.
5. Enable **AWS Config** and deploy the `restricted-ssh` managed rule, attaching the `AWS-DisablePublicAccessForSecurityGroup` SSM remediation document.