import { test, expect } from '@playwright/test';

test.describe('Danske Film Collection Test', () => {
  test('should create user, create collection, search for Jagten and add to collection', async ({ page }) => {
    // Step 1: Register a new user
    await page.goto('/register');
    
    // Fill registration form
    await page.fill('input[placeholder="Indtast brugernavn..."]', 'testuser' + Date.now());
    await page.fill('input[placeholder="Indtast e-mail..."]', 'test' + Date.now() + '@example.com');
    await page.fill('input[placeholder="Indtast adgangskode..."]', 'password123');
    await page.fill('input[placeholder="Bekræft adgangskode..."]', 'password123');
    
    // Submit registration
    await page.click('button[type="submit"]');
    
    // Should redirect to login page
    await expect(page).toHaveURL('/login');
    
    // Step 2: Login
    await page.fill('input[placeholder="Indtast brugernavn..."]', 'testuser' + Date.now());
    await page.fill('input[placeholder="Indtast adgangskode..."]', 'password123');
    await page.click('button[type="submit"]');
    
    // Should redirect to home page
    await expect(page).toHaveURL('/');
    
    // Step 3: Create a collection
    await page.goto('/collections');
    
    // Click create collection button
    await page.click('button:has-text("Opret ny filmkasse")');
    
    // Fill collection form
    await page.fill('input[placeholder="Indtast navn på filmkasse..."]', 'Danske film');
    await page.fill('textarea[placeholder="Beskriv filmkassen..."]', 'Mine yndlings danske film');
    
    // Submit collection
    await page.click('button:has-text("Opret filmkasse")');
    
    // Should see the collection in the list
    await expect(page.locator('.collection-card')).toContainText('Danske film');
    
    // Step 4: Search for Jagten
    await page.goto('/');
    
    // Search for Jagten
    await page.fill('input[placeholder="Indtast filmtitel..."]', 'Jagten');
    await page.click('button[type="submit"]');
    
    // Wait for search results
    await expect(page.locator('.search-results h3')).toContainText('Søgeresultater');
    
    // Click on first movie result
    const firstMovieCard = page.locator('.movie-card').first();
    await firstMovieCard.click();
    
    // Wait for movie detail page
    await expect(page).toHaveURL(/\/movie\/\d+/);
    
    // Step 5: Add movie to collection
    // Select the collection from dropdown
    await page.selectOption('select', 'Danske film');
    
    // Click add button
    await page.click('button:has-text("Tilføj")');
    
    // Should show success message or redirect
    await expect(page.locator('.success, .btn:has-text("Tilføjet")')).toBeVisible();
    
    // Step 6: Verify movie is in collection
    await page.goto('/collections');
    
    // Click on the collection to expand it
    await page.click('.collection-header:has-text("Danske film")');
    
    // Should see the movie in the collection
    await expect(page.locator('.collection-movies')).toContainText('Jagten');
  });

  test('should show collection as accordion with DVD-like appearance', async ({ page }) => {
    // This test verifies the accordion functionality and visual design
    await page.goto('/collections');
    
    // Create a test collection if none exist
    if (await page.locator('.no-collections').isVisible()) {
      await page.click('button:has-text("Opret din første filmkasse")');
      await page.fill('input[placeholder="Indtast navn på filmkasse..."]', 'Test Collection');
      await page.click('button:has-text("Opret filmkasse")');
    }
    
    // Check that collection looks like an accordion
    const collectionCard = page.locator('.collection-card').first();
    await expect(collectionCard).toBeVisible();
    
    // Check that it has a header with toggle icon
    const collectionHeader = collectionCard.locator('.collection-header');
    await expect(collectionHeader).toBeVisible();
    await expect(collectionHeader.locator('.toggle-icon')).toBeVisible();
    
    // Click to expand
    await collectionHeader.click();
    
    // Check that content is visible
    await expect(collectionCard.locator('.collection-content')).toBeVisible();
  });
});
