# void.lumin — Antigravity Software

> **A cognitive instrument, not an art generator.**  
> Your face is the only input. Your calm or your chaos drives the physics of the canvas.

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9%2B-green?style=flat-square&logo=opencv)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)

---

## Concept 1 — The Somatic Ghost

**Void Lumin 2.0** is a real-time biometric feedback instrument. It reads your facial micro-expressions every 250ms, maps them to actual neuroscience data (dopamine, serotonin, cortisol, adrenaline, GABA), and uses those chemical proxies as physical laws inside a generative particle simulation.

- **GABA + Serotonin** (calm/focus) → geometric coherence, orbital resonance, sacred geometry
- **Adrenaline + Cortisol** (stress/anger) → chaos vector fields, gravity fracture, turbulent storm

**Calm your face → the storm becomes a cathedral of light.**  
**Let anxiety rise → watch the cosmos shatter into fire.**

---

## What it looks like

| Mode | Description |
|------|-------------|
| **LINE** | Architectural ghost lines emitted from motion vectors |
| **SMOKE** | Diffuse smoke blobs, soft and atmospheric |
| **FUSION** | Live body rendered as a glowing magmatic entity (INFERNO colormap) |
| **QUANTUM** | Body silhouette dissolves into velocity-chromatic light particles |
| **EMOTION** | Full cognitive instrument — heated soul body, glowing anatomical brain inside head, pulsing somatic heart in chest, Generative Chaos Vector Field driven by your detected emotion |

---

## EMOTION Mode — The Full System

### What it renders

```
Your face detected
        │
        ├── Heated Soul Body
        │     INFERNO thermal colormap over your silhouette
        │     Emotion tint blended in (shifts with detected state)
        │     Feathered aura radiates outward in emotion color
        │
        ├── Glowing Anatomical Brain (inside head region)
        │     Left + right cerebral hemispheres
        │     Cerebellum + brain stem
        │     16 gyri fold paths that wiggle organically
        │     13 blinking synapse nodes
        │     Full glow pass — inner light visible through the skull
        │
        ├── Somatic Heart Core (inside chest region)
        │     Pulsing at Adrenaline-driven heartbeat frequency
        │     4 radiating aura rings
        │     6 neural spokes that fire like synaptic bursts
        │
        └── Generative Chaos Vector Field (particle physics)
              ⚡ Adrenaline/Cortisol → curl-noise turbulence
              🌀 GABA/Serotonin → orbital resonance around brain & heart
              💧 Viscosity → GABA slows the storm
              ↑↓ Gravity → Happy particles float up, Sad fall down
```

### Neuroscience data (real literature values)

| Emotion | Key Chemistry | Brain Region | Color |
|---------|--------------|--------------|-------|
| **Happy** | Dopamine ↑↑, Serotonin ↑, Endorphins ↑ | Nucleus Accumbens · VTA · PFC | Warm Gold |
| **Sad** | Serotonin ↓↓, Cortisol ↑, Dopamine ↓ | Anterior Cingulate · Amygdala | Deep Blue |
| **Angry** | Adrenaline ↑↑, Cortisol ↑, GABA ↓ | Amygdala · Hypothalamus · OFC | Crimson |
| **Fear** | Cortisol ↑↑, GABA ↓↓, Adrenaline ↑ | Amygdala · Hippocampus · LC | Deep Violet |
| **Surprise** | Dopamine spike, Norepinephrine ↑ | PFC · Thalamus · Sup. Colliculus | Electric Cyan |
| **Disgust** | Serotonin disruption | Insula · Basal Ganglia · OFC | Bile Green |
| **Neutral** | GABA balanced, Dopamine baseline | PFC (default mode) | Silver |

### BrainHUD panel
Live bottom-right overlay showing:
- Detected emotion + confidence %
- 6 neurotransmitter bars (real relative values from neuroscience literature)
- Active brain region
- Color psychology meaning

---

## Requirements

- Python 3.10+
- Webcam
- ~3 GB disk (TensorFlow for FER emotion detection)

---

