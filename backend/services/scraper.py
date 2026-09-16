from playwright.sync_api import sync_playwright

def scrape_page(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Navigate to the URL, wait until the DOM is loaded
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        # Extract text directly from the web page DOM
        # This captures headings, paragraphs, buttons, banners, alerts where dark patterns hide
        text = page.evaluate("""() => {
            const elements = document.querySelectorAll('p, h1, h2, h3, h4, span, a, button, [class*="alert"], [class*="badge"], [class*="timer"], [class*="popup"], [class*="banner"]');
            const parts = [];
            for (const el of elements) {
                const val = (el.innerText || '').trim();
                if (val && val.length > 3 && val.length < 500) {
                    parts.push(val);
                }
            }
            return parts.length > 0 ? parts.join(' ') : (document.body.innerText || '');
        }""")
        
        screenshot_bytes = page.screenshot(full_page=False)
        browser.close()
        return text, screenshot_bytes
