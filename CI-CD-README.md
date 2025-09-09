# CI/CD Pipeline Documentation

This repository contains comprehensive CI/CD pipelines using GitHub Actions for multiple application types.

## 🚀 Available Workflows

### 1. Main CI/CD Pipeline (`main-ci-cd.yml`)
- **Trigger**: Push to main/master/develop, PRs, manual dispatch
- **Purpose**: Orchestrates all other workflows based on changed files
- **Features**: 
  - Path-based change detection
  - Conditional workflow execution
  - Deployment status summary

### 2. Flask Application CI/CD (`flask-app-ci-cd.yml`)
- **Applications**: 
  - Simple webserver (`05_simple_webserver/`)
  - Docker Flask app (`Docker/`)
- **Features**:
  - Python linting with flake8
  - Unit testing with pytest
  - Code coverage reporting
  - Docker image building and pushing to GHCR
  - Security scanning with Trivy
  - Staging deployment simulation

### 3. Node.js Application CI/CD (`nodejs-ci-cd.yml`)
- **Application**: Course site with Node.js backend
- **Features**:
  - Frontend and backend testing
  - Security vulnerability scanning
  - Docker image building
  - Staging and production deployments
  - Performance testing

### 4. Kubernetes Deployment (`kubernetes-deploy.yml`)
- **Purpose**: Deploy and manage Kubernetes manifests
- **Features**:
  - Manifest validation with kubectl
  - Security scanning with kube-linter and Trivy
  - Helm chart linting and deployment
  - Environment-specific deployments

### 5. Nexus Package Upload (`nexus-upload.yml`)
- **Purpose**: Build and upload Python packages to Nexus repository
- **Features**: Existing workflow for Python package management

### 6. Security Scanning (`security-scan.yml`)
- **Schedule**: Weekly on Mondays at 2 AM
- **Features**:
  - Dependency vulnerability scanning
  - Docker image security analysis
  - Secret detection with GitLeaks
  - Code quality analysis with CodeQL

## 🔧 Setup Requirements

### GitHub Secrets
Configure the following secrets in your repository settings:

```
# Nexus Repository
NEXUS_PASS                 # Nexus repository password

# Security Scanning (Optional)
SNYK_TOKEN                 # Snyk API token for vulnerability scanning
GITLEAKS_LICENSE          # GitLeaks license (if using pro version)

# Deployment (Configure as needed)
STAGING_HOST              # Staging server hostname
STAGING_USER              # Staging server username
STAGING_SSH_KEY           # SSH private key for staging
PROD_HOST                 # Production server hostname
PROD_USER                 # Production server username
PROD_SSH_KEY              # SSH private key for production
KUBE_CONFIG_STAGING       # Base64 encoded kubeconfig for staging
KUBE_CONFIG_PROD          # Base64 encoded kubeconfig for production
```

### GitHub Container Registry
The workflows are configured to use GitHub Container Registry (GHCR) for Docker images. No additional setup required - uses `GITHUB_TOKEN` automatically.

## 📁 Project Structure

```
.
├── .github/workflows/
│   ├── main-ci-cd.yml           # Main orchestrator workflow
│   ├── flask-app-ci-cd.yml      # Flask applications CI/CD
│   ├── nodejs-ci-cd.yml         # Node.js application CI/CD
│   ├── kubernetes-deploy.yml    # Kubernetes deployments
│   ├── nexus-upload.yml         # Python package upload
│   └── security-scan.yml        # Security scanning
├── 05_simple_webserver/         # Flask web application
├── Docker/                      # Dockerized Flask app
├── course-site-with-nodejs-backend/  # Node.js application
├── k8s/                         # Kubernetes manifests
└── Nexus/                       # Python package
```

## 🔄 Workflow Triggers

| Workflow | Push (main/master) | Push (develop) | PR | Manual | Schedule |
|----------|-------------------|----------------|----|---------|---------| 
| Main CI/CD | ✅ | ✅ | ✅ | ✅ | ❌ |
| Flask Apps | ✅ | ✅ | ✅ | ✅ | ❌ |
| Node.js | ✅ | ✅ | ✅ | ✅ | ❌ |
| Kubernetes | ✅ | ❌ | ✅ | ✅ | ❌ |
| Nexus Upload | ✅ | ❌ | ✅ | ✅ | ❌ |
| Security Scan | ✅ | ✅ | ✅ | ✅ | ✅ (Weekly) |

## 🚀 Deployment Environments

### Staging
- **Trigger**: Push to `develop` branch
- **Purpose**: Testing and validation
- **URL**: https://staging.yourdomain.com

### Production
- **Trigger**: Push to `main`/`master` branch
- **Purpose**: Live application
- **URL**: https://yourdomain.com

## 🛡️ Security Features

- **Vulnerability Scanning**: Trivy, Snyk, Safety, Bandit
- **Secret Detection**: GitLeaks
- **Code Quality**: CodeQL, ESLint, flake8
- **Container Security**: Docker image scanning
- **Kubernetes Security**: Manifest validation and security policies

## 📊 Monitoring and Reporting

- **Code Coverage**: Codecov integration
- **Security Reports**: SARIF format uploaded to GitHub Security tab
- **Deployment Status**: Summary in workflow runs
- **Artifact Storage**: Build artifacts and reports

## 🔧 Customization

### Adding New Applications
1. Create application-specific workflow in `.github/workflows/`
2. Update `main-ci-cd.yml` to include new path filters
3. Add deployment configuration as needed

### Environment Configuration
1. Update environment URLs in workflow files
2. Configure secrets for deployment targets
3. Uncomment and modify deployment steps

### Security Scanning
1. Add API tokens for security tools
2. Configure severity thresholds
3. Set up notification channels

## 🚨 Troubleshooting

### Common Issues
1. **Missing Secrets**: Ensure all required secrets are configured
2. **Path Filters**: Verify file paths match your project structure
3. **Docker Registry**: Check GHCR permissions and authentication
4. **Kubernetes**: Validate cluster connectivity and permissions

### Debugging
- Check workflow logs in GitHub Actions tab
- Validate YAML syntax using online validators
- Test Docker builds locally before pushing
- Verify Kubernetes manifests with `kubectl --dry-run`

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Security Scanning Tools](https://github.com/analysis-tools-dev/static-analysis)
