import { test, expect } from '@playwright/test';

test.describe('Artwork Search', () => {
  test('should search for "Amager" and show results with images', async ({ page }) => {
    await page.goto('/');
    
    // Wait for the page to load
    await expect(page.locator('h1')).toContainText('Søg efter kunstværker');
    
    // Search for "Amager"
    await page.fill('input[placeholder*="Søg efter kunstværker"]', 'Amager');
    await page.click('button[type="submit"]');
    
    // Wait for search results
    await expect(page.locator('h2')).toContainText('Søgeresultater for "Amager"');
    
    // Check that we have at least one result
    const artworkCards = page.locator('[class*="artwork-card"]');
    await expect(artworkCards.first()).toBeVisible();
    
    // Check that at least one result has an image (not "Intet billede")
    const images = page.locator('[class*="artwork-card"] img');
    await expect(images.first()).toBeVisible();
    
    // Verify that no results show "Intet billede" text
    const noImageTexts = page.locator('text=Intet billede');
    await expect(noImageTexts).toHaveCount(0);
  });

  test('should show artwork details when clicking on a result', async ({ page }) => {
    await page.goto('/');
    
    // Search for "Amager"
    await page.fill('input[placeholder*="Søg efter kunstværker"]', 'Amager');
    await page.click('button[type="submit"]');
    
    // Wait for results and click on the first one
    await expect(page.locator('[class*="artwork-card"]').first()).toBeVisible();
    await page.click('[class*="artwork-card"]:first-child');
    
    // Check that we're on the artwork detail page
    await expect(page).toHaveURL(/\/artwork\//);
    await expect(page.locator('h1')).toBeVisible();
    
    // Check that the artwork has an image
    const artworkImage = page.locator('img').first();
    await expect(artworkImage).toBeVisible();
    
    // Check that we can see artwork details
    await expect(page.locator('text=Inventarnummer:')).toBeVisible();
    await expect(page.locator('text=Type:')).toBeVisible();
  });
});
