"""Capture the README's local MVP screenshots from an already served client/dist.

Requires Python Playwright, Pillow, and Chrome. Run `python -m http.server 4173 --directory dist`
from client/ before running this script. The signed-in session is mocked in the
browser; it never writes users, bookings, or payments to the real API.
"""

import base64
import json
from io import BytesIO
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image


BASE = "http://127.0.0.1:4173"
OUT = Path(__file__).parent
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"


def route_to(page, path):
    page.evaluate(
        """path => {
          history.pushState({}, '', path);
          dispatchEvent(new PopStateEvent('popstate'));
        }""",
        path,
    )
    page.wait_for_timeout(750)


def save(page, name, full_page=False):
    screenshot = page.screenshot(full_page=full_page, animations="disabled")
    Image.open(BytesIO(screenshot)).save(OUT / name, "WEBP", quality=92, method=6)
    print(name, page.url)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=CHROME, headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        device_scale_factor=2,
        reduced_motion="reduce",
    )
    page = context.new_page()
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(500)
    save(page, "01-home.webp")

    route_to(page, "/plans")
    page.locator("#onsite").scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.locator("#online").scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    save(page, "02-plans.webp", full_page=True)
    page.get_by_role("button", name="SELECT PLAN").first.click()
    page.wait_for_timeout(350)
    save(page, "03-order-summary.webp")

    route_to(page, "/login/user")
    save(page, "04-user-login.webp")

    route_to(page, "/skilltree")
    save(page, "08-skill-tree.webp")

    user = {"id": "readme-demo", "name": "Demo Trainee", "email": "demo@example.com", "role": "user"}
    payload = base64.urlsafe_b64encode(json.dumps({"exp": 4102444800}).encode()).decode().rstrip("=")
    token = f"eyJhbGciOiJub25lIn0.{payload}.demo"
    page.route("**/auth/me", lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps({"user": user, "token": token})))
    page.evaluate("value => localStorage.setItem('auth-storage', value)", json.dumps({"state": {"user": user, "token": token}, "version": 0}))
    page.goto(BASE, wait_until="networkidle")
    page.wait_for_timeout(500)

    route_to(page, "/dashboard")
    save(page, "05-dashboard.webp", full_page=True)
    route_to(page, "/payment")
    save(page, "06-payment.webp")
    page.get_by_role("button", name="ONLINE INTERMEDIATE").first.click()
    page.get_by_role("button", name="Continue", exact=True).click()
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="Confirm Payment").click()
    save(page, "06-payment-qr.webp")
    route_to(page, "/booking")
    save(page, "07-booking.webp")
    grid = page.locator('div[style*="height: 1248px"]').first
    grid.locator("div.cursor-pointer").click(position={"x": 300, "y": 50})
    page.get_by_role("button", name="ONLINE BASIS").click()
    page.get_by_role("button", name="Confirm Plan").click()
    page.get_by_role("button", name="CONFIRM TIME").click()
    save(page, "07-booking-summary.webp")

    browser.close()
