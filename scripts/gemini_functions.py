import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from gemini_api import gemini_api
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os




def generate_natural_language_explanation(user_data, card_number):
    # Extract data for the specified card_number.

    card_number = user_data['card_number']
    input_text = (
        f"User with card number {card_number} has a total transaction amount of {user_data['total_amount']}, "
        f"{user_data['transaction_count']} transactions, and an average transaction amount of {user_data['avg_amount']}. "
        f"They have been classified as '{user_data['credit_risk']}' risk."
    )
    explanation = gemini_api.generate_summary(input_text)
    return explanation

def generate_concise_report(user_data, pdf_filename='uploads/concise_credit_risk_report.pdf'):
    # Extract data for the specified card_number.
    card_number = user_data['card_number']

    
    # Build a concise prompt tailored to explain the predicted credit score result.
    prompt = (
        f"Based on the following details for the user with card number {card_number}: "
        f"Transaction Count: {user_data['total_transactions']}, "
        f"Average Amount after a transaction: {user_data['avg_amount_after']}, "
        "Provide a concise explanation in 2-3 sentences that describes the predicted credit score result. "
        "Explain simply what factors contributed to this result and what it means for the user's credit standing."
    )
    narrative = gemini_api.generate_summary(prompt)
    
    # Create a concise PDF report using ReportLab.
    os.makedirs('reports', exist_ok=True)
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title = f"Credit Score Report for Card Number {card_number}"
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 12))
    
    # Display key metrics.
    metrics = (
        f"<b>Transaction Count:</b> {user_data['total_transactions']}<br/>"
        f"<b>Average amount in account before a transaction:</b> {user_data['avg_amount_before']}<br/>"
        f"<b>Average amount in acocunt after a transaction:</b> {user_data['avg_amount_after']}<br/>"
    )
    story.append(Paragraph(metrics, styles['BodyText']))
    story.append(Spacer(1, 12))
    
    # Narrative explanation.
    story.append(Paragraph("Concise Explanation:", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(narrative, styles['BodyText']))
    
    doc.build(story)
    print(f"Concise PDF report generated as '{pdf_filename}'.")


def interactive_query_interface():
    print("Welcome to the Credit Risk Interactive Dashboard. Type 'exit' to quit.")
    while True:
        query = input("Enter your query: ")
        if query.lower() == 'exit':
            print("Exiting dashboard.")
            break
        response = gemini_api.answer_query(query)
        print("Response:", response)

def detect_anomalies(user_features):
    mean_amount = user_features['total_amount'].mean()
    std_amount = user_features['total_amount'].std()
    anomalies = user_features[user_features['total_amount'] > mean_amount + 2 * std_amount]
    
    if not anomalies.empty:
        anomaly_summary = anomalies[['card_number', 'total_amount']].to_string(index=False)
        alert_text = gemini_api.generate_anomaly_alert(anomaly_summary)
        print("Anomaly Alert:")
        print(alert_text)
    else:
        print("No anomalies detected.")

def forecast_risk_trends(historical_data):
    historical_data_str = historical_data.to_csv(index=False)
    forecast_narrative = gemini_api.forecast_risk_trends(historical_data_str)
    print("Risk Trend Forecast:")
    print(forecast_narrative)




