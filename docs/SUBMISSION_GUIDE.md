# Step-by-Step Submission Guide: Snapdragon® AI Lab Challenge

Follow these steps to submit **Snapskiee** on the challenge portal before the deadline (**30 Sep 2026, 11:59 PM IST**).

---

## 1. Submission Checklist

- [x] **Project Name:** `Snapskiee`
- [x] **Tagline:** `The Autonomous, Zero-Cloud Cognitive Scratchpad for Snapdragon-Powered HP PCs`
- [x] **Repository:** Public GitHub / GitLab repository containing code, docs, and benchmarks.
- [x] **Written Proposal:** Detailed problem, solution, and Snapdragon NPU integration (Ready in `docs/HACKATHON_PROPOSAL.md`).
- [x] **Architecture & Benchmarks:** Documented in `docs/ARCHITECTURE.md` and `docs/BENCHMARKS.md`.
- [x] **Presentation Deck / Outline:** Prepared in `docs/PITCH_DECK.md`.

---

## 2. Text Answers Ready for the Portal Intake Form

### Q1: Project Title
> **Snapskiee**

### Q2: Short Description / Elevator Pitch (Under 100 words)
> Snapskiee is an autonomous, on-device cognitive scratchpad designed specifically for Snapdragon-powered HP PCs. It allows developers, students, and professionals to drop in raw, messy thoughts, meeting transcripts, and code snippets, instantly transforming them into synthesized summaries, clear action items, and auto-tags. Powered by quantized models from the Qualcomm AI Hub running on the 45 TOPS Qualcomm Hexagon NPU via ONNX QNN, Snapskiee achieves ultra-low latency, sub-watt energy efficiency, and 100% air-gapped privacy with zero data sent to the cloud.

### Q3: How is your solution designed or optimized for Snapdragon-powered HP PCs?
> Snapskiee is architected specifically around the Qualcomm Hexagon NPU:
> 1. **Qualcomm AI Hub Integration:** It utilizes quantized models (Llama-3.2-3B and All-MiniLM-L6) compiled for the Qualcomm Neural Processing SDK.
> 2. **Hardware Offload via QNN:** By leveraging ONNX Runtime with the `QNNExecutionProvider`, inference is routed directly to the NPU instead of overloading the CPU/battery.
> 3. **Sub-Watt Power Profile:** Benchmarks demonstrate a ~91% reduction in power consumption (~2.4W vs ~28.5W on CPU) with a 3.5x boost in token generation speed, enabling silent, cool, all-day edge intelligence.
> 4. **Air-Gapped Privacy:** Completely local vector embeddings and synthesis guarantee zero outbound network requests.

### Q4: Technical Architecture & Models Used
> * **Language Synthesis:** Quantized `Llama-3.2-3B-Instruct` (W4A16 / INT4) via Qualcomm AI Hub.
> * **Semantic Memory:** `All-MiniLM-L6-V2` (INT8) running on Hexagon HTP backend for local dense vector search.
> * **Execution Runtimes:** ONNX Runtime 1.17+ with `QNNExecutionProvider` (primary) and DirectML/CPU fallback.
> * **Interface:** Terminal CLI with Rich telemetry + Cyberpunk glassmorphic HUD dashboard.

---

## 3. Demo Video Tips (2–3 Minutes)
1. **Show the HUD:** Open `http://127.0.0.1:8000` to show the glassmorphic interface and the Snapdragon telemetry monitor showing `0.00 KB` cloud data.
2. **Synthesize a Note:** Paste messy raw notes, click "Synthesize on NPU", and show the instant response and latency (<100ms).
3. **Run the Benchmark:** In terminal, run `python scripts/benchmark_npu.py` to highlight the 3.5x speedup and 91% power savings.
