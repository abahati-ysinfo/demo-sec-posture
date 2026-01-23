# Deployment Guide

This guide provides comprehensive instructions for deploying the EchoStor Security Posture Assessment Tool to production environments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Backend Deployment (Fly.io)](#backend-deployment-flyio)
- [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [Database Setup](#database-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [Maintenance and Updates](#maintenance-and-updates)

## 🛠️ Prerequisites

### Required Accounts
- **GitHub Account**: For repository access and CI/CD
- **Fly.io Account**: For backend and database hosting
- **Vercel Account**: For frontend hosting
- **OpenAI Account**: For AI-enhanced reports (optional)

### Required Tools
- **flyctl CLI**: Fly.io command-line tool
- **Vercel CLI**: Vercel command-line tool (optional)
- **Git**: Version control
- **Node.js 18+**: For frontend builds
- **Python 3.12+**: For backend development

### Installation
```bash
# Install Fly.io CLI
curl -L https://fly.io/install.sh | sh

# Install Vercel CLI (optional)
npm install -g vercel

# Verify installations
flyctl version
vercel --version
```

## ⚙️ Environment Configuration

### Backend Environment Variables

Create and configure the following environment variables in your backend deployment:

#### Required Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@hostname:5432/database_name

# JWT Configuration  
JWT_SECRET_KEY=your-super-secret-jwt-key-min-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
ADMIN_TOKEN_EXPIRE_HOURS=8

# Admin Configuration
ADMIN_EMAIL=aadish.bahati@echostor.com

# Application Settings
ASSESSMENT_EXPIRY_DAYS=15
AUTO_SAVE_INTERVAL_MINUTES=10

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app,https://www.yourdomain.com
```

#### Optional Variables
```bash
# OpenAI Integration (for AI reports)
OPENAI_API_KEY=your-openai-api-key

# OpenAI Keys Management (Required if using OpenAI Keys feature)
# Generate with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
OPENAI_KEYS_ENCRYPTION_KEY=your-fernet-encryption-key

# Admin Login (alternative to using database admin user)
ADMIN_LOGIN_USER=admin@yourdomain.com
ADMIN_PASSWORD_HASH=your-bcrypt-hashed-password

# Email Configuration (future feature)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key

# Redis Configuration (optional caching)
REDIS_URL=redis://username:password@hostname:6379

# Report Configuration
REPORT_DELIVERY_DAYS=5
MAX_FILE_SIZE_MB=10
```

### Frontend Environment Variables

Configure the following environment variables for your frontend deployment:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://your-backend-app.fly.dev

# Application Configuration
NEXT_PUBLIC_APP_NAME=EchoStor Security Posture Assessment

# Analytics (optional)
NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

## 🚀 Backend Deployment (Fly.io)

### Initial Setup

1. **Login to Fly.io**
   ```bash
   flyctl auth login
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/ec-aadishbahati/echostor-security-posture-tool.git
   cd echostor-security-posture-tool/backend
   ```

3. **Initialize Fly App**
   ```bash
   flyctl launch
   ```
   
   This will:
   - Create a new Fly.io app
   - Generate `fly.toml` configuration file
   - Set up basic deployment configuration

### Database Setup

1. **Create PostgreSQL Database**
   ```bash
   flyctl postgres create --name echostor-db --region iad
   ```

2. **Attach Database to App**
   ```bash
   flyctl postgres attach --app your-app-name echostor-db
   ```

3. **Get Database Connection String**
   ```bash
   flyctl postgres connect --app echostor-db
   ```

### Configure Secrets

Set environment variables as Fly.io secrets:

```bash
# Required secrets
flyctl secrets set DATABASE_URL="postgresql://user:pass@host:5432/db"
flyctl secrets set JWT_SECRET_KEY="your-super-secret-jwt-key-minimum-32-characters"
flyctl secrets set ADMIN_EMAIL="aadish.bahati@echostor.com"

# Optional secrets
flyctl secrets set OPENAI_API_KEY="your-openai-api-key"
flyctl secrets set ADMIN_PASSWORD_HASH="your-bcrypt-hashed-password"

# OpenAI Keys Management (Required if using OpenAI Keys feature)
# Generate encryption key with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
flyctl secrets set OPENAI_KEYS_ENCRYPTION_KEY="your-fernet-encryption-key"

# List all secrets to verify
flyctl secrets list
```

### Multi-Region Configuration

The app is configured for multi-region deployment in `fly.toml`:

```toml
[build]
dockerfile = "Dockerfile"

app = "echostor-security-posture-tool"
primary_region = "iad"

[deploy]
strategy = "rolling"

[[services]]
internal_port = 8000
protocol = "tcp"

[[services.ports]]
force_https = true
handlers = ["http"]
port = 80

[[services.ports]]
force_https = true
handlers = ["tls", "http"]
port = 443

# Multi-region machines
[[vm]]
size = "shared-cpu-1x"
regions = ["iad", "lax", "syd"]
```

### Deploy Backend

1. **Initial Deployment**
   ```bash
   flyctl deploy
   ```

2. **Run Database Migrations**
   ```bash
   flyctl ssh console
   # Inside the container:
   poetry run alembic upgrade head
   exit
   ```

3. **Scale Application**
   ```bash
   # Scale to multiple regions
   flyctl scale count 1 --region iad
   flyctl scale count 1 --region lax  
   flyctl scale count 1 --region syd
   ```

### Verify Backend Deployment

```bash
# Check app status
flyctl status

# Check health endpoint
curl https://your-app.fly.dev/health

# View logs
flyctl logs

# Monitor app
flyctl monitor
```

## 🌐 Frontend Deployment (Vercel)

### GitHub Integration Setup

1. **Connect Vercel to GitHub**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Import Project"
   - Connect your GitHub account
   - Select the repository

2. **Configure Build Settings**
   ```bash
   # Build Command
   cd frontend && pnpm run build
   
   # Output Directory
   frontend/.next
   
   # Install Command
   cd frontend && pnpm install
   ```

### Environment Variables

Configure in Vercel dashboard under Settings > Environment Variables:

```bash
# Production variables
NEXT_PUBLIC_API_URL=https://your-backend-app.fly.dev
NEXT_PUBLIC_APP_NAME=EchoStor Security Posture Assessment

# Optional analytics
NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

### Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://your-backend-app.fly.dev

vercel env add NEXT_PUBLIC_APP_NAME production
# Enter: EchoStor Security Posture Assessment
```

### Custom Domain Setup

1. **Add Domain in Vercel**
   - Go to Project Settings > Domains
   - Add your custom domain
   - Configure DNS records as instructed

2. **Update CORS in Backend**
   ```bash
   flyctl secrets set ALLOWED_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
   ```

## 🗄️ Database Setup

### Initial Schema Setup

1. **Connect to Database**
   ```bash
   flyctl postgres connect --app echostor-db
   ```

2. **Run Migrations**
   ```bash
   # From backend SSH session
   flyctl ssh console --app your-backend-app
   poetry run alembic upgrade head
   ```

### Create Admin User

```bash
# SSH into backend container
flyctl ssh console --app your-backend-app

# Start Python shell
poetry run python

# Create admin user
from app.models.user import User
from app.core.database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

admin_user = User(
    email="aadish.bahati@echostor.com",
    full_name="Admin User",
    company_name="EchoStor Technologies",
    password_hash=pwd_context.hash("your-secure-admin-password"),
    is_admin=True,
    is_active=True
)

db.add(admin_user)
db.commit()
db.close()
print("Admin user created successfully")
```

### Database Backups

```bash
# Create manual backup
flyctl postgres backup --app echostor-db

# List backups
flyctl postgres backup list --app echostor-db

# Restore from backup
flyctl postgres restore --app echostor-db --backup-id <backup-id>
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

The repository includes three GitHub Actions workflows:

#### 1. Backend CI (`/.github/workflows/backend-ci.yml`)
- **Triggers**: Push to main, PR with backend changes
- **Steps**: Lint (Ruff), format check, type check (mypy), tests (pytest)
- **Coverage**: Requires 80% test coverage

#### 2. Backend Deployment (`/.github/workflows/deploy-backend.yml`)
- **Triggers**: Push to main with backend changes
- **Steps**: Deploy to Fly.io automatically
- **Requirements**: `FLY_API_TOKEN` secret configured

#### 3. Frontend Deployment (`/.github/workflows/deploy-frontend.yml`)
- **Triggers**: Push to main with frontend changes  
- **Steps**: Lint, format check, build, deploy to Vercel
- **Requirements**: Vercel secrets configured

### Configure GitHub Secrets

Add the following secrets to your GitHub repository:

```bash
# Fly.io Deployment
FLY_API_TOKEN=your-fly-io-api-token

# Vercel Deployment (if using GitHub Actions)
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-vercel-org-id
VERCEL_PROJECT_ID=your-vercel-project-id
```

### Get Required Tokens

```bash
# Fly.io API Token
flyctl auth token

# Vercel Token
vercel login
# Go to https://vercel.com/account/tokens to create a token

# Vercel Org ID and Project ID
# Found in your project settings on Vercel dashboard
```

## 📊 Monitoring and Health Checks

### Health Check Endpoints

The backend provides several health check endpoints:

```bash
# Comprehensive health check
curl https://your-app.fly.dev/health

# Liveness probe (always returns 200 if app is running)
curl https://your-app.fly.dev/health/live

# Readiness probe (returns 200 if database is accessible)
curl https://your-app.fly.dev/health/ready
```

### Monitoring Setup

1. **Fly.io Monitoring**
   ```bash
   # View metrics
   flyctl monitor
   
   # Check logs
   flyctl logs --app your-app-name
   
   # Check app status
   flyctl status --app your-app-name
   ```

2. **Vercel Analytics**
   - Enabled automatically in Vercel dashboard
   - View metrics at vercel.com/dashboard/analytics

3. **Custom Alerts**
   ```bash
   # Set up Fly.io alerts for your app
   flyctl monitor --app your-app-name
   ```

### Log Aggregation

```bash
# Real-time logs
flyctl logs --app your-app-name

# Filtered logs
flyctl logs --app your-app-name | grep "ERROR"

# Export logs
flyctl logs --app your-app-name > app-logs.txt
```

## 🔧 Maintenance and Updates

### Updating the Application

1. **Code Changes**
   ```bash
   # Push changes trigger automatic deployment via GitHub Actions
   git push origin main
   
   # Or deploy manually
   cd backend
   flyctl deploy
   ```

2. **Database Migrations**
   ```bash
   # Create migration
   poetry run alembic revision --autogenerate -m "Description of changes"
   
   # Deploy migration
   flyctl ssh console --app your-app-name
   poetry run alembic upgrade head
   ```

3. **Environment Variable Updates**
   ```bash
   # Update Fly.io secrets
   flyctl secrets set VARIABLE_NAME="new-value"
   
   # Update Vercel environment variables via dashboard
   # Or using CLI:
   vercel env add VARIABLE_NAME production
   ```

### Scaling

```bash
# Scale vertically (more CPU/memory)
flyctl scale vm shared-cpu-2x --app your-app-name

# Scale horizontally (more instances)
flyctl scale count 2 --region iad --app your-app-name

# Scale to new regions
flyctl scale count 1 --region fra --app your-app-name
```

### Database Maintenance

```bash
# Monitor database performance
flyctl postgres connect --app echostor-db
# Run: SELECT * FROM pg_stat_activity;

# Vacuum database
flyctl ssh console --app echostor-db
# Run: VACUUM ANALYZE;

# Update database statistics
# Run: ANALYZE;
```

### Troubleshooting Deployments

1. **Check deployment logs**
   ```bash
   flyctl logs --app your-app-name
   ```

2. **Verify configuration**
   ```bash
   flyctl config show --app your-app-name
   ```

3. **Test health endpoints**
   ```bash
   curl -f https://your-app.fly.dev/health || echo "Health check failed"
   ```

4. **Check secrets**
   ```bash
   flyctl secrets list --app your-app-name
   ```

5. **Database connectivity**
   ```bash
   flyctl ssh console --app your-app-name
   poetry run python -c "from app.core.database import engine; print('DB connected')"
   ```

## 🛡️ Security Considerations

### Production Security Checklist

- [ ] **HTTPS Only**: Ensure all connections use HTTPS
- [ ] **Secrets Management**: All sensitive data stored as secrets, not in code
- [ ] **Database Security**: Database uses strong passwords and encryption
- [ ] **API Security**: Rate limiting and CORS properly configured
- [ ] **Access Control**: Admin access restricted to authorized users only
- [ ] **Backup Strategy**: Automated database backups configured
- [ ] **Monitoring**: Health checks and error monitoring in place
- [ ] **Updates**: Dependencies regularly updated for security patches

### Environment Separation

| Environment | Backend URL | Database | Purpose |
|------------|-------------|----------|---------|
| Development | http://localhost:8000 | Local PostgreSQL | Local development |
| Staging | https://staging-app.fly.dev | Staging database | Testing before production |
| Production | https://your-app.fly.dev | Production database | Live application |

## 📚 Additional Resources

- **Fly.io Documentation**: https://fly.io/docs/
- **Vercel Documentation**: https://vercel.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Next.js Deployment**: https://nextjs.org/docs/deployment

For troubleshooting common deployment issues, see [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

**Note**: Always test deployments in a staging environment before deploying to production. Keep your secrets secure and never commit them to version control.
