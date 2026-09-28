import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('assets/diagrams', exist_ok=True)

# 1. ARCHITECTURE FLOWCHART
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor('#0A0D14')
    ax.set_facecolor('#0A0D14')

    boxes = [
        ("Ingestion Layer\n(Notes / Code / Voice)", 0.5, 5.0, '#1E293B', '#38BDF8'),
        ("Presentation Layer\n(Dark Studio HUD / Terminal CLI)", 0.5, 3.8, '#111827', '#E01E37'),
        ("Cognitive Engine\n(NoteSynthesizer & Micro-Vector Memory)", 0.5, 2.6, '#111622', '#10B981'),
        ("Execution Runtime\n(ONNX Runtime + QNN Execution Provider)", 0.5, 1.4, '#1E1B4B', '#A855F7'),
        ("Snapdragon Silicon Layer\n(Qualcomm Hexagon NPU - 45 TOPS)", 0.5, 0.2, '#1E131D', '#E01E37'),
    ]

    for title, x, y, bg, border in boxes:
        rect = patches.FancyBboxPatch((x, y), 9.0, 0.8, boxstyle="round,pad=0.1",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + 4.5, y + 0.4, title, color='#FFFFFF', fontsize=11,
                fontweight='bold', ha='center', va='center')

    # Draw arrows
    for y_arrow in [4.9, 3.7, 2.5, 1.3]:
        ax.annotate('', xy=(5.0, y_arrow - 0.2), xytext=(5.0, y_arrow),
                    arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=2))

    ax.set_xlim(0, 10)
    ax.set_ylim(-0.2, 6.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('assets/diagrams/system_architecture.png', facecolor='#0A0D14')
    plt.close()
    print("Generated system_architecture.png")

# 2. BENCHMARK COMPARISON CHART
def generate_benchmark_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor('#0A0D14')
    ax1.set_facecolor('#111622')
    ax2.set_facecolor('#111622')

    categories = ['Host CPU (Fallback)', 'Qualcomm Hexagon NPU']
    speed = [14.2, 49.8] # tokens/sec
    power = [28.5, 2.4]  # Watts

    # Speed Bar Chart
    bars1 = ax1.bar(categories, speed, color=['#475569', '#10B981'], width=0.5, edgecolor='#38BDF8', linewidth=1)
    ax1.set_title('Inference Throughput (Tokens / Sec)', color='#FFFFFF', fontsize=12, fontweight='bold', pad=12)
    ax1.tick_params(colors='#94A3B8')
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 1.5, f"{yval:.1f} tok/s",
                 ha='center', va='bottom', color='#FFFFFF', fontweight='bold', fontsize=10)
    ax1.set_ylim(0, 60)
    ax1.spines['bottom'].set_color('#1F2637')
    ax1.spines['left'].set_color('#1F2637')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Power Bar Chart
    bars2 = ax2.bar(categories, power, color=['#EF4444', '#10B981'], width=0.5, edgecolor='#E01E37', linewidth=1)
    ax2.set_title('Thermal Power Draw (Watts)', color='#FFFFFF', fontsize=12, fontweight='bold', pad=12)
    ax2.tick_params(colors='#94A3B8')
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 1.0, f"{yval:.1f} W",
                 ha='center', va='bottom', color='#FFFFFF', fontweight='bold', fontsize=10)
    ax2.set_ylim(0, 35)
    ax2.spines['bottom'].set_color('#1F2637')
    ax2.spines['left'].set_color('#1F2637')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig('assets/diagrams/benchmark_charts.png', facecolor='#0A0D14')
    plt.close()
    print("Generated benchmark_charts.png")

# 3. QUALCOMM AI HUB MODEL PIPELINE
def generate_model_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    fig.patch.set_facecolor('#0A0D14')
    ax.set_facecolor('#0A0D14')

    models = [
        ("Llama-3.2-3B-Instruct\n(W4A16 Quantized)", 0.6, 2.5, '#E01E37'),
        ("All-MiniLM-L6-V2\n(INT8 Dense Embedding)", 0.6, 1.3, '#38BDF8'),
        ("MobileCLIP-S2\n(INT8 Vision-Language)", 0.6, 0.1, '#A855F7')
    ]

    tasks = [
        ("Executive Synthesis & Action Items", 6.2, 2.5, '#10B981'),
        ("Local Micro-Vector Memory Index", 6.2, 1.3, '#10B981'),
        ("Diagram & Screen Multimodal OCR", 6.2, 0.1, '#10B981')
    ]

    for title, x, y, border in models:
        r = patches.FancyBboxPatch((x, y), 3.2, 0.9, boxstyle="round,pad=0.1",
                                   facecolor='#111827', edgecolor=border, linewidth=1.5)
        ax.add_patch(r)
        ax.text(x + 1.6, y + 0.45, title, color='#FFFFFF', fontsize=9.5,
                fontweight='bold', ha='center', va='center')

    for title, x, y, border in tasks:
        r = patches.FancyBboxPatch((x, y), 3.4, 0.9, boxstyle="round,pad=0.1",
                                   facecolor='#111622', edgecolor=border, linewidth=1.5)
        ax.add_patch(r)
        ax.text(x + 1.7, y + 0.45, title, color='#FFFFFF', fontsize=9.5,
                fontweight='bold', ha='center', va='center')

    # Draw connectors via Hexagon NPU badge in center
    rect_center = patches.FancyBboxPatch((4.3, 1.1), 1.4, 1.4, boxstyle="round,pad=0.1",
                                        facecolor='#1E131D', edgecolor='#E01E37', linewidth=2)
    ax.add_patch(rect_center)
    ax.text(5.0, 1.8, "Qualcomm\nHexagon\nNPU", color='#E01E37', fontsize=9,
            fontweight='bold', ha='center', va='center')

    for _, _, y, _ in models:
        ax.annotate('', xy=(4.2, 1.8), xytext=(3.9, y + 0.45),
                    arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=1.5))

    for _, _, y, _ in tasks:
        ax.annotate('', xy=(6.1, y + 0.45), xytext=(5.8, 1.8),
                    arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=1.5))

    ax.set_xlim(0, 10)
    ax.set_ylim(-0.2, 3.8)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('assets/diagrams/model_pipeline.png', facecolor='#0A0D14')
    plt.close()
    print("Generated model_pipeline.png")

if __name__ == '__main__':
    generate_architecture_diagram()
    generate_benchmark_chart()
    generate_model_pipeline_diagram()
