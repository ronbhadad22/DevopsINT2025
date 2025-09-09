# Server-NodeJS CI/CD Pipeline

This document describes the CI/CD pipeline specifically created for the `course-site-with-nodejs-backend/server-nodejs` application.

## 🚀 Workflow Overview

### Main Workflow: `server-nodejs-ci-cd.yml`
- **Triggers**: 
  - Push to `main`, `master`, or `develop` branches
  - Pull requests to `main` or `master`
  - Manual dispatch
  - **Path Filter**: Only triggers when files in `course-site-with-nodejs-backend/server-nodejs/` change

### Pipeline Stages

#### 1. **Test and Lint** (`test-and-lint`)
- ✅ Node.js 18 setup
- ✅ Dependency installation with `npm ci`
- ✅ Syntax validation of `server.js`
- ✅ Test execution (or basic validation if no tests)
- ✅ Security audit with `npm audit`
- ✅ ESLint setup and code linting

#### 2. **Build Docker Image** (`build-docker`)
- ✅ Runs only on `main`, `master`, or `develop` branches
- ✅ Creates optimized Dockerfile with:
  - Node.js 18 Alpine base image
  - Non-root user security
  - Health check endpoint
  - Production dependencies only
- ✅ Pushes to GitHub Container Registry (GHCR)
- ✅ Tags: `latest`, branch name, and commit SHA

#### 3. **Deploy to Staging** (`deploy-staging`)
- ✅ Triggers on `develop` branch
- ✅ Uses GitHub Environment protection
- ✅ Deployment simulation (uncomment for real deployment)

#### 4. **Deploy to Production** (`deploy-production`)
- ✅ Triggers on `main`/`master` branch
- ✅ Uses GitHub Environment protection
- ✅ Deployment simulation (uncomment for real deployment)

#### 5. **Health Check** (`health-check`)
- ✅ Post-deployment validation
- ✅ Runs after successful deployments

## 🔧 Setup Requirements

### GitHub Secrets (Optional for real deployments)
```
STAGING_HOST      # Staging server hostname
STAGING_USER      # Staging server username  
STAGING_SSH_KEY   # SSH private key for staging
PROD_HOST         # Production server hostname
PROD_USER         # Production server username
PROD_SSH_KEY      # SSH private key for production
```

### Docker Registry
- Uses GitHub Container Registry (GHCR) automatically
- No additional setup required - uses `GITHUB_TOKEN`
- Images pushed to: `ghcr.io/YOUR_USERNAME/YOUR_REPO/server-nodejs`

## 📁 Application Structure Expected

```
course-site-with-nodejs-backend/
└── server-nodejs/
    ├── package.json          # Required
    ├── package-lock.json     # Required for caching
    ├── server.js             # Main application file
    └── [other files...]
```

## 🚀 Deployment Flow

### Development Workflow
1. **Push to `develop`** → Triggers CI/CD → Deploys to **Staging**
2. **Push to `main`** → Triggers CI/CD → Deploys to **Production**

### Docker Image Tags
- `develop` branch → `ghcr.io/.../server-nodejs:develop`
- `main` branch → `ghcr.io/.../server-nodejs:latest`
- Any branch → `ghcr.io/.../server-nodejs:branch-name-SHA`

## 🛡️ Security Features

- **Dependency Scanning**: `npm audit` checks for vulnerabilities
- **Code Linting**: ESLint for code quality
- **Container Security**: Non-root user, minimal Alpine image
- **Health Checks**: Built-in container health monitoring

## 🔧 Customization

### Enable Real Deployments
Uncomment the SSH deployment sections in the workflow:

```yaml
# Uncomment for actual deployment
- name: Deploy to staging server
  uses: appleboy/ssh-action@v1.0.0
  with:
    host: ${{ secrets.STAGING_HOST }}
    # ... rest of configuration
```

### Modify Docker Configuration
Edit the Dockerfile creation section in `build-docker` job to customize:
- Port exposure (default: 3000)
- Health check endpoint (default: `/health`)
- Environment variables
- Additional dependencies

### Add Tests
Add test scripts to your `package.json`:
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

## 📊 Monitoring

### GitHub Actions
- View workflow runs in **Actions** tab
- Check deployment status in **Environments** section
- Monitor build logs and test results

### Container Registry
- View pushed images at `ghcr.io/YOUR_USERNAME/YOUR_REPO/server-nodejs`
- Check image sizes and security scan results

## 🚨 Troubleshooting

### Common Issues
1. **Build Fails**: Check `package.json` and `server.js` syntax
2. **Docker Push Fails**: Verify GHCR permissions
3. **Deployment Fails**: Check server connectivity and SSH keys
4. **Health Check Fails**: Ensure `/health` endpoint exists or modify health check

### Debug Steps
1. Check workflow logs in GitHub Actions
2. Validate `package.json` and `package-lock.json`
3. Test Docker build locally:
   ```bash
   cd course-site-with-nodejs-backend/server-nodejs
   docker build -t test-server .
   docker run -p 3000:3000 test-server
   ```

## 🎯 Next Steps

1. **Push changes** to trigger the workflow
2. **Configure secrets** for real deployments
3. **Add health endpoint** to your server.js:
   ```javascript
   app.get('/health', (req, res) => {
     res.status(200).json({ status: 'OK', timestamp: new Date().toISOString() });
   });
   ```
4. **Monitor first deployment** in GitHub Actions

The pipeline is ready to use and will automatically trigger when you make changes to the `server-nodejs` directory!
