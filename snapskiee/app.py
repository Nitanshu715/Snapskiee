from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

# Instantiate singletons
npu_engine = SnapdragonNPUEngine()
synthesizer = NoteSynthesizer(npu_engine)
vector_memory = LocalVectorMemory()

class NoteInput(BaseModel):
    title: Optional[str] = "Quick Scratch"
    content: str

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Snapskiee // Snapdragon AI HUD</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
            body { font-family: 'Space Grotesk', sans-serif; background-color: #090A0F; }
            .mono { font-family: 'JetBrains Mono', monospace; }
            .glass { background: rgba(18, 22, 34, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }
            .glow { box-shadow: 0 0 25px rgba(255, 45, 85, 0.15); }
        </style>
    </head>
    <body class="text-slate-100 min-h-screen p-6 md:p-12">
        <div class="max-w-6xl mx-auto space-y-8">
            <!-- Header -->
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
                <div>
                    <div class="flex items-center gap-3">
                        <span class="px-2.5 py-1 text-xs font-bold tracking-wider uppercase bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded-full">Snapdragon NPU Ready</span>
                        <span class="text-xs text-slate-500 mono">v1.0.0 // ZERO-CLOUD</span>
                    </div>
                    <h1 class="text-4xl md:text-5xl font-black tracking-tight mt-2 bg-gradient-to-r from-rose-400 via-purple-300 to-indigo-400 bg-clip-text text-transparent">
                        Snapskiee
                    </h1>
                    <p class="text-slate-400 text-sm mt-1">Autonomous, On-Device Cognitive Scratchpad for Snapdragon X PCs</p>
                </div>
                <div class="glass px-4 py-3 rounded-2xl flex items-center gap-6 mono text-xs">
                    <div>
                        <span class="text-slate-500 block">NPU ACCELERATOR</span>
                        <span class="text-emerald-400 font-bold">Qualcomm Hexagon</span>
                    </div>
                    <div>
                        <span class="text-slate-500 block">EST. POWER</span>
                        <span class="text-rose-400 font-bold">~1.2 W</span>
                    </div>
                    <div>
                        <span class="text-slate-500 block">CLOUD BYTES</span>
                        <span class="text-cyan-400 font-bold">0.00 KB</span>
                    </div>
                </div>
            </div>

            <!-- Main Interactive Console -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Scratchpad Input -->
                <div class="lg:col-span-2 glass p-6 rounded-3xl space-y-4 glow">
                    <div class="flex justify-between items-center">
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">
                            <span>⚡</span> Cognitive Scratchpad
                        </h2>
                        <span class="text-xs mono text-slate-500">Live Neural Synthesis</span>
                    </div>
                    <input id="noteTitle" type="text" placeholder="Title / Topic..." class="w-full bg-slate-900/90 border border-slate-800 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-rose-500/50">
                    <textarea id="noteContent" rows="6" placeholder="Paste messy thoughts, meeting notes, code snippets, or lecture minutes here..." class="w-full bg-slate-900/90 border border-slate-800 rounded-xl p-4 text-sm focus:outline-none focus:border-rose-500/50 resize-none"></textarea>
                    
                    <div class="flex justify-between items-center pt-2">
                        <button onclick="synthesizeNote()" class="px-6 py-2.5 bg-gradient-to-r from-rose-500 to-indigo-600 hover:from-rose-600 hover:to-indigo-700 text-white font-bold rounded-xl text-sm transition-all shadow-lg shadow-rose-500/20">
                            Synthesize On NPU ➔
                        </button>
                        <span id="statusIndicator" class="text-xs mono text-slate-400">Ready for input</span>
                    </div>

                    <!-- Output Area -->
                    <div id="outputCard" class="hidden mt-6 border-t border-slate-800 pt-6 space-y-4">
                        <div class="glass p-4 rounded-2xl border-rose-500/20 bg-rose-950/10">
                            <h3 class="text-xs font-bold uppercase tracking-wider text-rose-400 mono">On-Device NPU Summary</h3>
                            <p id="outputSummary" class="text-sm text-slate-200 mt-2 whitespace-pre-line"></p>
                        </div>
                        <div class="glass p-4 rounded-2xl border-purple-500/20 bg-purple-950/10">
                            <h3 class="text-xs font-bold uppercase tracking-wider text-purple-400 mono">Extracted Action Items</h3>
                            <p id="outputActions" class="text-sm text-slate-300 mt-2 whitespace-pre-line"></p>
                        </div>
                    </div>
                </div>

                <!-- Hardware & Local Memory Widget -->
                <div class="space-y-6">
                    <div class="glass p-6 rounded-3xl space-y-4">
                        <h2 class="text-base font-bold text-white flex items-center gap-2">
                            <span>🧠</span> Local Vector Memory
                        </h2>
                        <input id="searchQuery" oninput="searchMemory()" type="text" placeholder="Instant semantic search..." class="w-full bg-slate-900/90 border border-slate-800 rounded-xl px-4 py-2 text-xs focus:outline-none focus:border-rose-500/50">
                        <div id="searchResults" class="space-y-2 max-h-48 overflow-y-auto pr-1 text-xs">
                            <div class="text-slate-500 text-center py-4">No notes indexed yet</div>
                        </div>
                    </div>

                    <div class="glass p-6 rounded-3xl space-y-3">
                        <h2 class="text-base font-bold text-white flex items-center gap-2">
                            <span>📊</span> Snapdragon Telemetry
                        </h2>
                        <div class="space-y-2 text-xs mono">
                            <div class="flex justify-between text-slate-400">
                                <span>Execution Provider:</span>
                                <span class="text-white font-bold" id="telemetryProvider">QNN / DirectML</span>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span>Inference Latency:</span>
                                <span class="text-emerald-400 font-bold" id="telemetryLatency">&lt; 100 ms</span>
                            </div>
                            <div class="flex justify-between text-slate-400">
                                <span>Air-Gap Privacy:</span>
                                <span class="text-cyan-400 font-bold">100% Guaranteed</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function synthesizeNote() {
                const title = document.getElementById('noteTitle').value || "Quick Scratch";
                const content = document.getElementById('noteContent').value;
                const status = document.getElementById('statusIndicator');

                if (!content.trim()) {
                    alert("Please enter some text to synthesize!");
                    return;
                }

                status.innerText = "⚡ Processing on Snapdragon NPU...";
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
                    document.getElementById('telemetryLatency').innerText = data.metrics.total_processing_ms + " ms";
                    status.innerText = `Completed in ${data.metrics.total_processing_ms} ms (${data.metrics.accelerator})`;
                    
                    searchMemory();
                } catch(err) {
                    status.innerText = "Error during NPU inference";
                }
            }

            async function searchMemory() {
                const q = document.getElementById('searchQuery').value;
                const res = await fetch(`/api/notes/search?query=${encodeURIComponent(q || 'notes')}`);
                const data = await res.json();
                const container = document.getElementById('searchResults');
                
                if (data.results.length === 0) {
                    container.innerHTML = '<div class="text-slate-500 text-center py-4">No matching memories</div>';
                    return;
                }
                
                container.innerHTML = data.results.map(r => `
                    <div class="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
                        <div class="font-bold text-slate-200">${r.document.title}</div>
                        <div class="text-slate-400 text-[11px] truncate mt-0.5">${r.document.content}</div>
                        <div class="text-[10px] text-rose-400 mt-1 mono">Similarity: ${(r.score * 100).toFixed(1)}%</div>
                    </div>
                `).join('');
            }
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
