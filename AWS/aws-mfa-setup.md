# AWS MFA Authentication Setup and Usage Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Script Installation](#script-installation)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [Security Considerations](#security-considerations)

---

## Overview

### What is AWS MFA?
Multi-Factor Authentication (MFA) adds an extra layer of security to your AWS account by requiring two forms of identification:
1. Something you know (your password/credentials)
2. Something you have (a time-based token from your MFA device)

### Why Use Temporary Credentials?
- **Enhanced Security**: Temporary credentials automatically expire, reducing the risk if they're compromised
- **Compliance**: Many organizations require MFA for production AWS access
- **Best Practice**: AWS recommends using temporary credentials instead of long-lived access keys
- **Session Management**: Temporary credentials can be scoped with specific permissions

### The ~/aws_mfa.sh Script
The `~/aws_mfa.sh` script is a lightweight utility that you call with `aws_env` to:
- Automatically detect your current AWS user
- Find your configured MFA device
- Generate temporary 12-hour session credentials
- Export them to your current shell environment
- Optionally save them for use in Jupyter notebooks

---

## Prerequisites

### Required Software
1. **AWS CLI** (version 2.x recommended)
   ```bash
   # Check if AWS CLI is installed
   aws --version
   
   # Install AWS CLI on macOS
   brew install awscli
   
   # Install AWS CLI on Linux
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

2. **Bash Shell** (standard on macOS and Linux)
   ```bash
   # Check bash version
   bash --version
   ```

3. **Python** (optional, for Jupyter notebook integration)
   ```bash
   # Check Python installation
   python --version
   ```

### AWS Account Requirements
1. **IAM User Account** with:
   - Programmatic access enabled
   - MFA device configured
   - Appropriate permissions for your tasks

2. **MFA Device Setup**
   - Virtual MFA device (Google Authenticator, Authy, etc.)
   - Hardware MFA token (YubiKey, RSA SecurID, etc.)

---

## Initial Setup

### Step 1: Configure AWS Credentials
Create or edit `~/.aws/credentials`:
```ini
[smce-veda]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

<span style="color:red">**NOTE**: These credentials are obtained within the AWS console when you register for an AWS account. You must get approval for this account.</span>

### Step 2: Configure AWS Config
Create or edit `~/.aws/config`:
```ini
[smce-veda]
region = us-west-2
```

