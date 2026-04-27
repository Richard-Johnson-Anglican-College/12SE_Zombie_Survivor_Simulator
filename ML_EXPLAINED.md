# How the Machine Learning Works (Teacher's Guide)

A simple, jargon-free explanation of the ML models powering the Zombie Survival Simulator.

---

## 🎯 The Big Picture

This app uses a **hybrid AI system** with **three chained models**:

1. **Decision Tree** — Decides the survival outcome (Apex Survivor, Scavenger, The Bait, Zombie Snack)
2. **Polynomial Ridge Regression** — Calculates the exact number of days survived
3. **Gemma Neural Network (LLM)** — Turns the ML output into a gritty radio dispatch narrative

Think of it like asking three experts in sequence: one gives a category, one gives a number, and one explains it like a human.

### 🔗 Chaining Flow

```text
Stage 1 (Classical ML): Decision Tree           -> outcome
Stage 2 (Classical ML): Polynomial Ridge        -> days_survived
Stage 3 (Neural Network): Gemma (Gemini API)    -> radio dispatch narrative
```

The key idea is **chaining**: Stage 1 + Stage 2 outputs are injected into the Stage 3 prompt.

---

## 🌳 Model 1: Decision Tree Classifier

### What It Does
Classifies survivors into 4 outcome categories based on their stats.

### How It Works (Simple Analogy)

Imagine a flowchart with yes/no questions:

```
Start Here
    ↓
Is awareness high (≥8)?
    ├─ YES → Is fitness high (≥7)?
    │           ├─ YES → "Apex Survivor" 🏆
    │           └─ NO → "Scavenger"
    └─ NO → Is awareness very low (<2)?
                ├─ YES → "Zombie Snack" 💀
                └─ NO → "The Bait"
```

**Real Example:**
- Input: Awareness = 9.5, Fitness = 10
- Tree follows: YES → YES → **"Apex Survivor"**

### Why It's Called a "Tree"
- **Root:** Starting question
- **Branches:** Each decision path
- **Leaves:** Final answers (10 leaves in our model)
- **Nodes:** Decision points (19 nodes total)

### Our Tree's Settings
- **Max Depth:** 4 levels deep (prevents memorizing data)
- **Min Samples per Leaf:** 3 people (ensures reliable patterns)
- **Total Nodes:** 19 decision points
- **Leaf Nodes:** 10 final outcomes

### How It Gives Probabilities

Each leaf contains training examples. If a leaf has:
- 6 "Apex Survivor" examples
- 1 "Scavenger" example
- 0 others

Then prediction = **86% Apex Survivor, 14% Scavenger**

**Teaching Moment:** This is why you sometimes see 100% confidence — the leaf only has one type of outcome!

---

## 📈 Model 2: Polynomial Ridge Regression

### What It Does
Predicts the exact number of days survived (e.g., 12.5 days, 310.2 days).

### How It Works (Simple Analogy)

Imagine drawing a curved line through dots on a graph:

```
Days
  ↑
365|                              • (best case)
   |
150|              •
   |         •
 50|    •  •
   |  •
0.1| •                            • (worst case)
   └────────────────────────────→
    Low                    High
        Awareness Score
```

The model finds the **best-fitting curve** through all 80+ training examples.

### Why "Polynomial"?

Instead of a straight line, it uses a **curved line** (degree 2):

**Straight line (boring):**
```
days = 200 - (awareness × 20)
```

**Polynomial (better):**
```
days = 50 + (fitness × 15) + (awareness² × 2) + (fitness × awareness × 5)
```

The `awareness²` and `fitness × awareness` parts capture **interactions** between features.

**Real Example:**
- High fitness (10) + High awareness (9.5) = Massive survival boost!
- The model learns: "These two together are better than the sum of parts"

### Feature Expansion

Our model expands **6 inputs into 28 features**:

**Original 6:**
1. fitness
2. resourcefulness
3. specialist_skills
4. awareness
5. scouting_freq
6. leadership

**Becomes 28 features including:**
- Original 6
- Squares: fitness², awareness², etc. (6 more)
- Interactions: fitness × awareness, fitness × resourcefulness, etc. (15 more)
- Constant term (1 more)

**Total:** 6 + 6 + 15 + 1 = 28 features

### Why "Ridge"?

Ridge = **Regularization** = Prevents the model from being too confident.

**Without Ridge:**
- Model might predict: "Max stats = 9999 days" (unrealistic!)

**With Ridge (alpha = 1.5):**
- Model predicts: "Max stats = 365 days" (realistic, capped at 1 year)

