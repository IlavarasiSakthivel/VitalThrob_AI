import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import FancyBboxPatch, Rectangle


def generate_clean_preprocessing_pipeline():
    """Generate clean and organized preprocessing pipeline diagram"""

    OUTPUT_DIR = Path("model_visualizations")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Create the diagram
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Set background color
    fig.patch.set_facecolor('#F9FAFB')
    ax.set_facecolor('#F9FAFB')

    # ------------------------------------------------------------
    # 1. HEADER
    # ------------------------------------------------------------
    # Main title
    title_box = FancyBboxPatch((0.05, 0.92), 0.9, 0.06,
                               facecolor='#1E3A8A', edgecolor='#1E40AF',
                               linewidth=2, alpha=0.95,
                               boxstyle="round,pad=0.02")
    ax.add_patch(title_box)

    ax.text(0.5, 0.95, 'Data Preprocessing Pipeline',
            fontsize=18, fontweight='bold', ha='center', color='white')

    ax.text(0.5, 0.93, 'Heart Disease Prediction System',
            fontsize=12, ha='center', color='#BFDBFE')

    # ------------------------------------------------------------
    # 2. PREPROCESSING FLOW (HORIZONTAL LAYOUT)
    # ------------------------------------------------------------
    ax.text(0.5, 0.85, 'Data Transformation Flow',
            fontsize=14, fontweight='bold', ha='center', color='#1E3A8A')

    # Flow steps with cleaner design
    steps = [
        {'x': 0.1, 'y': 0.75, 'icon': '📥', 'title': 'Raw Data',
         'desc': '13 Features\nCSV Format', 'color': '#3B82F6'},
        {'x': 0.3, 'y': 0.75, 'icon': '🧹', 'title': 'Clean',
         'desc': 'Handle Missing\nRemove Outliers', 'color': '#10B981'},
        {'x': 0.5, 'y': 0.75, 'icon': '📊', 'title': 'Split',
         'desc': 'Separate\nNum & Cat', 'color': '#F59E0B'},
        {'x': 0.7, 'y': 0.75, 'icon': '⚙️', 'title': 'Transform',
         'desc': 'Normalize\nEncode', 'color': '#8B5CF6'},
        {'x': 0.9, 'y': 0.75, 'icon': '✅', 'title': 'Ready',
         'desc': 'Model Input\nProcessed', 'color': '#EC4899'}
    ]

    for step in steps:
        # Create a rounded box for each step
        box = FancyBboxPatch((step['x'] - 0.09, step['y'] - 0.08),
                             0.18, 0.16,
                             facecolor='white', edgecolor=step['color'],
                             linewidth=2.5, alpha=0.9,
                             boxstyle="round,pad=0.02")
        ax.add_patch(box)

        # Icon
        ax.text(step['x'], step['y'] + 0.03, step['icon'],
                ha='center', va='center', fontsize=24, color=step['color'])

        # Title
        ax.text(step['x'], step['y'] - 0.01, step['title'],
                ha='center', va='center', fontsize=11, fontweight='bold',
                color=step['color'])

        # Description
        ax.text(step['x'], step['y'] - 0.05, step['desc'],
                ha='center', va='center', fontsize=9, color='#4B5563',
                linespacing=1.3)

    # Arrows between steps
    for i in range(len(steps) - 1):
        x1, y1 = steps[i]['x'], steps[i]['y']
        x2, y2 = steps[i + 1]['x'], steps[i + 1]['y']

        ax.annotate('', xy=(x2 - 0.09, y1), xytext=(x1 + 0.09, y1),
                    arrowprops=dict(arrowstyle='->', color='#6B7280',
                                    lw=2, alpha=0.8, shrinkA=5, shrinkB=5))

        # Arrow label
        label_x = (x1 + x2) / 2
        ax.text(label_x, y1 + 0.05, '→', ha='center', va='center',
                fontsize=16, color='#6B7280', alpha=0.7)

    # ------------------------------------------------------------
    # 3. TRANSFORMATION DETAILS (CLEAN GRID LAYOUT)
    # ------------------------------------------------------------
    # Section header
    section_box = Rectangle((0.05, 0.55), 0.9, 0.18,
                            facecolor='#F3F4F6', edgecolor='#D1D5DB',
                            linewidth=1.5, alpha=0.8)
    ax.add_patch(section_box)

    ax.text(0.5, 0.71, 'Transformation Details',
            fontsize=14, fontweight='bold', ha='center', color='#1E3A8A')

    # Numerical vs Categorical split
    ax.text(0.25, 0.67, '🔢 Numerical Features', fontsize=11,
            fontweight='bold', ha='center', color='#3B82F6')

    num_features = [
        'age (StandardScaler)',
        'blood_pressure (StandardScaler)',
        'cholesterol (StandardScaler)',
        'max_heart_rate (StandardScaler)',
        'st_depression (StandardScaler)'
    ]

    for i, feature in enumerate(num_features):
        y_pos = 0.63 - i * 0.025
        ax.text(0.25, y_pos, f'• {feature}', fontsize=9,
                ha='center', color='#4B5563')

    # Divider line
    ax.plot([0.5, 0.5], [0.58, 0.67], color='#D1D5DB', linewidth=1.5,
            alpha=0.6, linestyle='--')

    ax.text(0.75, 0.67, '🏷️ Categorical Features', fontsize=11,
            fontweight='bold', ha='center', color='#10B981')

    cat_features = [
        'sex (OneHotEncoder)',
        'chest_pain_type (OneHotEncoder)',
        'fasting_blood_sugar (OneHotEncoder)',
        'exercise_angina (OneHotEncoder)',
        'slope_st (OneHotEncoder)'
    ]

    for i, feature in enumerate(cat_features):
        y_pos = 0.63 - i * 0.025
        ax.text(0.75, y_pos, f'• {feature}', fontsize=9,
                ha='center', color='#4B5563')

    # ------------------------------------------------------------
    # 4. CODE SNIPPET (SIMPLE & CLEAN)
    # ------------------------------------------------------------
    ax.text(0.5, 0.51, 'Core Implementation',
            fontsize=14, fontweight='bold', ha='center', color='#7C3AED')

    # Code box
    code_box = FancyBboxPatch((0.05, 0.35), 0.9, 0.15,
                              facecolor='#1F2937', edgecolor='#374151',
                              linewidth=2, alpha=0.95,
                              boxstyle="round,pad=0.02")
    ax.add_patch(code_box)

    # Simple code example
    simple_code = """# Preprocessing Pipeline Setup
numerical_features = ['age', 'bp', 'cholesterol', 'max_hr', 'st_depression']
categorical_features = ['sex', 'chest_pain_type', 'fbs_over_120', 'exercise_angina']

# Create transformers
numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first')

# Combine in ColumnTransformer
preprocessor = ColumnTransformer([
    ('num', numerical_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])

# Use in Pipeline
model_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])"""

    ax.text(0.08, 0.44, simple_code, fontsize=9, ha='left', va='top',
            color='#E5E7EB', fontfamily='monospace', linespacing=1.4)

    # Code highlights
    highlights = [
        (0.07, 0.48, '📋', 'Feature Selection', '#3B82F6'),
        (0.07, 0.42, '⚙️', 'Transformers', '#10B981'),
        (0.07, 0.36, '🔗', 'ColumnTransformer', '#F59E0B'),
        (0.85, 0.36, '📦', 'Pipeline', '#8B5CF6')
    ]

    for x, y, icon, label, color in highlights:
        ax.text(x, y, icon, fontsize=12, color=color, fontweight='bold')
        ax.text(x + 0.02, y, label, fontsize=9, color=color, fontweight='bold',
                va='center')

    # ------------------------------------------------------------
    # 5. BEFORE/AFTER EXAMPLE
    # ------------------------------------------------------------
    ax.text(0.5, 0.28, 'Transformation Example',
            fontsize=14, fontweight='bold', ha='center', color='#DC2626')

    # Before box
    before_box = FancyBboxPatch((0.05, 0.15), 0.425, 0.12,
                                facecolor='white', edgecolor='#3B82F6',
                                linewidth=2, alpha=0.9,
                                boxstyle="round,pad=0.02")
    ax.add_patch(before_box)

    ax.text(0.2625, 0.23, '📄 Before Preprocessing', fontsize=12,
            fontweight='bold', ha='center', color='#3B82F6')

    before_examples = [
        "Age: 55",
        "Sex: Male",
        "BP: 140",
        "Cholesterol: 230"
    ]

    for i, example in enumerate(before_examples):
        y_pos = 0.19 - i * 0.025
        ax.text(0.2625, y_pos, f'• {example}', fontsize=10,
                ha='center', color='#4B5563')

    # Arrow
    ax.text(0.5, 0.2, '⟶', fontsize=28, ha='center', va='center',
            color='#DC2626', fontweight='bold')
    ax.text(0.5, 0.17, 'Transform', fontsize=10, ha='center',
            color='#DC2626', fontweight='bold')

    # After box
    after_box = FancyBboxPatch((0.525, 0.15), 0.425, 0.12,
                               facecolor='white', edgecolor='#10B981',
                               linewidth=2, alpha=0.9,
                               boxstyle="round,pad=0.02")
    ax.add_patch(after_box)

    ax.text(0.7375, 0.23, '✅ After Preprocessing', fontsize=12,
            fontweight='bold', ha='center', color='#10B981')

    after_examples = [
        "Age: -0.25 (Standardized)",
        "Sex: [1, 0] (One-hot)",
        "BP: 1.75 (Standardized)",
        "Cholesterol: 2.1 (Standardized)"
    ]

    for i, example in enumerate(after_examples):
        y_pos = 0.19 - i * 0.025
        ax.text(0.7375, y_pos, f'• {example}', fontsize=10,
                ha='center', color='#4B5563')

    # ------------------------------------------------------------
    # 6. KEY TRANSFORMERS
    # ------------------------------------------------------------
    ax.text(0.5, 0.08, 'Key Transformers Used',
            fontsize=12, fontweight='bold', ha='center', color='#92400E')

    transformers = [
        ('StandardScaler', 'Normalizes to mean=0, std=1', '#3B82F6'),
        ('OneHotEncoder', 'Converts categories to binary', '#10B981'),
        ('SimpleImputer', 'Handles missing values', '#F59E0B'),
        ('RobustScaler', 'Robust to outliers', '#8B5CF6')
    ]

    for i, (name, desc, color) in enumerate(transformers):
        x = 0.15 + (i % 4) * 0.233
        y = 0.03

        # Transformer badge
        badge = FancyBboxPatch((x - 0.1, y - 0.02), 0.2, 0.04,
                               facecolor=color + '20', edgecolor=color,
                               linewidth=1.5, alpha=0.9,
                               boxstyle="round,pad=0.01")
        ax.add_patch(badge)

        ax.text(x, y, name, fontsize=9, ha='center', va='center',
                color=color, fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'preprocessing_pipeline_clean.png',
                dpi=300, bbox_inches='tight', facecolor='#F9FAFB')
    plt.close()

    print("✓ Generated: preprocessing_pipeline_clean.png")

    # ------------------------------------------------------------
    # SIMPLIFIED FLOWCHART VERSION
    # ------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.patch.set_facecolor('#F9FAFB')
    ax.set_facecolor('#F9FAFB')

    # Title
    ax.text(0.5, 0.95, 'Preprocessing Flowchart',
            fontsize=16, fontweight='bold', ha='center', color='#1E3A8A')

    # Vertical flowchart
    flow_steps = [
        (0.5, 0.85, '📥 Input Data\n13 raw features', '#3B82F6'),
        (0.5, 0.7, '🔍 Data Cleaning\nRemove NaNs & outliers', '#10B981'),
        (0.3, 0.55, '🔢 Numerical\nStandardScaler', '#3B82F6'),
        (0.7, 0.55, '🏷️ Categorical\nOneHotEncoder', '#10B981'),
        (0.5, 0.4, '🔗 Combine\nColumnTransformer', '#F59E0B'),
        (0.5, 0.25, '✅ Ready for Model\nProcessed features', '#8B5CF6')
    ]

    for x, y, label, color in flow_steps:
        # Circle for each step
        circle = plt.Circle((x, y), 0.05, facecolor=color + '30',
                            edgecolor=color, linewidth=2.5)
        ax.add_patch(circle)

        # Step label
        ax.text(x, y, label, ha='center', va='center', fontsize=10,
                color='#1F2937', linespacing=1.3, fontweight='bold')

    # Connect with arrows
    connections = [
        ((0.5, 0.8), (0.5, 0.75)),  # Input → Clean
        ((0.5, 0.65), (0.3, 0.6)),  # Clean → Numerical
        ((0.5, 0.65), (0.7, 0.6)),  # Clean → Categorical
        ((0.3, 0.5), (0.4, 0.45)),  # Numerical → Combine
        ((0.7, 0.5), (0.6, 0.45)),  # Categorical → Combine
        ((0.5, 0.35), (0.5, 0.3))  # Combine → Ready
    ]

    for (x1, y1), (x2, y2) in connections:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#6B7280',
                                    lw=2, alpha=0.8, shrinkA=10, shrinkB=10))

    # Legend
    legend_text = """Preprocessing Steps:
    1. Data Loading: Import raw dataset
    2. Cleaning: Handle missing values
    3. Numerical Processing: Scale features
    4. Categorical Processing: Encode labels
    5. Combination: Merge transformations
    6. Output: Ready for ML models"""

    ax.text(0.1, 0.4, legend_text, fontsize=9, ha='left', va='top',
            color='#4B5563', bbox=dict(boxstyle='round', facecolor='white',
                                       edgecolor='#D1D5DB', pad=0.3))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'preprocessing_flowchart.png',
                dpi=300, bbox_inches='tight', facecolor='#F9FAFB')
    plt.close()

    print("✓ Generated: preprocessing_flowchart.png")
    return True


# Run the function
if __name__ == "__main__":
    generate_clean_preprocessing_pipeline()