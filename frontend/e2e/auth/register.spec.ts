import { test, expect } from '@playwright/test';
import { generateUniqueEmail } from '../utils/test-helpers';

test.describe('User Registration', () => {
  test('should successfully register a new user', async ({ page }) => {
    await page.goto('/auth/register');

    const email = generateUniqueEmail();

    await page.fill('input[placeholder*="full name"]', 'John Doe');
    await page.fill('input[type="email"]', email);
    await page.fill('input[placeholder*="company"]', 'Acme Corp');
    await page.fill('input[placeholder*="Enter your password"]', 'SecurePass123!');
    await page.fill('input[placeholder*="Confirm"]', 'SecurePass123!');

    await page.click('button[type="submit"]');

    await page.waitForURL(/\/dashboard/, { timeout: 10000 });
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('should display registration form', async ({ page }) => {
    await page.goto('/auth/register');

    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[placeholder*="full name"]')).toBeVisible();
    await expect(page.locator('input[placeholder*="company"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });
});
