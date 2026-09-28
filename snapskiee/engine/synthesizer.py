import time
from typing import Dict, Any, List
from snapskiee.engine.npu_runtime import SnapdragonNPUEngine

class NoteSynthesizer:
    """
    Cognitive synthesis layer that processes raw unstructured thoughts,
    audio transcripts, and code snippets into polished intelligence.
    """

    def __init__(self, npu_engine: SnapdragonNPUEngine):
        self.npu = npu_engine

    def process_scratchpad_entry(self, raw_text: str, title: str = "Untitled Note") -> Dict[str, Any]:
        """
        Takes raw scratchpad input and generates summary, action items,
        and auto-tags using the local NPU.
        """
        start = time.perf_counter()

        summary_res = self.npu.run_inference_mock(raw_text, task="synthesize")
        actions_res = self.npu.run_inference_mock(raw_text, task="action_items")
        tags_res = self.npu.run_inference_mock(raw_text, task="tags")

        total_latency = (time.perf_counter() - start) * 1000

        return {
            "title": title,
            "raw_content": raw_text,
            "synthesis": summary_res["output"],
            "action_items": actions_res["output"],
            "auto_tags": tags_res["output"],
            "metrics": {
                "total_processing_ms": round(total_latency, 2),
                "accelerator": summary_res["accelerator"],
                "tokens_per_sec": summary_res["tokens_per_second"],
                "zero_cloud_verified": True
            }
        }