## Install & Run

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/void.lumin.git
cd void.lumin

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python somatic_ghost.py
```

> **First launch:** TensorFlow + FER model will download (~500 MB). Subsequent launches are instant.

### Windows (using `py` launcher)

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py somatic_ghost.py
```

---

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Cycle modes: LINE → SMOKE → FUSION → QUANTUM → EMOTION |
| `R` | Hard reset canvas and all particles |
| `F` | Toggle HUD / BrainHUD overlay |
| `B` | Bloom intensity ±0.05 (FUSION mode) |
| `H` | Hallucination pulse ±0.05 |
| `+` / `-` | Sensitivity (motion threshold) |
| `Q` / `ESC` | Quit |

### Tips for best EMOTION mode experience

1. **Stand still for 5 seconds first** — the background subtractor needs to learn the scene
2. **Good lighting on your face** — FER needs a clear face feed
3. **Camera at eye level, ~1–2m away**
4. **Try it**: slowly smile → watch dopamine surge gold. Force a frown → watch serotonin collapse blue. Look shocked → electric cyan burst.
5. **Step out of frame** → brain and heart fade out over 2 seconds. Step back in → they revive.

---

## Architecture

```
Webcam Frame
     │
     ├──► FlowEngine (Farneback Dense Optical Flow)
     │         H×W×2 velocity field, every frame
     │
     ├──► EmotionEngine (background thread — zero UI hitching)
     │         FER detector runs every 12 frames (~250ms)
     │         → EmotionState: dominant emotion + 7 probabilities
     │         → Biometric Interpolation: face bbox lerped at 0.14 speed
     │         → 2-second decay: brain/heart fade when face lost
     │         → Physics proxies computed: chaos, coherence, viscosity,
     │                                     heart_rate, field_freq, gravity
     │
     └──► SomaticRenderer (main thread, target 60 FPS)
               │
               ├── [LINE/SMOKE/FUSION] GhostRenderer
               │
               └── [QUANTUM/EMOTION] SomaticRenderer
                     │
                     ├── MOG2 Background Subtractor → body silhouette
                     │
                     ├── [EMOTION only]
                     │     ├── Heated Soul body (INFERNO + emotion tint + feathered aura)
                     │     ├── Generative Chaos Vector Field (curl-noise driven by Adrenaline/Cortisol)
                     │     ├── Orbital Resonance Field (GABA/Serotonin → sacred geometry pull)
                     │     ├── Brain anatomy (hemispheres, gyri, synapses, glow)
                     │     └── Somatic heart core (adrenaline heartbeat, radiating rings)
                     │
                     └── Particle system (14,000 max particles)
                           Each particle subject to:
                           • Optical flow advection
                           • Chaos vector field force
                           • Orbital resonance force
                           • Viscosity damping
                           • Gravity (emotion-driven)
```

---

## Known Issues / Notes

- **`pkg_resources` warning** — cosmetic only. Fixed internally by importing `fer.fer.FER` directly.
- **TF Lite deprecation warning** — harmless. FER still works correctly.
- **Low FPS on EMOTION mode** — FER runs in a background thread so the main loop stays fast, but older CPUs may see particle simulation slow slightly. Press `R` to reset if particles pile up.
- **macOS camera permissions** — if camera doesn't open, grant Terminal access to the camera in System Preferences → Privacy.

---

## Roadmap

| Concept | Status | Technique |
|---------|--------|-----------|
| **1 — The Somatic Ghost** | ✅ **Done (v2.0)** | Optical flow + FER biometric → chaos physics + organ visualization |
| **2 — Latent Disfigurement** | 🔜 Next | MediaPipe landmarks → StyleGAN latent space walk |
| **3 — The Algorithmic Shadow** | 🔜 Planned | MediaPipe hands → Neural Cellular Automata |
| **Web Version** | 🔜 Planned | face-api.js + Canvas → Vercel deploy, zero install |

---

## License

MIT — use it, fork it, build on it.  
Credit appreciated: **void.lumin — Antigravity Software**

---

*You don't always know what's inside your own brain. This does.*
