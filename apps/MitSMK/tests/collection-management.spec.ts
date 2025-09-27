import { test, expect } from '@playwright/test';

test.describe('Collection Management', () => {
  test.beforeEach(async ({ page }) => {
    // Register and login before each test
    await page.goto('/register');
    
    const username = `testuser_${Date.now()}`;
    const email = `test_${Date.now()}@example.com`;
    const password = 'testpassword123';
    
    await page.fill('input[type="text"]', username);
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.fill('input[placeholder*="Bekræft"]', password);
    await page.click('button[type="submit"]');
    
    // Wait for registration to complete and redirect
    await page.waitForURL('/');
    
    // Now login
    await page.goto('/login');
    await page.fill('input[type="text"]', username);
    await page.fill('input[type="password"]', password);
    await page.click('button[type="submit"]');
    
    // Wait for login to complete
    await page.waitForURL('/');
  });

  test('should create a new collection "Amagerkana"', async ({ page }) => {
    // Listen for console messages
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    
    await page.goto('/collections');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
    
    // Check if we're logged in
    const isLoggedIn = await page.locator('text=Log ud').isVisible();
    console.log('Is logged in:', isLoggedIn);
    
    // Click create collection button
    await page.click('text=Opret ny samling');
    
    // Fill collection form
    await page.fill('input[placeholder*="Indtast samlingens navn"]', 'Amagerkana');
    await page.fill('textarea[placeholder*="Beskriv din samling"]', 'Samling af Amager-relaterede kunstværker');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait a bit for the request to complete
    await page.waitForTimeout(2000);
    
    // Check what's actually on the page
    const pageContent = await page.textContent('body');
    console.log('Page content after form submission:', pageContent);
    
    // Should see the new collection
    await expect(page.locator('text=Amagerkana')).toBeVisible();
    await expect(page.locator('text=Samling af Amager-relaterede kunstværker')).toBeVisible();
  });

  test('should add artwork to collection and view details', async ({ page }) => {
    // First create a collection
    await page.goto('/collections');
    await page.click('text=Opret ny samling');
    await page.fill('input[placeholder*="Indtast samlingens navn"]', 'Amagerkana');
    await page.click('button[type="submit"]');
    
    // Search for "Amager" artwork
    await page.goto('/');
    await page.fill('input[placeholder*="Søg efter kunstværker"]', 'Amager');
    await page.click('button[type="submit"]');
    
    // Wait for results and click on the first one
    await expect(page.locator('[class*="artwork-card"]').first()).toBeVisible();
    await page.click('[class*="artwork-card"]:first-child');
    
    // Add to collection
    await page.selectOption('select', 'Amagerkana');
    await page.fill('textarea[placeholder*="Tilføj en note"]', 'Fantastisk maleri af Amager');
    await page.click('button:has-text("Tilføj til samling")');
    
    // Go to collection to verify
    await page.goto('/collections');
    await page.click('text=Amagerkana');
    
    // Should see the artwork in the collection
    await expect(page.locator('[class*="artwork-card"]')).toHaveCountGreaterThan(0);
    await expect(page.locator('text=Fantastisk maleri af Amager')).toBeVisible();
    
    // Click on artwork to see details
    await page.click('[class*="artwork-card"]:first-child');
    
    // Should see artwork details
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('img[alt*="Kunstværk"]')).toBeVisible();
  });

  test('should remove artwork from collection', async ({ page }) => {
    // First add an artwork to a collection (reuse previous test setup)
    await page.goto('/collections');
    await page.click('text=Opret ny samling');
    await page.fill('input[placeholder*="Indtast samlingens navn"]', 'Amagerkana');
    await page.click('button[type="submit"]');
    
    await page.goto('/');
    await page.fill('input[placeholder*="Søg efter kunstværker"]', 'Amager');
    await page.click('button[type="submit"]');
    await page.click('[class*="artwork-card"]:first-child');
    await page.selectOption('select', 'Amagerkana');
    await page.click('button:has-text("Tilføj til samling")');
    
    // Go to collection
    await page.goto('/collections');
    await page.click('text=Amagerkana');
    
    // Remove artwork
    await page.click('text=Fjern fra samling');
    
    // Confirm removal
    await page.click('text=Er du sikker');
    
    // Should not see the artwork anymore
    await expect(page.locator('[class*="artwork-card"]')).toHaveCount(0);
  });
});