### Step 3: Enable MFA on Your IAM User
1. Log into [AWS Console](https://us-east-2.signin.aws.amazon.com/oauth?client_id=arn%3Aaws%3Asignin%3A%3A%3Aconsole%2Fcanvas&code_challenge=Axq26WoEX-egEAkfRiiIkSADTOvL2f4bjOgBHoLBCMU&code_challenge_method=SHA-256&response_type=code&redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3FhashArgs%3D%2523%26isauthcode%3Dtrue%26state%3DhashArgsFromTB_us-east-2_74b458e675f827d8)
2. Navigate to IAM → Users → Your Username
3. Select "Security credentials" tab
4. Click "Manage" next to MFA devices
5. Follow the setup wizard for your MFA device type

<span style="color:red">**NOTE**: I've found that having ONLY the MFA through phone app (e.g., Google Authenticator) is the only way to make this work. If you select Passkey and have an MFA through phone, they seem to conflict and the steps outlined will not work.</span>

### Step 4: Verify MFA Setup
```bash
# Replace YOUR_USERNAME with your actual IAM username
aws iam list-mfa-devices --user-name YOUR_USERNAME

# Output should show:
# "SerialNumber": "arn:aws:iam::123456789012:mfa/YOUR_USERNAME"
```

---

## Script Installation

### Step 1: Create the MFA Script
Create the file `~/aws_mfa.sh`:

```bash
#!/bin/bash

# 🔒 AWS MFA Credential Generator
# This script creates temporary (12-hour) credentials using your MFA device
# Requires terminal access for secure input
# License: GPL 2 or higher

# Check for terminal access
if [ ! -t 0 ]; then
  echo "❌ Error: This script requires terminal access for secure input" >&2
  return
fi

# Prevent token conflicts
if [ -n "$AWS_SESSION_TOKEN" ]; then
  echo "⚠️  Active session detected! 
   To generate new credentials, clear your current session:
   unset AWS_SESSION_TOKEN AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID
   Then ensure you have valid profile credentials configured." >&2
  return
fi

# Identify current user
identity=$(aws sts get-caller-identity --output json)
username=$(echo -- "$identity" | sed -n 's!.*"arn:aws:iam::.*:user/\(.*\)".*!\1!p')

if [ -z "$username" ]; then
  echo "❌ Unable to identify user. Expected format:
    arn:aws:iam::.....:user/YOUR_USERNAME
  
Current identity output:
$identity" >&2
  return
fi

echo "👤 Authenticated as: $username" >&2

# Find MFA device
mfa=$(aws iam list-mfa-devices --user-name "$username" --output json)
device=$(echo -- "$mfa" | sed -n 's!.*"SerialNumber": "\(.*\)".*!\1!p')

if [ -z "$device" ]; then
  echo "❌ No MFA device found for user: $username
  
MFA device output:
$mfa" >&2
  return
fi

echo "📱 MFA device found: $device" >&2

# Request MFA code
echo -n "🔢 Enter your MFA code: " >&2
read code

# Generate temporary credentials
tokens=$(aws sts get-session-token --serial-number "$device" --token-code $code --output json)

echo $tokens

# Extract credentials
secret=$(echo -- "$tokens" | sed -n 's!.*"SecretAccessKey": "\(.*\)".*!\1!p')
session=$(echo -- "$tokens" | sed -n 's!.*"SessionToken": "\(.*\)".*!\1!p')
access=$(echo -- "$tokens" | sed -n 's!.*"AccessKeyId": "\(.*\)".*!\1!p')
expire=$(echo -- "$tokens" | sed -n 's!.*"Expiration": "\(.*\)".*!\1!p')

if [ -z "$secret" -o -z "$session" -o -z "$access" ]; then
  echo "❌ Failed to generate temporary credentials
  
Token response:
$tokens" >&2
  return
fi

# Export credentials to environment
export AWS_SESSION_TOKEN=$session
export AWS_SECRET_ACCESS_KEY=$secret
export AWS_ACCESS_KEY_ID=$access

echo "✅ Temporary credentials activated! Expires: $expire" >&2

# Save credentials to .env file for Jupyter notebooks (optional)
# This will save the new credentials to a .env file in the current directory where you called "aws_env"
python ~/set_aws_creds.py
```

### Step 2: Make the Script Executable
```bash
chmod +x ~/aws_mfa.sh
```

### Step 3: Create AWS Environment Switcher Function (Recommended)
Add to your `~/.zshrc` (or `~/.bashrc`):

```bash
##################### CREATE AWS temporary credentials

# 🎯 AWS Environment Switcher
# Seamlessly switch between AWS accounts with MFA support
aws_env() {
  # Clear any existing session
  unset AWS_SESSION_TOKEN

  # Load credentials for the specified profile
  export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile $1)
  export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key --profile $1)
  export AWS_DEFAULT_REGION=$(aws configure get region --profile $1)

  # Profiles requiring MFA authentication
  MFA_PROFILES=("veda-smce" "smce-veda" "aq" "uah-veda")

  # Check if MFA is required for this profile
  if [[ " ${MFA_PROFILES[@]} " =~ " ${1} " ]]; then
    echo "🔐 MFA required for profile: $1"
    source ~/aws_mfa.sh
  fi

  echo "✅ Successfully switched to $1 environment!"
}
```

Alternatively, if you organize your shell configuration, you can add this to `~/.zshrc.d/functions` or similar.

Reload your shell configuration:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Step 4: Optional - Python Script for Jupyter Integration
If you use Jupyter notebooks, create `~/set_aws_creds.py`:

```python
#!/usr/bin/env python
import os

# Get credentials from environment
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
session_token = os.environ.get('AWS_SESSION_TOKEN')

if access_key and secret_key and session_token:
    # Save to .env file for Jupyter notebooks
    with open(os.path.expanduser('~/.env'), 'w') as f:
        f.write(f'AWS_ACCESS_KEY_ID={access_key}\n')
        f.write(f'AWS_SECRET_ACCESS_KEY={secret_key}\n')
        f.write(f'AWS_SESSION_TOKEN={session_token}\n')
    print("✅ Credentials saved to ~/.env for Jupyter notebooks")
else:
    print("❌ No credentials found in environment")
```

---

## Usage

### Basic Usage

#### Authenticate with MFA
```bash
# Switch to a profile with MFA support
aws_env smce-veda

# For profiles without MFA requirement
aws_env other-profile

# Or source the MFA script directly
source ~/aws_mfa.sh
```

The `aws_env` function will:
1. Load credentials for the specified profile
2. Check if MFA is required for that profile
3. If MFA is needed, automatically call the MFA script
4. The MFA script will detect your user and prompt for MFA code
5. Generate and export temporary credentials

#### Example Session
```bash
$ aws_env smce-veda
🔐 MFA required for profile: smce-veda
👤 Authenticated as: john.doe
📱 MFA device found: arn:aws:iam::123456789012:mfa/john.doe
🔢 Enter your MFA code: 123456
✅ Temporary credentials activated! Expires: 2024-01-01T12:00:00Z
✅ Successfully switched to smce-veda environment!
```

### Using the Temporary Credentials

Once authenticated, you can use AWS CLI commands normally:
```bash
# List S3 buckets
aws s3 ls s3://nasa-disasters/

# Get current identity
aws sts get-caller-identity
```

### Clearing Session
To clear your current MFA session:
```bash
unset AWS_SESSION_TOKEN AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Active session detected"
**Solution:** Clear your current session:
```bash
unset AWS_SESSION_TOKEN AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID
```

#### Issue 2: "Unable to identify user"
**Solutions:**
- Verify your AWS credentials are configured correctly
- Check that your credentials have permission to call `sts:GetCallerIdentity`
- Ensure you're using the correct AWS profile (if using multiple profiles)

#### Issue 3: "No MFA device found"
**Solutions:**
- Verify MFA is enabled on your IAM user
- Check that your user has permission to call `iam:ListMFADevices`
- Ensure the MFA device is properly attached to your user

#### Issue 4: "Failed to generate temporary credentials"
**Solutions:**
- Verify the MFA code is correct and hasn't expired
- Check that your user has permission to call `sts:GetSessionToken`
- Ensure your system clock is synchronized (MFA codes are time-based)

#### Issue 5: Script returns without setting credentials
**Solution:** Make sure to use `source` or the function:
```bash
# Correct - runs in current shell
source ~/aws_mfa.sh

# Wrong - runs in subshell
~/aws_mfa.sh
```

### Debugging Tips

#### Check Current Credentials
```bash
# View current identity
aws sts get-caller-identity

# Check environment variables
env | grep AWS
```

#### Verify MFA Device
```bash
# Replace USERNAME with your IAM username
aws iam list-mfa-devices --user-name USERNAME
```

#### Test Permissions
```bash
# Test basic permissions
aws iam get-user
aws sts get-session-token --serial-number YOUR_MFA_ARN --token-code 123456
```

---

## Best Practices

### Security Best Practices

1. **Never Share MFA Tokens**
   - MFA tokens are time-sensitive but should still be kept private
   - Don't log or store MFA tokens in scripts

2. **Regular Credential Rotation**
   ```bash
   # Create new access key
   aws iam create-access-key --user-name YOUR_USERNAME
   
   # Delete old access key
   aws iam delete-access-key --access-key-id OLD_ACCESS_KEY_ID --user-name YOUR_USERNAME
   ```

3. **Secure Credential Storage**
   ```bash
   # Set restrictive permissions on AWS files
   chmod 600 ~/.aws/credentials
   chmod 600 ~/.aws/config
   chmod 700 ~/.aws
   ```

4. **Use Least Privilege**
   - Only grant permissions necessary for your tasks
   - Consider using AWS IAM roles when possible

### Operational Best Practices

1. **Multiple AWS Profiles**
   If you use multiple AWS accounts, configure profiles in `~/.aws/credentials`:
   ```ini
   [smce-veda]
   aws_access_key_id = KEY1
   aws_secret_access_key = SECRET1
   
   [veda-smce]
   aws_access_key_id = KEY2
   aws_secret_access_key = SECRET2
   
   [aq]
   aws_access_key_id = KEY3
   aws_secret_access_key = SECRET3
   ```
   
   <span style="color:red">FUN FACT: You can have different credentials opened within each terminal. This can alleviate having to re-authenticate for different accounts.
   
   Switch profiles using the aws_env function:
   ```bash
   # Switch to a profile with automatic MFA handling
   aws_env smce-veda
   
   # Switch to another profile
   aws_env aq
   ```

2. **Automate Common Tasks**
   Create helper functions in your shell configuration:
   ```bash
   # Quick S3 listing
   s3ls() {
       aws s3 ls "s3://$1"
   }
   ```

3. **Session Management**
   Check if your session is still valid:
   ```bash
   aws sts get-caller-identity &>/dev/null && echo "✅ Session valid" || echo "❌ Session expired"
   ```

---

## Security Considerations

### Credential Security

1. **Never Commit Credentials**
   Add to `.gitignore`:
   ```gitignore
   # AWS credentials
   .aws/credentials
   .aws/config
   .env
   *.pem
   ```

2. **Environment Variables**
   - Temporary credentials are stored in environment variables
   - They're only available in the current shell session
   - Closing the terminal clears the credentials

3. **Session Duration**
   - Default session duration is 12 hours (43200 seconds)
   - Sessions automatically expire and cannot be renewed
   - Must generate new credentials after expiration

### MFA Device Security

1. **Virtual MFA Best Practices**
   - Use reputable authenticator apps
   - Enable cloud backup for MFA seeds
   - Keep backup codes in secure location

2. **Hardware MFA Best Practices**
   - Store device in secure location
   - Consider having a backup MFA device
   - Test device regularly

### Network Security

1. **Use VPN for Sensitive Operations**
   - Consider using VPN when accessing AWS from public networks
   - Be aware of IP-based IAM policies

2. **Audit Trail**
   - Enable CloudTrail for API call logging
   - Regularly review access patterns
   - Monitor for unusual activity

---

## Additional Resources

- [AWS MFA Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [STS GetSessionToken API](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)

---

*Last Updated: 2024*
*Version: 2.0*