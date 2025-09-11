# 🚀 AWS SSO Configuration Guide

## 🔐 Secure Your AWS Credentials with AWS Identity Center (SSO)

This guide walks you through setting up AWS Single Sign-On (SSO) to securely manage your AWS credentials without storing them in plain text.

---

## 📋 Prerequisites

- ✅ AWS CLI v2 installed (version 2.x or higher)
- ✅ Access to AWS Identity Center (formerly AWS SSO)
- ✅ Your organization's SSO portal URL

---

## 🛠️ Step-by-Step Setup Instructions

### Step 1: Initialize SSO Configuration
```bash
aws configure sso
```

### Step 2: Choose a Profile Name
When prompted for `SSO session name`, enter a descriptive name for your profile:
```
SSO session name (Recommended): disasters
```
💡 **Tip**: Use meaningful names like `prod-admin`, `dev-poweruser`, etc.

### Step 3: Enter Your SSO Start URL
Find your SSO URL in the AWS Identity Center portal and enter it:
```
SSO start URL [None]: https://d-9067c5bbc5.awsapps.com/start/#
```
📍 **Where to find**: Navigate to your AWS SSO portal → Look for the URL in your browser

### Step 4: Specify SSO Region
Enter the region where your Identity Center is configured:
```
SSO region [None]: us-east-1
```

### Step 5: SSO Registration Scopes
Press Enter to accept the default:
```
SSO registration scopes [sso:account:access]: 
```
✨ The default scope is sufficient for most use cases

### Step 6: Browser Authentication
🌐 A browser window will open automatically:
1. Log in with your corporate credentials
2. Click "Allow" to grant access to `AWS CLI (botocore)`
3. Return to your terminal

### Step 7: Select AWS Account
Enter your AWS account ID (12 digits):
```
AWS account ID: 867530900000
```
📝 Find this in your AWS SSO portal under the accounts tab

### Step 8: Choose IAM Role
Select from available roles:
```
There are 2 roles available to you.
> Project-Power-User
  ReadOnlyAccess
```
Use arrow keys to select, then press Enter

### Step 9: Set Default Region
Confirm or change the AWS region:
```
CLI default region [us-east-1]: us-east-1
```

### Step 10: Set Output Format
Choose your preferred output format:
```
CLI default output format [None]: json
```
Options: `json`, `yaml`, `text`, `table`

---

## ✅ Verification

Test your configuration:
```bash
aws s3 ls --profile disasters-sso
```

Expected output:
```
                           PRE browseui/
                           PRE california_wildfires_202501/
                           PRE disasters/
                           ...
```

---

## 🔄 Daily Usage

### Login to SSO Session
```bash
aws sso login --profile disasters-sso
```

### Use AWS Commands
```bash
# List S3 buckets
aws s3 ls --profile disasters-sso

# Get caller identity
aws sts get-caller-identity --profile disasters-sso
```

### Alternative: Set AWS_PROFILE Environment Variable
To avoid passing `--profile disasters-sso` with every command, you can set the `AWS_PROFILE` environment variable:

```bash
# Set the environment variable
export AWS_PROFILE=disasters-sso

# Now you can run commands without --profile
aws s3 ls
aws sts get-caller-identity
```

This is especially helpful when running many AWS commands in a session.

### Logout When Done
```bash
aws sso logout
```

---

## 📂 Configuration Files

Your SSO configuration is stored in `~/.aws/config`:

```ini
[profile disasters-sso]
sso_session = disasters
sso_account_id = 867530900000
sso_role_name = Project-Power-User
region = us-east-1
output = json

[sso-session disasters]
sso_start_url = https://d-9067c5bbc5.awsapps.com/start/#
sso_region = us-east-1
sso_registration_scopes = sso:account:access
```

---

## ⚠️ Important Notes

### 🕐 About Temporary Credentials
- AWS SSO provides **temporary credentials** that expire after 1-12 hours
- Credentials are automatically refreshed when you run commands
- No permanent credentials are stored on your machine

### 🔒 Why AWS-Vault Didn't Work
AWS-Vault expects permanent credentials to generate temporary ones. Since AWS SSO already provides temporary credentials:
- Adding SSO temporary credentials to aws-vault causes authentication errors
- SSO handles credential refresh automatically, making aws-vault redundant
- Use AWS SSO for temporary credential profiles, aws-vault for permanent ones

---

## 🚨 Troubleshooting

### "The security token included in the request is invalid"
**Cause**: Trying to use expired temporary credentials
**Solution**: Run `aws sso login --profile your-profile` to refresh

### Browser doesn't open automatically
**Solution**: Add `--use-device-code` flag:
```bash
aws sso login --profile disasters-sso --use-device-code
```

### Multiple AWS accounts/roles
Create separate profiles for each account/role combination:
```ini
[profile prod-admin]
sso_session = mycompany
sso_account_id = 111111111111
sso_role_name = Administrator

[profile dev-readonly]
sso_session = mycompany
sso_account_id = 222222222222
sso_role_name = ReadOnlyAccess
```

---

## 🎯 Best Practices

1. **Never store credentials in plain text** ❌
2. **Use SSO for all AWS access** ✅
3. **Logout when finished working** 🔒
4. **Use descriptive profile names** 📝
5. **Set up MFA on your SSO account** 🔐

---

## 🚀 Next Steps

1. Remove plain text credentials from `~/.aws/credentials`
2. Update scripts to use `--profile` flag
3. Set default profile: `export AWS_PROFILE=disasters-sso`
4. Consider using [aws-sso-util](https://github.com/benkehoe/aws-sso-util) for enhanced SSO features

---

## 📚 Resources

- [AWS CLI SSO Documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html)
- [IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)

---

*🔐 Remember: Security is everyone's responsibility. Keep your credentials safe!*