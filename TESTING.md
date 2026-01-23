# Testing Guide

## Overview

This document describes the testing strategy and infrastructure for the EchoStor Security Posture Assessment Tool. The project uses pytest for backend testing, Jest with React Testing Library for frontend unit testing, and Playwright for end-to-end testing.

## End-to-End Testing

### Overview

E2E tests use Playwright to test the complete user flows across frontend and backend.

### Running E2E Tests

```bash
# Start backend services
docker-compose up -d

# Run E2E tests
cd frontend
pnpm run test:e2e

# Run in UI mode
pnpm run test:e2e:ui

# Run in debug mode
pnpm run test:e2e:debug
```

### Test Coverage

- User registration flow
- Login and authentication
- Complete assessment flow with auto-save
- Report generation and download
- Admin user management (CRUD operations)

### CI Integration

E2E tests run automatically on pull requests via GitHub Actions (`.github/workflows/frontend-ci.yml`).

### Writing Tests

See `frontend/e2e/README.md` for test structure and guidelines.

## Backend Testing

### Running Tests

```bash
cd backend
poetry install  # Install dependencies including test tools
poetry run pytest  # Run all tests
```

### Running Tests with Coverage

```bash
poetry run pytest --cov=app --cov-report=term-missing --cov-report=html
```

View the HTML coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Test Structure

```
backend/tests/
├── conftest.py                    # Shared fixtures and test configuration
├── test_auth.py                   # Authentication endpoint tests
├── test_assessment_endpoints.py   # Assessment API tests
├── test_reports_endpoints.py      # Reports API tests
├── test_admin_endpoints.py        # Admin API tests
├── test_question_parser.py        # Question parser service tests
├── test_report_generator.py       # Report generator service tests
└── test_integration.py            # End-to-end integration tests
```

### Test Database

Tests use SQLite with an in-memory database that is created fresh for each test function. This ensures test isolation and prevents test pollution.

### Available Fixtures

The following fixtures are available from `conftest.py`:

- **`client`**: FastAPI test client with database override
- **`db_session`**: Fresh database session for each test
- **`test_user`**: Regular user fixture (email: test@example.com)
- **`test_admin_user`**: Admin user fixture (email: admin@example.com)
- **`auth_token`**: JWT token for regular user authentication
- **`admin_token`**: JWT token for admin user authentication
- **`test_assessment`**: In-progress assessment fixture
- **`completed_assessment`**: Completed assessment fixture
- **`test_assessment_response`**: Sample assessment response
- **`test_report`**: Sample report fixture

### Writing New Backend Tests

1. **Use appropriate fixtures**: Import fixtures from conftest.py
2. **Follow naming conventions**: `test_<functionality>_<scenario>`
3. **Test both success and failure cases**: Don't just test the happy path
4. **Mock external services**: Use `pytest-mock` or `unittest.mock` for OpenAI, file I/O
5. **Keep tests independent**: Each test should be able to run in isolation

Example:
```python
def test_login_valid_credentials(client, test_user):
    response = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Coverage Requirements

The backend has a minimum coverage threshold of **80%** enforced by pytest configuration in `pyproject.toml`. Tests will fail if coverage drops below this threshold.

## Frontend Testing

### Running Tests

```bash
cd frontend
npm install  # or pnpm install
npm test     # Run all tests
```

### Running Tests with Coverage

```bash
npm run test:coverage
```

### Running Tests in Watch Mode

```bash
npm run test:watch
```

### Test Structure

```
frontend/
├── tests/
│   └── pages/
│       ├── auth/
│       │   ├── login.test.tsx
│       │   └── register.test.tsx
│       └── dashboard.test.tsx
└── src/
    ├── pages/
    │   ├── auth/
    │   │   ├── login.tsx
    │   │   └── register.tsx
    │   └── dashboard.tsx
    └── components/
        └── __tests__/
            └── (component tests)
```

**Important Note on Test File Location:**

Test files for pages are located in the `frontend/tests/pages/` directory, **not** inside `frontend/src/pages/`. This is because Next.js treats all files in the `pages/` directory as routes, which would cause build failures with test files.

Component tests can use the `__tests__/` directory pattern alongside the components since they're not in the `pages/` directory.

### Writing New Frontend Tests

1. **Use React Testing Library**: Focus on user interactions, not implementation details
2. **Mock API calls**: Use Jest mocks for API responses
3. **Mock Next.js router**: Use `next-router-mock` for router functionality
4. **Follow accessibility best practices**: Use `getByRole`, `getByLabelText`, etc.
5. **Test user flows**: Simulate what users actually do

Example:
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import Login from '../login'

describe('Login Page', () => {
  it('renders login form', () => {
    render(<Login />)
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
  })
})
```

