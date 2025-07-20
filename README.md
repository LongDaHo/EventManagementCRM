# Project Name

A FastAPI-based backend service integrated with DynamoDB and AWS SES. The project features modular structure, clean service separation, and support for email sending and tracking.

## Features

- FastAPI backend
- DynamoDB integration
- Email sending with AWS SES
- SNS-compatible email tracking
- Modular routers and services
- Configuration handled directly in `config.py` (no `.env` required)

## Directory Structure

```
.
├── src
│   ├── db
│   ├── models
│   ├── routers
│   ├── services
│   ├── utils
│   ├── main.py
│   └── config.py
├── test
│   ├── push_test_data copy.py
│   ├── push_test_data.py
│   ├── create_user_table.py
│   ├── create_event_table.py
│   ├── test_queries.py
│   └── test_send_emails.py
├── README.md
└── requirements.txt
```

## Installation

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## AWS CLI Setup

Before running the application or tests, configure AWS credentials:

```bash
aws configure
```

Fill in your credentials when prompted:

```
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: ap-southeast-1
Default output format [None]: json
```

## Running the App

Start the FastAPI application:

```bash
python3 src/main.py
```

## Configuration

Edit the configuration in `src/config.py`:

```python
aws_region: str = "ap-southeast-1"
aws_dynamodb_table_name_events: str = "crm-events-table"
aws_dynamodb_table_name_users: str = "crm-users-table"
aws_ses_sender_email: str = "noreply@example.com"
aws_ses_config_set: str = "crm-config-set"
```

## Running Tests

To test the application step-by-step:

### 1. Create DynamoDB Tables

Run the following scripts to create the necessary DynamoDB tables:

```bash
python3 test/create_user_table.py
python3 test/create_event_table.py
```

### 2. Insert Test Data

Push test data into the tables:

```bash
python3 test/push_test_data.py
```

### 3. Run Query Tests

This will test reading/querying data from DynamoDB:

```bash
python3 test/test_queries.py
```

### 4. Run Email Sending Test

This will trigger email sending using AWS SES:

```bash
python3 test/test_send_emails.py
```

> **Note:** Ensure that the email address defined in `aws_ses_sender_email` is verified in your SES console if you're in the SES sandbox.  
> To enable production use and avoid sandbox restrictions, you should:
> - Verify the sender domain (e.g., `example.com`) in SES.
> - Set up the required DNS records (TXT, CNAME, MX) from SES in your domain provider (e.g., Route53, GoDaddy).
> - Request to move your SES account out of the sandbox

