import ollama


class AIEngine:

    def analyze_job(self, text):

        prompt = f"""
        Analyze this job description.

        Return:
        1. Match score out of 100
        2. Important skills
        3. Short summary

        Job Description:
        {text[:4000]}
        """

        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        return response['message']['content']