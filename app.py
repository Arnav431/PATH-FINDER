from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyAhQYUFnrrvrb7FEf49y-TiKbN-83pFlQk"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

@app.route('/api/career-recommendations', methods=['POST'])
def get_career_recommendations():
    try:
        data = request.json
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

        gemini_data = {
            'contents': [{
                'parts': [{'text': prompt}]
            }],
            'generationConfig': {
                'temperature': 0.7,
                'topK': 40,
                'topP': 0.95,
                'maxOutputTokens': 2048
            }
        }

        response = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=gemini_data)
        response.raise_for_status()

        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            content = "No response from Gemini"

        return jsonify({'recommendations': content})

    except requests.exceptions.RequestException as e:
        print(f'[Gemini API RequestException] {e}')
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except KeyError as e:
        print(f'[Gemini API KeyError] {e}')
        return jsonify({'error': f'Missing expected data in API response: {str(e)}'}), 500
    except Exception as e:
        print(f'[Gemini API Unknown Exception] {e}')
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
