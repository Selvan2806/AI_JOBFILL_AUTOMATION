from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

        # Block images/fonts/media
        self.page.route(
            "**/*",
            self.handle_route
        )

    def handle_route(self, route):

        resource_type = route.request.resource_type

        if resource_type in [
            "image",
            "media",
            "font"
        ]:
            route.abort()

        else:
            route.continue_()

    def open(self, url):

        self.page.goto(
            url,
            wait_until="domcontentloaded"
        )

    def close(self):

        self.browser.close()

        self.playwright.stop()