# Troubleshooting Guide

This guide provides solutions for common issues encountered while developing, deploying, and maintaining the EchoStor Security Posture Assessment Tool.

## 📋 Table of Contents

- [Environment Setup Issues](#environment-setup-issues)
- [Development Issues](#development-issues)
- [Authentication Issues](#authentication-issues)
- [Database Issues](#database-issues)
- [API and Network Issues](#api-and-network-issues)
- [CI/CD Issues](#cicd-issues)
- [Deployment Issues](#deployment-issues)
- [Runtime Issues](#runtime-issues)
- [Performance Issues](#performance-issues)

## 🛠️ Environment Setup Issues

### Poetry Not Found
**Error**: `poetry: command not found`

**Solutions**:
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc

# Verify installation
poetry --version
```

### Node.js/pnpm Not Found
**Error**: `node: command not found` or `pnpm: command not found`

**Solutions**:
```bash
# Install Node.js 18+ using nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# Install pnpm
npm install -g pnpm

# Verify installations
node --version
pnpm --version
```

### Python Version Issues
**Error**: `Python 3.12 required, but found 3.x`

**Solutions**:
```bash
# Using pyenv (recommended)
curl https://pyenv.run | bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv install 3.12.0
pyenv global 3.12.0

# Verify version
python --version
```

### Docker Issues
**Error**: `docker: command not found` or permission denied

**Solutions**:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (Ubuntu/Debian)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

## 💻 Development Issues

### Port Already in Use
**Error**: `Error: listen EADDRINUSE: address already in use :::3000` or `:8000`

**Solutions**:
```bash
# Find and kill process using port 3000
lsof -ti:3000 | xargs kill -9

# Find and kill process using port 8000  
lsof -ti:8000 | xargs kill -9

# For Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Use different ports
cd frontend && PORT=3001 pnpm run dev
cd backend && uvicorn app.main:app --port 8001 --reload
```

### Database Connection Errors
**Error**: `could not connect to server: Connection refused`

**Solutions**:
```bash
# Check if PostgreSQL is running
sudo service postgresql status

# Start PostgreSQL
sudo service postgresql start

# For Docker Compose setup
docker-compose up postgres

# Check DATABASE_URL format
# Correct format: postgresql://user:password@host:port/database
DATABASE_URL="postgresql://echostor:password@localhost:5432/security_posture"

# Test connection
cd backend
poetry run python -c "from app.core.database import engine; print('Connected successfully')"
```

### Frontend Can't Connect to Backend
**Error**: `Network Error` or CORS errors in browser console

**Solutions**:
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify environment variables
cd frontend
cat .env.local
# Should contain: NEXT_PUBLIC_API_URL=http://localhost:8000

# Check CORS configuration in backend
# In backend/.env, verify:
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Restart both services
cd backend && poetry run uvicorn app.main:app --reload
cd frontend && pnpm run dev
```

### Missing Environment Variables
**Error**: `KeyError: 'DATABASE_URL'` or similar

**Solutions**:
```bash
# Backend - copy and edit .env file
cd backend
cp .env.example .env
nano .env  # Edit with your values

# Frontend - create .env.local if needed
cd frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=EchoStor Security Posture Assessment
EOF

# Check if variables are loaded
cd backend
poetry run python -c "import os; print(os.getenv('DATABASE_URL'))"
```

## 🔐 Authentication Issues

### JWT Token Errors
**Error**: `Could not validate credentials` or `Token has expired`

**Solutions**:
```bash
# Check JWT_SECRET_KEY is set and consistent
cd backend
poetry run python -c "import os; print(len(os.getenv('JWT_SECRET_KEY', '')))"
# Should be at least 32 characters

# Clear browser cookies/localStorage and re-login
# Or programmatically:
localStorage.removeItem('access_token');
document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

# Check token expiration settings
# In backend/.env:
ACCESS_TOKEN_EXPIRE_HOURS=24
ADMIN_TOKEN_EXPIRE_HOURS=8
```

### Admin Can't Login
**Error**: `Invalid credentials` for admin user

**Solutions**:
```bash
# Check admin email configuration
echo $ADMIN_EMAIL  # Should be: aadish.bahati@echostor.com

# Create/recreate admin user
cd backend
poetry run python << EOF
from app.models.user import User
from app.core.database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

# Check if admin exists
admin = db.query(User).filter(User.email == "aadish.bahati@echostor.com").first()
if admin:
    # Update password
    admin.password_hash = pwd_context.hash("your-new-password")
    admin.is_admin = True
    admin.is_active = True
else:
    # Create new admin
    admin = User(
        email="aadish.bahati@echostor.com",
        full_name="Admin User",
        company_name="EchoStor Technologies",
        password_hash=pwd_context.hash("your-new-password"),
        is_admin=True,
        is_active=True
    )
    db.add(admin)

db.commit()
db.close()
print("Admin user updated successfully")
EOF
```

### Password Hash Issues
**Error**: Invalid password hash format

**Solutions**:
```bash
# Generate proper bcrypt hash
cd backend
poetry run python << EOF
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hash_value = pwd_context.hash("your-password")
print(f"ADMIN_PASSWORD_HASH={hash_value}")
EOF

# Use the output in your .env file or Fly.io secrets
flyctl secrets set ADMIN_PASSWORD_HASH="$2b$12$..."
```

## 🗄️ Database Issues

### Migration Errors
**Error**: `Target database is not up to date` or migration conflicts

**Solutions**:
```bash
cd backend

# Check migration status
poetry run alembic current

# Check pending migrations
poetry run alembic heads

# Reset to head (careful - this will lose data)
poetry run alembic stamp head

# Create new migration after model changes
poetry run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
poetry run alembic upgrade head

# Downgrade if needed (careful)
poetry run alembic downgrade -1
```

### Database Permission Errors
**Error**: `permission denied for table` or similar

**Solutions**:
```bash
# Connect to database as admin
psql postgresql://user:password@host:port/database

-- Grant permissions to application user
GRANT ALL PRIVILEGES ON DATABASE security_posture TO echostor;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO echostor;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO echostor;

-- Check current user permissions
\dp
```

### Database Connection Pool Exhausted
**Error**: `QueuePool limit of size 5 overflow 10 reached`

**Solutions**:
```python
# In backend/app/core/database.py, adjust pool settings
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

## 🌐 API and Network Issues

### CORS Errors
**Error**: `Access to fetch at ... has been blocked by CORS policy`

**Solutions**:
```bash
# Check ALLOWED_ORIGINS in backend
echo $ALLOWED_ORIGINS

# Should include your frontend URL
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.vercel.app

# For development, temporary fix:
ALLOWED_ORIGINS="*"  # Only for development!

# Restart backend after changing CORS settings
```

### API Rate Limiting
**Error**: `429 Too Many Requests`

**Solutions**:
```bash
# Check rate limit configuration in backend/app/api/
# Temporarily disable for testing (not recommended for production)

# Or implement exponential backoff in frontend
# This is already implemented in api.ts with axios-retry
```

### SSL Certificate Issues
**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions**:
```bash
# For development only - disable SSL verification
export PYTHONHTTPSVERIFY=0

# Better solution - update certificates
pip install --upgrade certifi

# For requests library
import certifi
import requests
response = requests.get('https://api.example.com', verify=certifi.where())
```

## ⚙️ CI/CD Issues

### Lint Failures
**Error**: Ruff or ESLint errors in CI

**Solutions**:
```bash
# Backend - fix Ruff issues
cd backend
poetry run ruff check . --fix
poetry run ruff format .

# Frontend - fix ESLint issues  
cd frontend
pnpm run lint:fix
pnpm run format

# Check what CI is running
cat .github/workflows/backend-ci.yml
cat .github/workflows/deploy-frontend.yml
```

### Format Check Failures
**Error**: Code formatting issues

**Solutions**:
```bash
# Backend formatting
cd backend
poetry run ruff format .

# Frontend formatting
cd frontend  
pnpm run format

# Check format before committing
pnpm run format:check
```

### Type Check Failures
**Error**: mypy or TypeScript errors

**Solutions**:
```bash
# Backend type check
cd backend
poetry run mypy app --ignore-missing-imports

# Frontend type check
cd frontend
pnpm run type-check

# Fix common TypeScript issues
# Add type annotations or use 'any' temporarily:
const data: any = await fetchData();
```

### Test Failures
**Error**: pytest or Jest test failures

**Solutions**:
```bash
# Run tests locally to debug
cd backend
poetry run pytest -v

cd frontend  
pnpm run test

# Run specific test file
poetry run pytest tests/test_auth.py -v

# Check test coverage
poetry run pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## 🚀 Deployment Issues

### Fly.io Deployment Fails
**Error**: Various Fly.io deployment errors

**Solutions**:
```bash
# Check fly.toml configuration
flyctl config validate

# Check app status
flyctl status --app your-app-name

# View deployment logs
flyctl logs --app your-app-name

# Check secrets are set
flyctl secrets list --app your-app-name

# Redeploy with verbose output
flyctl deploy --verbose

# Check if app is healthy
flyctl checks list --app your-app-name
```

### Vercel Build Fails
**Error**: Build failures on Vercel

**Solutions**:
```bash
# Check build locally
cd frontend
pnpm run build

# Check environment variables in Vercel dashboard
# Settings > Environment Variables

# Check build logs in Vercel dashboard
# Or with CLI:
vercel logs

# Redeploy
vercel --prod
```

### Database Migration Fails in Production
**Error**: Migration errors during deployment

**Solutions**:
```bash
# SSH into Fly.io container
flyctl ssh console --app your-app-name

# Run migrations manually
poetry run alembic upgrade head

# Check migration status
poetry run alembic current

# If migration is stuck, stamp current version
poetry run alembic stamp head
```

### DNS/Domain Issues
**Error**: Domain not resolving or SSL certificate issues

**Solutions**:
```bash
# Check DNS propagation
nslookup your-domain.com
dig your-domain.com

# For Vercel domains, check configuration in dashboard
# For custom domains, ensure DNS records are correct:
# A record: @ -> Vercel IP
# CNAME: www -> your-app.vercel.app

# Check SSL certificate
openssl s_client -connect your-domain.com:443
```

## 🔧 Runtime Issues

### 404 Errors
**Error**: API endpoints returning 404

**Solutions**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check API routes are registered
curl http://localhost:8000/docs

# Verify URL in frontend matches backend routes
# Frontend: /api/auth/login
# Backend: /api/auth/login (should match)

# Check NEXT_PUBLIC_API_URL
echo $NEXT_PUBLIC_API_URL
```

### 500 Internal Server Errors
**Error**: Server errors on API requests

**Solutions**:
```bash
# Check backend logs
flyctl logs --app your-app-name

# For local development
cd backend
poetry run uvicorn app.main:app --reload --log-level debug

# Check database connectivity
poetry run python -c "from app.core.database import engine; engine.connect()"

# Check for missing environment variables
poetry run python -c "
import os
required_vars = ['DATABASE_URL', 'JWT_SECRET_KEY', 'ADMIN_EMAIL']
for var in required_vars:
    print(f'{var}: {\"✓\" if os.getenv(var) else \"✗ MISSING\"}')"
```

### Report Generation Fails
**Error**: PDF report generation errors

**Solutions**:
```bash
# Check OpenAI API key (for AI reports)
echo $OPENAI_API_KEY

# Check file system permissions
ls -la /tmp/reports  # or wherever reports are stored

# Check background task logs
flyctl logs --app your-app-name | grep "report"

# Test report generation locally
cd backend
poetry run python -c "
from app.services.report_generator import generate_standard_report
# Test with a valid assessment ID
"
```

### Memory Issues
**Error**: `MemoryError` or out of memory errors

**Solutions**:
```bash
# Scale up Fly.io machine
flyctl scale vm shared-cpu-2x --app your-app-name

# Check memory usage
flyctl ssh console --app your-app-name
htop

# Optimize database queries
# Add indexes for slow queries
# Use pagination for large data sets
```

## ⚡ Performance Issues

### Slow API Responses
**Problem**: API endpoints taking too long to respond

**Solutions**:
```bash
# Check database query performance
flyctl postgres connect --app your-db-name
\timing on
EXPLAIN ANALYZE SELECT * FROM assessments WHERE user_id = 'some-id';

# Add missing indexes
CREATE INDEX CONCURRENTLY idx_assessments_user_status ON assessments(user_id, status);

# Enable query logging in PostgreSQL
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000; -- Log queries > 1s
SELECT pg_reload_conf();
```

### Slow Frontend Loading
**Problem**: Frontend pages loading slowly

**Solutions**:
```bash
# Analyze bundle size
cd frontend
pnpm run build
npx @next/bundle-analyzer

# Implement code splitting
# Use dynamic imports for large components:
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <div>Loading...</div>
});

# Optimize images
# Use Next.js Image component:
import Image from 'next/image'
<Image src="/image.png" alt="Alt text" width={500} height={300} />
```

### Database Connection Issues
**Problem**: Connection pool exhaustion or slow queries

**Solutions**:
```python
# Optimize connection pool
# In backend/app/core/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Increase pool size
    max_overflow=30,       # Allow more overflow connections
    pool_pre_ping=True,    # Test connections before use
    pool_recycle=3600,     # Recycle connections after 1 hour
)

# Use connection pooling with pgbouncer for production
# Add to fly.toml:
[env]
DATABASE_URL = "postgresql://user:pass@pgbouncer:6432/db"
```

## 🆘 Getting Help

### Debug Information to Collect

When asking for help, include:

1. **Error Messages**: Full error text and stack traces
2. **Environment**: OS, Python version, Node.js version
3. **Reproduction Steps**: How to recreate the issue
4. **Logs**: Recent application logs
5. **Configuration**: Relevant environment variables (sanitized)

### Useful Commands for Debugging

```bash
# System information
uname -a
python --version
node --version
docker --version

# Application status
flyctl status --app your-app-name
flyctl logs --app your-app-name | tail -100

# Environment check
cd backend && poetry run python -c "
import os, sys
print('Python:', sys.version)
print('DATABASE_URL set:', bool(os.getenv('DATABASE_URL')))
print('JWT_SECRET_KEY length:', len(os.getenv('JWT_SECRET_KEY', '')))
"

# Network connectivity
curl -I https://your-app.fly.dev/health
telnet your-db-host 5432
```

### Contact Support

- **GitHub Issues**: Create an issue with detailed information
- **Email Support**: aadish.bahati@echostor.com
- **Emergency**: For critical production issues

### Additional Resources

- [FastAPI Debugging](https://fastapi.tiangolo.com/tutorial/debugging/)
- [Next.js Debugging](https://nextjs.org/docs/advanced-features/debugging)
- [Fly.io Troubleshooting](https://fly.io/docs/reference/troubleshoot/)
- [Vercel Troubleshooting](https://vercel.com/docs/concepts/deployments/troubleshoot-a-build)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Remember**: Always test solutions in a development environment first before applying them to production.
