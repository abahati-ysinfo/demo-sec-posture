# E2E Tests

End-to-end tests for the EchoStor Security Posture Assessment Tool using Playwright.

## Running Tests

### Local Development

```bash
# Start backend services
docker-compose up -d

# Run all E2E tests
cd frontend
pnpm run test:e2e

# Run tests in UI mode
pnpm run test:e2e:ui

# Run tests in debug mode
pnpm run test:e2e:debug

# Run specific test file
pnpm run test:e2e e2e/auth/login.spec.ts
```

### CI Environment

Tests automatically run on pull requests via GitHub Actions.

## Test Structure

- `auth/` - Authentication tests (login, register)
- `assessment/` - Assessment flow tests
- `reports/` - Report generation and download tests
- `admin/` - Admin user management tests
- `fixtures/` - Test fixtures and helpers
- `utils/` - Shared utilities

## Configuration

See `playwright.config.ts` for test configuration including:

- Browsers: Chromium, Firefox, WebKit
- Base URL
- Retries and timeouts
- Screenshots and traces

## Environment Variables

- `PLAYWRIGHT_BASE_URL` - Base URL for tests (default: http://localhost:3000)
- `ADMIN_EMAIL` - Admin email for admin tests
- `ADMIN_PASSWORD` - Admin password for admin tests
