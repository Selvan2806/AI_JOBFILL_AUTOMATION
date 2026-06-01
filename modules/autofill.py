import json
import time


class AutoFill:

    def __init__(self, page):

        self.page = page

        with open("profile.json", "r") as f:
            self.profile = json.load(f)

    def click_apply_button(self):

        apply_buttons = [
            "Apply",
            "Apply Now",
            "Easy Apply",
            "Submit Application"
        ]

        for text in apply_buttons:

            try:
                self.page.get_by_text(
                    text,
                    exact=False
                ).click(timeout=3000)

                print(f"Clicked: {text}")

                time.sleep(3)

                return

            except:
                pass

    def select_candidate(self):

        candidate_options = [
            "Candidate",
            "Applicant",
            "Student",
            "Job Seeker"
        ]

        for text in candidate_options:

            try:
                self.page.get_by_text(
                    text,
                    exact=False
                ).click(timeout=2000)

                print(f"Selected: {text}")

                time.sleep(2)

                return

            except:
                pass

    def fill_text_inputs(self):

        field_values = {
            "email": self.profile["email"],
            "name": self.profile["name"],
            "phone": self.profile["phone"],
            "mobile": self.profile["phone"],
            "linkedin": self.profile["linkedin"],
            "github": self.profile["github"],
            "college": self.profile["college"]
        }

        inputs = self.page.locator("input")

        count = inputs.count()

        for i in range(count):

            try:
                input_box = inputs.nth(i)

                name_attr = (
                    input_box.get_attribute("name") or ""
                ).lower()

                placeholder = (
                    input_box.get_attribute("placeholder") or ""
                ).lower()

                combined = name_attr + " " + placeholder

                for key, value in field_values.items():

                    if key in combined:

                        try:
                            input_box.fill(value)

                            print(f"Filled {key}")

                            break

                        except:
                            pass

            except:
                pass

    def fill_textareas(self):

        try:
            textareas = self.page.locator("textarea")

            count = textareas.count()

            for i in range(count):

                try:
                    textareas.nth(i).fill(
                        self.profile["about"]
                    )

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

            time.sleep(2)

        except:
            print("Resume upload field not found")

    def click_buttons(self):

        buttons = [
            "Next",
            "Continue",
            "Submit",
            "Apply",
            "Finish"
        ]

        for _ in range(10):

            clicked = False

            for text in buttons:

                try:
                    self.page.get_by_text(
                        text,
                        exact=False
                    ).click(timeout=2000)

                    print(f"Clicked: {text}")

                    clicked = True

                    time.sleep(3)

                    break

                except:
                    pass

            if not clicked:
                break

    def run(self):

        self.click_apply_button()

        self.select_candidate()

        self.fill_text_inputs()

        self.fill_textareas()

        self.upload_resume()

        self.click_buttons()