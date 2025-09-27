import { test, expect } from '@playwright/test'

test('should load homepage without blank page', async ({ page }) => {
  // Go to homepage
  await page.goto('/')
  
  // Wait for page to load
  await page.waitForLoadState('networkidle')
  
  // Check that the page has content
  await expect(page.locator('h1')).toContainText('Søg efter kunstværker')
  await expect(page.locator('nav')).toBeVisible()
  await expect(page.locator('input[placeholder*="Søg efter kunstværker"]')).toBeVisible()
  
  // Check that there are no JavaScript errors
  const errors = []
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text())
    }
  })
  
  // Wait a bit to catch any errors
  await page.waitForTimeout(2000)
  
  // Should have no errors
  expect(errors).toHaveLength(0)
})

