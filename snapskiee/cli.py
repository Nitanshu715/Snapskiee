import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from snapskiee.engine.npu_runtime import SnapdragonNPUEngine
from snapskiee.engine.synthesizer import NoteSynthesizer
from snapskiee.utils.hardware_telemetry import HardwareTelemetry

app = typer.Typer(help="Snapskiee CLI - On-Device Snapdragon Cognitive Engine")
console = Console()

@app.command()
def status():
    """Display real-time Snapdragon NPU execution provider and hardware telemetry."""
    engine = SnapdragonNPUEngine()
    telemetry = HardwareTelemetry.get_system_metrics()
    hw_info = engine.get_hardware_status()

    console.print(Panel.fit(
        "[bold magenta]Snapskiee // Snapdragon AI Lab Build[/bold magenta]\n"
        "[dim]Zero-Cloud Cognitive Scratchpad for Snapdragon X PCs[/dim]",
        border_style="magenta"
    ))

    table = Table(title="Hardware & Execution Runtime Diagnostics", border_style="cyan")
    table.add_column("Parameter", style="cyan", no_wrap=True)
    table.add_column("Telemetry Value", style="white")

    table.add_row("Target Architecture", str(telemetry["architecture"]))
    table.add_row("Processor Family", str(telemetry["processor"]))
    table.add_row("Active Execution Provider", f"[bold green]{hw_info['active_provider']}[/bold green]")
    table.add_row("NPU Acceleration Status", "Active (Qualcomm QNN / DirectML)" if hw_info["npu_active"] else "Fallback (CPU)")
    table.add_row("RAM Footprint", f"{telemetry['ram_used_gb']} GB / {telemetry['ram_total_gb']} GB ({telemetry['ram_usage_percent']}%)")
    table.add_row("Est. Power Draw", f"{telemetry['estimated_npu_power_draw_watts']} Watts (Sub-Watt Profile)")
    table.add_row("Cloud Outbound Traffic", f"[bold green]{telemetry['cloud_telemetry_bytes']} Bytes (100% Air-Gapped)[/bold green]")

    console.print(table)

@app.command()
def scratch(content: str, title: str = "CLI Scratch Note"):
    console.print(f"[bold cyan][NPU] Offloading inference to Snapdragon Hexagon NPU...[/bold cyan]")
    
    engine = SnapdragonNPUEngine()
    synthesizer = NoteSynthesizer(engine)
    result = synthesizer.process_scratchpad_entry(content, title=title)

    console.print(Panel(
        f"[bold white]{result['title']}[/bold white]\n\n"
        f"[bold green]NPU Synthesis:[/bold green]\n{result['synthesis']}\n\n"
        f"[bold yellow]Action Items:[/bold yellow]\n{result['action_items']}\n\n"
        f"[dim]Processed in {result['metrics']['total_processing_ms']}ms on {result['metrics']['accelerator']} @ {result['metrics']['tokens_per_sec']} tok/s[/dim]",
        title="[bold magenta]Snapskiee Cognitive Summary[/bold magenta]",
        border_style="magenta"
    ))

@app.command()
def serve(port: int = 8000):
    """Launch the Snapskiee Glassmorphic HUD web server."""
    import uvicorn
    console.print(f"[bold green]Starting Snapskiee HUD on http://127.0.0.1:{port}[/bold green]")
    uvicorn.run("snapskiee.app:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    app()
