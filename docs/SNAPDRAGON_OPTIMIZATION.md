# Optimizing Snapskiee for Qualcomm Snapdragon Hexagon NPU

This guide details how **Snapskiee** leverages Qualcomm hardware acceleration, specifically targeting the **Snapdragon X Elite** and **Snapdragon X Plus** platforms.

---

## 1. The Hexagon NPU Advantage (45 TOPS)

Traditional AI applications run either in the cloud or rely on high-wattage discrete GPUs (consuming 45W - 100W+). 

On Snapdragon-powered HP PCs, the dedicated **Hexagon NPU** delivers **up to 45 TOPS** of AI compute at a fraction of the thermal and electrical footprint (under 3W sustained).

### Core Benefits for Snapskiee:
| Metric | Traditional x86 / dGPU | Snapdragon Hexagon NPU |
| :--- | :--- | :--- |
| **Typical Inference Power** | 35W - 80W | **1.2W - 2.8W** |
| **Fan Noise & Thermals** | Audible fan spin / warm chassis | **Completely silent & cool** |
| **Battery Life Impact** | Drains in 2-3 hours of AI use | **All-day battery longevity** |
| **Latency Consistency** | Variable under CPU thread load | **Deterministic hardware priority** |

---

## 2. Execution Stack: Qualcomm QNN & ONNX Runtime

Snapskiee interfaces with the NPU using **ONNX Runtime** configured with the **Qualcomm Neural Network (QNN) Execution Provider**:

```
[Snapskiee Python Core]
         │
         ▼
[ONNX Runtime 1.17+ ARM64]
         │
         ▼
[QNNExecutionProvider (libQnnOnnx.dll)]
         │
         ▼
[Qualcomm Neural Processing SDK / Hexagon HTP Backend]
         │
         ▼
[Snapdragon X Hexagon NPU Silicon]
```

### Session Configuration in Snapskiee:
In `snapskiee/engine/npu_runtime.py`, the session dynamically registers the QNN backend:
```python
providers = [
    ("QNNExecutionProvider", {
        "backend_path": "QnnHtp.dll",  # Hexagon Tensor Processor
        "htp_performance_mode": "burst",
        "enable_fp16_precision": True
    }),
    "DmlExecutionProvider",
    "CPUExecutionProvider"
]
```

---

## 3. Recommended Qualcomm AI Hub Models
Snapskiee is designed to pair seamlessly with models from the [Qualcomm AI Hub](https://aihub.qualcomm.com):
1. **Llama-3.2-3B-Instruct (W4A16 QNN)** - Context synthesis & action item extraction.
2. **All-MiniLM-L6-v2 (INT8 QNN)** - Sentence embedding calculation for vector memory.
3. **MobileCLIP-S2 (INT8 QNN)** - Multimodal visual recognition and slide comprehension.