It adds a "penalty" for extreme predictions, keeping results sensible.

---

## 🧠 Model 3: Gemma Neural Network Narrator (Stage 3)

### What It Does
Converts the structured ML output into a gritty radio dispatch with personality.

### Why We Need It
- Stage 1 + 2 are great at numbers and categories
- But they do not write natural language
- Stage 3 (Gemma) bridges that gap

### How It Is Chained

The app builds a prompt using a structured template:
- `ROLE` — Grizzled radio operator at Station Plumpton
- `CONTEXT` — Zombie apocalypse in Western Sydney, 2026
- `TASK` — Write a darkly funny radio dispatch
- `INPUT` — ML outputs + raw user stats

Inside `INPUT`, it includes:
- Predicted outcome (from Decision Tree)
- Predicted days survived (from Polynomial Ridge)
- Original 6 user features

So Stage 3 is not guessing blindly; it is reasoning over the upstream ML outputs.

### Runtime Notes (Classroom-Friendly)
- Model: `gemma-3n-e4b-it`
- Accessed via Gemini API
- On-demand (radio icon), not auto-run
- If API key is missing, app degrades gracefully with a friendly message

---

## ⚖️ Feature Importance (What Matters Most)

The Decision Tree learns which features are most important. Exact values depend on training data, but the general pattern:

| Feature | Role | What This Means |
|---------|------|-----------------|
| **Awareness** | Primary split | Most important! Low awareness = instant Zombie Snack |
| **Fitness** | High weight | Can you outrun the horde? |
| **Resourcefulness** | Moderate weight | Practical survival ability |
| **Leadership** | Moderate weight | Do others follow you? |
| **Scouting Freq** | Lower weight | Risk vs. reward tradeoff |
| **Specialist Skills** | Variable | Tree may not split on it — but Polynomial model uses it! |

### 🤔 The Skills Mystery: Two Models Disagree!

The Decision Tree may assign **low importance** to specialist_skills, but does that mean skills don't matter? **No!**

**Decision Tree says:** "I rarely use skills to make decisions"
**Polynomial Ridge says:** "Skills matter through interactions — there's a sweet spot!"

### Why the Models Disagree

- **Decision Trees** use *hard splits* (e.g., "is skills > 5?"). If no single threshold cleanly separates the data, the feature gets ignored.
- **Polynomial Ridge** uses *smooth curves* and creates **28 features** from 6 inputs — including interactions like `skills × resourcefulness` and `skills²`. This captures subtle effects.

### 🎓 Teaching Moment

**"Low tree importance ≠ no impact!"**

This is a great lesson about ML:
- Different models see the same data differently
- Feature importance from one model doesn't tell the whole story
- Interaction effects can hide a feature's true contribution
- Always validate findings with multiple approaches

---

## 🎓 How the Models Learn (Training Process)

### Step 1: Load Training Data
- 80+ survivor profiles from `data.csv`
- Each has 6 features + 2 outcomes (outcome category + days_survived)

### Step 2: Decision Tree Learning

The tree asks: **"What question best splits the data?"**

**Example iteration:**
1. Try splitting on "awareness ≥ 8"
   - Left branch: 30 people → 80% "Zombie Snack"
   - Right branch: 50 people → 70% "Apex Survivor"
   - **Good split!** Clear separation

2. Try splitting on "specialist_skills ≥ 5"
   - Left branch: 40 people → 50% "Scavenger", 50% "The Bait"
   - Right branch: 40 people → 50% "Scavenger", 50% "The Bait"
   - **Bad split!** No clear pattern

The tree picks the best split at each level, 4 levels deep.

### Step 3: Polynomial Ridge Learning

The regression model asks: **"What curve fits the data best?"**

**Process:**
1. Expand 6 features → 28 polynomial features
2. Try different coefficients (weights) for each feature
3. Calculate error: How far off are predictions?
4. Adjust coefficients to minimize error
5. Add ridge penalty to prevent overfitting
6. Repeat until error stops improving

**Result:** A formula like:
```
days = 50.0
       + (awareness × 25.0)
       + (fitness × 18.0)
       + (resourcefulness × 8.0)
       + (fitness × awareness × 5.0)
       ... (28 terms total)
```

### Step 4: Validation

Check accuracy on the training data:
- **Decision Tree:** ~80% accuracy (intentionally not 100% to avoid memorization)
- **Polynomial Ridge:** Error varies with dataset

---

## 🔍 Real Prediction Example (Step-by-Step)

