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
        body = request.body.decode()
        data = json.loads(body)
        interests = data.get('interests', '')
        skill_level = data.get('skillLevel', '')
        degree_type = data.get('degreeType', '')
        degree_field = data.get('degreeField', '')

        prompt = f"""As an expert career counselor and professional mentor, provide personalized career recommendations for someone with these details:

**Interests:** {interests}
**Current Skill Level:** {skill_level}
**Education Level:** {degree_type}
{f'**Degree Field:** {degree_field}' if degree_field else ''}

Please provide 3-4 specific, realistic career recommendations that align with both their interests AND educational background.

**For each career:**
- Start with a large heading (e.g., `## Job Title` `## Conclusion`).
- For each section (Description, Perfect Match Reasons, Essential Skills, Salary Range, Getting Started), use bold titles and extra line breaks.

For each career, include:
1. **Job Title** (with relevant emoji)
2. **Engaging Description** (2-3 sentences about what they do daily)
3. **Perfect Match Reasons** (why this aligns with their interests AND education)
4. **Essential Skills** (3-4 key skills needed)
5. **Salary Range** (realistic range for their skill level and education in ₹)
6. **Getting Started** (specific, actionable first steps that leverage their education)

Consider how their {degree_type}{f' in {degree_field}' if degree_field else ''} can be leveraged or transferred to these career paths. If they need additional education, mention specific programs or certifications.

Format your response with clear headings, horizontal rules, and make it encouraging, actionable, and visually appealing with emojis. Include a motivational conclusion with next steps.

Make the tone professional but friendly, and ensure all advice is practical and achievable for someone at the {skill_level} level with their educational background.

always give a conclusion at the end.
"""

        API_KEY = os.environ.get("GEMINI_API_KEY")
        if not API_KEY:
            return (
                json.dumps({"error": "Missing Gemini API key"}),
                500,
                {"Content-Type": "application/json"}
            )

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