const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function capture() {
  const outputDir = path.join(__dirname, '..', 'screenshots');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch({ 
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true 
  });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 2
  });

  const page = await context.newPage();
  console.log('Navigating to live deployment...');
  await page.goto('https://help-q-multi-tier-clinical-rag-tria.vercel.app/', { waitUntil: 'networkidle' });

  // 1. Capture Full Platform Dashboard in Dark Mode
  console.log('Capturing 01_HELP-Q_Full_Platform_Dashboard_4K.png...');
  await page.screenshot({ path: path.join(outputDir, '01_HELP-Q_Full_Platform_Dashboard_4K.png'), fullPage: false });

  // 2. Click Prompt Chip 2 (Skin Rash & Itching) to trigger live response & telemetry
  console.log('Triggering Prompt 2...');
  const prompt2 = page.locator('button.prompt-chip').nth(1);
  await prompt2.click();

  // Wait for response or response bubble
  await page.waitForTimeout(5000);
  console.log('Capturing 02_HELP-Q_Clinical_Triage_Prompt_Response_4K.png...');
  await page.screenshot({ path: path.join(outputDir, '02_HELP-Q_Clinical_Triage_Prompt_Response_4K.png') });

  // 3. Open Developer Verification Modal
  console.log('Opening Developer Verification Modal...');
  const devBtn = page.locator('button.dev-profile-btn');
  await devBtn.click();
  await page.waitForTimeout(1000);
  console.log('Capturing 03_HELP-Q_Developer_Verification_Modal_4K.png...');
  await page.screenshot({ path: path.join(outputDir, '03_HELP-Q_Developer_Verification_Modal_4K.png') });

  // Close modal
  const closeBtn = page.locator('.modal-backdrop button').first();
  await closeBtn.click();
  await page.waitForTimeout(500);

  // 4. Toggle Light Mode
  console.log('Toggling Light Theme...');
  const themeBtn = page.locator('button.theme-toggle-btn');
  await themeBtn.click();
  await page.waitForTimeout(1000);
  console.log('Capturing 04_HELP-Q_Clinical_Light_Mode_4K.png...');
  await page.screenshot({ path: path.join(outputDir, '04_HELP-Q_Clinical_Light_Mode_4K.png') });

  await browser.close();
  console.log('SUCCESS: All 4K Screenshots captured cleanly!');
}

capture().catch(err => {
  console.error('Capture Error:', err);
  process.exit(1);
});
