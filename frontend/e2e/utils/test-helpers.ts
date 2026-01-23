import { Page } from '@playwright/test';

export async function waitForToast(page: Page, message: string) {
  await page.waitForSelector(`text=${message}`, { timeout: 5000 });
}

export async function fillAssessmentQuestion(
  page: Page,
  questionType: 'radio' | 'checkbox' | 'text',
  value: string | string[]
) {
  if (questionType === 'radio') {
    await page.click(`input[type="radio"][value="${value}"]`);
  } else if (questionType === 'checkbox' && Array.isArray(value)) {
    for (const val of value) {
      await page.click(`input[type="checkbox"][value="${val}"]`);
    }
  } else if (questionType === 'text') {
    await page.fill('textarea', value as string);
  }
}

export function generateUniqueEmail(): string {
  return `test-${Date.now()}-${Math.random().toString(36).substring(7)}@example.com`;
}
