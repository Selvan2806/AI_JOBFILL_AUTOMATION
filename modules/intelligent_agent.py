from itertools import count
import json
import time
from urllib import response
import ollama


class IntelligentAgent:

    def __init__(self, page, profile):

        self.page = page
        self.profile = profile

    def get_all_inputs(self):

        elements = self.page.locator(
            "input, textarea, select"
        )

        fields = []

        count = elements.count()

        for i in range(count):

            try:
                el = elements.nth(i)

                field = {
                    "index": i,
                    "tag": el.evaluate(
                        "(e) => e.tagName"
                    ),
                    "type": el.get_attribute("type"),
                    "name": el.get_attribute("name"),
                    "placeholder": el.get_attribute("placeholder"),
                    "label": el.get_attribute("aria-label")
                }
                if field["type"] == "file":
                    continue

                combined = str(field).lower()

                skip_words = [
                "search",
                "newsletter",
                "subscribe",
                "login",
                "password",
                "verify",
                "honeypot"
                ]

                if any(word in combined for word in skip_words):
                    continue

                fields.append(field)

            except:
                pass

        return fields

    def ask_ai(self, fields):

        prompt = f"""
        Map the fields with profile values.

        Profile:
            {json.dumps(self.profile)}

        Fields:
            {json.dumps(fields)}

        Return ONLY JSON.
        """

        response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

        content = response["message"]["content"]

        start = content.find("{")
        end = content.rfind("}") + 1

        clean_json = content[start:end]

        return clean_json

    def fill_fields(self):

        elements = self.page.locator(
        "input, textarea, select"
    )

        count = elements.count()

        for i in range(count):

            try:

                element = elements.nth(i)

                field_type = (
                element.get_attribute("type") or ""
            ).lower()

                name = (
                element.get_attribute("name") or ""
            ).lower()

                placeholder = (
                element.get_attribute("placeholder") or ""
            ).lower()

                combined = name + " " + placeholder

                value = None

            # NAME
                if (
                "name" in combined or
                "first" in combined
            ):
                    value = self.profile["name"]

            # EMAIL
                elif "email" in combined:
                    value = self.profile["email"]

            # PHONE
                elif (
                "phone" in combined or
                "mobile" in combined or
                field_type == "tel"
            ):
                    value = self.profile["phone"]

            # LINKEDIN
                elif "linkedin" in combined:
                    value = self.profile["linkedin"]

            # GITHUB
                elif "github" in combined:
                    value = self.profile["github"]

            # ABOUT
                elif (
                    element.evaluate(
                    "(e) => e.tagName"
                ) == "TEXTAREA"
            ):
                    value = self.profile["about"]

                if value:

                    try:

                        element.fill(value)

                        print(f"Filled: {combined}")

                    except:
                        pass

            except:
                pass

    def upload_resume(self):

        try:
            self.page.set_input_files(
                'input[type="file"]',
                'resume.pdf'
            )

            print("Resume Uploaded")

        except:
            print("Resume field not found")

    def click_buttons(self):

        button_words = [
        "Submit Application",
        "Submit",
        "Continue",
        "Next Step",
        "Apply"
    ]

        already_clicked = set()

        for word in button_words:

            try:

                buttons = self.page.locator(
                    f'text="{word}"'
                )   

                count = buttons.count()

                for i in range(count):

                    try:

                        button = buttons.nth(i)

                        text = button.inner_text()

                        if text in already_clicked:
                            continue

                        button.click(timeout=1000)

                        already_clicked.add(text)

                        print(f"Clicked: {text}")

                        time.sleep(5)

                        return

                    except:
                        pass

            except:
                pass

    def run(self):

        time.sleep(5)

        self.open_real_application()

        time.sleep(5)

        self.fill_fields()

        self.upload_resume()

        self.click_buttons()

    def open_real_application(self):

        apply_keywords = [
        "Apply",
        "Apply Now",
        "Apply Here",
        "External Apply",
        "Continue Application"
    ]

        for word in apply_keywords:

            try:
                buttons = self.page.get_by_text(
                word,
                exact=False
                )   

                count = buttons.count()

                for i in range(count):

                    try:
                        buttons.nth(i).click()

                        print(f"Clicked apply button: {word}")

                        time.sleep(5)

                        return

                    except:
                        pass

            except:
                pass