import { test, expect } from '@playwright/test';

test.describe('User Registration and Login', () => {
  test('should register a new user', async ({ page }) => {
    await page.goto('/register');
    
    // Fill registration form
    const username = `testuser_${Date.now()}`;
    const email = `test_${Date.now()}@example.com`;
    const password = 'testpassword123';
    
    await page.fill('input[type="text"]', username);
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.fill('input[placeholder*="Bekræft"]', password);
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should redirect to home page after successful registration
    await expect(page).toHaveURL('/');
    
    // Should show user is logged in
    await expect(page.locator(`text=Hej, ${username}`)).toBeVisible();
  });

  test('should login with existing user', async ({ page }) => {
    // First register a user
    await page.goto('/register');
    
    const username = `testuser_${Date.now()}`;
    const email = `test_${Date.now()}@example.com`;
    const password = 'testpassword123';
    
    await page.fill('input[type="text"]', username);
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.fill('input[placeholder*="Bekræft"]', password);
    await page.click('button[type="submit"]');
    
    // Logout
    await page.click('text=Log ud');
    
    // Login
    await page.goto('/login');
    await page.fill('input[type="text"]', username);
    await page.fill('input[type="password"]', password);
    await page.click('button[type="submit"]');
    
    // Should be logged in
    await expect(page).toHaveURL('/');
    await expect(page.locator(`text=Hej, ${username}`)).toBeVisible();
  });
});

