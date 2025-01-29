from openai import OpenAI
import json


class UXwriter:
    client = None
    manual = None
    data_schema = None
    is_English:bool = False

    def __init__(self, api_key, manual, is_English:bool):
        self.client = OpenAI(api_key=api_key)
        self.manual = manual
        self.is_English = is_English
        self.data_schema = self._generate_data_schema()

    def _generate_data_schema(self):
        """Create the data schema using provided Core Values and Principles."""
        def _parse_values(text):
            lines = text.strip().split("\n")
            values = [line.split("//")[0].split("-")[1].strip() for line in lines if "//" in line]
            return values
        def _format_key(key):
            """Convert spaces in keys to underscores for JSON schema compatibility."""
            return key.replace(" ", "_")
        keywords = [_format_key(value) for value in _parse_values(self.manual.core_values)] + [_format_key(value) for value in _parse_values(self.manual.principles)]
        return {
            "type": "object",
            "properties": {
                "Core_Values": {
                    "type": "object",
                    "properties": {keyword: {"type": "boolean"} for keyword in keywords},
                },
            },
            "required": ["Core_Values", "Principles"],
        }


    def get_score(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert in evaluating content based on predefined values and principles. 
                    For each of the core values and Principles provided, you will return a True or False assessment.""",
                },
                {"role": "user", "content": prompt},
            ],
            functions=[
                {
                    "name": "evaluate_content",
                    "description": "Evaluate the content based on Core Vlues and Principles",
                    "parameters": self.data_schema,
                }
            ],
            function_call={"name": "evaluate_content"},
        )
        result = response.choices[0].message.function_call.arguments
        return result


    def edit(self, prompt, score):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": self._edit_system_prompt()},
                {
                    "role": "user",
                    "content": f"""Content: 
                        {prompt}

                        Content Evaluation Criteria:
                        {json.dumps(score)}

                        no talk; just do. only sentence
                    """,
                },
            ],
        )
        return response.choices[0].message.content
    
    def _edit_system_prompt(self):
        return f"""{'The output should always be in English' if self.is_English else 'The output should be in the same language as the input'}.
                            {self.manual.system_prompt}
                            no talk; just do.
                    
                    Core Values:
                    {self.manual.core_values}

                    Principles:
                    {self.manual.principles}
                    """