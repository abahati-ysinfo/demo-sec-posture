import { test, expect } from '@playwright/test';
import { test as authTest } from '../fixtures/auth';

test.describe('User Login', () => {
  authTest('should successfully login and redirect to dashboard', async ({
    authenticatedPage,
  }) => {
    await expect(authenticatedPage).toHaveURL(/\/assessment\/overview|\/dashboard/);
  });

  test('should display login form', async ({ page }) => {
    await page.goto('/auth/login');

    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });
});
