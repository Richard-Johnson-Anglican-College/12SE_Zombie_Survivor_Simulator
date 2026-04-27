from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime
from ml_engine import ZombieSurvivalPredictor, explain
import ai_narrator
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

app = Flask(__name__)
predictor = ZombieSurvivalPredictor()

# Color palette matching the zombie UI
COLORS = {
    'primary': '#4ade80',      # zombie green
    'secondary': '#6b7280',    # dim text
    'text': '#e4e4e7',         # light text
    'bg': '#0f1117',           # dark background
    'accent': '#22c55e',       # green accent
    'surface': '#181b23',      # card background
    'red': '#ef4444',          # danger red
}


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for HTML embedding"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100,
                facecolor=fig.get_facecolor(), edgecolor='none')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    return img_str


def generate_polynomial_curve():
    """Generate polynomial regression curve showing awareness vs predicted days"""
    if not predictor.is_trained:
        return None

    # Vary awareness, hold others at average
    awareness_range = np.linspace(0, 10, 60)
    days_predictions = []

    for aw in awareness_range:
        sample = {
            'fitness': 5,
            'resourcefulness': 5,
            'specialist_skills': 3,
            'awareness': float(aw),
            'scouting_freq': 3,
            'leadership': 5
        }
        pred = predictor.predict(sample)
        days_predictions.append(pred['days'])

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.plot(awareness_range, days_predictions, color=COLORS['primary'],
            linewidth=3, label='Polynomial Ridge (degree=2)')
    ax.fill_between(awareness_range, days_predictions,
                    alpha=0.15, color=COLORS['primary'])

    # Add markers for key points
    ax.scatter([1, 5, 9], [
        predictor.predict({'fitness': 5, 'resourcefulness': 5, 'specialist_skills': 3,
                           'awareness': 1, 'scouting_freq': 3, 'leadership': 5})['days'],
        predictor.predict({'fitness': 5, 'resourcefulness': 5, 'specialist_skills': 3,
                           'awareness': 5, 'scouting_freq': 3, 'leadership': 5})['days'],
        predictor.predict({'fitness': 5, 'resourcefulness': 5, 'specialist_skills': 3,
                           'awareness': 9, 'scouting_freq': 3, 'leadership': 5})['days'],
    ], color=COLORS['accent'], s=100, zorder=5, edgecolors=COLORS['text'], linewidths=2)

    ax.set_xlabel('Situational Awareness (0-10)', fontsize=12, color=COLORS['text'])
    ax.set_ylabel('Predicted Days Survived', fontsize=12, color=COLORS['text'])
    ax.set_title('Polynomial Ridge Regression: How Awareness Affects Survival',
                 fontsize=13, color=COLORS['text'], pad=15, fontweight='bold')
    ax.grid(True, alpha=0.15, linestyle='--', color=COLORS['secondary'])
    ax.set_facecolor(COLORS['surface'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['secondary'])
    ax.spines['bottom'].set_color(COLORS['secondary'])
    ax.tick_params(colors=COLORS['text'])
    ax.legend(loc='upper left', frameon=False, fontsize=10, labelcolor=COLORS['text'])

    # Annotation
    ax.annotate('Notice the curve!\n(Not a straight line)',
                xy=(5, days_predictions[30]), xytext=(7, max(days_predictions) * 0.6),
                fontsize=10, color=COLORS['text'],
                arrowprops=dict(arrowstyle='->', color=COLORS['primary']))

    return fig_to_base64(fig)


def generate_decision_tree_chart():
    """Generate visualization of the actual decision tree structure"""
    if not predictor.is_trained:
        return None

    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('white')
    feature_names = ['Fitness', 'Resourceful', 'Skills', 'Awareness', 'Scouting', 'Leadership']

    plot_tree(predictor.tree_model,
              feature_names=feature_names,
              class_names=list(predictor.tree_model.classes_),
              filled=True,
              rounded=True,
              fontsize=9,
              ax=ax,
              proportion=False,
              impurity=False)

    ax.set_title('Decision Tree Structure (Actual sklearn Model)',
                 fontsize=13, color='#1a1a1a', pad=15, fontweight='bold')
    ax.set_facecolor('white')

    return fig_to_base64(fig)


def generate_feature_interaction_chart():
    """Generate 2D heatmap showing how two features interact"""
    if not predictor.is_trained:
        return None

    # Vary fitness and awareness
    fitness_range = np.arange(1, 11)
    awareness_range = np.linspace(0, 10, 11)

    grid = np.zeros((len(fitness_range), len(awareness_range)))

    for i, fit in enumerate(fitness_range):
        for j, aw in enumerate(awareness_range):
            sample = {
                'fitness': int(fit),
                'resourcefulness': 5,
                'specialist_skills': 3,
                'awareness': float(aw),
                'scouting_freq': 3,
                'leadership': 5
            }
            pred = predictor.predict(sample)
            grid[i, j] = pred['days']

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(COLORS['bg'])
    im = ax.imshow(grid, aspect='auto', origin='lower', cmap='RdYlGn',
                   extent=[0, 10, 1, 10])

    ax.set_xlabel('Situational Awareness (0-10)', fontsize=12, color=COLORS['text'])
    ax.set_ylabel('Fitness (1-10)', fontsize=12, color=COLORS['text'])
    ax.set_title('Feature Interaction: Fitness × Awareness → Days Survived',
                 fontsize=13, color=COLORS['text'], pad=15, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Predicted Days Survived', fontsize=11, color=COLORS['text'])
    cbar.ax.tick_params(colors=COLORS['text'])

    ax.set_facecolor(COLORS['surface'])
    ax.tick_params(colors=COLORS['text'])

    return fig_to_base64(fig)

def get_csv_record_count():
    """Get record count from CSV file"""
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        return len(df)
    return 0

@app.route('/')
def index():
    """Main prediction page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        # Get raw input
        data = {
            'fitness': int(request.form.get('fitness', 5)),
            'resourcefulness': int(request.form.get('resourcefulness', 5)),
            'specialist_skills': int(request.form.get('specialist_skills', 3)),
            'awareness': float(request.form.get('awareness', 5)),
            'scouting_freq': int(request.form.get('scouting_freq', 3)),
            'leadership': int(request.form.get('leadership', 5))
        }
        
        # Validate and cap inputs to realistic ranges
        validation_errors = []
        
        if not (1 <= data['fitness'] <= 10):
            validation_errors.append("Fitness must be between 1-10")
            data['fitness'] = max(1, min(10, data['fitness']))
        
        if not (1 <= data['resourcefulness'] <= 10):
            validation_errors.append("Resourcefulness must be between 1-10")
            data['resourcefulness'] = max(1, min(10, data['resourcefulness']))
        
        if not (0 <= data['specialist_skills'] <= 15):
            validation_errors.append("Specialist Skills must be between 0-15")
            data['specialist_skills'] = max(0, min(15, data['specialist_skills']))
        
        if not (0 <= data['awareness'] <= 10):
            validation_errors.append("Awareness must be between 0-10")
            data['awareness'] = max(0, min(10, data['awareness']))
        
        if not (0 <= data['scouting_freq'] <= 7):
            validation_errors.append("Scouting Frequency must be between 0-7")
            data['scouting_freq'] = max(0, min(7, data['scouting_freq']))
        
        if not (1 <= data['leadership'] <= 10):
            validation_errors.append("Leadership must be between 1-10")
            data['leadership'] = max(1, min(10, data['leadership']))
        
        # Warning for risky combinations
        if data['awareness'] < 2 and data['fitness'] >= 7:
            validation_errors.append("Warning: High fitness won't save you with awareness that low!")
        
        if data['scouting_freq'] >= 6:
            validation_errors.append("Warning: Scouting 6+ times/week is extremely risky!")
        
        if not predictor.is_trained:
            if os.path.exists('models.pkl'):
                predictor.load_models()
            else:
                if os.path.exists('data.csv'):
                    predictor.train('data.csv')
                    predictor.save_models()
                else:
                    raise ValueError("No training data found. Please ensure data.csv exists.")
        
        prediction = predictor.predict(data)
        reasons = explain(data, prediction)
        
        return render_template('index.html', 
                             prediction=prediction,
                             reasons=reasons,
                             form_data=data,
                             ai_available=ai_narrator.is_available(),
                             validation_warnings=validation_errors if validation_errors else None)
    
    except Exception as e:
        return render_template('index.html', 
                             error=f"Prediction error: {str(e)}")


@app.route('/ai_narrate', methods=['POST'])
def ai_narrate():
    """Generate a playful AI narrative for a prediction (on-demand)."""
    try:
        payload = request.get_json(silent=True) or {}

        # Validate required fields
        required = ['category', 'days', 'fitness', 'resourcefulness',
                    'specialist_skills', 'awareness', 'scouting_freq',
                    'leadership']
        for field in required:
            if field not in payload:
                return jsonify({
                    'success': False,
                    'message': f'Missing field: {field}'
                })

        result = ai_narrator.generate_narrative(payload)
        return jsonify(result)

    except Exception as e:
        print(f"[/ai_narrate] Error: {e}")
        return jsonify({
            'success': False,
            'message': ai_narrator.FRIENDLY_FAILURE_MESSAGE
        })


@app.route('/admin')
def admin():
    """Admin dashboard with metrics and visualizations"""
    record_count = get_csv_record_count()
    
    if not predictor.is_trained:
        if os.path.exists('models.pkl'):
            predictor.load_models()
        else:
            if record_count > 0 and os.path.exists('data.csv'):
                predictor.train('data.csv')
                predictor.save_models()
    
    last_trained = "Never"
    if os.path.exists('models.pkl'):
        timestamp = os.path.getmtime('models.pkl')
        dt = datetime.fromtimestamp(timestamp)
        last_trained = dt.strftime('%Y-%m-%d %H:%M')
    
    feature_importance = predictor.feature_importance if predictor.is_trained else {}
    
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    feature_labels = {
        'fitness': 'Cardio / Fitness',
        'resourcefulness': 'Resourcefulness',
        'specialist_skills': 'Specialist Skills',
        'awareness': 'Situational Awareness',
        'scouting_freq': 'Scouting Frequency',
        'leadership': 'Leadership / Trust'
    }
    
    chart_data = [
        {
            'label': feature_labels.get(name, name),
            'value': round(importance, 2)
        }
        for name, importance in sorted_features
    ]
    
    # Get actual model parameters to prove ML is real
    model_details = {}
    if predictor.is_trained:
        # Decision Tree details
        tree = predictor.tree_model
        model_details['tree'] = {
            'max_depth': tree.max_depth,
            'min_samples_leaf': tree.min_samples_leaf,
            'n_leaves': tree.get_n_leaves(),
            'n_nodes': tree.tree_.node_count,
            'classes': list(tree.classes_)
        }
        
        # Polynomial Ridge details
        poly_pipeline = predictor.poly_model
        ridge = poly_pipeline.named_steps['ridge']
        poly_features = poly_pipeline.named_steps['polynomialfeatures']
        model_details['ridge'] = {
            'degree': poly_features.degree,
            'alpha': ridge.alpha,
            'n_features_in': ridge.n_features_in_,
            'n_features_out': poly_features.n_output_features_
        }
    
    # Sample prediction to show probabilities (using average profile for mixed probabilities)
    sample_probs = None
    sample_input = None
    sample_category = None
    sample_days = None
    sample_prompt_preview = None
    if predictor.is_trained:
        sample_input = {
            'fitness': 5,
            'resourcefulness': 5,
            'specialist_skills': 3,
            'awareness': 5,
            'scouting_freq': 3,
            'leadership': 5
        }
        sample_pred = predictor.predict(sample_input)
        sample_probs = {k: round(v * 100, 1) for k, v in sample_pred['probabilities'].items()}
        sample_category = sample_pred['category']
        sample_days = sample_pred['days']

        # Build the Stage 3 prompt preview (shows how Stage 1+2 outputs chain into the LLM prompt)
        prompt_payload = {**sample_input,
                          'category': sample_category,
                          'days': sample_days}
        sample_prompt_preview = ai_narrator.build_prompt(prompt_payload)

    # Generate visualization charts
    polynomial_chart = generate_polynomial_curve() if predictor.is_trained else None
    tree_chart = generate_decision_tree_chart() if predictor.is_trained else None
    interaction_chart = generate_feature_interaction_chart() if predictor.is_trained else None

    return render_template('admin.html',
                         record_count=record_count,
                         last_trained=last_trained,
                         tree_accuracy=round(predictor.training_accuracy, 1) if predictor.is_trained else 0,
                         poly_error=round(predictor.training_error, 2) if predictor.is_trained else 0,
                         feature_importance=chart_data,
                         probabilities=sample_probs,
                         model_details=model_details,
                         polynomial_chart=polynomial_chart,
                         tree_chart=tree_chart,
                         interaction_chart=interaction_chart,
                         ai_available=ai_narrator.is_available(),
                         sample_input=sample_input,
                         sample_category=sample_category,
                         sample_days=sample_days,
                         sample_prompt_preview=sample_prompt_preview)

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain models with current CSV data"""
    try:
        record_count = get_csv_record_count()
        
        if record_count < 10:
            return jsonify({
                'success': False,
                'message': f'Not enough data to train. Need at least 10 records, have {record_count}.'
            })
        
        metrics = predictor.train('data.csv')
        predictor.save_models()
        
        return jsonify({
            'success': True,
            'message': f'Models retrained successfully with {record_count} records!',
            'metrics': metrics
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Training failed: {str(e)}'
        })

if __name__ == '__main__':
    if not os.path.exists('data.csv'):
        print("Training data not found!")
        print("Please ensure data.csv exists in the project directory")
        print("You can run 'python seed_data.py' to generate sample data")
    else:
        print(f"[OK] Found data.csv with {get_csv_record_count()} records")
        app.run(debug=True, port=5000)
