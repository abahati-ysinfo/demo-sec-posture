# Contributing to EchoStor Security Posture Assessment Tool

Thank you for your interest in contributing to the EchoStor Security Posture Assessment Tool! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Branch Naming](#branch-naming)
- [Commit Guidelines](#commit-guidelines)

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful, professional, and constructive in all interactions.

## 🛠️ Development Setup

### Option 1: Docker Compose (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/ec-aadishbahati/echostor-security-posture-tool.git
cd echostor-security-posture-tool

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services Available:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Option 2: Manual Setup

If you prefer to run services manually:

#### Prerequisites
- **Node.js**: 18.x or higher
- **Python**: 3.12 or higher  
- **PostgreSQL**: 15 or higher
- **Poetry**: Python dependency management
- **pnpm**: Node.js package manager (preferred over npm/yarn)

#### Backend Setup
```bash
cd backend

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
poetry run alembic upgrade head

# Start development server
poetry run uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install pnpm if not already installed
npm install -g pnpm

# Install dependencies
pnpm install

# Set up environment variables (optional)
cp .env.local.example .env.local
# Edit .env.local if needed

# Start development server
pnpm run dev
```

#### Quick Setup Script
Alternatively, use our automated setup script:
```bash
./scripts/setup.sh
```

### 🔧 Development Tools

Install recommended VS Code extensions:
- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense

## 🔄 Development Workflow

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/your-username/echostor-security-posture-tool.git
cd echostor-security-posture-tool
git remote add upstream https://github.com/ec-aadishbahati/echostor-security-posture-tool.git
```

### 2. Create Feature Branch
```bash
# Get latest changes
git checkout main
git pull upstream main

# Create feature branch (see Branch Naming section)
git checkout -b devin/$(date +%s)-your-feature-name
```

### 3. Make Changes
- Follow code standards (see Code Standards section)
- Write tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 4. Run Quality Checks
```bash
# Backend checks
cd backend
poetry run ruff check . --fix          # Lint and auto-fix
poetry run ruff format .                # Format code
poetry run mypy app --ignore-missing-imports  # Type check
poetry run pytest --cov=app            # Run tests with coverage

# Frontend checks  
cd frontend
pnpm run lint                          # ESLint check
pnpm run lint:fix                      # Auto-fix lint issues
pnpm run format:check                  # Check Prettier formatting
pnpm run format                        # Format code
pnpm run type-check                    # TypeScript check
pnpm run test                          # Run tests
```

### 5. Commit and Push
```bash
# Stage your changes (don't use `git add .`)
git add path/to/changed/files

# Commit with conventional commit message
git commit -m "feat: add new assessment feature"

# Push to your fork
git push origin your-branch-name
```

### 6. Create Pull Request
- Open PR against the `main` branch
- Use the PR template if provided
- Ensure all CI checks pass
- Request review from maintainers

## 📏 Code Standards

### Python (Backend)

#### Style Guide
- **Linter**: Ruff (replaces Black, isort, flake8)
- **Type Checking**: mypy with strict mode
- **Line Length**: 88 characters (Black default)
- **Import Sorting**: Automated via Ruff

#### Code Structure
```python
# Standard imports first
import os
from datetime import datetime

# Third-party imports  
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Local imports last
from app.models.user import User
from app.core.database import get_db
```

#### Naming Conventions
- **Functions/Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files/Modules**: `snake_case.py`

#### Documentation
```python
def create_assessment(user_id: str, db: Session) -> Assessment:
    """Create a new assessment for the user.
    
    Args:
        user_id: The unique identifier for the user
        db: Database session
        
    Returns:
        Assessment: The created assessment instance
        
    Raises:
        HTTPException: If user not found or assessment already exists
    """
```

### TypeScript/React (Frontend)

#### Style Guide
- **Linter**: ESLint with TypeScript rules
- **Formatter**: Prettier
- **Line Length**: 80 characters
- **Semicolons**: Always required
- **Quotes**: Single quotes preferred

#### Component Structure
```typescript
// ComponentName.tsx
import React from 'react';
import { SomeType } from '../types';

interface ComponentNameProps {
  title: string;
  onSubmit?: (data: SomeType) => void;
}

export default function ComponentName({ title, onSubmit }: ComponentNameProps) {
  // Component logic here
  
  return (
    <div className="component-container">
      {/* JSX here */}
    </div>
  );
}
```

#### Naming Conventions
- **Components**: `PascalCase.tsx`
- **Hooks**: `useCamelCase.ts`
- **Utilities**: `camelCase.ts`
- **Types**: `PascalCase` interfaces
- **Constants**: `UPPER_SNAKE_CASE`

#### File Organization
```
src/
├── components/          # Reusable components
├── pages/              # Next.js pages
├── lib/                # Utilities and API client
├── hooks/              # Custom React hooks  
├── types/              # TypeScript type definitions
└── styles/             # Global styles
```

## 🧪 Testing Requirements

### Backend Testing
- **Minimum Coverage**: 80%
- **Framework**: pytest with fixtures
- **Location**: `backend/tests/`

```bash
# Run tests
cd backend
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_auth.py -v
```

#### Writing Tests
```python
def test_user_registration(client, db_session):
    """Test successful user registration."""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword123",
        "full_name": "Test User",
        "company_name": "Test Company"
    })
    
    assert response.status_code == 201
    assert "access_token" in response.json()
