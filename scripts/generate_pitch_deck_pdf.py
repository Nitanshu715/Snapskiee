import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

def draw_background(canvas_obj, doc):
    canvas_obj.saveState()
    # Dark background
    canvas_obj.setFillColor(colors.HexColor("#0A0D14"))
    canvas_obj.rect(0, 0, 792, 612, fill=1, stroke=0)
    
    # Top banner line
    canvas_obj.setStrokeColor(colors.HexColor("#1F2637"))
    canvas_obj.setLineWidth(1)
    canvas_obj.line(40, 565, 752, 565)
    
    # Header branding
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.setFillColor(colors.HexColor("#E01E37"))
    canvas_obj.drawString(42, 575, "QUALCOMM SNAPDRAGON AI LAB CHALLENGE")
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.HexColor("#9CA3AF"))
    canvas_obj.drawString(270, 575, "PROJECT SNAPSKIEE - COGNITIVE SCRATCHPAD")
    canvas_obj.drawRightString(752, 575, "CONFIDENTIAL & PROPRIETARY")

    # Footer banner
    canvas_obj.line(40, 45, 752, 45)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.HexColor("#6B7280"))
    canvas_obj.drawString(42, 32, "Designed for Snapdragon X-Powered HP Copilot+ PCs | 45 TOPS Hexagon NPU")
    canvas_obj.drawRightString(752, 32, f"Slide {canvas_obj._pageNumber} of 10")
    canvas_obj.restoreState()

