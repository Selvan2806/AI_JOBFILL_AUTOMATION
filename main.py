import time
import json

from modules.browser import BrowserManager
from modules.intelligent_agent import IntelligentAgent


def main():

    url = input("Enter Job URL: ")

    browser = BrowserManager()

    browser.open(url)

    # wait for website to load
    try:
        browser.page.wait_for_load_state(
        "domcontentloaded",
        timeout=10000
    )
    except:
        print("Page load timeout, continuing...")

    # load your profile details
    with open("profile.json", "r") as f:
        profile = json.load(f)

    # start intelligent agent
    agent = IntelligentAgent(
        browser.page,
        profile
    )

    # run automation
    agent.run()

    input("\nPress ENTER to close browser...")

    browser.close()


if __name__ == "__main__":
    main()