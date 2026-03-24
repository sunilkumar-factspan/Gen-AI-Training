from playwright.sync_api import sync_playwright

def run():
    browser = None
    page = None
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            page.goto("https://www.flipkart.com/", wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            try:
                page.locator("button:has-text('Accept'), button:has-text('Agree')").first.click(timeout=3000)
            except:
                pass
            page.locator("#container > div > div._36fx1h._6WQwDJ._3vin1D > div.Mi_tTq._1BjWcj > form > div > input").press_sequentially("laptops under 50000", delay=100)
            page.keyboard.press("Enter")
            page.wait_for_selector("#container > div > div._36fx1h._6WQwDJ._3vin1D > div._1YokD2._2GoDe3.col-12-12 > div._1AtVbE.col-12-12._3xX09h > div._13oc-S > div.recko-col > div > div > div > div._3wU53B")
            if page is not None:
                page.screenshot(path="output.png")
        except Exception as e:
            if page is not None:
                page.screenshot(path="error.png")
        finally:
            if browser is not None:
                browser.close()

run()