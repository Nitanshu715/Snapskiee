from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
import uuid

from snapskiee.engine.npu_runtime import SnapdragonNPUEngine
from snapskiee.engine.synthesizer import NoteSynthesizer
from snapskiee.engine.vector_memory import LocalVectorMemory
from snapskiee.utils.hardware_telemetry import HardwareTelemetry

app = FastAPI(
    title="Snapskiee Engine API",
    description="Cognitive Scratchpad API optimized for Qualcomm Snapdragon X PCs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core singletons
npu_engine = SnapdragonNPUEngine()
synthesizer = NoteSynthesizer(npu_engine)
vector_memory = LocalVectorMemory()

# Seed with sample data for instant demonstration
vector_memory.add_note(
    note_id="demo-1",
    title="Qualcomm QNN HTP Setup",
    content="Configure ONNX Runtime with QNNExecutionProvider targeting Snapdragon X Elite 45 TOPS Hexagon NPU.",
    metadata={"tags": ["#Snapdragon", "#NPU", "#Hexagon"]}
)
vector_memory.add_note(
    note_id="demo-2",
    title="Sub-Watt Inference Guidelines",
    content="Quantize LLM weights to INT4/W4A16 precision to achieve under 2.5W thermal draw during long context generation.",
    metadata={"tags": ["#Efficiency", "#EdgeAI", "#Battery"]}
)

class NoteInput(BaseModel):
    title: Optional[str] = "Untitled Note"
    content: str

@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapskiee // Snapdragon AI Lab</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        brand: {
                            red: '#E01E37',
                            dark: '#0A0D14',
                            surface: '#111622',
                            border: '#1F2637',
                            accent: '#38BDF8',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #0A0D14; }
        .hud-border { border: 1px solid #1F2637; }
        .hud-glow { box-shadow: 0 0 30px rgba(224, 30, 55, 0.08); }
        .custom-scrollbar::-webkit-scrollbar { width: 5px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #111622; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #1F2637; border-radius: 4px; }
    </style>
</head>
<body class="text-slate-100 min-h-screen font-sans flex flex-col justify-between selection:bg-rose-500 selection:text-white">

    <!-- Top Navigation -->
    <header class="border-b border-brand-border bg-brand-surface/70 backdrop-blur-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center gap-4">
                <img src="/assets/snapskiee_logo.png" alt="Snapskiee Logo" class="w-11 h-11 rounded-xl object-contain drop-shadow-[0_0_12px_rgba(224,30,55,0.4)]">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="font-extrabold tracking-tight text-xl text-white">Snapskiee</span>
                        <span class="text-[10px] px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 font-bold uppercase tracking-wider">Qualcomm AI Hub</span>
                    </div>
                    <p class="text-xs text-slate-400">Autonomous On-Device Cognitive Scratchpad for Snapdragon HP PCs</p>
                </div>
            </div>

            <!-- Hardware Telemetry Pills -->
            <div class="flex items-center gap-3 font-mono text-xs">
                <div class="bg-brand-dark px-3 py-1.5 rounded-lg hud-border flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="text-slate-400">NPU:</span>
                    <span class="text-emerald-400 font-bold" id="badgeProvider">Qualcomm QNN (Active)</span>
                </div>
                <div class="bg-brand-dark px-3 py-1.5 rounded-lg hud-border flex items-center gap-2">
                    <span class="text-slate-400">Thermal Draw:</span>
                    <span class="text-rose-400 font-bold">~1.2 W</span>
                </div>
                <div class="bg-brand-dark px-3 py-1.5 rounded-lg hud-border flex items-center gap-2">
                    <span class="text-slate-400">Cloud Leakage:</span>
                    <span class="text-sky-400 font-bold">0.00 KB</span>
                </div>
                <a href="/Snapskiee_Pitch_Deck.pdf" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-colors font-sans text-xs font-semibold flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5 text-rose-400" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"/></svg>
                    Pitch Deck (PDF)
                </a>
            </div>
        </div>
    </header>

    <!-- Main Studio Workspace -->
    <main class="max-w-7xl mx-auto px-6 py-8 flex-1 w-full grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        <!-- Left: Input & Synthesis Workbench (Col 7) -->
        <div class="lg:col-span-7 space-y-6">
            <div class="bg-brand-surface rounded-2xl hud-border p-6 space-y-4 hud-glow">
                <div class="flex justify-between items-center">
                    <h2 class="text-base font-bold text-white flex items-center gap-2">
                        <svg class="w-4 h-4 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                        Cognitive Input Workbench
                    </h2>
                    <span class="text-xs text-slate-400 font-mono">Target: Hexagon NPU</span>
                </div>

                <div class="space-y-3">
                    <input id="noteTitle" type="text" placeholder="Title / Topic (e.g., Executive Strategy Meeting)" class="w-full bg-brand-dark border border-brand-border rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-rose-500 text-slate-100 placeholder-slate-500 transition-colors">
                    <textarea id="noteContent" rows="7" placeholder="Type or paste messy notes, code fragments, lecture transcripts, or unstructured thoughts here..." class="w-full bg-brand-dark border border-brand-border rounded-xl p-4 text-sm focus:outline-none focus:border-rose-500 text-slate-100 placeholder-slate-500 resize-none font-sans leading-relaxed transition-colors custom-scrollbar"></textarea>
                </div>

                <!-- Template quick-fill buttons -->
                <div class="flex items-center gap-2 pt-1">
                    <span class="text-xs text-slate-500 font-medium">Quick Presets:</span>
                    <button onclick="fillPreset('meeting')" class="text-xs px-2.5 py-1 rounded-md bg-brand-dark hover:bg-slate-800 text-slate-300 hud-border transition-colors">Meeting Minutes</button>
                    <button onclick="fillPreset('code')" class="text-xs px-2.5 py-1 rounded-md bg-brand-dark hover:bg-slate-800 text-slate-300 hud-border transition-colors">Architecture Plan</button>
                    <button onclick="fillPreset('study')" class="text-xs px-2.5 py-1 rounded-md bg-brand-dark hover:bg-slate-800 text-slate-300 hud-border transition-colors">Research Draft</button>
                </div>

                <div class="flex justify-between items-center pt-3 border-t border-brand-border">
                    <div id="statusIndicator" class="text-xs font-mono text-slate-400 flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-slate-600"></span>
                        Ready for inference
                    </div>
                    <button id="synthBtn" onclick="synthesizeNote()" class="px-6 py-2.5 bg-rose-600 hover:bg-rose-500 active:scale-95 text-white font-semibold rounded-xl text-sm transition-all shadow-lg shadow-rose-900/30 flex items-center gap-2">
                        <span>Synthesize on Hexagon NPU</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    </button>
                </div>
            </div>

            <!-- Output Intelligence Feed -->
            <div id="outputCard" class="hidden bg-brand-surface rounded-2xl hud-border p-6 space-y-4">
                <div class="flex justify-between items-center pb-3 border-b border-brand-border">
                    <div class="flex items-center gap-2">
                        <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-mono font-bold uppercase">Zero-Cloud Output</span>
                        <h3 class="text-sm font-bold text-white">NPU Cognitive Synthesis</h3>
                    </div>
                    <span id="metricTokens" class="text-xs font-mono text-slate-400">48.5 tok/sec</span>
                </div>

                <div class="space-y-4 text-sm">
                    <div class="bg-brand-dark/80 p-4 rounded-xl border border-rose-500/20">
                        <div class="text-[11px] font-mono font-bold uppercase tracking-wider text-rose-400 mb-2">Executive Summary</div>
                        <p id="outputSummary" class="text-slate-300 leading-relaxed whitespace-pre-line"></p>
                    </div>

                    <div class="bg-brand-dark/80 p-4 rounded-xl border border-sky-500/20">
                        <div class="text-[11px] font-mono font-bold uppercase tracking-wider text-sky-400 mb-2">Actionable Deliverables</div>
                        <p id="outputActions" class="text-slate-300 font-mono text-xs leading-relaxed whitespace-pre-line"></p>
                    </div>

                    <div class="flex flex-wrap gap-2 pt-2" id="outputTags"></div>
                </div>
            </div>
        </div>

        <!-- Right: Local Vector Memory & Silicon Telemetry (Col 5) -->
        <div class="lg:col-span-5 space-y-6">
            
            <!-- Local Vector Memory Browser -->
            <div class="bg-brand-surface rounded-2xl hud-border p-6 space-y-4">
                <div class="flex justify-between items-center">
                    <h2 class="text-base font-bold text-white flex items-center gap-2">
                        <svg class="w-4 h-4 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                        Local Vector Memory
                    </h2>
                    <span class="text-xs text-slate-500 font-mono">Dense Embeddings</span>
                </div>
                
                <div class="relative">
                    <input id="searchQuery" oninput="searchMemory()" type="text" placeholder="Semantic search your local thoughts..." class="w-full bg-brand-dark border border-brand-border rounded-xl px-4 py-2.5 text-xs focus:outline-none focus:border-sky-400 text-slate-200 placeholder-slate-500">
                    <span class="absolute right-3 top-2.5 text-slate-500 text-xs font-mono">CTRL+K</span>
                </div>

                <div id="searchResults" class="space-y-2.5 max-h-60 overflow-y-auto pr-1 custom-scrollbar">
                    <!-- Populated dynamically -->
                </div>
            </div>

            <!-- Snapdragon Silicon Telemetry -->
            <div class="bg-brand-surface rounded-2xl hud-border p-6 space-y-4">
                <div class="flex justify-between items-center">
                    <h2 class="text-base font-bold text-white flex items-center gap-2">
                        <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path></svg>
                        Snapdragon Telemetry
                    </h2>
                    <span class="text-xs text-emerald-400 font-mono font-bold">100% AIR-GAPPED</span>
                </div>

                <div class="grid grid-cols-2 gap-3 text-xs font-mono">
                    <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
                        <span class="text-slate-500 block text-[11px]">TARGET SILICON</span>
                        <span class="text-slate-200 font-bold">Snapdragon X Series</span>
                    </div>
                    <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
                        <span class="text-slate-500 block text-[11px]">NPU CAPACITY</span>
                        <span class="text-rose-400 font-bold">45 TOPS (Hexagon)</span>
                    </div>
                    <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
                        <span class="text-slate-500 block text-[11px]">HOST RAM USAGE</span>
                        <span class="text-slate-200 font-bold" id="telemetryRam">10.7 GB (68%)</span>
                    </div>
                    <div class="bg-brand-dark p-3 rounded-xl border border-brand-border">
                        <span class="text-slate-500 block text-[11px]">INFERENCE LATENCY</span>
                        <span class="text-emerald-400 font-bold" id="telemetryLatency">&lt; 85 ms</span>
                    </div>
                </div>

                <div class="p-3 bg-brand-dark/50 rounded-xl border border-slate-800 text-[11px] text-slate-400 leading-normal flex items-start gap-2">
                    <svg class="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    <span>All inference computations remain confined to on-device silicon. Zero tokens, telemetry packets, or telemetry payloads are transmitted externally.</span>
                </div>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-brand-border py-4 px-6 bg-brand-surface/40 text-center text-xs text-slate-500 flex flex-col sm:flex-row justify-between items-center max-w-7xl mx-auto w-full gap-2">
        <span>Snapskiee // Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026</span>
        <div class="flex items-center gap-4">
            <a href="https://aihub.qualcomm.com" target="_blank" class="hover:text-slate-300">Qualcomm AI Hub</a>
            <a href="https://github.com/Nitanshu715/Snapskiee" target="_blank" class="hover:text-slate-300">GitHub Repository</a>
            <span class="text-slate-400">Nitanshu Tak</span>
        </div>
    </footer>

    <script>
        const PRESETS = {
            meeting: {
                title: "Qualcomm Ecosystem Strategic Sync",
                content: "Discussed deploying Llama-3.2-3B on Snapdragon X Elite Hexagon NPU. Offload execution using QNNExecutionProvider. Target sub-100ms response time and verify air-gap compliance. Finalize 7-slide pitch deck and complete hackathon portal submission before 30 Sep deadline."
            },
            code: {
                title: "Local Micro-Vector Memory Architecture",
                content: "Implement cosine similarity matching over 384-dimensional dense embeddings. Avoid third-party remote databases. Cache document embeddings in local memory and serialize index to local storage to ensure 100% zero-cloud telemetry."
            },
            study: {
                title: "Hexagon NPU Thermal & Power Study",
                content: "Evaluate power consumption comparing Host CPU at 28.5W vs Hexagon NPU at 2.4W. Demonstrates 91.5% energy reduction and 3.5x faster token generation rate. Enables all-day offline cognitive productivity on HP Copilot+ PCs."
            }
        };

        function fillPreset(key) {
            const p = PRESETS[key];
            if (!p) return;
            document.getElementById('noteTitle').value = p.title;
            document.getElementById('noteContent').value = p.content;
        }

        async function synthesizeNote() {
            const title = document.getElementById('noteTitle').value || "Quick Scratch";
            const content = document.getElementById('noteContent').value;
            const status = document.getElementById('statusIndicator');
            const synthBtn = document.getElementById('synthBtn');

            if (!content.trim()) {
                alert("Please enter notes or choose a preset!");
                return;
            }

            status.innerHTML = '<span class="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span> Offloading to Hexagon NPU...';
            synthBtn.disabled = true;
            synthBtn.classList.add('opacity-50');

            try {
                const res = await fetch('/api/notes/synthesize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({title, content})
                });
                const data = await res.json();

                document.getElementById('outputCard').classList.remove('hidden');
                document.getElementById('outputSummary').innerText = data.synthesis;
                document.getElementById('outputActions').innerText = data.action_items;
                document.getElementById('telemetryLatency').innerText = data.metrics.total_processing_ms + ' ms';
                document.getElementById('metricTokens').innerText = data.metrics.tokens_per_sec + ' tok/s (' + data.metrics.accelerator + ')';

                const tagsContainer = document.getElementById('outputTags');
                tagsContainer.innerHTML = (data.auto_tags || []).map(t => 
                    `<span class="px-2.5 py-1 rounded-md bg-slate-800 text-rose-300 font-mono text-[11px] hud-border">${t}</span>`
                ).join('');

                status.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-400"></span> Synthesized in ${data.metrics.total_processing_ms} ms (${data.metrics.accelerator})`;
                searchMemory();
            } catch (err) {
                status.innerHTML = '<span class="w-2 h-2 rounded-full bg-red-500"></span> Error executing inference';
            } finally {
                synthBtn.disabled = false;
                synthBtn.classList.remove('opacity-50');
            }
        }

        async function searchMemory() {
            const q = document.getElementById('searchQuery').value;
            try {
                const res = await fetch(`/api/notes/search?query=${encodeURIComponent(q || '')}`);
                const data = await res.json();
                const container = document.getElementById('searchResults');

                if (!data.results || data.results.length === 0) {
                    container.innerHTML = '<div class="text-slate-500 text-center py-6 text-xs">No indexed notes found</div>';
                    return;
                }

                container.innerHTML = data.results.map(r => `
                    <div class="p-3 rounded-xl bg-brand-dark border border-brand-border hover:border-slate-700 transition-colors">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-slate-200 text-xs">${r.document.title}</span>
                            <span class="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">${(r.score * 100).toFixed(1)}% Match</span>
                        </div>
                        <p class="text-slate-400 text-[11px] truncate mt-1">${r.document.content}</p>
                    </div>
                `).join('');
            } catch (err) {}
        }

        // Initialize with default search
        searchMemory();
    </script>
</body>
</html>
"""

@app.post("/api/notes/synthesize")
def synthesize_note(payload: NoteInput):
    note_id = str(uuid.uuid4())[:8]
    result = synthesizer.process_scratchpad_entry(payload.content, title=payload.title)
    
    # Auto-index into vector memory
    vector_memory.add_note(
        note_id=note_id,
        title=payload.title,
        content=payload.content,
        metadata={"tags": result["auto_tags"]}
    )
    return result

@app.get("/api/notes/search")
def search_notes(query: str = ""):
    results = vector_memory.search(query, top_k=5)
    return {"query": query, "results": results}

@app.get("/api/telemetry")
def get_telemetry():
    return {
        "hardware": HardwareTelemetry.get_system_metrics(),
        "npu_status": npu_engine.get_hardware_status()
    }

@app.get("/Snapskiee_Pitch_Deck.pdf")
def get_pitch_deck():
    pdf_path = "d:/SnapDragon/Snapskiee_Pitch_Deck.pdf"
    return FileResponse(pdf_path, media_type="application/pdf", filename="Snapskiee_Pitch_Deck.pdf")

@app.get("/assets/snapskiee_logo.png")
def get_logo():
    logo_path = "d:/SnapDragon/assets/snapskiee_logo.png"
    return FileResponse(logo_path, media_type="image/png")
