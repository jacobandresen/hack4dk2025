import { test, expect } from '@playwright/test'

test.describe('Artwork KMS1', () => {
  test('should show "not found" for artwork kms1 with missing data', async ({ page }) => {
    // Go to artwork detail page for kms1
    await page.goto('/artwork/kms1')
    
    // Wait for page to load
    await page.waitForLoadState('networkidle')
    
    // Check that we're on the artwork detail page
    await expect(page).toHaveURL(/\/artwork\/kms1/)
    
    // Since this artwork has very limited data (title is null, artist is null),
    // our system treats it as "not found" and shows the appropriate message
    const notFoundMessage = page.locator('text=Kunstværk ikke fundet')
    await expect(notFoundMessage).toBeVisible()
    
    // Check that the "not found" message is properly displayed
    await expect(page.locator('h2')).toContainText('Kunstværk ikke fundet')
    await expect(page.locator('text=Det ønskede kunstværk kunne ikke findes.')).toBeVisible()
    
    // Check that there's a link back to search
    const backToSearchLink = page.locator('text=Tilbage til søgning')
    await expect(backToSearchLink).toBeVisible()
  })

  test('should verify that kms1 is not attributed to Cornelis Corneliszoon van Haarlem', async ({ page }) => {
    // Go to artwork detail page for kms1
    await page.goto('/artwork/kms1')
    
    // Wait for page to load
    await page.waitForLoadState('networkidle')
    
    // Check that we're on the artwork detail page
    await expect(page).toHaveURL(/\/artwork\/kms1/)
    
    // Since this artwork has no data, it shows "not found"
    // This means it's NOT attributed to Cornelis Corneliszoon van Haarlem
    const notFoundMessage = page.locator('text=Kunstværk ikke fundet')
    await expect(notFoundMessage).toBeVisible()
    
    // Verify that there's no mention of Cornelis Corneliszoon van Haarlem
    const cornelisMention = page.locator('text=Cornelis Corneliszoon van Haarlem')
    await expect(cornelisMention).not.toBeVisible()
    
    // Verify that there's no artist information displayed at all
    const artistSection = page.locator('text=Kunstner:')
    await expect(artistSection).not.toBeVisible()
    
    // This test confirms that kms1 is NOT attributed to Cornelis Corneliszoon van Haarlem
    // because the artwork has no data in the SMK API
  })

  test('should verify that artist names are now displayed correctly for other artworks', async ({ page }) => {
    // Go to homepage and search for Amager to test artist name display
    await page.goto('/')
    
    // Search for Amager
    await page.fill('input[placeholder*="Søg efter kunstværker"]', 'Amager')
    await page.click('button[type="submit"]')
    
    // Wait for search results
    await expect(page.locator('h2')).toContainText('Søgeresultater for "Amager"')
    
    // Check that we have results
    const artworkCards = page.locator('[class*="artwork-card"]')
    await expect(artworkCards.first()).toBeVisible()
    
    // Click on the first artwork to see details
    await page.click('[class*="artwork-card"]:first-child')
    
    // Check that we're on the artwork detail page
    await expect(page).toHaveURL(/\/artwork\//)
    
    // Now that we fixed the artist parsing, we should see artist information
    // The artist field should be visible (not hidden like before)
    const artistField = page.locator('text=Kunstner:')
    await expect(artistField).toBeVisible()
    
    // There should be an artist name displayed
    // We can see "Henneberg, H. C." in the page content, so let's check for it
    const artistName = page.locator('text=Henneberg, H. C.')
    await expect(artistName).toBeVisible()
  })
})
