# Security Posture Assessment Tool

A comprehensive security posture assessment platform that helps organizations evaluate their cybersecurity maturity across 19 key domains with 409 detailed questions. Built with modern web technologies and designed for scalability, reliability, and user experience.

## 🚀 Features

### Core Functionality
- **Comprehensive Assessment**: 409 carefully crafted questions across 19 security domains
- **Progressive Assessment Flow**: Intuitive step-by-step assessment with section navigation
- **Auto-Save Functionality**: Automatic progress saving every 10 minutes to prevent data loss
- **15-Day Assessment Period**: Flexible completion timeframe for thorough evaluation
- **Consultation Integration**: Built-in consultation request system for expert guidance

### Reporting & Analytics
- **PDF Report Generation**: Professional, branded security posture reports
- **AI-Enhanced Reports**: ChatGPT-powered intelligent analysis and personalized recommendations
- **Multi-Format Reports**: Standard and AI-enhanced report options
- **Report Management**: Complete report lifecycle management and download system

### Administration & Management
- **Comprehensive Admin Dashboard**: Complete visibility into user assessments and system metrics
- **User Management**: Admin tools for user oversight and support
- **Assessment Monitoring**: Real-time tracking of assessment progress and completion rates
- **Audit Logging**: Complete audit trail of admin actions and system events

### Technical Excellence
- **Error Boundaries**: React Error Boundaries for graceful error handling and user experience
- **API Retry Logic**: Intelligent retry mechanisms with exponential backoff for network resilience
- **Multi-Region Support**: Optimized for US users with Australia admin access
- **Real-time Updates**: Live progress tracking and status updates
- **Mobile Responsive**: Fully responsive design for all device types

## 🏗️ Architecture

- **Frontend**: Next.js 14 with React 18, TypeScript, and Tailwind CSS
- **Backend**: FastAPI with Python 3.12, SQLAlchemy ORM
- **Database**: PostgreSQL with Alembic migrations
- **Authentication**: JWT-based secure authentication with bcrypt password hashing
- **AI Integration**: OpenAI GPT integration for intelligent report generation
- **Deployment**: Multi-region deployment on Fly.io (backend) and Vercel (frontend)
- **Monitoring**: Health checks, liveness probes, and comprehensive logging

For detailed architecture information, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **UI Library**: React 18 with React Query for state management
- **Styling**: Tailwind CSS with Headless UI components
- **Forms**: React Hook Form with validation
- **Charts**: Recharts for data visualization
- **Error Handling**: React Error Boundary
- **HTTP Client**: Axios with retry logic

### Backend
- **Framework**: FastAPI with async support
- **Language**: Python 3.12
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Authentication**: JWT with passlib/bcrypt
- **API Documentation**: OpenAPI/Swagger (auto-generated)
- **Rate Limiting**: Built-in middleware
- **Background Tasks**: FastAPI BackgroundTasks

### DevOps & Tools
- **Package Managers**: Poetry (Python), pnpm (Node.js)
- **Code Quality**: Ruff (Python), ESLint + Prettier (TypeScript)
- **Type Checking**: mypy (Python), TypeScript compiler
- **Testing**: pytest + coverage (Python), Jest + React Testing Library (JavaScript)
- **CI/CD**: GitHub Actions
- **Deployment**: Fly.io + Vercel

## 📋 Quick Start

### Option 1: Docker Compose (Recommended for Development)
```bash
git clone https://github.com/abahati-ysinfo/demo-sec-posture.git
cd demo-sec-posture
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup
```bash
# Run automated setup script
./scripts/setup.sh

# Or follow manual steps:
# 1. Backend setup
cd backend
poetry install
cp .env.example .env  # Edit with your configuration
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload

# 2. Frontend setup (in new terminal)
cd frontend
pnpm install
pnpm run dev
```

### Prerequisites
- **Node.js**: 18.x or higher
- **Python**: 3.12 or higher
- **PostgreSQL**: 15 or higher
- **Docker**: Optional, for containerized development

For detailed setup instructions, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📚 Documentation

- **[API Reference](docs/API.md)** - Complete API endpoint documentation with examples
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design, database schema, and diagrams
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions
- **[Contributing Guidelines](CONTRIBUTING.md)** - Development workflow and standards
- **[Testing Guide](TESTING.md)** - Testing strategy and running tests
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### API Documentation
The backend provides auto-generated interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Security Features

- **Authentication**: JWT-based authentication with secure token management
- **Password Security**: bcrypt hashing with salt
- **Rate Limiting**: API endpoint protection against abuse
- **CORS Protection**: Configured for cross-origin request security
- **Input Validation**: Comprehensive input sanitization and validation
- **Audit Logging**: Complete audit trail of admin actions
- **Error Handling**: Secure error responses without information leakage

## 🚀 Deployment

### Production Environments
- **Frontend**: Vercel (automatic deployment from `main` branch)
- **Backend**: Fly.io multi-region deployment (IAD, LAX, SYD)
- **Database**: PostgreSQL on Fly.io with automatic backups

### CI/CD Pipeline
- **Backend**: Lint (Ruff), format check, type check (mypy), tests (pytest)
- **Frontend**: Lint (ESLint), format check (Prettier), type check, build verification
- **Deployment**: Automatic deployment on merge to `main` branch

For detailed deployment instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## 📊 Project Structure

```
demo-sec-posture/
├── frontend/                   # Next.js frontend application
│   ├── src/
│   │   ├── pages/             # Next.js pages and API routes
│   │   ├── components/        # Reusable React components
│   │   ├── lib/              # Utilities and API client
│   │   └── styles/           # Global styles and Tailwind config
│   ├── tests/                # Frontend test files
│   └── package.json          # Node.js dependencies and scripts
├── backend/                   # FastAPI backend application
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   ├── models/           # SQLAlchemy database models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # Business logic services
│   │   └── core/             # Configuration and database setup
│   ├── tests/                # Backend test files
│   ├── migrations/           # Alembic database migrations
│   └── pyproject.toml        # Python dependencies and configuration
├── docs/                     # Comprehensive documentation
├── scripts/                  # Deployment and utility scripts
├── .github/workflows/        # GitHub Actions CI/CD workflows
├── docker-compose.yml        # Local development environment
└── README.md                # This file
```

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for information about:
- Development setup and workflow
- Code style and standards
- Testing requirements
- Pull request process
- Branch naming conventions

## 📄 License

Proprietary. All rights reserved.

## 📞 Support

For questions, issues, or support:
- **GitHub Issues**: For bug reports and feature requests

