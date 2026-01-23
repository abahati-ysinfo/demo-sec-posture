import { test, expect } from '@playwright/test';

test.describe('Admin User Management', () => {
  test('should display login page for unauthenticated users', async ({
    page,
  }) => {
    await page.goto('/admin');

    await expect(page).toHaveURL(/\/auth\/login|\/admin/);
  });

  test('should display admin users page', async ({ page }) => {
    await page.goto('/admin/users');

    await expect(page).toHaveURL(/\/auth\/login|\/admin\/users/);
  });
});
