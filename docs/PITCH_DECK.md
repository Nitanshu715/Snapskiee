# Snapskiee Hackathon Presentation & Pitch Deck Outline

**Presentation Time:** 3 - 5 Minutes  
**Slide Deck Target:** 7 Slides  

---

### Slide 1: Title & Hook
* **Title:** **Snapskiee**
* **Subtitle:** The Autonomous, Zero-Cloud Cognitive Scratchpad for Snapdragon-Powered HP PCs
* **Speaker:** Nitanshu Tak | Snapdragon AI Lab Build & Present Challenge
* **Visual:** Futuristic glassmorphism logo with Hexagon NPU badge and tagline: *"Zero Cloud. Sub-Watt. Instant Synthesis."*

---

### Slide 2: The Core Problem
* **The "Cloud AI" Dilemma:**
  1. **Latency:** Cloud LLMs take 2–5 seconds over Wi-Fi.
  2. **Privacy Breach:** Copy-pasting sensitive code, research notes, and meeting minutes to remote servers violates company/student privacy.
  3. **Battery Penalty:** Wi-Fi radios and heavy browser tabs drain laptop batteries rapidly.

---

### Slide 3: The Solution — Snapskiee
* An ambient, always-ready cognitive scratchpad running **100% locally** on the Snapdragon Hexagon NPU.
* Drop in messy thoughts, voice memos, or code snippets.
* Instantly extracts:
  * Executive Summary
  * Action Items & Next Steps
  * Auto-Tags & Local Vector Memory Search

---

### Slide 4: System Architecture & Qualcomm AI Hub
* **NPU Offloading:** Direct execution via `QNNExecutionProvider` (Qualcomm Neural Processing SDK).
* **Models Utilized:** Curated, quantized models from Qualcomm AI Hub (`Llama-3.2-3B` & `MiniLM-L6`).
* **Micro-Vector Engine:** Local cosine-similarity memory index without cloud databases.

---

### Slide 5: Performance Benchmarks (NPU vs. CPU)
* **3.5x Faster** token generation speed.
* **5.9x Lower** Time-To-First-Token (TTFT).
* **91.5% Reduction** in power consumption (~2.4W vs ~28.5W).
* **0 Bytes** transmitted outside the device.

---

### Slide 6: Product Demo (CLI & Cyber-HUD)
* *Screenshots / Screen recording:*
  * Modern Cyberpunk Glassmorphic Dashboard (`http://127.0.0.1:8000`).
  * Live Snapdragon Telemetry monitor showing real-time NPU provider status and 0.00 KB outbound traffic.
  * Instant search over local memory bank.

---

### Slide 7: Roadmap & Vision
* **Phase 1 (Current):** On-device text deconstruction, semantic search, and hardware telemetry.
* **Phase 2:** Multimodal screen indexing using `MobileCLIP-S2` on Qualcomm AI Hub.
* **Phase 3:** Hardware expansion with **Arduino UNO Q** sensor telemetry (ambient desk presence and smart triggers).
* **Conclusion:** *"Snapskiee turns Snapdragon HP PCs into self-contained cognitive workstations."*
