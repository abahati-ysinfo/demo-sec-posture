import { test as base, Page } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
  adminPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    const timestamp = Date.now();
    const email = `test-user-${timestamp}@example.com`;
    const password = 'TestPassword123!';

    await page.goto('/auth/register');
    await page.fill('input[placeholder*="full name"]', 'Test User');
    await page.fill('input[type="email"]', email);
    await page.fill('input[placeholder*="company"]', 'Test Company');
    await page.fill('input[placeholder*="Enter your password"]', password);
    await page.fill('input[placeholder*="Confirm"]', password);
    await page.click('button[type="submit"]');

    await page.waitForURL((url) => url.pathname.replace(/\/$/, '') === '/dashboard', {
      timeout: 10000,
    });

    const token = await page.evaluate(() => (window as { __getAuthToken?: () => string | null }).__getAuthToken?.());
    if (token) {
      await page.addInitScript((t) => {
        (window as { __AUTH_TOKEN?: string }).__AUTH_TOKEN = t;
      }, token);
    }

    await use(page);
  },

  adminPage: async ({ page }, use) => {
    const adminEmail = 'admin@echostor.com';
    const adminPassword = 'admin_test_password_123';

    await page.goto('/auth/login');
    await page.fill('input[type="email"]', adminEmail);
    await page.fill('input[type="password"]', adminPassword);
    await page.click('button[type="submit"]');

    await page.waitForURL((url) => url.pathname.replace(/\/$/, '') === '/admin', {
      timeout: 10000,
    });

    const token = await page.evaluate(() => (window as { __getAuthToken?: () => string | null }).__getAuthToken?.());
    if (token) {
      await page.addInitScript((t) => {
        (window as { __AUTH_TOKEN?: string }).__AUTH_TOKEN = t;
      }, token);
    }

    await use(page);
  },
});

export { expect } from '@playwright/test';
