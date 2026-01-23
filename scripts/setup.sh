#!/bin/bash


set -e

echo "🚀 Setting up EchoStor Security Posture Assessment Tool..."

if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📦 Setting up backend..."
cd backend

if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install Poetry first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo "   Installing Python dependencies..."
poetry install

if [ ! -f ".env" ]; then
    echo "   Creating .env file from example..."
    cp .env.example .env
    echo "   ⚠️  Please edit backend/.env with your configuration"
fi

echo "   Running database migrations..."
if poetry run alembic upgrade head 2>/dev/null; then
    echo "   ✅ Database migrations completed"
else
    echo "   ⚠️  Database migrations failed - please check your database configuration"
fi

cd ..

echo "📦 Setting up frontend..."
cd frontend

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first"
    exit 1
fi

echo "   Installing Node.js dependencies..."
npm install

if [ ! -f ".env.local" ]; then
    echo "   Creating .env.local file..."
    cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=EchoStor Security Posture Assessment
EOF
    echo "   ✅ Created .env.local file"
fi

cd ..

echo "🔐 Generating admin password..."
ADMIN_PASSWORD=$(openssl rand -base64 12)
ADMIN_PASSWORD_HASH=$(python3 -c "
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
print(pwd_context.hash('$ADMIN_PASSWORD'))
" 2>/dev/null || echo "")

if [ -n "$ADMIN_PASSWORD_HASH" ]; then
    echo "   ✅ Admin password generated: $ADMIN_PASSWORD"
    echo "   📝 Add this to your backend/.env file:"
    echo "      ADMIN_PASSWORD_HASH=$ADMIN_PASSWORD_HASH"
else
    echo "   ⚠️  Could not generate admin password hash. Please install passlib:"
    echo "      pip install passlib[bcrypt]"
fi

echo ""
echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "   1. Configure your environment variables:"
echo "      - Edit backend/.env with your database URLs and API keys"
echo "      - Edit frontend/.env.local if needed"
echo ""
echo "   2. Start the development servers:"
echo "      Backend:  cd backend && poetry run uvicorn app.main:app --reload"
echo "      Frontend: cd frontend && npm run dev"
echo ""
echo "   3. Access the application:"
echo "      Frontend: http://localhost:3000"
echo "      Backend API: http://localhost:8000"
echo "      API Docs: http://localhost:8000/docs"
echo ""
echo "   4. Admin login:"
echo "      Email: aadish.bahati@echostor.com"
echo "      Password: $ADMIN_PASSWORD"
echo ""
echo "🎉 Happy coding!"
