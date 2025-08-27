# AWS S3 Commands and Operations Guide

## Table of Contents
- [AWS CLI Installation and Configuration](#aws-cli-installation-and-configuration)
- [Basic S3 Commands](#basic-s3-commands)
- [S3 API Commands](#s3-api-commands)
- [Recursive Operations](#recursive-operations)
- [Data Upload and Sync Operations](#data-upload-and-sync-operations)
- [Bucket Management](#bucket-management)
- [Object Management](#object-management)
- [Access Control and Permissions](#access-control-and-permissions)
- [Performance Optimization](#performance-optimization)
- [Cost Management](#cost-management)
- [Troubleshooting](#troubleshooting)
- [Official AWS Resources](#official-aws-resources)

## AWS CLI Installation and Configuration

### Installation
```bash
# macOS using Homebrew
brew install awscli

# Using pip
pip install awscli --upgrade --user

# Verify installation
aws --version
```

### Configuration
```bash
# Configure AWS CLI with credentials
aws configure

# Configure specific profile
aws configure --profile myprofile

# List configuration
aws configure list

# Set region for current session
export AWS_DEFAULT_REGION=us-east-1
```

## Basic S3 Commands

### List Buckets and Objects
```bash
# List all buckets
aws s3 ls

# List objects in a bucket
aws s3 ls s3://my-bucket/

# List objects with human-readable sizes
aws s3 ls s3://my-bucket/ --human-readable

# List objects with summary
aws s3 ls s3://my-bucket/ --summarize

# List objects recursively
aws s3 ls s3://my-bucket/ --recursive

# List objects with specific prefix
aws s3 ls s3://my-bucket/prefix/ --recursive
```

### Copy Operations
```bash
# Copy file to S3
aws s3 cp file.txt s3://my-bucket/

# Copy from S3 to local
aws s3 cp s3://my-bucket/file.txt ./

# Copy between S3 buckets
aws s3 cp s3://source-bucket/file.txt s3://dest-bucket/

# Copy with specific storage class
aws s3 cp file.txt s3://my-bucket/ --storage-class GLACIER

# Copy with server-side encryption
aws s3 cp file.txt s3://my-bucket/ --sse AES256
```

### Move Operations
```bash
# Move file to S3
aws s3 mv file.txt s3://my-bucket/

# Move from S3 to local
aws s3 mv s3://my-bucket/file.txt ./

# Move between S3 locations
aws s3 mv s3://my-bucket/old-path/ s3://my-bucket/new-path/ --recursive
```

### Delete Operations
```bash
# Delete single object
aws s3 rm s3://my-bucket/file.txt

# Delete all objects with prefix
aws s3 rm s3://my-bucket/prefix/ --recursive

# Delete bucket (must be empty)
aws s3 rb s3://my-bucket/

# Force delete bucket with contents
aws s3 rb s3://my-bucket/ --force
```

## S3 API Commands

### Create and Configure Buckets
```bash
# Create bucket (us-east-1)
aws s3api create-bucket --bucket my-bucket

# Create bucket in specific region
aws s3api create-bucket --bucket my-bucket \
  --region us-west-2 \
  --create-bucket-configuration LocationConstraint=us-west-2

# Enable versioning
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Enable server-side encryption by default
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

### Upload Objects with S3 API
```bash
# Put object
aws s3api put-object --bucket my-bucket --key file.txt --body ./file.txt

# Put object with metadata
aws s3api put-object --bucket my-bucket --key file.txt \
  --body ./file.txt \
  --metadata '{"author":"John Doe","version":"1.0"}'

# Put object with content type
aws s3api put-object --bucket my-bucket --key image.jpg \
  --body ./image.jpg \
  --content-type image/jpeg

# Put object with tags
aws s3api put-object --bucket my-bucket --key file.txt \
  --body ./file.txt \
  --tagging 'environment=production&team=data'
```

### Multipart Upload
```bash
# Initiate multipart upload
aws s3api create-multipart-upload --bucket my-bucket --key large-file.zip

# Upload part
aws s3api upload-part --bucket my-bucket \
  --key large-file.zip \
  --part-number 1 \
  --body part1.dat \
  --upload-id "upload-id-here"

# Complete multipart upload
aws s3api complete-multipart-upload --bucket my-bucket \
  --key large-file.zip \
  --upload-id "upload-id-here" \
  --multipart-upload file://parts.json

# Abort multipart upload
aws s3api abort-multipart-upload --bucket my-bucket \
  --key large-file.zip \
  --upload-id "upload-id-here"
```

### Get Object Information
```bash
# Get object metadata
aws s3api head-object --bucket my-bucket --key file.txt

# Get object ACL
aws s3api get-object-acl --bucket my-bucket --key file.txt

# Get object tags
aws s3api get-object-tagging --bucket my-bucket --key file.txt

# List object versions
aws s3api list-object-versions --bucket my-bucket --prefix folder/
```

## Recursive Operations

### Sync Operations
```bash
# Sync local directory to S3
aws s3 sync ./local-folder s3://my-bucket/folder/

# Sync S3 to local
aws s3 sync s3://my-bucket/folder/ ./local-folder

# Sync with delete (remove files not in source)
aws s3 sync ./local-folder s3://my-bucket/folder/ --delete

# Sync only specific file types
aws s3 sync ./local-folder s3://my-bucket/folder/ \
  --exclude "*" --include "*.jpg"

# Sync with size-only comparison (faster)
aws s3 sync ./local-folder s3://my-bucket/folder/ --size-only

# Dry run to preview changes
aws s3 sync ./local-folder s3://my-bucket/folder/ --dryrun
```

### Recursive Copy
```bash
# Copy entire directory
aws s3 cp ./local-folder s3://my-bucket/folder/ --recursive

# Copy with exclude patterns
aws s3 cp s3://my-bucket/ s3://backup-bucket/ \
  --recursive \
  --exclude "*.tmp" \
  --exclude "logs/*"

# Copy with include patterns
aws s3 cp s3://my-bucket/ s3://backup-bucket/ \
  --recursive \
  --exclude "*" \
  --include "*.pdf" \
  --include "*.docx"

# Copy files modified after specific date
aws s3 cp s3://my-bucket/ ./local-folder/ \
  --recursive \
  --exclude "*" \
  --include "*" \
  --metadata-directive COPY
```

## Data Upload and Sync Operations

### Batch Upload
```bash
# Upload multiple files with parallel transfers
aws s3 cp ./data-folder s3://my-bucket/data/ \
  --recursive \
  --cli-write-timeout 0 \
  --cli-read-timeout 0

# Upload with progress bar
aws s3 cp large-file.zip s3://my-bucket/ \
  --no-guess-mime-type \
  --cli-progress-bar on

# Upload with bandwidth limit (KB/s)
aws configure set s3.max_bandwidth 5000KB/s
aws s3 cp ./large-folder s3://my-bucket/ --recursive
```

### Advanced Sync Options
```bash
# Sync with exact timestamps
aws s3 sync ./folder s3://my-bucket/ --exact-timestamps

# Sync with follow symlinks
aws s3 sync ./folder s3://my-bucket/ --follow-symlinks

# Sync with no follow symlinks
aws s3 sync ./folder s3://my-bucket/ --no-follow-symlinks

# Sync with ACL settings
aws s3 sync ./folder s3://my-bucket/ --acl public-read

# Sync with storage class
aws s3 sync ./folder s3://my-bucket/ \
  --storage-class INTELLIGENT_TIERING
```

## Bucket Management

### Bucket Policies
```bash
# Get bucket policy
aws s3api get-bucket-policy --bucket my-bucket

# Put bucket policy
aws s3api put-bucket-policy --bucket my-bucket \
  --policy file://bucket-policy.json

# Delete bucket policy
aws selman get-bucket-policy --bucket my-bucket

# Example bucket policy (bucket-policy.json)
cat > bucket-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
EOF
```

### Lifecycle Rules
```bash
# Put lifecycle configuration
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json

# Get lifecycle configuration
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket

# Example lifecycle configuration
cat > lifecycle.json << 'EOF'
{
  "Rules": [
    {
      "ID": "Archive old files",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "INTELLIGENT_TIERING"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    }
  ]
}
EOF
```

### CORS Configuration
```bash
# Put CORS configuration
aws s3api put-bucket-cors --bucket my-bucket \
  --cors-configuration file://cors.json

# Get CORS configuration
aws s3api get-bucket-cors --bucket my-bucket

# Example CORS configuration
cat > cors.json << 'EOF'
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
EOF
```

## Object Management

### Object Operations
```bash
# Copy object within same bucket
aws s3api copy-object \
  --bucket my-bucket \
  --copy-source my-bucket/old-key \
  --key new-key

# Restore object from Glacier
aws s3api restore-object \
  --bucket my-bucket \
  --key archived-file.txt \
  --restore-request Days=7

# Generate presigned URL (expires in 1 hour)
aws s3 presign s3://my-bucket/file.txt --expires-in 3600

# Batch delete objects
aws s3api delete-objects --bucket my-bucket \
  --delete file://delete.json

# Example delete.json
cat > delete.json << 'EOF'
{
  "Objects": [
    {"Key": "file1.txt"},
    {"Key": "file2.txt"},
    {"Key": "folder/file3.txt"}
  ]
}
EOF
```

### Object Tagging
```bash
# Put object tags
aws s3api put-object-tagging \
  --bucket my-bucket \
  --key file.txt \
  --tagging 'TagSet=[{Key=environment,Value=prod},{Key=owner,Value=teamA}]'

# Get object tags
aws s3api get-object-tagging --bucket my-bucket --key file.txt

# Delete object tags
aws s3api delete-object-tagging --bucket my-bucket --key file.txt
```

## Access Control and Permissions

### Bucket and Object ACLs
```bash
# Put bucket ACL
aws s3api put-bucket-acl --bucket my-bucket --acl private

# Put object ACL
aws s3api put-object-acl --bucket my-bucket --key file.txt --acl public-read

# Grant specific permissions
aws s3api put-object-acl --bucket my-bucket --key file.txt \
  --grant-read emailaddress=user@example.com \
  --grant-write emailaddress=admin@example.com

# Put bucket public access block
aws s3api put-public-access-block --bucket my-bucket \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false
```

### IAM Policies for S3
```bash
# Example IAM policy for S3 access
cat > s3-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::my-bucket"
    }
  ]
}
EOF

# Attach policy to user
aws iam put-user-policy --user-name myuser \
  --policy-name S3Access \
  --policy-document file://s3-policy.json
```

## Performance Optimization

### Transfer Acceleration
```bash
# Enable transfer acceleration
aws s3api put-bucket-accelerate-configuration \
  --bucket my-bucket \
  --accelerate-configuration Status=Enabled

# Use accelerated endpoint
aws s3 cp file.txt s3://my-bucket/ \
  --endpoint-url https://my-bucket.s3-accelerate.amazonaws.com
```

### Parallel Transfers
```bash
# Configure concurrent requests
aws configure set s3.max_concurrent_requests 20
aws configure set s3.max_queue_size 10000

# Use multipart threshold for large files
aws configure set s3.multipart_threshold 64MB
aws configure set s3.multipart_chunksize 16MB

# Set max bandwidth
aws configure set s3.max_bandwidth 100MB/s
```

### Request Payer
```bash
# Enable requester pays
aws s3api put-bucket-request-payment \
  --bucket my-bucket \
  --request-payment-configuration Payer=Requester

# Access requester-pays bucket
aws s3 cp s3://requester-pays-bucket/file.txt ./ --request-payer requester
```

## Cost Management

### Storage Class Analysis
```bash
# Put analytics configuration
aws s3api put-bucket-analytics-configuration \
  --bucket my-bucket \
  --id analysis-1 \
  --analytics-configuration file://analytics.json

# List analytics configurations
aws s3api list-bucket-analytics-configurations --bucket my-bucket
```

### Intelligent Tiering
```bash
# Put intelligent tiering configuration
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket my-bucket \
  --id config-1 \
  --intelligent-tiering-configuration file://tiering.json
```

### Metrics and Monitoring
```bash
# Get bucket metrics configuration
aws s3api get-bucket-metrics-configuration \
  --bucket my-bucket \
  --id metrics-1

# List bucket metrics
aws s3api list-bucket-metrics-configurations --bucket my-bucket
```

## Troubleshooting

### Common Issues and Solutions

#### Check Bucket Existence and Access
```bash
# Test if bucket exists
aws s3api head-bucket --bucket my-bucket

# Check bucket location
aws s3api get-bucket-location --bucket my-bucket

# List bucket with debug output
aws s3 ls s3://my-bucket/ --debug
```

#### Verify Permissions
```bash
# Check IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/username \
  --action-names s3:GetObject s3:PutObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

#### Network and Connectivity
```bash
# Test S3 endpoint connectivity
aws s3 ls --debug 2>&1 | grep "endpoint"

# Use specific endpoint
aws s3 ls --endpoint-url https://s3.us-west-2.amazonaws.com

# Check DNS resolution
nslookup s3.amazonaws.com
```

## Advanced Operations

### S3 Select
```bash
# Query CSV file with S3 Select
aws s3api select-object-content \
  --bucket my-bucket \
  --key data.csv \
  --expression "SELECT * FROM S3Object WHERE age > 25" \
  --expression-type SQL \
  --input-serialization '{"CSV": {"FileHeaderInfo": "USE"}}' \
  --output-serialization '{"CSV": {}}' \
  output.csv
```

### S3 Inventory
```bash
# Put inventory configuration
aws s3api put-bucket-inventory-configuration \
  --bucket my-bucket \
  --id inventory-1 \
  --inventory-configuration file://inventory.json
```

### S3 Batch Operations
```bash
# Create batch job
aws s3control create-job \
  --account-id 123456789012 \
  --manifest file://manifest.json \
  --operation file://operation.json \
  --priority 10 \
  --role-arn arn:aws:iam::123456789012:role/batch-operations-role
```

## Best Practices

### Security Best Practices
```bash
# Enable default encryption
aws s3api put-bucket-encryption --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:us-east-1:123456789012:key/12345678"
      }
    }]
  }'

# Enable bucket logging
aws s3api put-bucket-logging --bucket my-bucket \
  --bucket-logging-status file://logging.json

# Enable MFA delete
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "arn:aws:iam::123456789012:mfa/root-account-mfa-device 123456"
```

### Data Integrity
```bash
# Upload with checksum
aws s3api put-object --bucket my-bucket --key file.txt \
  --body ./file.txt \
  --content-md5 $(openssl dgst -md5 -binary file.txt | base64)

# Verify object integrity
aws s3api head-object --bucket my-bucket --key file.txt \
  --checksum-mode ENABLED
```

## Official AWS Resources

### Documentation
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [AWS S3 API Reference](https://docs.aws.amazon.com/cli/latest/reference/s3api/)
- [S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

### Tutorials and Guides
- [Getting Started with S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
- [S3 Transfer Acceleration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html)
- [S3 Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html)
- [S3 Replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)

### Developer Resources
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html)
- [AWS SDK for JavaScript](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/S3.html)
- [S3 API Examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/service_code_examples.html)
- [S3 Select Examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-select-sql-reference.html)

### Tools and Utilities
- [AWS CLI Installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [S3 Browser Tools](https://aws.amazon.com/s3/tools/)
- [CloudFormation S3 Templates](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html)

### Monitoring and Troubleshooting
- [S3 CloudWatch Metrics](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudwatch-monitoring.html)
- [S3 Access Logging](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html)
- [S3 Troubleshooting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/troubleshooting.html)
- [S3 Error Responses](https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html)

### Cost Optimization
- [S3 Pricing](https://aws.amazon.com/s3/pricing/)
- [S3 Cost Optimization](https://aws.amazon.com/s3/cost-optimization/)
- [S3 Storage Lens](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)

### Compliance and Governance
- [S3 Compliance](https://aws.amazon.com/compliance/services-in-scope/)
- [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)
- [AWS Config Rules for S3](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)
- [S3 Access Points](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html)

## Quick Reference Card

### Most Common Commands
```bash
# Upload file
aws s3 cp file.txt s3://bucket/

# Download file
aws s3 cp s3://bucket/file.txt ./

# Sync directory
aws s3 sync ./folder s3://bucket/folder/

# List contents
aws s3 ls s3://bucket/ --recursive

# Delete file
aws s3 rm s3://bucket/file.txt

# Create bucket
aws s3 mb s3://new-bucket/

# Remove bucket
aws s3 rb s3://bucket/ --force

# Get object info
aws s3api head-object --bucket bucket --key file.txt

# Generate presigned URL
aws s3 presign s3://bucket/file.txt

# Check bucket access
aws s3api head-bucket --bucket bucket
```

## Environment Variables

```bash
# AWS Credentials
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_SESSION_TOKEN=your-session-token

# AWS Configuration
export AWS_DEFAULT_REGION=us-east-1
export AWS_DEFAULT_OUTPUT=json
export AWS_PROFILE=myprofile

# S3 Specific
export AWS_S3_ENDPOINT=https://s3.amazonaws.com
export S3_USE_ACCELERATE_ENDPOINT=true
```

## Conclusion

This guide covers the essential AWS S3 commands and operations for data management. Always refer to the official AWS documentation for the most up-to-date information and additional features. Remember to follow security best practices and implement proper access controls when working with S3 buckets and objects.