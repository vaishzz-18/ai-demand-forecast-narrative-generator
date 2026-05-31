import os
import requests
from dotenv import load_dotenv

def build_prompt(stats: dict) -> str:
    prompt = f"""Act as a senior supply chain analyst.
Write a 3-paragraph executive narrative regarding the historical trends, forecast outlook, and business implications for the following data.
Then, write exactly 5 bullet points, each starting with "•" and each beginning with an action verb.
Do not use markdown headers or bold text. Format all monetary values in Indian Rupees (₹).

Data summary:
- Analysis Period: {stats.get('start_date', 'N/A')} to {stats.get('end_date', 'N/A')} ({stats.get('num_weeks', 'N/A')} weeks)
- Total Historical Revenue: {stats.get('total_revenue', 'N/A')}
- Peak Week: {stats.get('peak_week', 'N/A')} with value {stats.get('peak_value', 'N/A')}
- Trough Week: {stats.get('trough_week', 'N/A')} with value {stats.get('trough_value', 'N/A')}
- Prior {stats.get('forecast_horizon', 12)} Weeks Total: {stats.get('prior_n_total', 'N/A')}
- Forecast Total (Next {stats.get('forecast_horizon', 12)} Weeks): {stats.get('forecast_total', 'N/A')}
- Forecast Change vs Prior {stats.get('forecast_horizon', 12)} Weeks: {stats.get('forecast_change_pct', 'N/A')}%
- Current Trend Direction: {stats.get('trend_direction', 'N/A')}
- Top Products: {stats.get('top_products', 'N/A')}
- Top Country: {stats.get('top_country', 'N/A')}
"""
    return prompt

def generate_narrative(stats: dict) -> tuple[str, str]:
    try:
        load_dotenv(encoding="utf-8")
    except UnicodeDecodeError:
        load_dotenv(encoding="utf-16")
        
    api_key = os.getenv("GEMINI_API_KEY")
    prompt = build_prompt(stats)
    
    fallback_narrative = f"""Historically, from {stats.get('start_date')} to {stats.get('end_date')}, revenue trends showed a total of ₹{stats.get('total_revenue')}. The peak occurred during {stats.get('peak_week')} with a value of ₹{stats.get('peak_value')}, while the lowest point was {stats.get('trough_week')} at ₹{stats.get('trough_value')}. The overall trend direction has been {stats.get('trend_direction')}.

Looking ahead, the forecast for the next {stats.get('forecast_horizon', 12)} weeks predicts a total revenue of ₹{stats.get('forecast_total')}, representing a {stats.get('forecast_change_pct')}% change compared to the prior {stats.get('forecast_horizon', 12)} weeks total of ₹{stats.get('prior_n_total')}. The top country remains {stats.get('top_country')}, driving most of the sales for {stats.get('top_products')}.

Given this outlook, supply chain operations should align inventory strategies with the {stats.get('trend_direction')} trend. Capacity planning and raw material sourcing must reflect the projected {stats.get('forecast_change_pct')}% shift to ensure service levels are maintained without accumulating excess stock."""

    fallback_bullets = f"""• Optimize safety stock levels in accordance with the {stats.get('forecast_change_pct')}% forecast change.
• Realign production schedules to match the anticipated demand for {stats.get('top_products')}.
• Allocate distribution resources preferentially towards the {stats.get('top_country')} market.
• Review supplier lead times to mitigate risks associated with the {stats.get('trend_direction')} trend.
• Monitor weekly revenue actuals against the ₹{stats.get('forecast_total')} target to adjust plans dynamically."""

    if not api_key:
        return fallback_narrative, fallback_bullets

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 800
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if not text:
            raise ValueError("No text returned from API")
        
        # Split on first bullet
        if "•" in text:
            parts = text.split("•", 1)
            narrative = parts[0].strip()
            bullets = "•" + parts[1].strip()
            return narrative, bullets
        else:
            return text, fallback_bullets
            
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return fallback_narrative, fallback_bullets
