"""
AI Narrator Module — Gemini-powered playful explanations for ML predictions.

Uses the proven ROLE / CONTEXT / TASK / INPUT prompt pattern.
Gracefully degrades if config.py or API key is missing.
"""

import json
import google.generativeai as genai

# Try to load API key from config.py (gitignored)
_API_KEY_AVAILABLE = False
try:
    import config
    if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY and config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=config.GEMINI_API_KEY)
        _API_KEY_AVAILABLE = True
        print("[AI Narrator] Gemini API key loaded successfully.")
    else:
        print("[AI Narrator] WARNING: config.py exists but GEMINI_API_KEY is not set.")
except ImportError:
    print("[AI Narrator] WARNING: config.py not found. AI Narrator will be unavailable.")
except Exception as e:
    print(f"[AI Narrator] WARNING: Failed to configure Gemini: {e}")


MODEL_NAME = 'gemma-3n-e4b-it'

FRIENDLY_FAILURE_MESSAGE = "� Radio silence. The station is down. Try again later."


def is_available() -> bool:
    """Check whether the AI Narrator is configured and ready to use."""
    return _API_KEY_AVAILABLE


def build_prompt(prediction_data: dict) -> str:
    """
    Build the structured prompt for Gemini.

    prediction_data must include:
        category, days, fitness, resourcefulness, specialist_skills,
        awareness, scouting_freq, leadership
    """
    return f"""### ROLE ###
You are a grizzled, deadpan radio operator broadcasting from Station Plumpton in Western Sydney during a zombie apocalypse (the year is 2026). You deliver survival dispatches with dry Australian humour, theatrical exaggeration, and the calm tone of someone who has seen it all. Underneath the sarcasm there's genuine respect for survivors. Your audience is a Year 12 Software Engineering student who is in on the joke. Channel: the narrator from a gritty Australian survival show mixed with a sardonic war correspondent.

### CONTEXT ###
This is a deliberately fun machine learning demo that predicts zombie survival outcomes based on personal stats. The backend uses:
- Decision Tree Classifier (sklearn) → predicts the survival category (outcome)
- Polynomial Ridge Regression (sklearn) → predicts days survived

Categories the model can output: Apex Survivor, Scavenger, The Bait, Zombie Snack.

The setting is Western Sydney (Plumpton, Blacktown, Rooty Hill, Penrith, Mt Druitt, St Marys, Great Western Hwy). Lean into local landmarks and zombie apocalypse absurdity.

### TASK ###
Write a 4-5 sentence radio dispatch that is **gritty, witty, and darkly funny**. Follow these rules:

1. **Open with radio static flavour** — e.g. "Static crackles… This is Station Plumpton." or "Radio check…" then immediately comment on their fate.
2. **Reference at least TWO specific input values** with exaggerated commentary (e.g. "awareness of 0.5 — kid was scrolling Reddit near the Rooty Hill RSL"). Use specific numbers.
3. **Mock the model or the absurdity** — reference the algorithm, the days number, or the very idea of predicting zombie survival with polynomial regression.
4. **Never be genuinely cruel or discouraging.** The dark humour should feel like gallows comedy among friends, not bullying.
5. **End with a sardonic sign-off** — something that reads as grim but is secretly encouraging. End with "Out." for radio flavour.
6. Use dry Aussie humour, hyperbole, irony, and deadpan. Reference Western Sydney landmarks where it fits naturally (ECQ Outlet, Great Western Hwy, Richard Johnson Anglican College, Mt Druitt, Penrith, etc.).
7. Format Output: a single clean JSON object, NO markdown, NO code fences, NO extra text. Exactly this shape: `{{"narrative": "..."}}`

### TONE EXAMPLES (style only — do NOT copy these phrases)
- "Static crackles… This is Station Plumpton. We've got a live one. 9 out of 10 on cardio, near-perfect awareness. The AI says 310 days. If you're hearing this… follow their signal. Out."
- "Radio check… just lost another one near the Great Western Hwy. Kid had 8 out of 10 Cardio but his awareness was a 0.5. Lasted 0.8 days. Put the phone down. Out."
- "The polynomial regression says 62 days. That's two months of dodging shamblers and raiding Coles. Respect. Out."

### INPUT ###
* Predicted outcome: {prediction_data['category']}
* Days survived: {prediction_data['days']}
* Cardio / Fitness: {prediction_data['fitness']}/10
* Resourcefulness: {prediction_data['resourcefulness']}/10
* Specialist Skills: {prediction_data['specialist_skills']}
* Situational Awareness: {prediction_data['awareness']}/10
* Scouting Frequency: {prediction_data['scouting_freq']}x per week
* Leadership / Trust: {prediction_data['leadership']}/10
"""


def generate_narrative(prediction_data: dict) -> dict:
    """
    Generate a playful AI narrative for the given prediction.

    Returns:
        {'success': True, 'narrative': '...'}  on success
        {'success': False, 'message': '...'}   on any failure
    """
    if not _API_KEY_AVAILABLE:
        return {
            'success': False,
            'message': FRIENDLY_FAILURE_MESSAGE
        }

    try:
        prompt = build_prompt(prediction_data)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        # Strip any code fences the model might add
        text = response.text.strip()
        if text.startswith('```'):
            # Remove leading fence (```json or just ```)
            text = text.split('\n', 1)[1] if '\n' in text else text
        if text.endswith('```'):
            text = text.rsplit('```', 1)[0]
        text = text.strip()

        # Parse JSON
        data = json.loads(text)

        narrative = data.get('narrative', '').strip()
        if not narrative:
            return {
                'success': False,
                'message': FRIENDLY_FAILURE_MESSAGE
            }

        return {
            'success': True,
            'narrative': narrative
        }

    except json.JSONDecodeError as e:
        print(f"[AI Narrator] JSON parse error: {e}")
        # Last-ditch attempt: use the raw text if it looks reasonable
        try:
            raw = response.text.strip()
            if 30 < len(raw) < 800:
                return {'success': True, 'narrative': raw}
        except Exception:
            pass
        return {
            'success': False,
            'message': FRIENDLY_FAILURE_MESSAGE
        }
    except Exception as e:
        print(f"[AI Narrator] Generation error: {e}")
        return {
            'success': False,
            'message': FRIENDLY_FAILURE_MESSAGE
        }