**User Input:**
- Fitness: 10
- Resourcefulness: 9
- Specialist Skills: 7
- Awareness: 9.5
- Scouting Freq: 7x/week
- Leadership: 10

### Decision Tree Process

**Level 1:** Is awareness ≥ 8?
- Answer: YES (9.5 ≥ 8)
- Go to right branch

**Level 2:** Is fitness ≥ 7?
- Answer: YES (10 ≥ 7)
- Go to right branch

**Level 3:** Is leadership ≥ 8?
- Answer: YES (10 ≥ 8)
- Go to right branch

**Level 4:** Reached Leaf Node
- Contains: Mostly "Apex Survivor" examples
- **Prediction: "Apex Survivor" with high confidence**

### Polynomial Ridge Process

**Step 1:** Expand features
```
Original: [10, 9, 7, 9.5, 7, 10]
Expanded: [10, 9, 7, 9.5, 7, 10, 100, 81, 49, 90.25, 49, 100,
           90, 70, 95, 63, 66.5, 67.5, ...]
           (28 features total)
```

**Step 2:** Apply learned formula
```
days = 50.0
       + (9.5 × 25.0)    [awareness]
       + (10 × 18.0)      [fitness]
       + (9 × 8.0)        [resourcefulness]
       + (10 × 9.5 × 5.0) [fitness × awareness]
       + ... (24 more terms)
     ≈ 365.0 days
```

**Final Result:**
- **Outcome:** Apex Survivor (from Decision Tree)
- **Days Survived:** 365.0 (from Polynomial Ridge)

---

## 🎯 Why Use a 3-Stage Hybrid System?

### Decision Tree Strengths
✅ Easy to understand (flowchart logic)
✅ Handles categories well
✅ Shows clear decision rules
✅ Fast predictions

### Decision Tree Weaknesses
❌ Can only predict categories (not exact numbers)
❌ Tends to overfit (memorize data)
❌ Predictions are "steppy" (jumps between values)

### Polynomial Ridge Strengths
✅ Predicts exact numbers (0.8 days, 310.2 days)
✅ Smooth predictions (no jumps)
✅ Captures feature interactions
✅ Regularization prevents overfitting

### Polynomial Ridge Weaknesses
❌ Hard to interpret (complex formula)
❌ Can't explain "why" in simple terms
❌ Requires numerical targets (not categories)

### Gemma Stage 3 Strengths
✅ Explains outputs in plain language
✅ Improves engagement and readability
✅ Can reference multiple input features naturally

### Gemma Stage 3 Weaknesses
❌ Not deterministic (wording varies)
❌ Depends on API availability and quota
❌ Should not replace numeric models for core prediction math

### Together They're Better
- Stage 1 predicts **WHAT outcome** (survival category)
- Stage 2 predicts **HOW LONG** (exact days)
- Stage 3 explains **SO WHAT** (radio dispatch narrative)

That combination is why this project is a **hybrid system**.

---

## 📊 Model Performance Metrics

### Decision Tree Accuracy: ~80%

**What this means:**
- Out of 80+ training examples, it correctly predicts ~80% of outcome categories
- Some are misclassified (e.g., "Scavenger" predicted as "The Bait")

**Why not 100%?**
- 100% = Memorization (overfitting)
- 80% = Learning patterns (good generalization)

**Teaching Moment:** Show students that perfect scores can be bad!

### Polynomial Ridge Error

**What this means:**
- Average prediction is off by some number of days
- Example: True = 200 days, Predicted = 185 days

**Why is there error?**
- Survival is messy! Not everyone follows exact patterns
- Model finds the "best fit" curve, not a perfect fit

**Teaching Moment:** All models have error — it's about minimizing it!

---

## 🚨 Common Misconceptions (Teaching Points)

### Misconception 1: "The model is just if-else statements"
**Truth:** The tree structure is learned from data, not hardcoded. Different data = different tree!

### Misconception 2: "More data always = better model"
**Truth:** Quality > Quantity. 80 good examples beats 1000 messy examples.

### Misconception 3: "100% accuracy = best model"
**Truth:** 100% = overfitting. The model memorized instead of learned.

### Misconception 4: "All features are equally important"
**Truth:** Awareness matters far more than some other features.

### Misconception 5: "The model knows about zombie survival"
**Truth:** It only knows patterns in the training data. Garbage in = garbage out!

---

## 🔬 Overfitting Demonstration (Built-In!)

This app is **intentionally designed** to show overfitting:

