import json
import requests
import os

def handler(request):
    if request.method != "POST":
        return (
            json.dumps({"error": "Method not allowed"}),
            405,
            {"Content-Type": "application/json"}
        )

    try:
        data = request.json
        interests = data.get('interests', '')
        skill_level = data.get('skillLevel', '')
        degree_type = data.get('degreeType', '')
        degree_field = data.get('degreeField', '')

        prompt = f"""As an expert career counselor and professional mentor, provide personalized career recommendations for someone with these details:\n\n**Interests:** {interests}\n**Current Skill Level:** {skill_level}\n**Education Level:** {degree_type}\n{f'**Degree Field:** {degree_field}' if degree_field else ''}\n\nPlease provide 3-4 specific, realistic career recommendations that align with both their interests AND educational background.\n\n**For each career:**\n- Start with a large heading (e.g., `## Job Title` `## Conclusion`).\n- For each section (Description, Perfect Match Reasons, Essential Skills, Salary Range, Getting Started), use bold titles and extra line breaks.\n\nFor each career, include:\n- Description\n- Why this is a perfect match\n- Essential skills\n- Typical salary range\n- How to get started\n\nEnd with a short, motivational conclusion.\n"""

        API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
        GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            return (
                json.dumps({"error": "Gemini API error", "details": response.text}),
                500,
                {"Content-Type": "application/json"}
            )
        gemini_data = response.json()
        try:
            recommendations = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            recommendations = gemini_data
        return (
            json.dumps({"recommendations": recommendations}),
            200,
            {"Content-Type": "application/json"}
        )
    except Exception as e:
        return (
            json.dumps({"error": str(e)}),
            500,
            {"Content-Type": "application/json"}
        )
