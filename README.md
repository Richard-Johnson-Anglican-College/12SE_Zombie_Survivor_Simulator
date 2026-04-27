# 🧟 Zombie Survival Simulator — Western Sydney 2026

A **hybrid AI web application** that predicts how long you'd survive a zombie apocalypse in Western Sydney, based on personal survival stats. Built for Year 12 Software Engineering to demonstrate a real-world hybrid architecture **chaining classical machine learning with a neural network (LLM)**.

### 🧬 Hybrid Architecture (3 chained models)

```
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────────┐
  │  Decision Tree   │ →  │ Polynomial Ridge │ →  │ Gemma Neural Network │
  │  Classifier      │    │ Regression       │    │ (LLM via Gemini API) │
  │  (sklearn)       │    │ (sklearn)        │    │                      │
  │  → outcome       │    │ → days_survived  │    │ → radio dispatch     │
  └──────────────────┘    └──────────────────┘    └──────────────────────┘
        Stage 1                  Stage 2                  Stage 3
        Classical ML             Classical ML             Neural Network
```

**Hybrid system** = different model families working together. **Chaining** = the output of each stage feeds the next.

---

## 🎯 Features

- **Hybrid AI System (3 chained models):**
  - **Stage 1 — Decision Tree Classifier** (sklearn) — predicts outcome: Apex Survivor, Scavenger, The Bait, Zombie Snack
  - **Stage 2 — Polynomial Ridge Regression** (sklearn) — predicts days survived
  - **Stage 3 — Gemma Neural Network** (Google's LLM via Gemini API) — generates a gritty radio dispatch narrative chained from Stage 1 + 2 outputs
  - Model architecture transparency (19 nodes, 10 leaves, 28 polynomial features, transformer-based LLM)

- **Interactive Web Interface:**
  - Dark zombie-themed UI with Creepster/Road Rage fonts and green glow palette
  - Real-time predictions with detailed, ML-driven survival explanations
  - Admin dashboard with model metrics, ML transparency features
  - Visual ML charts: polynomial curve, decision tree diagram, interaction heatmap
  - Input validation with realistic range checking

- **Educational Focus:**
  - Demonstrates overfitting concepts
  - Shows feature importance with actual weights
  - Includes training metrics and warnings
  - Comprehensive teaching documentation (ML_EXPLAINED.md)
  - Optimization analysis guide (OPTIMAL_PREDICTIONS.md)
  - Proves real ML is used (not hardcoded JavaScript)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Training Data

Use the existing `data.csv` (80+ records included).

### 3. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 📁 Project Structure

```
12SE_Zombie_Survivor_Simulator/
├── app.py                      # Flask routes and server
├── ml_engine.py                # ML models (Decision Tree + Ridge)
├── ai_narrator.py              # Stage 3 — Gemma LLM radio dispatch narrator
├── config.example.py           # Template for Gemini API key
├── requirements.txt            # Python dependencies
├── data.csv                    # Training data (CSV format) — PRIMARY DATA SOURCE
├── models.pkl                  # Trained models (auto-generated)
├── CHANGELOG.md                # Project history and updates
├── README.md                   # Main documentation (this file)
├── SPEC.md                     # Original specification
├── ZOMBIE_SPEC.md              # Zombie theme design spec
├── ML_EXPLAINED.md             # Teaching guide (jargon-free)
├── OPTIMAL_PREDICTIONS.md      # Optimization analysis
├── DEPLOY.md                   # PythonAnywhere deployment guide
├── static/
│   ├── css/
│   │   └── style.css           # Zombie theme styles
│   └── images/                 # Hero image, feature icons, class images
├── templates/
│   ├── index.html              # Main prediction interface
│   └── admin.html              # Admin dashboard with ML transparency
└── utils/                      # Utility scripts
    ├── seed_data.py            # Generate sample training data
    ├── test_data_quality.py    # Automated data analysis
    └── TESTING_GUIDE.md        # Testing documentation
```

## 🎨 UI Design

- **Typography:** Creepster (hero title), Road Rage (h2/h3), Inter (body), Roboto Mono (code)
- **Color Palette:**
  - Background: `#0f1117` (dark)
  - Primary: `#4ade80` (zombie green)
  - Accent: `#22c55e` (green glow)
  - Danger: `#ef4444` (red)
- **Style:** Dark mode, scanline overlay, green glow effects

## 🧠 How It Works (The Hybrid Chain)

1. **Data Collection:** User inputs 6 survival features (validated server-side)
2. **Stage 1 — Classical ML (Classification):**
   - Decision Tree classifies into survival outcome (with probability distribution)
3. **Stage 2 — Classical ML (Regression):**
   - Polynomial Ridge Regression estimates days survived (with feature interactions)
4. **Stage 3 — Neural Network (LLM, On-Demand):**
   - User clicks the 📻 radio icon
   - Stage 1 + Stage 2 outputs are **chained** into a structured prompt
   - Gemma neural network (transformer LLM) generates a gritty radio dispatch
   - This is the **hybrid handoff**: classical ML's numbers → neural network's natural language
5. **Rule-Based Explanation:** ML-driven system provides instant feedback:
   - Model confidence levels
   - Feature-specific analysis (✓ Strengths, ⚠ Watch Out)
   - Both classical models explicitly mentioned
6. **Training Pipeline:**
   - CSV data → Stage 1+2 model training → Pickle storage
   - Stage 3 uses a pre-trained foundation model (no local training needed)
   - Edit `data.csv` directly to add/modify training data
   - Click "Retrain Models" in admin to update Stage 1+2 predictions

## 📊 Machine Learning Details

### Stage 1: Decision Tree Classifier (Classical ML)
- `max_depth=4` — Prevents deep memorization
- `min_samples_leaf=3` — Requires minimum samples per leaf
- Output **chained** into Stage 3 prompt as `outcome`

### Stage 2: Polynomial Ridge Regression (Classical ML)
- `degree=2` — Captures non-linear relationships
- `alpha=1.5` — Regularization to prevent overfitting
- Output **chained** into Stage 3 prompt as `days_survived`

### Stage 3: Gemma Neural Network (LLM)
- Model: `gemma-3n-e4b-it` (Google's transformer-based language model via Gemini API)
- Receives: Stage 1 outcome + Stage 2 days + raw survival features
- Generates: 4-5 sentence radio dispatch narrative
- Purpose: Demonstrates **hybrid architecture** — neural network reasoning over classical ML output

## 🔧 Admin Features

- **Hybrid Chain Pipeline Diagram** — Stage 1 → 2 → 3 visual
- **Model Architecture Cards** — Decision Tree, Polynomial Ridge, Gemma details
- **Chain in Action Demo** — Live end-to-end hybrid execution
- **Classical ML vs Neural Network Comparison Table**
- **Stage 3 Prompt Inspector** — Shows the actual chained prompt
- **Visual ML Charts** — Polynomial curve, decision tree, feature interaction heatmap
- **Live Prediction Example** — Real `predict_proba()` output
- **Feature Importance** — Visual bar chart with actual weights
- **Retrain Button** — One-click model retraining

## 📝 Adding Training Data

Edit `data.csv` directly:

```csv
fitness,resourcefulness,specialist_skills,awareness,scouting_freq,leadership,outcome,days_survived
9,8,6,8.5,5,7,Apex Survivor,310.2
```

Then click "Retrain Models" in the admin dashboard.

## ⚠️ Educational Notes

- **Overfitting Warning:** 100% training accuracy = memorization
- **Small Dataset:** Intentionally small for teaching
- **No Validation Split:** Simplified for classroom use
- **Disclaimer:** Predictions are fictional!

## 🎓 Teaching Hooks

1. **The "Cheat Test":** Can students game the model by changing awareness?
2. **The "Accuracy Illusion":** Why does 80% accuracy beat 100%?
3. **Feature Importance:** Which survival traits matter most?
4. **ML Transparency:** Show students the actual sklearn model parameters
5. **Optimization Challenge:** Find the combination that gives max days survived
6. **Overfitting Demo:** Input exact training data → 100% confidence (memorization!)

## 📚 Documentation

- **`ML_EXPLAINED.md`** — Complete teaching guide (jargon-free)
- **`OPTIMAL_PREDICTIONS.md`** — Optimization analysis (max survival combinations)
- **`DEPLOY.md`** — PythonAnywhere deployment guide
- **`ZOMBIE_SPEC.md`** — Zombie theme design specification

## 📝 License

Educational project for classroom use — Richard Johnson Anglican College.