### Why Our Model Overfits
1. **Small dataset:** Only 80+ examples (real ML uses thousands)
2. **High tree depth:** 4 levels (could be shallower)
3. **Training on same data we test on:** No separate validation set

### How to Show Students

**Test 1:** Input exact training example
- Result: 100% confidence, perfect prediction
- **Why?** Model memorized this exact case!

**Test 2:** Input slightly different values
- Result: Lower confidence, different prediction
- **Why?** Model hasn't seen this exact combination!

**Teaching Moment:** This is why real ML uses train/test splits!

---

## 💡 Classroom Activities

### Activity 1: Feature Importance Experiment
1. Students predict which survival feature matters most
2. Check the feature importance chart
3. Discuss why awareness dominates

### Activity 2: Overfitting Hunt
1. Find a training example in `data.csv`
2. Input exact values → Get 100% confidence
3. Change one value slightly → Watch confidence drop
4. Discuss: Is this good or bad?

### Activity 3: Model Comparison
1. Make same prediction with both models
2. Compare outcome (tree) vs. days (ridge)
3. Discuss: Why do we need both?

### Activity 4: Chain Inspection Lab
1. Open the admin dashboard pipeline diagram
2. Run "Chain in Action" to execute Stage 1 → Stage 2 → Stage 3
3. Expand the Prompt Inspector
4. Highlight where `outcome` and `days` are chained into Stage 3
5. Discuss: Which part is deterministic vs. generative?

### Activity 5: Edge Case Testing
1. Input all 10s → What happens?
2. Input all 1s → What happens?
3. Input realistic values → Compare results
4. Discuss: Model limitations

---

## 📚 Key Vocabulary (Student-Friendly)

| Term | Simple Definition | Example |
|------|-------------------|---------|
| **Decision Tree** | A flowchart that makes decisions | "If awareness ≥ 8, go right" |
| **Regression** | Predicting a number | "You survived 310.5 days" |
| **Classification** | Predicting a category | "Apex Survivor" vs "Zombie Snack" |
| **Feature** | An input to the model | Fitness, awareness, etc. |
| **Training** | Teaching the model from examples | Showing it 80+ survivor profiles |
| **Prediction** | Model's guess for new data | "Scavenger, 62.4 days" |
| **Overfitting** | Memorizing instead of learning | 100% accuracy on training data |
| **Regularization** | Preventing overconfidence | Ridge penalty keeps predictions realistic |
| **Feature Importance** | Which inputs matter most | Awareness is the primary split |
| **Polynomial** | Curved relationship | fitness² captures diminishing returns |
| **Hybrid System** | Combining model families | Classical ML + neural network in one app |
| **Chaining** | Passing one model's output into another | outcome + days injected into LLM prompt |
| **Neural Network (LLM)** | A language model with many parameters | Gemma writes the radio dispatch |
| **Transformer** | Neural architecture used by modern LLMs | Gemma is a decoder-only transformer |
| **Prompt Engineering** | Structuring instructions for an LLM | ROLE/CONTEXT/TASK/INPUT |

---

## 🎓 Learning Outcomes

After using this app, students should understand:

1. ✅ **ML models learn from data** (not hardcoded rules)
2. ✅ **Different models have different strengths** (tree vs regression)
3. ✅ **Feature importance varies** (some inputs matter more)
4. ✅ **Overfitting is a real problem** (100% accuracy can be bad)
5. ✅ **Models have limitations** (prediction floor/ceiling)
6. ✅ **Context matters** (skills alone ≠ important, but skills × resourcefulness = important)
7. ✅ **Real ML requires validation** (train/test splits)
8. ✅ **Hybrid architecture benefits** (classical ML + neural network)
9. ✅ **Chaining mechanics** (Stage 1+2 outputs become Stage 3 inputs)
10. ✅ **Deterministic vs generative behavior** (stable math vs variable language)

---

## 🔧 Technical Details (For Advanced Students)

### Scikit-Learn Implementation

**Decision Tree:**
```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    max_depth=4,              # 4 levels deep
    min_samples_leaf=3,       # At least 3 examples per leaf
    random_state=42           # Reproducible results
)
```

**Polynomial Ridge:**
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline

model = Pipeline([
    ('polynomialfeatures', PolynomialFeatures(degree=2)),
    ('ridge', Ridge(alpha=1.5))
])
```

### Model Persistence
Models are saved to `models.pkl` using Python's `pickle` module, so they don't need to be retrained every time.

---

*This guide is designed for Year 12 Software Engineering students learning about Machine Learning.*
*Feel free to adapt the complexity based on your class level!*
