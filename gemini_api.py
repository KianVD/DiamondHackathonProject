import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

class GeminiAPI:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.api_secret = api_secret or os.environ.get("GEMINI_API_SECRET")
        # Create a client using the google.genai package.
        self.client = genai.Client(api_key=self.api_key)
        # The model to use.
        self.model = "gemini-2.0-flash"

    def generate_content(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

    def generate_summary(self, input_text):
        """
        Generates a concise narrative explanation of credit risk based on the input text.
        """
        prompt = (
            f"Provide a concise explanation for the following credit risk data: {input_text} "
            "in 2-3 sentences, highlighting the key factors that led to the risk assessment."
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

    def generate_report_summary(self, input_data):
        """
        Generates a detailed report summary for credit risk predictions.
        """
        prompt = (
            "Generate a detailed report summarizing credit risk predictions based on user transaction data. "
            "Highlight key metrics such as total transaction amount, transaction count, average transaction amount, "
            "and assigned risk levels (Low, Medium, High). Discuss any trends or insights that might have influenced the risk assessments. "
            "Here is the data summary:\n" + input_data
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

    def answer_query(self, query):
        prompt = f"Answer the following question regarding credit risk predictions: {query}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

    def generate_anomaly_alert(self, anomaly_summary):
        prompt = f"Based on the following anomaly summary from credit risk data, provide a brief alert: {anomaly_summary}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

    def forecast_risk_trends(self, historical_data):
        prompt = f"Based on the following historical credit risk data: {historical_data}, forecast the risk trends for the upcoming period in a concise manner."
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text

# Instantiate the Gemini API using the API key from the environment.
gemini_api = GeminiAPI()

if __name__ == '__main__':
    prompt = "Explain how AI works"
    result = gemini_api.generate_content(prompt)
    print(result)






