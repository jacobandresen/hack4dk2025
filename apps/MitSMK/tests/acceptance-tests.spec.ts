import { test, expect } from '@playwright/test';

test.describe('Acceptance Tests - MitSMK Requirements', () => {
  test('should search for "Amager" and show at least 1 result with 1 image', async ({ page }) => {
    await page.goto('/');
    
    // Search for "Amager"
    await page.fill('input[placeholder*="Søg efter kunstværker"]', 'Amager');
    await page.click('button[type="submit"]');
    
    // Wait for search results
    await expect(page.locator('h2')).toContainText('Søgeresultater for "Amager"');
    
    // Check that we have at least 1 result
    const artworkCards = page.locator('[class*="artwork-card"]');
    await expect(artworkCards).toHaveCountGreaterThan(0);
    
    // Check that at least one result has an image (not "Intet billede")
    const images = page.locator('img[alt*="Kunstværk"]');
    await expect(images).toHaveCountGreaterThan(0);
    
    // Verify that no results show "Intet billede" text
    const noImageTexts = page.locator('text=Intet billede');
    await expect(noImageTexts).toHaveCount(0);
  });

  test('should create user and collection "Amagerkana"', async ({ page }) => {
    // Register a new user
    await page.goto('/register');
    
    const username = `testuser_${Date.now()}`;
    const email = `test_${Date.now()}@example.com`;
    const password = 'testpassword123';
    
    await page.fill('input[type="text"]', username);
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.fill('input[placeholder*="Bekræft"]', password);
    await page.click('button[type="submit"]');
    
    // Should be logged in
    await expect(page).toHaveURL('/');
    await expect(page.locator(`text=Hej, ${username}`)).toBeVisible();
    
    // Create collection "Amagerkana"
    await page.goto('/collections');
    await page.click('text=Opret ny samling');
    await page.fill('input[placeholder*="Indtast samlingens navn"]', 'Amagerkana');
    await page.click('button[type="submit"]');
    
    // Should see the collection
    await expect(page.locator('text=Amagerkana')).toBeVisible();
  });

  test('should search for "Amager", add first image to "Amagerkana" collection, and view details', async ({ page }) => {
    // First register and create collection
    await page.goto('/register');
    
    const username = `testuser_${Date.now()}`;
    const email = `test_${Date.now()}@example.com`;
    const password = 'testpassword123';
    
    await page.fill('input[type="text"]', username);
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.fill('input[placeholder*="Bekræft"]', password);
    await page.click('button[type="submit"]');
    
    // Create collection "Amagerkana"
    await page.goto('/collections');
    await page.click('text=Opret ny samling');
    await page.fill('input[placeholder*="Indtast samlingens navn"]', 'Amagerkana');
    await page.click('button[type="submit"]');
    
    // Search for "Amager"
    await page.goto('/');
    await page.fill('input[placeholder*="Søg efter kunstværker"]', 'Amager');
    await page.click('button[type="submit"]');
    
    // Wait for results and click on the first one
    await expect(page.locator('[class*="artwork-card"]')).toHaveCountGreaterThan(0);
    await page.click('[class*="artwork-card"]:first-child');
    
    // Verify we can see the image
    const artworkImage = page.locator('img[alt*="Kunstværk"]').first();
    await expect(artworkImage).toBeVisible();
    
    // Add to collection "Amagerkana"
    await page.selectOption('select', 'Amagerkana');
    await page.click('button:has-text("Tilføj til samling")');
    
    // Go to collection to verify
    await page.goto('/collections');
    await page.click('text=Amagerkana');
    
    // Should see the artwork in the collection with image
    await expect(page.locator('[class*="artwork-card"]')).toHaveCountGreaterThan(0);
    const collectionImage = page.locator('img[alt*="Kunstværk"]').first();
    await expect(collectionImage).toBeVisible();
    
    // Click on artwork to see details
    await page.click('[class*="artwork-card"]:first-child');
    
    // Should see artwork details with image
    await expect(page.locator('h1')).toBeVisible();
    const detailImage = page.locator('img[alt*="Kunstværk"]').first();
    await expect(detailImage).toBeVisible();
    
    // Should see artwork information
    await expect(page.locator('text=Kunstner:')).toBeVisible();
    await expect(page.locator('text=År:')).toBeVisible();
  });
});

