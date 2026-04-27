# Optimal Predictions Guide

## Finding the Maximum Survival Duration

This document shows the analysis of what input combinations produce the **highest days survived** in the Zombie Survival Simulator.

---

## 🏆 Apex Survivor Profile: **365.0 days**

### Optimal Combination

| Feature | Value |
|---------|-------|
| **Fitness** | 10/10 |
| **Resourcefulness** | 9/10 |
| **Specialist Skills** | 7 |
| **Awareness** | 9.5/10 |
| **Scouting Frequency** | 7x/week |
| **Leadership** | 10/10 |

---

## 🔍 Key Insights

### Critical Factors (In Order of Importance)

1. **Awareness** ⭐ Most important feature
   - The Decision Tree's root split — low awareness kills you instantly
   - Must be high (8+) to reach Apex Survivor

2. **Fitness** ⭐ Very important
   - Can you outrun the horde?
   - High fitness × high awareness = exponential survival boost (polynomial interaction)

3. **Resourcefulness**
   - Can you hotwire a car, fortify a fence, find supplies?
   - Interacts heavily with specialist skills in the polynomial model

4. **Leadership**
   - Strong leaders attract groups, groups survive longer
   - 8+ is the sweet spot

5. **Scouting Frequency**
   - Regular scouting (3-5x/week) is optimal
   - Too high (6-7x) increases exposure risk — diminishing returns

6. **Specialist Skills**
   - First Aid, Carpentry, Mechanics — all help
   - 5-8 is the sweet spot; more doesn't always help

---

## 🎯 Common Patterns in Top Survivors

All Apex Survivor profiles share:

- ✅ **Awareness:** Always 8.5+
- ✅ **Fitness:** Always 8+
- ✅ **Resourcefulness:** Always 7+
- ✅ **Leadership:** Always 8+
- ✅ **Specialist Skills:** Always 5-8
- ✅ **Scouting Frequency:** 3-7x/week

---

## 🚫 Surprising Findings

### What DOESN'T Help (or Hurts)

1. **Maxing everything to 10** — Not optimal!
   - Extreme scouting (7x/week) increases death risk
   - The polynomial model penalizes overexposure

2. **Perfect fitness with low awareness** — Instant death
   - The Decision Tree's root split on awareness overrides everything
   - You can sprint, but if you don't see them coming, it's over

3. **High specialist skills (10+) with low fitness** — Zombie Snack
   - You know how to fix a generator but can't run to it

---

## 📈 Model Behavior

### Prediction Floor
- **Minimum prediction:** ~0.1 days
- Lowest-awareness, lowest-fitness profiles get classified as Zombie Snack instantly

### Prediction Ceiling
- **Maximum prediction:** ~365 days
- Based on training data range (best outcome was 365.0 days — one full year)

---

## 💡 How to Optimize Your Score

### Starting from Average Profile (5/5/3/5/2/5)

**To reach Apex Survivor:**
1. **Awareness:** 5 → **9.5** (most important!)
2. **Fitness:** 5 → **9** (critical)
3. **Resourcefulness:** 5 → **8** (important)
4. **Leadership:** 5 → **9** (helpful)
5. **Specialist Skills:** 3 → **7** (sweet spot)
6. **Scouting Frequency:** 2 → **5** (moderate is best)

---

## 🔬 Technical Notes

- **Models Used:** Decision Tree Classifier + Polynomial Ridge Regression
- **Training Data:** 80+ balanced records
- **Polynomial Degree:** 2 (includes feature interactions like fitness × awareness)
- **Regularization:** Alpha = 1.5 (prevents overfitting)
- **Outcome Categories:** Apex Survivor, Scavenger, The Bait, Zombie Snack

---

## 📝 Educational Value

This analysis demonstrates:
- **Feature importance** in ML models
- **Diminishing returns** (maxing everything ≠ best result)
- **Sweet spots** in input ranges
- **Model limitations** (prediction floor/ceiling)
- **Feature interactions** (fitness × awareness synergy)

Perfect for teaching students about:
- How ML models make decisions
- Why data quality matters
- Feature engineering and interactions
- Model interpretation

---

*Generated from analysis of the Zombie Survival Simulator ML application*
*Dataset: 80+ records | Models: Decision Tree + Polynomial Ridge Regression*