### Coverage Requirements

The frontend currently has a **foundational test suite** with minimal coverage thresholds configured in `jest.config.js` (current: ~10% lines, ~8% branches, ~9% statements, ~3% functions).

**Current State**: The test infrastructure is fully set up with Jest and React Testing Library. Basic tests exist for:
- Authentication pages (login, register)
- Dashboard page

**⚠️ Future Work Required**: This represents phase 1 of frontend testing. To match backend standards (80%+), the following work is needed:
- **Assessment Flow**: Test question navigation, answer selection, progress saving, consultation questions
- **Admin Pages**: Test user management, assessment monitoring, report generation, consultation requests
- **Reports Page**: Test report listing, downloading, status checking
- **API Client**: Unit tests for all API functions
- **User Interactions**: Form submissions, validation, error handling, navigation flows
- **Loading & Error States**: Test loading indicators, error boundaries, retry logic
- **Integration Tests**: Complete user workflows end-to-end

**Target**: Expand coverage to 70%+ to match backend testing standards.

## Integration Tests

Integration tests verify complete user flows across multiple components and API endpoints. They are located in `backend/tests/test_integration.py`.

### Example Flows Tested

1. **Complete User Registration and Assessment Flow**:
   - Register new user
   - Login
   - Start assessment
   - Save progress
   - Complete assessment
   - Generate report

2. **Admin Workflow**:
   - View users
   - View assessments
   - View dashboard statistics
   - Generate AI reports

### Running Integration Tests

```bash
cd backend
poetry run pytest tests/test_integration.py -v
```

## Mocking External Services

### Backend

**OpenAI API**: Mocked using `unittest.mock.patch`:
```python
@patch("app.services.report_generator.openai")
async def test_generate_ai_insights(mock_openai):
    mock_openai.ChatCompletion.create = AsyncMock(return_value={
        "choices": [{"message": {"content": "Test AI insights"}}]
    })
    # Test code here
```

**File I/O**: Mocked for PDF generation:
```python
@patch("app.services.report_generator.HTML")
async def test_generate_report(mock_html):
    mock_html.return_value.write_pdf = MagicMock()
    # Test code here
```

### Frontend

**API Calls**: Mocked using Jest:
```typescript
jest.mock('@/lib/api', () => ({
  assessmentAPI: {
    getCurrentAssessment: jest.fn().mockResolvedValue({ data: null }),
  },
}))
```

**Next.js Router**: Mocked using `next-router-mock`:
```typescript
jest.mock('next/router', () => require('next-router-mock'))
```

## CI/CD Integration

Tests run automatically on every pull request via GitHub Actions. Both backend and frontend tests must pass before merging.

### GitHub Actions Workflow

The CI pipeline:
1. Checks out code
2. Sets up Python 3.12 and Node.js
3. Installs dependencies
4. Runs backend tests with coverage
5. Runs frontend tests with coverage
6. Fails if coverage is below thresholds
7. Uploads coverage reports as artifacts

## Troubleshooting

### Common Issues

**Backend tests fail with database errors**:
- Ensure you're running tests with `poetry run pytest` (not just `pytest`)
- Check that `DATABASE_URL` is set in conftest.py

**Frontend tests fail with module not found**:
- Run `npm install` to ensure all dependencies are installed
- Check that Jest configuration in `jest.config.js` is correct

**Coverage is below threshold**:
- Identify untested code: `poetry run pytest --cov=app --cov-report=html`
- Add tests for uncovered code paths
- Don't modify coverage thresholds to artificially pass

**Tests are slow**:
- Backend: Use function-scoped fixtures instead of session-scoped
- Frontend: Mock API calls instead of making real requests
- Run specific test files: `pytest tests/test_auth.py`

## Best Practices

1. **Write tests first** (TDD): Define expected behavior before implementation
2. **Keep tests simple**: One assertion per test when possible
3. **Use descriptive test names**: `test_login_fails_with_invalid_password`
4. **Don't test framework code**: Focus on your application logic
5. **Mock external dependencies**: Keep tests fast and deterministic
6. **Maintain test isolation**: Tests should not depend on each other
7. **Keep coverage high**: Aim for 80%+ backend, 70%+ frontend
8. **Review test failures**: Don't ignore failing tests or disable them

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [React Testing Library](https://testing-library.com/react)
- [Jest documentation](https://jestjs.io/docs/getting-started)
- [Testing best practices](https://testingjavascript.com/)
