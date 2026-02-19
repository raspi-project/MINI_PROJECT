from openai import OpenAI
import json
import time

# ================= AI CONFIG =================

ai_client = OpenAI(
    api_key="AI_API_KEY",   # <-- Add your API key
    base_url="https://openrouter.ai/api/v1"
)

# ================= SYSTEM PROMPT =================

SYSTEM_PROMPT = """
You are an expert agricultural advisor.

You will receive:
1. Farm sensor data
2. Weather data
3. A question from the farmer

Rules:
- Use ONLY the provided farm and weather data.
- Answer ONLY the farmer's question.
- Do NOT provide extra suggestions.
- Do NOT explain everything if not asked.
- Keep the answer short, clear, and practical.
- If data is not enough, say so briefly.

Speak like an agricultural expert, not like an AI.
"""


# ================= AI FUNCTION =================

def generate_ai_advice(combined_data, farmer_question):
    """
    Takes:
        combined_data (dict) → sensor + weather data
        farmer_question (str) → question asked by farmer

    Returns:
        Focused answer to the farmer's question.
    """
  
    try:
        context_data = json.dumps(combined_data, indent=2)

        user_message = f"""
        Farm Data:
        {context_data}

        Farmer Question:
        {farmer_question}

        Answer only the question using the farm data above.
        """

        response = ai_client.chat.completions.create(
            model="openai/gpt-5.2",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=500
        )
        time.sleep(0.8)
        reply = response.choices[0].message.content.strip()
        time.sleep(1)
        return reply

    except Exception as e:
        print("⚠ AI Error:", e)
        return "Unable to generate advice at the moment."