```

### Frontend Testing
- **Current Coverage**: Foundational (~10%)
- **Target Coverage**: 70%+
- **Framework**: Jest + React Testing Library
- **Location**: `frontend/tests/` (NOT in `src/pages/`)

```bash
# Run tests
cd frontend
pnpm run test

# Run with coverage
pnpm run test:coverage

# Run in watch mode
pnpm run test:watch
```

#### Writing Tests
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import LoginForm from '../components/LoginForm';

describe('LoginForm', () => {
  it('renders login form correctly', () => {
    render(<LoginForm onSubmit={jest.fn()} />);
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });
});
```

## 🔀 Pull Request Process

### Before Submitting
1. **Sync with upstream**: `git pull upstream main`
2. **Run all quality checks**: Linting, formatting, type checking, tests
3. **Test locally**: Verify your changes work end-to-end
4. **Update documentation**: If you changed APIs or added features
5. **Review your own changes**: Check the diff before submitting

### PR Requirements
- **Title**: Use conventional commit format (see Commit Guidelines)
- **Description**: Clear description of changes and motivation
- **Tests**: Include tests for new functionality
- **Documentation**: Update relevant documentation
- **Breaking Changes**: Clearly document any breaking changes
- **Screenshots**: Include screenshots for UI changes

### Review Process
1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Manual testing for significant changes
4. **Approval**: Maintainer approval required for merge

### After Approval
- **Squash and Merge**: Use squash commits for clean history
- **Delete Branch**: Clean up feature branches after merge

## 🌿 Branch Naming

Use the following format for branch names:

```
devin/{timestamp}-{descriptive-slug}
```

**Examples:**
```bash
# Feature branch
git checkout -b devin/1759893834-add-user-dashboard

# Bug fix branch  
git checkout -b devin/1759893835-fix-authentication-error

# Documentation update
git checkout -b devin/1759893836-update-api-docs
```

**Guidelines:**
- Use lowercase letters and hyphens only
- Keep descriptions concise but clear
- Generate timestamp with: `date +%s`
- Use descriptive slugs that indicate the change

## 💬 Commit Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- **feat**: New feature for users
- **fix**: Bug fix for users  
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring without functionality changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system or dependency changes
- **ci**: CI/CD configuration changes
- **chore**: Other changes that don't modify src or test files

### Examples
```bash
# Feature commits
git commit -m "feat(auth): add password reset functionality"
git commit -m "feat: add assessment progress tracking"

# Bug fixes
git commit -m "fix(api): resolve authentication token expiry issue"
git commit -m "fix: correct calculation in security score"

# Documentation
git commit -m "docs: update API endpoint documentation"
git commit -m "docs(readme): add Docker setup instructions"

# Breaking changes
git commit -m "feat!: change API response format for assessments

BREAKING CHANGE: The assessment API now returns scores as objects instead of arrays"
```

### Commit Message Guidelines
- **Use imperative mood**: "add" not "added" or "adds"
- **Be concise**: Limit first line to 72 characters
- **Be descriptive**: Explain what and why, not how
- **Reference issues**: Use "closes #123" or "fixes #123" when applicable

## 🚨 Common Pitfalls

### Code Quality
- **Don't skip linting**: Always run linters before committing
- **Don't ignore TypeScript errors**: Fix all type errors
- **Don't reduce test coverage**: Maintain or improve coverage
- **Don't commit secrets**: Use environment variables for sensitive data

### Git Workflow  
- **Don't work directly on main**: Always use feature branches
- **Don't use `git add .`**: Stage files intentionally
- **Don't force push to main**: Only force push to feature branches if needed
- **Don't mix unrelated changes**: Keep commits focused on single concerns

### Development
- **Don't hardcode URLs**: Use environment variables
- **Don't skip error handling**: Handle errors gracefully
- **Don't ignore accessibility**: Follow accessibility best practices
- **Don't skip documentation**: Update docs when changing APIs

## 🆘 Getting Help

If you need help:

1. **Check existing documentation**: README, API docs, architecture docs
2. **Search existing issues**: Someone might have faced the same problem
3. **Ask in discussions**: Use GitHub Discussions for questions
4. **Contact maintainers**: aadish.bahati@echostor.com

## 📚 Additional Resources

- **[Architecture Guide](docs/ARCHITECTURE.md)**: System design and structure
- **[API Documentation](docs/API.md)**: Complete API reference
- **[Testing Guide](TESTING.md)**: Testing strategy and best practices
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Production deployment
- **[Troubleshooting](docs/TROUBLESHOOTING.md)**: Common issues and solutions

---

Thank you for contributing to the EchoStor Security Posture Assessment Tool! 🎉
