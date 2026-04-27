import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
import pickle
import os

class ZombieSurvivalPredictor:
    def __init__(self):
        self.tree_model = DecisionTreeClassifier(
            max_depth=4,
            min_samples_leaf=3,
            random_state=42
        )
        
        self.poly_model = make_pipeline(
            PolynomialFeatures(degree=2),
            Ridge(alpha=1.5)
        )
        
        self.feature_names = [
            'fitness',
            'resourcefulness',
            'specialist_skills',
            'awareness',
            'scouting_freq',
            'leadership'
        ]
        
        self.is_trained = False
        self.training_accuracy = 0
        self.training_error = 0
        self.feature_importance = {}
    
    def train(self, csv_path='data.csv'):
        """Train both models on data from CSV"""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Training data not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        X = df[self.feature_names].values
        y_class = df['outcome'].values
        y_reg = df['days_survived'].values
        
        self.tree_model.fit(X, y_class)
        self.poly_model.fit(X, y_reg)
        
        self.training_accuracy = self.tree_model.score(X, y_class) * 100
        
        y_pred = self.poly_model.predict(X)
        self.training_error = np.mean(np.abs(y_pred - y_reg))
        
        importances = self.tree_model.feature_importances_
        self.feature_importance = {
            name: float(imp) for name, imp in zip(self.feature_names, importances)
        }
        
        self.is_trained = True
        
        return {
            'records': len(df),
            'tree_accuracy': round(self.training_accuracy, 1),
            'poly_error': round(self.training_error, 2),
            'feature_importance': self.feature_importance
        }
    
    def predict(self, data):
        """Make prediction on new data"""
        if not self.is_trained:
            raise ValueError("Models not trained. Call train() first.")
        
        X = np.array([[
            data['fitness'],
            data['resourcefulness'],
            data['specialist_skills'],
            data['awareness'],
            data['scouting_freq'],
            data['leadership']
        ]])
        
        category = self.tree_model.predict(X)[0]
        days = float(self.poly_model.predict(X)[0])
        days = max(0.1, round(days, 1))
        
        probabilities = self.tree_model.predict_proba(X)[0]
        classes = self.tree_model.classes_
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        
        return {
            'category': category,
            'days': days,
            'probabilities': prob_dict
        }
    
    def save_models(self, path='models.pkl'):
        """Save trained models to disk"""
        with open(path, 'wb') as f:
            pickle.dump({
                'tree': self.tree_model,
                'poly': self.poly_model,
                'feature_importance': self.feature_importance,
                'training_accuracy': self.training_accuracy,
                'training_error': self.training_error
            }, f)
    
    def load_models(self, path='models.pkl'):
        """Load trained models from disk"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.tree_model = data['tree']
                self.poly_model = data['poly']
                self.feature_importance = data['feature_importance']
                self.training_accuracy = data['training_accuracy']
                self.training_error = data['training_error']
                self.is_trained = True
            return True
        return False

def explain(data, prediction_result=None):
    """Generate detailed ML-driven explanation for prediction"""
    reasons = []
    
    # Positive factors (help prediction)
    positive_factors = []
    negative_factors = []
    neutral_factors = []
    
    # Analyze each feature with specific thresholds and context
    
    # Fitness (1-10)
    if data['fitness'] >= 8:
        positive_factors.append(f"Outstanding cardio ({data['fitness']}/10) — you can outrun the horde")
    elif data['fitness'] <= 3:
        negative_factors.append(f"Low fitness ({data['fitness']}/10) — the undead will catch you")
    else:
        neutral_factors.append(f"Average fitness ({data['fitness']}/10) — you'll survive a light jog")
    
    # Resourcefulness (1-10)
    if data['resourcefulness'] >= 8:
        positive_factors.append(f"High resourcefulness ({data['resourcefulness']}/10) — you can hotwire a Hilux and fortify a fence")
    elif data['resourcefulness'] <= 3:
        negative_factors.append(f"Low resourcefulness ({data['resourcefulness']}/10) — can you even open a tin can?")
    
    # Awareness (0-10) — MOST IMPORTANT FEATURE
    if data['awareness'] >= 8:
        positive_factors.append(f"Excellent awareness ({data['awareness']}/10) — you see them coming before anyone else")
    elif data['awareness'] >= 5:
        positive_factors.append(f"Decent awareness ({data['awareness']}/10) — you'll notice the obvious ones")
    elif data['awareness'] < 2:
        negative_factors.append(f"Catastrophic awareness ({data['awareness']}/10) — the Root Node killed you instantly")
    elif data['awareness'] < 4.5:
        negative_factors.append(f"Dangerously low awareness ({data['awareness']}/10) — you were scrolling TikTok while a shambler walked up")
    else:
        neutral_factors.append(f"Borderline awareness ({data['awareness']}/10) — keep your head on a swivel")
    
    # Scouting Frequency (0-7)
    if data['scouting_freq'] >= 6:
        negative_factors.append(f"Extreme scouting ({data['scouting_freq']}x/week) — every run is a death lottery")
    elif data['scouting_freq'] >= 3:
        positive_factors.append(f"Regular scouting ({data['scouting_freq']}x/week) — you know where the supplies are")
    elif data['scouting_freq'] <= 1:
        neutral_factors.append(f"Minimal scouting ({data['scouting_freq']}x/week) — safe but starving")
    
    # Specialist Skills (0-15)
    if data['specialist_skills'] >= 8:
        positive_factors.append(f"Many specialist skills ({data['specialist_skills']}) — First Aid, Carpentry, Mechanical know-how")
    elif data['specialist_skills'] >= 4:
        positive_factors.append(f"Some useful skills ({data['specialist_skills']}) — enough to patch a wound or fix a generator")
    elif data['specialist_skills'] <= 1:
        neutral_factors.append(f"Almost no specialist skills ({data['specialist_skills']}) — hope someone in your group does")
    
    # Leadership (1-10)
    if data['leadership'] >= 8:
        positive_factors.append(f"Strong leadership ({data['leadership']}/10) — people follow you into the wasteland")
    elif data['leadership'] <= 3:
        negative_factors.append(f"Low leadership ({data['leadership']}/10) — you're on your own out there")
    
    # Build explanation with ML context
    if prediction_result:
        reasons.append(f"Model Analysis: Decision Tree classified you as '{prediction_result['category']}' with {max(prediction_result['probabilities'].values())*100:.0f}% confidence")
        reasons.append(f"Timeline Prediction: Polynomial Ridge Regression calculated {prediction_result['days']:.1f} days based on feature interactions")
    
    # Add positive factors first
    if positive_factors:
        reasons.append("✓ Strengths:")
        reasons.extend([f"  • {factor}" for factor in positive_factors])
    
    # Add negative factors
    if negative_factors:
        reasons.append("⚠ Watch Out:")
        reasons.extend([f"  • {factor}" for factor in negative_factors])
    
    # Add neutral observations
    if neutral_factors and len(positive_factors) < 2:
        reasons.append("→ Observations:")
        reasons.extend([f"  • {factor}" for factor in neutral_factors])
    
    # Add ML insight about feature importance
    reasons.append("🔬 ML Insight: The model weighs 'awareness' and 'fitness' most heavily. Your Fitness × Resourcefulness synergy affects days exponentially.")
    
    # Fallback if somehow no reasons
    if len(reasons) <= 1:
        reasons.append("Average survivor profile — the model sees nothing remarkable")
    
    return reasons
