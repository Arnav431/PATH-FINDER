from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Configuration to serve static files (images, gifs)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAhQYUFnrrvrb7FEf49y-TiKbN-83pFlQk")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/recommendations', methods=['POST'])
def recommendations():
    try:
        data = request.json
        degree_field = data.get('degreeField', '')
        degree_type = data.get('degreeType', '')
        skill_level = data.get('skillLevel', '')
        interests = data.get('interests', '')
        prompt = f"""As an expert career counselor and professional mentor, provide personalized career recommendations for someone with these details:\n\n**Interests:** {interests}\n**Current Skill Level:** {skill_level}\n**Education Level:** {degree_type}\n{f'**Degree Field:** {degree_field}' if degree_field else ''}\n\nPlease provide 3-4 specific, realistic career recommendations that align with both their interests AND educational background.\n\n**For each career:**\n- Start with a large heading (e.g., `## Job Title` `## Conclusion`).\n- For each section (Description, Perfect Match Reasons, Essential Skills, Salary Range, Getting Started), use bold titles and extra line breaks.\n\nFor each career, include:\n1. **Job Title** (with relevant emoji)\n2. **Engaging Description** (2-3 sentences about what they do daily)\n3. **Perfect Match Reasons** (why this aligns with their interests AND education)\n4. **Essential Skills** (3-4 key skills needed)\n5. **Salary Range** (realistic range for their skill level and education in ₹)\n6. **Getting Started** (specific, actionable first steps that leverage their education)\n\nConsider how their {degree_type}{f' in {degree_field}' if degree_field else ''} can be leveraged or transferred to these career paths. If they need additional education, mention specific programs or certifications.\n\nFormat your response with clear headings, horizontal rules, and make it encouraging, actionable, and visually appealing with emojis. Include a motivational conclusion with next steps.\n\nMake the tone professional but friendly, and ensure all advice is practical and achievable for someone at the {skill_level} level with their educational background.\n\nalways give a conclusion at the end."""
        response = requests.post(API_URL, headers={"Content-Type": "application/json"}, json={
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        })
        if response.status_code != 200:
            return f"Gemini API error: {response.text}", 500
        gemini_data = response.json()
        try:
            recommendations = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            recommendations = str(gemini_data)
        return recommendations
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
