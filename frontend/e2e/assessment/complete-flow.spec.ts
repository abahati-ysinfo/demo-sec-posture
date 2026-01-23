import { test, expect } from '../fixtures/auth';

test.describe('Assessment Flow', () => {
  test('should display dashboard page', async ({ authenticatedPage }) => {
    await expect(authenticatedPage.locator('h1, h2')).toContainText([/Welcome|Dashboard/]);
  });

  test('should navigate to assessment questions page', async ({ authenticatedPage }) => {
    await authenticatedPage.goto('/assessment/questions');

    await expect(authenticatedPage).toHaveURL(/\/assessment\/questions/);

    const pageContent = await authenticatedPage.content();
    expect(pageContent.length).toBeGreaterThan(0);
  });
});
