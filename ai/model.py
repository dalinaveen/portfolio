import os
import json
import requests

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Load data (education, skills, and projects)
def load_portfolio_data():
    try:
        with open("data/data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        education = data.get("education", {})
        skills = data.get("skills", {})
        projects = data.get("projects", [])

        # 📘 Build education summary
        edu_context = (
            f"{education.get('degree', '')} from {education.get('college', '')}, "
            f"{education.get('university', '')} (completed in {education.get('year_of_completion', '')}, "
            f"CGPA: {education.get('cgpa', '')}). "
        )

        # 🧠 Build skills summary
        skill_context = "\n".join([
            f"{category}: {', '.join(items)}"
            for category, items in skills.items()
        ])

        # 💡 Build projects summary
        project_context = "\n".join([
            f"{p['title']}: {p['description']}"
            for p in projects
        ])

        # 🔗 Combine everything into one context block
        context = (
            f"Education:\n{edu_context}\n\n"
            f"Skills:\n{skill_context}\n\n"
            f"Projects:\n{project_context}"
        )
        return context

    except Exception as e:
        print("❌ Error loading portfolio data:", e)
        return "No portfolio data available."

# 🧩 Function to get Groq AI response
def get_chatbot_response(user_message):
    portfolio_context = load_portfolio_data()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                 "role": "system",
    "content": (
        "You are an AI assistant representing Dali Naveen’s professional portfolio. "
        "You know his skills, education, and projects from the provided data. "
        "When responding, sound confident, natural, and conversational — not robotic. "
        "Keep answers short (2–3 lines) and flow like a real conversation. "
        "Focus on clarity and tone, not listing. "
        "When asked about skills, summarize like a human (e.g., 'Naveen works mainly with Python and AI frameworks like LangChain and Hugging Face'). "
        "When asked about projects, describe them briefly with context. "
        "Use friendly transitions like 'He’s also skilled in...', 'In his recent work...', or 'His focus areas include...'. "
        "Avoid repetitive phrases like 'has skills in' or 'is skilled in'. "
        "Always keep replies professional but personable."
    )
            },
            {"role": "user", "content": user_message}
        ],
        "max_completion_tokens": 350,
        "temperature": 0.6
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()
        return reply

    except requests.exceptions.RequestException as e:
        print("❌ Groq API Error:", e)
        return "Sorry, I'm having trouble connecting to the AI service right now."
