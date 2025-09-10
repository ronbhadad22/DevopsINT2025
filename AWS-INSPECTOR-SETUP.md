# AWS Inspector SBOM Pipeline Setup

This document provides setup instructions for the AWS Inspector SBOM generation and vulnerability scanning pipelines.

## 🚀 Pipeline Overview

Two new workflows have been created:

1. **`aws-inspector-sbom.yml`** - Standalone AWS Inspector scanning
2. **`aws-inspector-integration.yml`** - Integrated with existing CI/CD pipeline

## 🔧 AWS Setup Requirements

### 1. AWS Account Configuration

#### Enable AWS Inspector V2
```bash
# Enable Inspector for ECR scanning
aws inspector2 enable --resource-types ECR --account-ids YOUR_ACCOUNT_ID
```

#### Create ECR Repository
```bash
# Create repository for Inspector scanning
aws ecr create-repository --repository-name server-nodejs-inspector
```

#### Create S3 Bucket for SBOM Storage (Optional)
```bash
# Create bucket for SBOM artifacts
aws s3 mb s3://your-sbom-bucket-name
```

### 2. IAM Role for GitHub Actions

Create an IAM role with the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:DescribeRepositories",
        "ecr:CreateRepository",
        "ecr:DescribeImages",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:PutImage",
        "ecr:BatchDeleteImage",
        "ecr:ListImages"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "inspector2:BatchGetFindingDetails",
        "inspector2:ListFindings",
        "inspector2:BatchGetFreeTrialInfo",
        "inspector2:Enable",
        "inspector2:GetConfiguration"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:PutObjectAcl"
      ],
      "Resource": "arn:aws:s3:::your-sbom-bucket-name/*"
    }
  ]
}
```

### 3. Trust Policy for GitHub Actions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_USERNAME/YOUR_REPO:*"
        }
      }
    }
  ]
}
```

## 🔐 GitHub Secrets Configuration

Configure the following secrets in your GitHub repository settings:

```
AWS_ACCOUNT_ID            # Your AWS Account ID (950555670656)
AWS_S3_SBOM_BUCKET       # S3 bucket name for SBOM storage (optional)
```

### Example Values:
```
AWS_ACCOUNT_ID: 950555670656
AWS_S3_SBOM_BUCKET: my-company-sbom-storage
```

**Note**: The AWS role ARN `arn:aws:iam::950555670656:role/github-oidc` is already configured in the workflows.

## 📋 Workflow Features

### AWS Inspector SBOM Workflow (`aws-inspector-sbom.yml`)

**Triggers:**
- Push to main/master/develop branches
- Pull requests
- Manual dispatch
- Weekly schedule (Mondays at 6 AM)

**Features:**
- ✅ Builds and pushes images to ECR
- ✅ Runs AWS Inspector V2 scans
- ✅ Generates SBOM in SPDX and CycloneDX formats
- ✅ Exports findings to S3
- ✅ Creates GitHub attestations
- ✅ Generates security reports
- ✅ Cleans up old ECR images

### AWS Inspector Integration (`aws-inspector-integration.yml`)

**Triggers:**
- After successful completion of main CI/CD pipeline
- Manual dispatch with image tag selection

**Features:**
- ✅ Copies images from GHCR to ECR
- ✅ Comprehensive Inspector scanning
- ✅ Enhanced SBOM with vulnerability data
- ✅ Multiple export formats (CycloneDX, SPDX)
- ✅ S3 storage with organized structure
- ✅ Detailed security summaries

## 📊 Generated Artifacts

### SBOM Files
- `aws-inspector-sbom.json` - CycloneDX format with vulnerabilities
- `aws-inspector-sbom-spdx.json` - SPDX format
- `sbom-summary.json` - Scan summary and metrics

### Security Reports
- `inspector-findings-detailed.json` - Detailed vulnerability findings
- `ecr-image-details.json` - ECR metadata
- `security-report.md` - Human-readable security report

### S3 Storage Structure
```
s3://your-bucket/
├── inspector-sbom/
│   └── your-repo/
│       └── commit-sha/
│           ├── cyclonedx-sbom.json
│           ├── spdx-sbom.json
│           ├── summary.json
│           ├── inspector-findings.json
│           └── ecr-metadata.json
└── sbom/
    └── your-repo/
        └── commit-sha/
            ├── aws-inspector-sbom.json
            ├── enhanced-aws-sbom.json
            └── inspector-findings.json
```

## 🔍 Vulnerability Analysis

The pipelines provide comprehensive vulnerability analysis:

- **AWS Inspector V2** - Native AWS container scanning
- **CVE Detection** - Common Vulnerabilities and Exposures
- **Severity Scoring** - Critical, High, Medium, Low ratings
- **Remediation Guidance** - AWS Inspector recommendations
- **Compliance Mapping** - CWE (Common Weakness Enumeration)

## 🚨 Troubleshooting

### Common Issues

1. **Inspector Not Enabled**
   ```bash
   aws inspector2 enable --resource-types ECR --account-ids YOUR_ACCOUNT_ID
   ```

2. **ECR Permission Denied**
   - Verify IAM role has ECR permissions
   - Check trust policy allows GitHub Actions

3. **S3 Upload Fails**
   - Verify S3 bucket exists
   - Check IAM permissions for S3

4. **No Findings Returned**
   - Inspector scans may take time to complete
   - Check Inspector console for scan status

### Debug Commands

```bash
# Check Inspector status
aws inspector2 get-configuration

# List ECR repositories
aws ecr describe-repositories

# Check S3 bucket contents
aws s3 ls s3://your-sbom-bucket-name/inspector-sbom/
```

## 🔄 Integration with Existing Pipeline

The AWS Inspector integration automatically triggers after your main CI/CD pipeline completes successfully. This provides:

- **Seamless Integration** - No changes to existing workflow
- **Dual Scanning** - Both Syft/Grype and AWS Inspector
- **Comprehensive Coverage** - Multiple security tools and formats
- **Centralized Storage** - All SBOMs in one S3 location

## 📈 Monitoring and Alerts

Consider setting up:

- **CloudWatch Alarms** - For high/critical vulnerabilities
- **SNS Notifications** - Security team alerts
- **S3 Event Notifications** - SBOM upload notifications
- **Inspector Findings** - AWS Security Hub integration

## 🎯 Next Steps

1. Configure AWS account and IAM roles
2. Set up GitHub secrets
3. Test with manual workflow dispatch
4. Monitor S3 bucket for SBOM files
5. Review Inspector findings in AWS console
6. Set up monitoring and alerting
