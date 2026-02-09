import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import FancyBboxPatch, Ellipse  # Added Ellipse here


def generate_three_tier_architecture():
    """Generate Three-Tier Microservices Architecture diagram"""

    OUTPUT_DIR = Path("model_visualizations")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Create the diagram
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Title
    ax.text(0.5, 0.97, 'Three-Tier Microservices Architecture',
            fontsize=18, fontweight='bold', ha='center', color='#1E3A8A')

    ax.text(0.5, 0.94, 'Heart Disease Prediction System',
            fontsize=14, ha='center', color='#374151')

    # ------------------------------------------------------------
    # 1. TIER 1: PRESENTATION TIER (Frontend)
    # ------------------------------------------------------------
    ax.text(0.5, 0.88, 'TIER 1: PRESENTATION LAYER',
            fontsize=12, fontweight='bold', ha='center', color='#2563EB',
            bbox=dict(boxstyle='round', facecolor='#EFF6FF', edgecolor='#3B82F6', pad=0.3))

    # Frontend Services
    presentation_services = [
        {
            'name': 'User Interface',
            'x': 0.25, 'y': 0.8,
            'icon': '👤',
            'details': ['React.js', 'Tailwind CSS', 'Medical UI', 'Real-time Updates'],
            'color': '#DBEAFE'
        },
        {
            'name': 'API Gateway',
            'x': 0.5, 'y': 0.8,
            'icon': '🚪',
            'details': ['Request Routing', 'Load Balancing', 'Rate Limiting', 'CORS Handling'],
            'color': '#BFDBFE'
        },
        {
            'name': 'Authentication',
            'x': 0.75, 'y': 0.8,
            'icon': '🔐',
            'details': ['JWT Tokens', 'User Sessions', 'Role Management', 'Security'],
            'color': '#93C5FD'
        }
    ]

    # Draw presentation tier services
    for service in presentation_services:
        # Service box - using FancyBboxPatch for rounded corners
        rect = FancyBboxPatch((service['x'] - 0.1, service['y'] - 0.08),
                              0.2, 0.16,
                              facecolor=service['color'], edgecolor='#1E40AF',
                              linewidth=2, alpha=0.9, zorder=1,
                              boxstyle="round,pad=0.02")
        ax.add_patch(rect)

        # Icon
        ax.text(service['x'], service['y'] + 0.03, service['icon'],
                ha='center', va='center', fontsize=24, zorder=2)

        # Service name
        ax.text(service['x'], service['y'] - 0.02, service['name'],
                ha='center', va='center', fontsize=10, fontweight='bold',
                color='#1E3A8A', zorder=2)

        # Service details
        for i, detail in enumerate(service['details']):
            y_pos = service['y'] - 0.05 - i * 0.02
            ax.text(service['x'], y_pos, detail,
                    ha='center', va='center', fontsize=7,
                    color='#374151', zorder=2)

    # Arrow: User Interface → API Gateway
    ax.annotate('', xy=(0.5 - 0.1, 0.8), xytext=(0.25 + 0.1, 0.8),
                arrowprops=dict(arrowstyle='->', color='#3B82F6', lw=2, alpha=0.8))
    ax.text(0.375, 0.83, 'HTTP Requests',
            ha='center', va='center', fontsize=8, fontweight='bold', color='#1D4ED8')

    # Arrow: API Gateway → Authentication
    ax.annotate('', xy=(0.75 - 0.1, 0.8), xytext=(0.5 + 0.1, 0.8),
                arrowprops=dict(arrowstyle='->', color='#3B82F6', lw=2, alpha=0.8))
    ax.text(0.625, 0.83, 'Auth Check',
            ha='center', va='center', fontsize=8, fontweight='bold', color='#1D4ED8')

    # ------------------------------------------------------------
    # 2. TIER 2: APPLICATION TIER (Microservices)
    # ------------------------------------------------------------
    ax.text(0.5, 0.65, 'TIER 2: APPLICATION LAYER (Microservices)',
            fontsize=12, fontweight='bold', ha='center', color='#059669',
            bbox=dict(boxstyle='round', facecolor='#ECFDF5', edgecolor='#10B981', pad=0.3))

    # Microservices
    microservices = [
        {
            'name': 'Prediction\nService',
            'x': 0.2, 'y': 0.5,
            'icon': '🧠',
            'details': ['TensorFlow Model', 'Real-time Inference', 'Risk Calculation'],
            'color': '#A7F3D0',
            'api': '/api/predict'
        },
        {
            'name': 'Patient\nService',
            'x': 0.4, 'y': 0.5,
            'icon': '📋',
            'details': ['Patient Records', 'Medical History', 'Data Management'],
            'color': '#6EE7B7',
            'api': '/api/patients'
        },
        {
            'name': 'Analytics\nService',
            'x': 0.6, 'y': 0.5,
            'icon': '📊',
            'details': ['Performance Metrics', 'Usage Statistics', 'Health Monitoring'],
            'color': '#34D399',
            'api': '/api/analytics'
        },
        {
            'name': 'Notification\nService',
            'x': 0.8, 'y': 0.5,
            'icon': '🔔',
            'details': ['Email Alerts', 'SMS Notifications', 'Report Generation'],
            'color': '#10B981',
            'api': '/api/notify'
        }
    ]

    # Draw microservices
    for service in microservices:
        # Service box (hexagon for microservices)
        points = []
        for i in range(6):
            angle = np.pi / 3 * i - np.pi / 6
            px = service['x'] + 0.07 * np.cos(angle)
            py = service['y'] + 0.07 * np.sin(angle)
            points.append((px, py))

        hexagon = plt.Polygon(points, facecolor=service['color'],
                              edgecolor='#047857', linewidth=2, alpha=0.9, zorder=1)
        ax.add_patch(hexagon)

        # Icon
        ax.text(service['x'], service['y'] + 0.02, service['icon'],
                ha='center', va='center', fontsize=20, zorder=2)

        # Service name
        ax.text(service['x'], service['y'] - 0.02, service['name'],
                ha='center', va='center', fontsize=9, fontweight='bold',
                color='#064E3B', zorder=2)

        # API endpoint
        ax.text(service['x'], service['y'] - 0.06, service['api'],
                ha='center', va='center', fontsize=7, fontweight='bold',
                color='#065F46', zorder=2, style='italic')

    # Connect API Gateway to Microservices
    for service in microservices:
        # Arrow from API Gateway to each microservice
        ax.annotate('', xy=(service['x'], 0.5 + 0.07),
                    xytext=(0.5, 0.8 - 0.08),
                    arrowprops=dict(arrowstyle='->', color='#059669', lw=1.5, alpha=0.7,
                                    connectionstyle="arc3,rad=0.2"))

    # ------------------------------------------------------------
    # 3. TIER 3: DATA TIER (Databases)
    # ------------------------------------------------------------
    ax.text(0.5, 0.35, 'TIER 3: DATA LAYER',
            fontsize=12, fontweight='bold', ha='center', color='#7C3AED',
            bbox=dict(boxstyle='round', facecolor='#F5F3FF', edgecolor='#8B5CF6', pad=0.3))

    # Databases
    databases = [
        {
            'name': 'Model\nDatabase',
            'x': 0.25, 'y': 0.2,
            'icon': '🗄️',
            'type': 'TensorFlow Models',
            'tech': 'Keras/HDF5',
            'color': '#DDD6FE'
        },
        {
            'name': 'Patient\nDatabase',
            'x': 0.5, 'y': 0.2,
            'icon': '💾',
            'type': 'SQL Database',
            'tech': 'PostgreSQL',
            'color': '#C4B5FD'
        },
        {
            'name': 'Cache\nDatabase',
            'x': 0.75, 'y': 0.2,
            'icon': '⚡',
            'type': 'In-Memory Cache',
            'tech': 'Redis',
            'color': '#A78BFA'
        }
    ]

    # Draw databases
    for db in databases:
        # Database box (cylinder shape)
        # Main rectangle
        rect = plt.Rectangle((db['x'] - 0.08, db['y'] - 0.06),
                             0.16, 0.12,
                             facecolor=db['color'], edgecolor='#5B21B6',
                             linewidth=2, alpha=0.9, zorder=1)
        ax.add_patch(rect)

        # Top ellipse (for cylinder effect) - FIXED HERE
        ellipse = Ellipse((db['x'], db['y'] + 0.06), 0.16, 0.03,
                          facecolor=db['color'], edgecolor='#5B21B6',
                          linewidth=2, alpha=0.9, zorder=2)
        ax.add_patch(ellipse)

        # Icon
        ax.text(db['x'], db['y'] + 0.02, db['icon'],
                ha='center', va='center', fontsize=20, zorder=3)

        # Database name
        ax.text(db['x'], db['y'] - 0.01, db['name'],
                ha='center', va='center', fontsize=9, fontweight='bold',
                color='#5B21B6', zorder=3)

        # Database type
        ax.text(db['x'], db['y'] - 0.05, f'{db["type"]}\n{db["tech"]}',
                ha='center', va='center', fontsize=7,
                color='#6D28D9', zorder=3)

    # Connect Microservices to Databases
    connections = [
        (0.2, 0.5, 0.25, 0.2, 'Model Storage'),  # Prediction → Model DB
        (0.4, 0.5, 0.5, 0.2, 'Patient Data'),  # Patient → Patient DB
        (0.6, 0.5, 0.75, 0.2, 'Cache Results'),  # Analytics → Cache
        (0.8, 0.5, 0.5, 0.2, 'Store Reports'),  # Notification → Patient DB
    ]

    for x1, y1, x2, y2, label in connections:
        ax.annotate('', xy=(x2, y2 + 0.06),
                    xytext=(x1, y1 - 0.07),
                    arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=1.5, alpha=0.7))

        # Label at midpoint
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y, label,
                ha='center', va='center', fontsize=7, fontweight='bold',
                color='#6D28D9', rotation=-15)

    # ------------------------------------------------------------
    # 4. COMMUNICATION PATTERNS
    # ------------------------------------------------------------
    ax.text(0.5, 0.07, 'Communication Patterns',
            fontsize=11, fontweight='bold', ha='center', color='#DC2626')

    # Communication methods
    comm_methods = [
        ('REST API', 'HTTP/JSON', '#FECACA'),
        ('Message Queue', 'RabbitMQ', '#FCA5A5'),
        ('gRPC', 'Protocol Buffers', '#F87171'),
        ('WebSocket', 'Real-time', '#EF4444')
    ]

    for i, (method, tech, color) in enumerate(comm_methods):
        x_pos = 0.15 + i * 0.25
        y_pos = 0.03

        # Method box - using FancyBboxPatch for rounded corners
        rect = FancyBboxPatch((x_pos - 0.1, y_pos - 0.025),
                              0.2, 0.05,
                              facecolor=color, edgecolor='#B91C1C',
                              linewidth=1, alpha=0.8, zorder=1,
                              boxstyle="round,pad=0.01")
        ax.add_patch(rect)

        # Method name
        ax.text(x_pos, y_pos + 0.008, method,
                ha='center', va='center', fontsize=9, fontweight='bold',
                color='#7F1D1D', zorder=2)

        # Technology
        ax.text(x_pos, y_pos - 0.01, tech,
                ha='center', va='center', fontsize=7,
                color='#991B1B', zorder=2)

    # ------------------------------------------------------------
    # 5. ARCHITECTURE BENEFITS
    # ------------------------------------------------------------
    benefits = """
    Architecture Benefits:
    • Scalability: Each tier scales independently
    • Maintainability: Microservices can be updated separately
    • Resilience: Failure in one service doesn't break entire system
    • Technology Flexibility: Different tech stacks per service
    • Continuous Deployment: Independent CI/CD pipelines
    """

    # Benefits box - using FancyBboxPatch
    benefits_box = FancyBboxPatch((0.03, 0.09), 0.94, 0.08,
                                  facecolor='#FEF3C7', edgecolor='#F59E0B',
                                  linewidth=2, alpha=0.9, zorder=1,
                                  boxstyle="round,pad=0.02")
    ax.add_patch(benefits_box)

    ax.text(0.5, 0.125, benefits, fontsize=8, ha='center', va='center',
            color='#92400E', linespacing=1.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'three_tier_microservices.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("✓ Generated: three_tier_microservices.png")

    # ------------------------------------------------------------
    # SIMPLIFIED VERSION
    # ------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Title
    ax.text(0.5, 0.95, 'Three-Tier Architecture - Simplified View',
            fontsize=16, fontweight='bold', ha='center', color='#1E3A8A')

    # Draw the three tiers with clear separation
    # Tier 1: Presentation - using FancyBboxPatch
    tier1_box = FancyBboxPatch((0.1, 0.75), 0.8, 0.15,
                               facecolor='#EFF6FF', edgecolor='#3B82F6',
                               linewidth=3, alpha=0.7,
                               boxstyle="round,pad=0.02")
    ax.add_patch(tier1_box)
    ax.text(0.5, 0.825, 'TIER 1: PRESENTATION LAYER\n(React Frontend + API Gateway)',
            ha='center', va='center', fontsize=11, fontweight='bold', color='#1D4ED8')

    # Tier 2: Application - using FancyBboxPatch
    tier2_box = FancyBboxPatch((0.1, 0.45), 0.8, 0.15,
                               facecolor='#ECFDF5', edgecolor='#10B981',
                               linewidth=3, alpha=0.7,
                               boxstyle="round,pad=0.02")
    ax.add_patch(tier2_box)
    ax.text(0.5, 0.525, 'TIER 2: APPLICATION LAYER\n(4 Microservices)',
            ha='center', va='center', fontsize=11, fontweight='bold', color='#059669')

    # Tier 3: Data - using FancyBboxPatch
    tier3_box = FancyBboxPatch((0.1, 0.15), 0.8, 0.15,
                               facecolor='#F5F3FF', edgecolor='#8B5CF6',
                               linewidth=3, alpha=0.7,
                               boxstyle="round,pad=0.02")
    ax.add_patch(tier3_box)
    ax.text(0.5, 0.225, 'TIER 3: DATA LAYER\n(3 Databases + Cache)',
            ha='center', va='center', fontsize=11, fontweight='bold', color='#7C3AED')

    # Simple flow arrows
    # Arrow 1: Tier 1 → Tier 2
    ax.annotate('', xy=(0.5, 0.75), xytext=(0.5, 0.6),
                arrowprops=dict(arrowstyle='->', color='#3B82F6', lw=3, alpha=0.9))
    ax.text(0.5, 0.675, 'HTTP Requests',
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#3B82F6', alpha=0.2))

    # Arrow 2: Tier 2 → Tier 3
    ax.annotate('', xy=(0.5, 0.45), xytext=(0.5, 0.3),
                arrowprops=dict(arrowstyle='->', color='#10B981', lw=3, alpha=0.9))
    ax.text(0.5, 0.375, 'Database Queries',
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#10B981', alpha=0.2))

    # Arrow 3: Tier 3 → Tier 2 (Response)
    ax.annotate('', xy=(0.6, 0.6), xytext=(0.6, 0.45),
                arrowprops=dict(arrowstyle='->', color='#8B5CF6', lw=3, alpha=0.9,
                                linestyle='--'))
    ax.text(0.6, 0.525, 'Data Response',
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#8B5CF6', alpha=0.2))

    # Arrow 4: Tier 2 → Tier 1 (Response)
    ax.annotate('', xy=(0.4, 0.825), xytext=(0.4, 0.75),
                arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=3, alpha=0.9,
                                linestyle='--'))
    ax.text(0.4, 0.7875, 'API Response',
            ha='center', va='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#F59E0B', alpha=0.2))

    # Key benefits
    simple_benefits = [
        "• Presentation Tier: User interface and API gateway",
        "• Application Tier: Business logic in microservices",
        "• Data Tier: Persistent storage and caching",
        "• Each tier can scale independently",
        "• Clear separation of concerns"
    ]

    for i, benefit in enumerate(simple_benefits):
        y_pos = 0.1 - i * 0.025
        ax.text(0.1, y_pos, benefit, fontsize=9, color='#374151', va='center')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'three_tier_simple.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("✓ Generated: three_tier_simple.png")
    return True


# Run the function
if __name__ == "__main__":
    generate_three_tier_architecture()