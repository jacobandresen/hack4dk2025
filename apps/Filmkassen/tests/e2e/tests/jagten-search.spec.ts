import { test, expect } from '@playwright/test';

test.describe('Jagten Search Test', () => {
  test('should search for Jagten and show at least 1 result with poster', async ({ page }) => {
    // Navigate to home page
    await page.goto('/');
    
    // Wait for the page to load
    await expect(page.locator('h2')).toContainText('Søg efter film');
    
    // Fill in search form
    await page.fill('input[placeholder="Indtast filmtitel..."]', 'Jagten');
    
    // Click search button
    await page.click('button[type="submit"]');
    
    // Wait for search results
    await expect(page.locator('.search-results h3')).toContainText('Søgeresultater');
    
    // Check that we have at least 1 result
    const movieCards = page.locator('.movie-card');
    await expect(movieCards).toHaveCountGreaterThan(0);
    
    // Check that at least one result has a poster or placeholder
    const firstMovieCard = movieCards.first();
    const poster = firstMovieCard.locator('.movie-poster, .movie-poster-placeholder');
    await expect(poster).toBeVisible();
    
    // Check that the movie title contains "Jagten" (case insensitive)
    const movieTitle = firstMovieCard.locator('.movie-title');
    await expect(movieTitle).toContainText(/jagten/i);
    
    // Check that year is displayed
    const movieYear = firstMovieCard.locator('.movie-year');
    await expect(movieYear).toBeVisible();
    
    // Check that director is displayed
    const movieDirector = firstMovieCard.locator('.movie-director');
    await expect(movieDirector).toBeVisible();
  });

  test('should navigate to movie details when clicking on search result', async ({ page }) => {
    // Navigate to home page
    await page.goto('/');
    
    // Search for Jagten
    await page.fill('input[placeholder="Indtast filmtitel..."]', 'Jagten');
    await page.click('button[type="submit"]');
    
    // Wait for search results
    await expect(page.locator('.search-results h3')).toContainText('Søgeresultater');
    
    // Click on first movie result
    const firstMovieCard = page.locator('.movie-card').first();
    await firstMovieCard.click();
    
    // Wait for navigation to movie detail page
    await expect(page).toHaveURL(/\/movie\/\d+/);
    
    // Check that movie details are displayed
    await expect(page.locator('.movie-title')).toContainText(/jagten/i);
    await expect(page.locator('.movie-year')).toBeVisible();
    await expect(page.locator('.movie-director')).toBeVisible();
  });
});
