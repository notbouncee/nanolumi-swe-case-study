import { test, expect } from '@playwright/test';

test.describe('Operator User Flow', () => {
  test('should load map, open device modal, and request measurement', async ({ page }) => {
    // 1. Navigate to the frontend
    await page.goto('/');

    // 2. Wait for the map to load and markers to appear
    // The Leaflet map contains images with the class 'leaflet-marker-icon'
    await page.waitForSelector('.leaflet-marker-icon', { timeout: 10000 });

    // 3. Find and click on a device marker (using the first one available)
    const marker = page.locator('.leaflet-marker-icon').first();
    await marker.click();

    // 4. Verify the modal opens and displays device info
    const modalTitle = page.locator('[role="dialog"] h2'); // DialogTitle renders as h2
    await expect(modalTitle).toBeVisible();
    await expect(modalTitle).not.toBeEmpty();

    // 5. Find the button in the modal
    const modal = page.locator('[role="dialog"]');
    const requestButton = modal.getByRole('button').filter({ hasText: /Measurement/i }).first();
    await expect(requestButton).toBeVisible();
    
    // We only click if it says "Request Measurement" and is not disabled
    const buttonText = await requestButton.textContent();
    if (buttonText && buttonText.includes('Request Measurement') && await requestButton.isEnabled()) {
      await requestButton.click();
      
      // 6. Verify the button changes to the disabled/loading state
      await expect(modal.getByRole('button', { name: /Measurement in Progress/i })).toBeVisible();
    }

    // 7. Wait for the measurement to complete (simulator delay is up to 5s, so we wait up to 15s)
    // We look for a badge that says COMPLETED, FAILED, DELAYED, or INCOMPLETE.
    const statusBadge = page.locator('.bg-green-500, .bg-red-500, .bg-yellow-500, .bg-gray-400').first();
    await expect(statusBadge).toBeVisible({ timeout: 15000 });
    
    // Check that we got some data
    const phText = page.locator('text=pH').locator('..').locator('p.font-medium').first();
    await expect(phText).toBeVisible();
  });
});