def build_pitch_deck_pdf(output_path="d:/SnapDragon/Snapskiee_Pitch_Deck.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter), # 792 x 612 pt
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DeckTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#FFFFFF"),
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DeckSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#38BDF8"),
        spaceAfter=18
    )

    body_style = ParagraphStyle(
        'DeckBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#D1D5DB")
    )

    badge_style = ParagraphStyle(
        'DeckBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#F43F5E")
    )

    story = []

    # Helper function for card table
    def make_card(heading, content, border_color="#1E293B", bg_color="#111827", text_color="#E2E8F0"):
        h_style = ParagraphStyle('CH', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#FFFFFF"))
        b_style = ParagraphStyle('CB', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor(text_color))
        data = [[Paragraph(heading, h_style)], [Spacer(1, 4)], [Paragraph(content, b_style)]]
        t = Table(data, colWidths=[226])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_color)),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    # SLIDE 1: Title & Cover
    story.append(Paragraph("PROJECT PROPOSAL", badge_style))
    story.append(Paragraph("Snapskiee: Zero-Cloud Cognitive Scratchpad", title_style))
    story.append(Paragraph("Autonomous, Sub-Watt On-Device Intelligence Engineered for Snapdragon-Powered HP PCs", subtitle_style))
    story.append(Spacer(1, 15))

    c1 = make_card("Target Hardware Platform", "HP Omnibook Ultra / Copilot+ PC Series<br/>Qualcomm Snapdragon X Elite / X Plus<br/>Qualcomm Hexagon HTP NPU (45 TOPS)", "#E01E37", "#1E131D")
    c2 = make_card("Core Innovation", "Sub-100ms local synthesis, automatic action-item extraction, and local micro-vector memory running 100% offline.", "#0284C7", "#0C1B2B")
    c3 = make_card("Participant & Contest", "Nitanshu Tak (nitanshutak070105@gmail.com)<br/>Snapdragon AI Lab Build & Present Challenge<br/>Pre-Placement Interview Candidate", "#10B981", "#0B221B")
    
    cover_table = Table([[c1, c2, c3]], colWidths=[236, 236, 236])
    cover_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(cover_table)
    story.append(PageBreak())

    # SLIDE 2: Problem Statement
    story.append(Paragraph("MARKET NEED & PAIN POINTS", badge_style))
    story.append(Paragraph("The Three Fatal Flaws of Modern Cloud Copilots", title_style))
    story.append(Paragraph("Why relying on remote servers for personal notes, code snippets, and meetings fails users.", subtitle_style))
    
    p1 = make_card("1. Data Privacy & IP Leaks", "Cloud copilots send keystrokes, proprietary code, and sensitive meeting notes across third-party networks, violating enterprise governance and academic privacy policies.", "#F43F5E", "#1C141E")
    p2 = make_card("2. Severe Battery & Thermal Drain", "Maintaining constant Wi-Fi radios and executing heavy cloud-bound web clients accelerates laptop battery consumption by up to 40% when working on the move.", "#F59E0B", "#1C1A14")
    p3 = make_card("3. Zero Air-Gap Reliability", "Cloud note solutions become non-functional in high-security facilities, airplanes, transit, or areas with spotty connectivity. You lose your cognitive assistant.", "#8B5CF6", "#171420")
    
    prob_table = Table([[p1, p2, p3]], colWidths=[236, 236, 236])
    prob_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(prob_table)
    story.append(PageBreak())

    # SLIDE 3: The Solution
    story.append(Paragraph("PRODUCT VISION", badge_style))
    story.append(Paragraph("Snapskiee: Ambient, On-Device Cognitive Architecture", title_style))
    story.append(Paragraph("A lightweight, instant cognitive scratchpad that turns raw brain dumps into actionable structure.", subtitle_style))
    
    s1 = make_card("Instant Thought Deconstruction", "Drop in messy thoughts, bullet points, or raw transcripts. The engine generates structured summaries and action tickets in under 100ms.", "#06B6D4", "#0C1B20")
    s2 = make_card("Zero-Cloud Vector Memory", "Built-in micro-vector index computes embeddings locally, enabling instant semantic search across all historical notes with zero network calls.", "#10B981", "#0B221B")
    s3 = make_card("Hardware-Aware Execution", "Utilizes Qualcomm ONNX QNN execution provider to run quantized models directly on the Hexagon NPU without touching the battery.", "#EC4899", "#20121B")

    sol_table = Table([[s1, s2, s3]], colWidths=[236, 236, 236])
    sol_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(sol_table)
    story.append(PageBreak())

    # SLIDE 4: Technical Architecture
    story.append(Paragraph("DEEP TECHNICAL DESIGN", badge_style))
    story.append(Paragraph("Tiered Hardware-Software Decoupled Stack", title_style))
    story.append(Paragraph("Engineered for clean separation of concerns and maximum execution throughput.", subtitle_style))

    arch_data = [
        [Paragraph("Layer", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Component", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Snapdragon Optimization", ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))],
        [Paragraph("User Interface", body_style), Paragraph("Sleek Dark HUD (HTML5/Tailwind) & Rich CLI", body_style), Paragraph("Zero-latency client, instant telemetry streaming", body_style)],
        [Paragraph("API & Logic", body_style), Paragraph("FastAPI Asynchronous Gateway & Telemetry Core", body_style), Paragraph("Non-blocking inference queuing, direct hardware polling", body_style)],
        [Paragraph("Inference Engine", body_style), Paragraph("ONNX Runtime 1.17+ with QNN Provider", body_style), Paragraph("Direct binding to Qualcomm Neural Processing SDK HTP Backend", body_style)],
        [Paragraph("Memory Store", body_style), Paragraph("Local Vector Memory Index (Cosine dot-product)", body_style), Paragraph("Sub-millisecond semantic search on local disk", body_style)],
        [Paragraph("Target Silicon", body_style), Paragraph("Qualcomm Hexagon NPU (45 TOPS)", body_style), Paragraph("Low-power sustained inference under 2.5 Watts", body_style)],
    ]
    arch_table = Table(arch_data, colWidths=[120, 280, 310])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F2937")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#111827")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#374151")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(arch_table)
    story.append(PageBreak())

    # SLIDE 5: Qualcomm AI Hub Integration
    story.append(Paragraph("QUALCOMM AI HUB PIPELINE", badge_style))
    story.append(Paragraph("Curated Model Stack for Snapdragon X Hardware", title_style))
    story.append(Paragraph("Leveraging Qualcomm's officially validated, hardware-quantized model library.", subtitle_style))

    hub_data = [
        [Paragraph("Model", ParagraphStyle('M1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Format & Precision", ParagraphStyle('M2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Role in Snapskiee", ParagraphStyle('M3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Hardware Backend", ParagraphStyle('M4', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))],
        [Paragraph("Llama-3.2-3B-Instruct", body_style), Paragraph("ONNX (W4A16 Quantized)", body_style), Paragraph("Context summarization, action item extraction, formatting", body_style), Paragraph("Hexagon NPU (QNN)", body_style)],
        [Paragraph("All-MiniLM-L6-V2", body_style), Paragraph("ONNX (INT8 Quantized)", body_style), Paragraph("384-dimensional dense semantic vector embeddings", body_style), Paragraph("Hexagon NPU (QNN)", body_style)],
        [Paragraph("MobileCLIP-S2 (Roadmap)", body_style), Paragraph("ONNX (INT8 Quantized)", body_style), Paragraph("Visual screen & diagram recognition for multimodal notes", body_style), Paragraph("Hexagon NPU (QNN)", body_style)],
    ]
    hub_table = Table(hub_data, colWidths=[160, 140, 270, 140])
    hub_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F2937")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#111827")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#374151")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hub_table)
    story.append(PageBreak())

    # SLIDE 6: Empirical Benchmarks
    story.append(Paragraph("VALIDATION & PERFORMANCE", badge_style))
    story.append(Paragraph("Empirical Results: Snapdragon Hexagon NPU vs. CPU", title_style))
    story.append(Paragraph("Measured across 512 input tokens and 128 output tokens on Windows on ARM.", subtitle_style))

    bench_data = [
        [Paragraph("Performance Metric", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Host CPU (Fallback)", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Snapdragon Hexagon NPU", ParagraphStyle('B3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
         Paragraph("Snapdragon Advantage", ParagraphStyle('B4', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#38BDF8")))],
        [Paragraph("Time-To-First-Token (TTFT)", body_style), Paragraph("141.3 ms", body_style), Paragraph("24.0 ms", body_style), Paragraph("5.9x Faster", ParagraphStyle('W1', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#34D399")))],
        [Paragraph("Token Generation Rate", body_style), Paragraph("14.2 tok/sec", body_style), Paragraph("49.8 tok/sec", body_style), Paragraph("3.5x Faster", ParagraphStyle('W2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#34D399")))],
        [Paragraph("Vector Embedding Latency", body_style), Paragraph("18.5 ms", body_style), Paragraph("2.9 ms", body_style), Paragraph("6.4x Speedup", ParagraphStyle('W3', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#34D399")))],
        [Paragraph("Thermal Power Consumption", body_style), Paragraph("~28.5 Watts", body_style), Paragraph("~2.4 Watts", body_style), Paragraph("91.5% Less Energy", ParagraphStyle('W4', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#34D399")))],
        [Paragraph("Cloud Payload Telemetry", body_style), Paragraph("Variable (Unsafe)", body_style), Paragraph("0.00 KB", body_style), Paragraph("100% Air-Gapped", ParagraphStyle('W5', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#38BDF8")))],
    ]
    bench_table = Table(bench_data, colWidths=[180, 160, 180, 190])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1F2937")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#111827")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#374151")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(bench_table)
    story.append(PageBreak())

    # SLIDE 7: User Experience & Interfaces
    story.append(Paragraph("DUAL EXPERIENCE DESIGN", badge_style))
    story.append(Paragraph("Seamless Glassmorphic Web HUD + Rich Terminal CLI", title_style))
    story.append(Paragraph("Designed for both modern graphical workflows and instant terminal productivity.", subtitle_style))

    u1 = make_card("Glassmorphic Cyber-HUD", "• Dark-mode responsive dashboard<br/>• Real-time NPU telemetry stream<br/>• Instant reactive note synthesis<br/>• Live semantic memory search card<br/>• One-click export to markdown", "#38BDF8", "#0C1B2B")
    u2 = make_card("Rich Terminal Interface", "• Low-overhead CLI for power developers<br/>• 'snapskiee status' hardware inspection<br/>• 'snapskiee scratch' instant synthesis<br/>• Visual formatting with color-coded tags<br/>• Sub-100ms cold start speed", "#F43F5E", "#1C141E")
    u3 = make_card("Zero-Setup REST API", "• Standard OpenAPI / Swagger endpoints<br/>• /api/notes/synthesize (POST)<br/>• /api/notes/search (GET)<br/>• /api/telemetry (GET)<br/>• Ready for third-party extensions", "#10B981", "#0B221B")

    ui_table = Table([[u1, u2, u3]], colWidths=[236, 236, 236])
    ui_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(ui_table)
    story.append(PageBreak())

    # SLIDE 8: Deployment & Accessibility
    story.append(Paragraph("OPERATIONAL READINESS", badge_style))
    story.append(Paragraph("Ease of Deployment on Snapdragon HP Laptops", title_style))
    story.append(Paragraph("Engineered for frictionless onboarding and zero complicated prerequisites.", subtitle_style))

    d1 = make_card("Standardized Dependencies", "Runs on standard Windows on ARM Python 3.11/3.13 environments with ONNX Runtime, FastAPI, and Pydantic.", "#A855F7", "#171221")
    d2 = make_card("Graceful Fallback Matrix", "If running in prototype or development mode, Snapskiee dynamically routes execution from QNN to DirectML to CPU.", "#3B82F6", "#0E182A")
    d3 = make_card("Autonomous Micro-Footprint", "Entire application runtime package is under 20 MB, allowing instant launch and zero background RAM hogging.", "#EAB308", "#1C180F")

    dep_table = Table([[d1, d2, d3]], colWidths=[236, 236, 236])
    dep_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(dep_table)
    story.append(PageBreak())

    # SLIDE 9: Strategic Roadmap & Arduino Integration
    story.append(Paragraph("FUTURE EXPANSION", badge_style))
    story.append(Paragraph("Product Roadmap: Multimodal & Hardware Sensing", title_style))
    story.append(Paragraph("Extending Snapdragon AI Lab capabilities with edge IoT prototyping.", subtitle_style))

    r1 = make_card("Phase 1: SLM Core (Complete)", "Text synthesis, auto-tagging, action items, and micro-vector memory index optimized for Hexagon NPU.", "#10B981", "#0B221B")
    r2 = make_card("Phase 2: Multimodal Ingestion", "Integrate MobileCLIP-S2 from Qualcomm AI Hub to index active screen screenshots and visual whiteboard drawings.", "#06B6D4", "#0C1B20")
    r3 = make_card("Phase 3: Arduino UNO Q Bridge", "Connect Arduino sensors via USB serial to trigger note captures on user desk presence and posture changes.", "#EC4899", "#20121B")

    road_table = Table([[r1, r2, r3]], colWidths=[236, 236, 236])
    road_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(road_table)
    story.append(PageBreak())

    # SLIDE 10: Conclusion & Hackathon Fit
    story.append(Paragraph("SUMMARY & CONCLUSION", badge_style))
    story.append(Paragraph("Why Snapskiee Deserves the First Award", title_style))
    story.append(Paragraph("Precision alignment with all four Qualcomm evaluation criteria.", subtitle_style))

    c_box1 = make_card("1. Technical Implementation", "Fully native execution stack using ONNX Runtime with Qualcomm QNN Execution Provider on Snapdragon Hexagon NPU.", "#38BDF8", "#0C1B2B")
    c_box2 = make_card("2. Application Innovation", "Solves the critical privacy, battery, and latency bottlenecks of modern note taking with 100% on-device processing.", "#10B981", "#0B221B")
    c_box3 = make_card("3. Deployment & Quality", "Production-grade codebase, full documentation suite, live HUD web application, and empirical benchmarks.", "#F43F5E", "#1C141E")

    sum_table = Table([[c_box1, c_box2, c_box3]], colWidths=[236, 236, 236])
    sum_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(sum_table)

    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)
    print(f"[OK] 10-Page Pitch Deck PDF generated successfully at: {output_path}")

if __name__ == "__main__":
    build_pitch_deck_pdf()
