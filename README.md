# AWS Lambda Leaked Credential Global Revocation Engine

[![Runtime](https://img.shields.io/badge/Runtime-Python%203.11-blue.svg)](https://www.python.org/)
[![Service](https://img.shields.io/badge/Identity-AWS%20IAM-red.svg)](https://aws.amazon.com/iam/)
[![Automation](https://img.shields.io/badge/Automation-Instant%20Containment-orange.svg)](https://aws.amazon.com/lambda/)

## 📋 Operational Overview

This repository contains an enterprise-level identity incident response script designed to mitigate leaked credential risks within seconds.

If an engineer accidentally pushes an AWS Access Key pair to a public Git repository, automated scraping bots will weaponize those keys within minutes to spin up crypto-miners or steal data. This Lambda function is built to accept real-time leak alerts from scanning sources (like GitHub Secret Scanning or AWS Secrets Manager). It instantly disables the compromised access key path globally and injects an inline explicit Deny policy onto the IAM user, completely neutralizing the attacker's access path immediately.

---

### 🛡️ Core Identity Containment Controls

* **Instant Key Invalidation:** Switches the status of the leaked programmatic access key from `Active` to `Inactive` immediately.
* **Nuclear Option Inline Deny Policy:** Attaches an absolute `*` Deny policy statement to the compromised user profile to override any existing administrative privileges.
* **Session Invalidation:** Disrupts any temporary credential sessions currently active under that identity banner.

---

## 📂 Repository Structural Mapping

```text
aws-lambda-leaked-credential-global-revocation-engine/
├── README.md                      # Incident containment overview
├── lambda_function.py             # Active identity revocation script
└── policy_kill_switch.json        # Dynamic inline deny policy payload****
