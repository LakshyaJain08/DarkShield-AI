from playwright.sync_api import sync_playwright
import time

BOT_CHALLENGE_KEYWORDS = [
    "validatecaptcha",
    "robot check",
    "make sure you're not a robot",
    "type the characters you see",
    "enter the characters you see below",
    "please verify you are a human",
    "cf-browser-verification",
    "attention required! | cloudflare",
    "click the button below to continue shopping",
    "sorry, we just need to make sure you're not a robot"
]

def _is_bot_challenge(url: str, text: str) -> bool:
    url_lower = url.lower()
    text_lower = text[:800].lower()
    if "continue shopping" in text_lower and len(text.strip()) < 800:
        return True
    for kw in BOT_CHALLENGE_KEYWORDS:
        if kw in url_lower or kw in text_lower:
            return True
    return False

def _fetch_dom(p, url: str, browser_type: str = "chromium"):
    if browser_type == "firefox":
        browser = p.firefox.launch(headless=True)
    else:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="en-US"
    )
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=35000)
    
    # Wait briefly for dynamic elements/badges to hydrate
    page.wait_for_timeout(1500)
    
    # Extract rich DOM text and discrete candidate UI snippets where deceptive cues live
    dom_data = page.evaluate("""() => {
        const selectors = [
            'button', '[class*="alert"]', '[class*="badge"]', '[class*="timer"]',
            '[class*="popup"]', '[class*="banner"]', '[class*="modal"]',
            '[class*="deal"]', '[class*="price"]', '[class*="scarcity"]',
            '[class*="urgency"]', '[id*="deal"]', '[id*="price"]', '[id*="timer"]',
            '[class*="coupon"]', '[id*="coupon"]', '[class*="offer"]',
            '[class*="saving"]', '[class*="discount"]', '[id*="saving"]', '[id*="discount"]',
            'h1', 'h2', 'h3', 'p', 'span', 'a'
        ];
        const elements = document.querySelectorAll(selectors.join(', '));
        const rawSnippets = [];
        const allParts = [];
        for (const el of elements) {
            if (['SCRIPT', 'STYLE', 'SVG', 'NOSCRIPT', 'IFRAME'].includes(el.tagName)) continue;
            const val = (el.innerText || '').trim();
            if (val && val.length >= 4 && val.length <= 260 && !val.includes('\\n\\n')) {
                rawSnippets.push(val);
            }
            if (val && val.length > 3 && val.length < 500) {
                allParts.push(val);
            }
        }
        
        // Deduplicate snippets
        const uniqueSnippets = [];
        const seen = new Set();
        for (const s of rawSnippets) {
            const clean = s.replace(/\\s+/g, ' ').trim();
            if (!seen.has(clean.toLowerCase()) && clean.length >= 4) {
                seen.add(clean.toLowerCase());
                uniqueSnippets.push(clean);
            }
        }
        
        return {
            snippets: uniqueSnippets,
            text: allParts.length > 0 ? allParts.join(' ') : (document.body.innerText || '')
        };
    }""")
    
    screenshot_bytes = page.screenshot(full_page=False)
    final_url = page.url
    browser.close()
    return dom_data["text"], dom_data["snippets"], screenshot_bytes, final_url

def scrape_page(url: str):
    with sync_playwright() as p:
        try:
            text, snippets, screenshot_bytes, final_url = _fetch_dom(p, url, browser_type="chromium")
        except Exception:
            text, snippets, screenshot_bytes, final_url = _fetch_dom(p, url, browser_type="firefox")
        
        # If blocked on first attempt, retry once with alternate clean firefox context
        if _is_bot_challenge(final_url, text):
            time.sleep(1)
            text, snippets, screenshot_bytes, final_url = _fetch_dom(p, url, browser_type="firefox")
            
        if _is_bot_challenge(final_url, text):
            raise RuntimeError(
                "Amazon Anti-Bot Firewall (CAPTCHA) intercepted the request. "
                "The automated scraper received Amazon's 'Robot Check' challenge instead of product DOM."
            )
            
        return text, snippets, screenshot_bytes

