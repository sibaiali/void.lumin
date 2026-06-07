"""
╔══════════════════════════════════════════════════════════════════╗
║          void.lumin — Antigravity Software                       ║
║          Concept 1: The Somatic Ghost  [v4 — VOID LUMIN 2.0]     ║
║                                                                  ║
║  A cognitive instrument. Not an art generator.                   ║
║                                                                  ║
║  You are the conductor. Your face, your breath, your calm        ║
║  or your chaos — they are the only inputs the system accepts.    ║
║                                                                  ║
║  GABA + Serotonin  → geometric coherence, orbital resonance,     ║
║                       sacred geometry, crystalline structure.    ║
║  Adrenaline + Cortisol → chaos vector fields, gravity fracture,  ║
║                           turbulence, particle storm.             ║
║                                                                  ║
║  Your detected emotion drives physical laws inside this canvas.  ║
║  Calm your face → the storm becomes a cathedral of light.        ║
║  Let anxiety rise → watch the cosmos shatter into fire.          ║
║                                                                  ║
║  The brain glows inside you. Live.                               ║
╚══════════════════════════════════════════════════════════════════╝

Five render modes  (SPACE to cycle):
  LINE    — architectural ghost lines from motion
  SMOKE   — diffuse smoke blobs
  FUSION  — live body as glowing magmatic entity
  QUANTUM — body silhouette dissolves into light particles
  EMOTION — Full Void Lumin 2.0 cognitive instrument:
               • Heated Soul body (thermal INFERNO colormap)
               • Glowing anatomical brain inside head
               • Pulsing somatic heart core in chest
               • Generative Chaos Vector Field (emotion → physics)
               • Biometric Interpolation Engine (2-second decay)
               • BrainHUD: live neurotransmitter chemistry panel

Controls:
  Q / ESC  — Quit
  SPACE    — Cycle modes
  R        — Hard reset canvas / particles
  F        — Toggle HUD
  B        — Bloom ±0.05 (FUSION)
  H        — Hallucination ±0.05
  +/-      — Sensitivity
"""

import sys
import io
import cv2
import numpy as np
import time
import math
import threading
from enum import Enum, auto
from dataclasses import dataclass, field

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Optional emotion detection ──────────────────────────────────────
# fer's __init__.py may not re-export FER on all installs, and
# fer.fer imports pkg_resources which may be absent even when
# setuptools is installed (editable installs / new pip).
# We patch both issues here before anything else touches sys.modules.
try:
    import sys as _sys
    import types as _types
    try:
        import pkg_resources as _pr  # noqa: F401
    except ImportError:
        _pr = _types.ModuleType('pkg_resources')
        _pr.get_distribution = lambda x: _types.SimpleNamespace(version='0.0.0')
        _pr.DistributionNotFound = Exception
        _sys.modules['pkg_resources'] = _pr

    from fer.fer import FER          # bypass broken fer/__init__.py
    EMOTION_AVAILABLE = True
    print("[EmotionEngine] fer imported OK.")
except Exception as _fer_err:
    EMOTION_AVAILABLE = False
    print(f"[Notice] EMOTION mode unavailable: {_fer_err}")
    print("         Run: py -m pip install fer setuptools")


# ═══════════════════════════════════════════════════════════════════
#  NEUROSCIENCE + COLOR PSYCHOLOGY  (real literature values)
# ═══════════════════════════════════════════════════════════════════

EMOTION_SCIENCE = {
    'happy': {
        'label':           'HAPPY',
        'chemicals': {
            'Dopamine':    0.85,
            'Serotonin':   0.75,
            'Endorphins':  0.70,
            'Cortisol':    0.15,
            'Adrenaline':  0.20,
            'GABA':        0.50,
        },
        'brain_region':    'Nucleus Accumbens · VTA · PFC',
        'color_primary':   (  0, 185, 255),  # warm gold/amber (BGR)
        'color_secondary': (  0, 120, 255),
        'color_name':      'Warm Gold / Solar Amber',
        'color_meaning':   'Outward expansion  ·  vitality  ·  reward',
        'fade_alpha':      0.85,
        'emit_mult':       1.65,
        'vel_scale':       1.25,
        'drift_y':        -0.35,
        'drift_scatter':   0.8,
    },
    'sad': {
        'label':           'SAD',
        'chemicals': {
            'Dopamine':    0.20,
            'Serotonin':   0.15,
            'Endorphins':  0.18,
            'Cortisol':    0.75,
            'Adrenaline':  0.15,
            'GABA':        0.40,
        },
        'brain_region':    'Anterior Cingulate Cortex · Amygdala',
        'color_primary':   (200,  60,  15),  # deep blue
        'color_secondary': (160,  30,   8),
        'color_name':      'Deep Blue / Indigo Dusk',
        'color_meaning':   'Withdrawal  ·  introspection  ·  time slowing',
        'fade_alpha':      0.94,
        'emit_mult':       0.45,
        'vel_scale':       0.55,
        'drift_y':         0.45,
        'drift_scatter':   0.2,
    },
    'angry': {
        'label':           'ANGRY',
        'chemicals': {
            'Dopamine':    0.35,
            'Serotonin':   0.25,
            'Endorphins':  0.20,
            'Cortisol':    0.82,
            'Adrenaline':  0.90,
            'GABA':        0.20,
        },
        'brain_region':    'Amygdala · Hypothalamus · Orbitofrontal Cortex',
        'color_primary':   ( 25,  25, 220),  # crimson red
        'color_secondary': (  0, 100, 255),
        'color_name':      'Crimson / Combustion Orange',
        'color_meaning':   'Explosive activation  ·  threat  ·  heat',
        'fade_alpha':      0.73,
        'emit_mult':       2.30,
        'vel_scale':       1.90,
        'drift_y':         0.0,
        'drift_scatter':   2.0,
    },
    'fear': {
        'label':           'FEAR',
        'chemicals': {
            'Dopamine':    0.25,
            'Serotonin':   0.20,
            'Endorphins':  0.15,
            'Cortisol':    0.88,
            'Adrenaline':  0.80,
            'GABA':        0.12,
        },
        'brain_region':    'Amygdala · Hippocampus · Locus Coeruleus',
        'color_primary':   (185,  25, 110),  # deep violet
        'color_secondary': (220,   0,  75),
        'color_name':      'Deep Violet / Shadow',
        'color_meaning':   'Collapse inward  ·  vigilance  ·  the unknown',
        'fade_alpha':      0.89,
        'emit_mult':       0.80,
        'vel_scale':       0.90,
        'drift_y':         0.25,
        'drift_scatter':   1.2,
    },
    'surprise': {
        'label':           'SURPRISE',
        'chemicals': {
            'Dopamine':    0.92,
            'Serotonin':   0.55,
            'Endorphins':  0.45,
            'Cortisol':    0.30,
            'Adrenaline':  0.65,
            'GABA':        0.35,
        },
        'brain_region':    'Prefrontal Cortex · Thalamus · Superior Colliculus',
        'color_primary':   (255, 230,   0),  # electric cyan / white-hot
        'color_secondary': (255, 255, 200),
        'color_name':      'Electric Cyan / Flash White',
        'color_meaning':   'Novelty shock  ·  pattern break  ·  open attention',
        'fade_alpha':      0.78,
        'emit_mult':       2.60,
        'vel_scale':       2.10,
        'drift_y':        -0.60,
        'drift_scatter':   1.5,
    },
    'disgust': {
        'label':           'DISGUST',
        'chemicals': {
            'Dopamine':    0.20,
            'Serotonin':   0.25,
            'Endorphins':  0.15,
            'Cortisol':    0.55,
            'Adrenaline':  0.30,
            'GABA':        0.45,
        },
        'brain_region':    'Insula · Basal Ganglia · OFC',
        'color_primary':   ( 30, 140,  55),  # bile green / olive
        'color_secondary': ( 20, 100,  35),
        'color_name':      'Bile Green / Olive',
        'color_meaning':   'Rejection  ·  boundary assertion  ·  avoidance',
        'fade_alpha':      0.87,
        'emit_mult':       0.70,
        'vel_scale':       0.80,
        'drift_y':         0.30,
        'drift_scatter':   0.9,
    },
    'neutral': {
        'label':           'NEUTRAL',
        'chemicals': {
            'Dopamine':    0.42,
            'Serotonin':   0.48,
            'Endorphins':  0.40,
            'Cortisol':    0.30,
            'Adrenaline':  0.20,
            'GABA':        0.62,
        },
        'brain_region':    'Prefrontal Cortex (default mode)',
        'color_primary':   (190, 190, 190),  # silver-white
        'color_secondary': (220, 220, 220),
        'color_name':      'Silver / Neutral White',
        'color_meaning':   'Homeostasis  ·  open presence  ·  clear baseline',
        'fade_alpha':      0.88,
        'emit_mult':       1.00,
        'vel_scale':       1.00,
        'drift_y':         0.00,
        'drift_scatter':   0.5,
    },
}

CHEMICAL_ORDER = ['Dopamine', 'Serotonin', 'Endorphins', 'Cortisol', 'Adrenaline', 'GABA']


# ═══════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

class Config:
    CAMERA_INDEX        = 0
    FRAME_WIDTH         = 1280
    FRAME_HEIGHT        = 720
    TARGET_FPS          = 60

    FB_PYR_SCALE        = 0.5
    FB_LEVELS           = 3
    FB_WINSIZE          = 15
    FB_ITERATIONS       = 3
    FB_POLY_N           = 5
    FB_POLY_SIGMA       = 1.2
    FB_FLAGS            = 0

    VELOCITY_THRESHOLD  = 1.2
    VELOCITY_SCALE      = 6.0
    STEP                = 16
    FADE_ALPHA          = 0.88
    LINE_THICKNESS      = 1
    PARTICLE_RADIUS     = 1
    SMOKE_BLUR_KSIZE    = (7, 7)
    SMOKE_BLUR_SIGMA    = 2.0
    GHOST_COLOR_BASE    = (220, 220, 220)
    ACCENT_COLOR        = (180, 160, 255)
    VELOCITY_ACCENT_THR = 8.0

    FUSION_FADE_ALPHA   = 0.80
    FUSION_STEP         = 10
    FUSION_VEL_SCALE    = 8.0
    BLOOM_STRENGTH      = 0.55
    CHROMA_SHIFT        = 3
    EDGE_GLOW_ALPHA     = 1.0
    CLAHE_CLIP          = 3.5
    BLOOM_KSIZE         = (31, 31)
    BLOOM_SIGMA         = 12.0
    HUMAN_ALPHA         = 0.68
    GHOST_ALPHA         = 0.90

    QUANTUM_MAX_PART    = 16000
    QUANTUM_EMIT_BASE   = 90
    QUANTUM_FADE        = 0.83
    QUANTUM_VEL_INF     = 0.06
    QUANTUM_VEL_DECAY   = 0.97
    QUANTUM_LIFE_BASE   = 22
    QUANTUM_LIFE_SPREAD = 18
    BG_HISTORY          = 130
    BG_THRESHOLD        = 45

    # Emotion / Biometric
    EMOTION_DETECT_INTERVAL = 12    # frames between FER calls (faster = more responsive)
    EMOTION_LERP_SPEED      = 0.06  # color transition smoothing
    FACE_BOX_LERP           = 0.14  # bounding box interpolation speed
    FACE_VISIBILITY_LERP    = 0.07  # brain/heart fade-in/out speed
    FACE_DECAY_SECONDS      = 2.0   # seconds before brain fades when face lost

    HALLUCINATION_PERIOD    = 3.5
    HALLUCINATION_STRENGTH  = 0.40

    WINDOW_NAME         = "void.lumin -- The Somatic Ghost"
    SHOW_FPS_DEFAULT    = True


# ═══════════════════════════════════════════════════════════════════
#  RENDER MODES
# ═══════════════════════════════════════════════════════════════════

class RenderMode(Enum):
    LINE    = auto()
    SMOKE   = auto()
    FUSION  = auto()
    QUANTUM = auto()
    EMOTION = auto()


# ═══════════════════════════════════════════════════════════════════
#  CAMERA
# ═══════════════════════════════════════════════════════════════════

class CameraManager:
    def __init__(self, index, width, height):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera at index {index}.")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS,          Config.TARGET_FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE,   1)
        self.width  = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"[Camera] {self.width}x{self.height}")

    def read(self):
        ok, frame = self.cap.read()
        return frame if ok else None

    def release(self):
        self.cap.release()


# ═══════════════════════════════════════════════════════════════════
#  OPTICAL FLOW
# ═══════════════════════════════════════════════════════════════════

class FlowEngine:
    def __init__(self):
        self.prev_gray = None

    def update(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = None
        if self.prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                self.prev_gray, gray, None,
                Config.FB_PYR_SCALE, Config.FB_LEVELS, Config.FB_WINSIZE,
                Config.FB_ITERATIONS, Config.FB_POLY_N, Config.FB_POLY_SIGMA,
                Config.FB_FLAGS,
            )
        self.prev_gray = gray
        return flow


# ═══════════════════════════════════════════════════════════════════
#  BIOMETRIC INTERPOLATION ENGINE  (Void Lumin 2.0 core)
# ═══════════════════════════════════════════════════════════════════

class EmotionState:
    """
    Biometric Interpolation Engine — the stateful, non-blocking bridge
    between raw FER detections and the generative rendering pipeline.

    All values are smoothly lerped so that emotional transitions act
    as fluid multipliers on physical laws, never causing visual jarring.

    Two-second decay: when the user leaves the frame, the brain and
    heart visualizations smoothly dissolve over 2 seconds rather than
    snapping off.
    """

    def __init__(self):
        self.dominant    = 'neutral'
        self.probs       = {k: 0.0 for k in EMOTION_SCIENCE}
        self.probs['neutral'] = 1.0

        sci = EMOTION_SCIENCE['neutral']
        # Smoothly lerped visual parameters
        self._col        = list(sci['color_primary'])
        self._tgt_col    = list(sci['color_primary'])
        self._fade       = sci['fade_alpha']
        self._emit       = sci['emit_mult']
        self._vel        = sci['vel_scale']
        self._drift      = sci['drift_y']
        self._scatter    = sci['drift_scatter']

        # ── Biometric face tracking state ──────────────────────────
        # Raw face bounding box [x, y, w, h] (pixel coords)
        self.face_box        = None    # current lerped box
        self._tgt_face_box   = None    # target box from detection thread
        self.face_visible    = 0.0     # 0.0 = fully hidden, 1.0 = fully visible
        self._tgt_visible    = 0.0     # target visibility
        self._last_face_t    = 0.0     # timestamp of last successful detection

        # ── Derived physics proxies (written in tick(), read by renderer) ──
        # These are the "physical law multipliers" the render engine uses
        self.chaos           = 0.0   # Adrenaline/Cortisol → turbulence intensity
        self.coherence       = 0.0   # GABA/Serotonin → orbital resonance strength
        self.viscosity       = 0.97  # particle damping (higher = calmer)
        self.heart_rate      = 5.0   # beats/s proxy for chest core pulse
        self.field_freq      = 0.005 # spatial frequency of chaos vector field
        self.gravity         = 0.0   # per-emotion vertical pull

    # ──────────────────────────────────────────────────────────────
    #  Called from emotion background thread (with lock held)
    # ──────────────────────────────────────────────────────────────

    def update_detection(self, dominant: str, probs: dict, box=None):
        """Set new emotion target.  box = (x, y, w, h) or None."""
        self.dominant  = dominant
        self.probs     = probs
        sci            = EMOTION_SCIENCE[dominant]
        self._tgt_col  = list(sci['color_primary'])

        if box is not None:
            x, y, w, h = box
            # Sanity-clamp: reject wildly wrong boxes
            if w > 20 and h > 20:
                self._tgt_face_box  = [float(x), float(y), float(w), float(h)]
                self._tgt_visible   = 1.0
                self._last_face_t   = time.perf_counter()

    def mark_no_face(self):
        """Called when a detection frame produces no face."""
        # Do not immediately hide — let decay timer handle it
        pass

    # ──────────────────────────────────────────────────────────────
    #  Called every render frame (main thread, no lock needed)
    # ──────────────────────────────────────────────────────────────

    def tick(self):
        """
        Lerp all visual parameters toward their targets.
        Compute physics proxy values.
        Manage 2-second face decay.
        """
        sci = EMOTION_SCIENCE[self.dominant]
        s   = Config.EMOTION_LERP_SPEED

        # Smooth color & particle params
        for i in range(3):
            self._col[i] += (self._tgt_col[i] - self._col[i]) * s
        self._fade    += (sci['fade_alpha']    - self._fade)    * s
        self._emit    += (sci['emit_mult']     - self._emit)    * s
        self._vel     += (sci['vel_scale']     - self._vel)     * s
        self._drift   += (sci['drift_y']       - self._drift)   * s
        self._scatter += (sci['drift_scatter'] - self._scatter) * s

        # ── 2-second decay ─────────────────────────────────────────
        if self._last_face_t > 0:
            age = time.perf_counter() - self._last_face_t
            if age > Config.FACE_DECAY_SECONDS:
                self._tgt_visible = 0.0

        self.face_visible += (self._tgt_visible - self.face_visible) * Config.FACE_VISIBILITY_LERP

        # ── Lerp bounding box ──────────────────────────────────────
        if self._tgt_face_box is not None:
            if self.face_box is None:
                self.face_box = list(self._tgt_face_box)
            else:
                lk = Config.FACE_BOX_LERP
                for i in range(4):
                    self.face_box[i] += (self._tgt_face_box[i] - self.face_box[i]) * lk

        # ── Derive physics proxies from chemistry ──────────────────
        chems = sci['chemicals']
        adr   = chems.get('Adrenaline', 0.2)
        cor   = chems.get('Cortisol',   0.3)
        ser   = chems.get('Serotonin',  0.5)
        gab   = chems.get('GABA',       0.5)

        self.chaos       = adr * 2.8 + cor * 1.6            # → turbulence
        self.coherence   = ser * 0.65 + gab * 0.35          # → orbital resonance
        self.viscosity   = max(0.84, min(0.995,             # → damping
                               0.94 + ser * 0.03 + gab * 0.02
                                    - adr * 0.07 - cor * 0.03))
        self.heart_rate  = 5.0 + adr * 8.5 + cor * 2.8 - gab * 2.0
        self.field_freq  = 0.005 + adr * 0.018 + cor * 0.006
        self.gravity     = sci['drift_y']

    # ── Properties ────────────────────────────────────────────────

    @property
    def color(self):
        return tuple(int(max(0, min(255, c))) for c in self._col)

    @property
    def fade_alpha(self):   return self._fade
    @property
    def emit_mult(self):    return self._emit
    @property
    def vel_scale(self):    return self._vel
    @property
    def drift_y(self):      return self._drift
    @property
    def scatter(self):      return self._scatter
    @property
    def science(self):      return EMOTION_SCIENCE[self.dominant]
    @property
    def confidence(self):   return self.probs.get(self.dominant, 0.0)
    @property
    def face_is_live(self): return self.face_visible > 0.05 and self.face_box is not None


# ═══════════════════════════════════════════════════════════════════
#  EMOTION ENGINE  (threaded FER — zero main-thread hitching)
# ═══════════════════════════════════════════════════════════════════

class EmotionEngine:
    """
    Non-blocking biometric detection pipeline.
    FER runs in a daemon thread at its own pace.
    The main render loop submits frames and reads results instantly.
    """

    def __init__(self):
        self.active    = EMOTION_AVAILABLE
        self.state     = EmotionState()
        self._lock     = threading.Lock()
        self._pending  = None
        self._frame_n  = 0
        self._running  = True

        if self.active:
            self._detector = FER(mtcnn=False)
            self._thread   = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()
            print("[EmotionEngine] FER ready — running async on background thread.")
        else:
            print("[EmotionEngine] Inactive (fer not installed).")

    def _worker(self):
        while self._running:
            frame = None
            with self._lock:
                if self._pending is not None:
                    frame         = self._pending
                    self._pending = None
            if frame is not None:
                try:
                    results = self._detector.detect_emotions(frame)
                    with self._lock:
                        if results:
                            emotions = results[0]['emotions']
                            dominant = max(emotions, key=emotions.get)
                            box      = results[0]['box']   # (x, y, w, h)
                            self.state.update_detection(dominant, emotions, box)
                        else:
                            self.state.mark_no_face()
                except Exception:
                    pass  # never crash the render loop
            time.sleep(0.006)

    def submit(self, frame: np.ndarray):
        """Submit frame for background detection — non-blocking."""
        self._frame_n += 1
        if self.active and self._frame_n % Config.EMOTION_DETECT_INTERVAL == 0:
            with self._lock:
                self._pending = frame.copy()

    def tick(self):
        """Advance the biometric interpolator — call every render frame."""
        with self._lock:
            self.state.tick()

    def get_state(self) -> EmotionState:
        with self._lock:
            return self.state

    def stop(self):
        self._running = False


# ═══════════════════════════════════════════════════════════════════
#  HUMAN FX  (FUSION mode)
# ═══════════════════════════════════════════════════════════════════

class HumanFX:
    def __init__(self):
        self._clahe = cv2.createCLAHE(clipLimit=Config.CLAHE_CLIP, tileGridSize=(8, 8))

    def apply(self, frame, pulse=0.0, bloom_strength=None):
        if bloom_strength is None:
            bloom_strength = Config.BLOOM_STRENGTH
        gray     = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = self._clahe.apply(gray)
        cf       = cv2.applyColorMap(enhanced, cv2.COLORMAP_INFERNO).astype(np.float32)
        cf       = self._chroma(cf, Config.CHROMA_SHIFT)
        edges    = cv2.Canny(enhanced, 35, 110)
        eg       = cv2.GaussianBlur(edges, (21, 21), 7).astype(np.float32) / 255.0
        el       = np.zeros_like(cf)
        el[:, :, 0] = eg * 255; el[:, :, 1] = eg * 80; el[:, :, 2] = eg * 100
        cf  = np.clip(cf + el * Config.EDGE_GLOW_ALPHA, 0, 255)
        bloom = cv2.GaussianBlur(cf.astype(np.uint8), Config.BLOOM_KSIZE, Config.BLOOM_SIGMA)
        cf  = np.clip(cf + bloom.astype(np.float32) * (bloom_strength + pulse * 0.25), 0, 255)
        if pulse > 0.05:
            wash = np.zeros_like(cf)
            wash[:, :, 0] = 50 * pulse; wash[:, :, 2] = 90 * pulse
            cf = np.clip(cf + wash, 0, 255)
        return cf.astype(np.uint8)

    @staticmethod
    def _chroma(f, s):
        if s <= 0: return f
        r = f.copy(); w = f.shape[1]
        r[:, s:,  2] = f[:, :w - s, 2]
        r[:, :w - s, 0] = f[:, s:, 0]
        return r


# ═══════════════════════════════════════════════════════════════════
#  PARTICLE
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Particle:
    x: float;  y: float
    vx: float; vy: float
    life: int; max_life: int
    color: tuple   # (B, G, R) floats


# ═══════════════════════════════════════════════════════════════════
#  SOMATIC RENDERER  (QUANTUM + EMOTION modes)
# ═══════════════════════════════════════════════════════════════════

class SomaticRenderer:
    """
    Void Lumin 2.0 core render engine.

    QUANTUM mode: velocity-chromatic silhouette particles.

    EMOTION mode: The full cognitive instrument —
      1. Heated Soul body (INFERNO thermal + emotion tint + feathered aura)
      2. Generative Chaos Vector Field (Adrenaline/Cortisol → physics forces)
      3. Orbital Resonance Field (GABA/Serotonin → sacred geometry gravity)
      4. Anatomical Brain Visualization (head region, gyri, synapses, glow)
      5. Somatic Heart Core (chest, adrenaline-driven heartbeat pulse)
      6. Emotion-reactive particle system with full physics simulation
    """

    _MORPH_K = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    def __init__(self, width, height):
        self.width   = width
        self.height  = height
        self.canvas  = np.zeros((height, width, 3), dtype=np.float32)
        self.particles: list[Particle] = []
        self.sensitivity_scale = 1.0
        self._bg     = cv2.createBackgroundSubtractorMOG2(
            history=Config.BG_HISTORY,
            varThreshold=Config.BG_THRESHOLD,
            detectShadows=False)
        self._rng    = np.random.default_rng()
        self._clahe  = cv2.createCLAHE(clipLimit=Config.CLAHE_CLIP, tileGridSize=(8, 8))

    def reset(self):
        self.canvas[:] = 0
        self.particles.clear()
        self._bg = cv2.createBackgroundSubtractorMOG2(
            history=Config.BG_HISTORY,
            varThreshold=Config.BG_THRESHOLD,
            detectShadows=False)

    # ── Main update ────────────────────────────────────────────────

    def update(self, frame, flow, pulse=0.0, emotion_state: EmotionState = None):
        emotion_mode = emotion_state is not None
        t = time.perf_counter()

        # ── Physics parameters ─────────────────────────────────────
        if emotion_mode:
            fade    = emotion_state.fade_alpha
            n_base  = Config.QUANTUM_EMIT_BASE * emotion_state.emit_mult
            drift_y = emotion_state.drift_y
            scatter = emotion_state.scatter
            emo_col = emotion_state.color
            damping = emotion_state.viscosity
            chaos   = emotion_state.chaos * (1.0 + pulse * 1.5)
            freq    = emotion_state.field_freq
            coherence = emotion_state.coherence
        else:
            fade    = Config.QUANTUM_FADE
            n_base  = Config.QUANTUM_EMIT_BASE
            drift_y = 0.0
            scatter = 0.5
            emo_col = None
            damping = Config.QUANTUM_VEL_DECAY
            chaos   = 0.0
            freq    = 0.0
            coherence = 0.0

        # ── Background subtraction → body silhouette ───────────────
        fg = self._bg.apply(frame)
        fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, self._MORPH_K)
        fg = cv2.dilate(fg, self._MORPH_K, iterations=3)

        edges    = cv2.Canny(fg, 50, 150)
        edge_pts = np.column_stack(np.where(edges > 0)) if np.any(edges > 0) else np.empty((0, 2), dtype=np.int32)

        # ── Biometric organ anchor points ──────────────────────────
        brain_cx, brain_cy = 0, 0
        heart_cx, heart_cy = 0, 0
        bw, bh = 0, 0
        face_live = False

        if emotion_mode and emotion_state.face_is_live:
            bx, by, bw, bh = emotion_state.face_box
            bw, bh = max(1, bw), max(1, bh)
            brain_cx = int(bx + bw * 0.5)
            brain_cy = int(by + bh * 0.08)
            brain_cx = max(0, min(self.width  - 1, brain_cx))
            brain_cy = max(0, min(self.height - 1, brain_cy))
            heart_cx = brain_cx
            heart_cy = int(brain_cy + bh * 1.85)
            heart_cx = max(0, min(self.width  - 1, heart_cx))
            heart_cy = max(0, min(self.height - 1, heart_cy))
            face_live = True

        # ── Emit particles ─────────────────────────────────────────
        if flow is not None and len(edge_pts) > 0:
            n_emit = int(n_base * (1.0 + pulse * 2.4))
            n_emit = min(n_emit, len(edge_pts))
            idx    = self._rng.choice(len(edge_pts), n_emit, replace=False)

            for ey, ex in edge_pts[idx]:
                if ex >= flow.shape[1] or ey >= flow.shape[0]:
                    continue
                fx    = float(flow[ey, ex, 0])
                fy    = float(flow[ey, ex, 1])
                speed = math.sqrt(fx * fx + fy * fy)
                if speed < 0.6:
                    continue

                inv = 1.0 / (speed + 1e-6)
                sc  = float(self._rng.uniform(-scatter, scatter))
                vx  = fx * inv + sc
                vy  = fy * inv + float(self._rng.uniform(-0.2, 0.2))
                vel = speed * 0.9 * (emotion_state.vel_scale if emotion_mode else 1.0) \
                      + float(self._rng.uniform(0, 1.8))

                if emotion_mode:
                    br  = min(1.0, 0.4 + speed / 18.0 + pulse * 0.3)
                    col = tuple(min(255.0, emo_col[i] * br) for i in range(3))
                else:
                    tc  = min(1.0, speed / 14.0)
                    br  = min(255.0, 70.0 + speed * 14.0)
                    col = (
                        min(255.0, (160 + tc * 95) * br / 255),
                        min(255.0, tc * 230 * br / 255),
                        min(255.0, (80 - tc * 65) * br / 255),
                    )

                life = int(Config.QUANTUM_LIFE_BASE + speed * 2.5
                           + float(self._rng.uniform(0, Config.QUANTUM_LIFE_SPREAD)))
                self.particles.append(Particle(
                    float(ex), float(ey),
                    vx * vel, vy * vel + drift_y,
                    life, life, col,
                ))

        # ── Fade canvas (persistent trail) ────────────────────────
        self.canvas *= fade

        # ── Simulate & draw particles ──────────────────────────────
        alive = []
        h, w  = self.height, self.width
        hf    = flow is not None

        for p in self.particles:
            ix, iy = int(p.x), int(p.y)

            # 1. Optical flow advection
            if hf and 0 <= iy < flow.shape[0] and 0 <= ix < flow.shape[1]:
                p.vx += flow[iy, ix, 0] * Config.QUANTUM_VEL_INF
                p.vy += flow[iy, ix, 1] * Config.QUANTUM_VEL_INF

            if emotion_mode:
                # ────────────────────────────────────────────────────
                # 2. GENERATIVE CHAOS VECTOR FIELD
                #    Adrenaline/Cortisol fracture the geometry.
                #    Each particle position samples a curl-noise field
                #    whose frequency and amplitude scale with volatility.
                # ────────────────────────────────────────────────────
                if chaos > 0.05:
                    angle = (
                        math.sin(p.x * freq + t * 1.2) +
                        math.cos(p.y * freq - t * 0.9) +
                        math.sin((p.x + p.y) * freq * 0.6 + t * 1.6)
                    ) * math.pi
                    p.vx += math.cos(angle) * chaos * 0.08
                    p.vy += math.sin(angle) * chaos * 0.08

                # ────────────────────────────────────────────────────
                # 3. ORBITAL RESONANCE FIELD (Sacred Geometry Gravity)
                #    GABA/Serotonin pull particles into orbital loops
                #    around the brain and heart anchor points.
                #    Calm = structure. High coherence = cathedral.
                # ────────────────────────────────────────────────────
                if face_live and coherence > 0.15:
                    for (acx, acy) in [(brain_cx, brain_cy), (heart_cx, heart_cy)]:
                        dx   = p.x - acx
                        dy   = p.y - acy
                        dist = math.sqrt(dx * dx + dy * dy) + 1e-5
                        if dist < 380:
                            attract = math.exp(-dist * 0.004)
                            # Tangential (orbit) + radial (pull) components
                            p.vx += (-dy / dist * 0.45 + -dx / dist * 0.10) * coherence * attract
                            p.vy += ( dx / dist * 0.45 + -dy / dist * 0.10) * coherence * attract

                # 4. Gravity (emotion-driven vertical drift)
                p.vy += drift_y * 0.04

            # 5. Viscosity damping (GABA/Serotonin slow the storm)
            p.vx *= damping
            p.vy *= damping

            p.x += p.vx; p.y += p.vy; p.life -= 1
            if p.life <= 0:
                continue
            px, py = int(p.x), int(p.y)
            if not (0 <= px < w and 0 <= py < h):
                continue

            alpha = (p.life / p.max_life) ** 0.6
            cv2.circle(self.canvas, (px, py), 1,
                       (min(255.0, p.color[0] * alpha),
                        min(255.0, p.color[1] * alpha),
                        min(255.0, p.color[2] * alpha)), -1)
            alive.append(p)

        if len(alive) > Config.QUANTUM_MAX_PART:
            alive = alive[-Config.QUANTUM_MAX_PART:]
        self.particles = alive

        # ── Build output ───────────────────────────────────────────
        output = self.canvas.copy()

        if not emotion_mode:
            return np.clip(output, 0, 255).astype(np.uint8)

        # ══════════════════════════════════════════════════════════
        #  EMOTION MODE — HEATED SOUL + ORGANS
        # ══════════════════════════════════════════════════════════

        # ── 1. Heated Soul Body ────────────────────────────────────
        gray     = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enhanced = self._clahe.apply(gray)
        thermal  = cv2.applyColorMap(enhanced, cv2.COLORMAP_INFERNO).astype(np.float32)

        # Emotion tint blended over the thermal body
        tint = np.zeros_like(thermal)
        tint[:] = emo_col
        blend   = 0.20 + pulse * 0.18
        thermal = thermal * (1.0 - blend) + tint * blend

        # Feathered body mask so the soul has soft glowing edges
        fg_soft   = cv2.GaussianBlur(fg, (27, 27), 0).astype(np.float32) / 255.0
        fg_3d     = np.stack([fg_soft] * 3, axis=-1)
        body_soul = thermal * fg_3d

        # ── 2. Outer Body Aura ─────────────────────────────────────
        aura_mask = cv2.GaussianBlur(fg, (71, 71), 0).astype(np.float32) / 255.0
        aura_3d   = np.stack([aura_mask] * 3, axis=-1)
        aura      = aura_3d * np.array(emo_col, dtype=np.float32) * 0.45

        output = np.clip(output + aura + body_soul, 0, 255)

        # ── 3. Biometric Organs (Brain + Heart) ────────────────────
        if face_live:
            organs = np.zeros((h, w, 3), dtype=np.float32)
            self._draw_brain(organs, brain_cx, brain_cy, bw, bh, emo_col, t)
            self._draw_heart(organs, heart_cx, heart_cy, bw, emo_col,
                             emotion_state.heart_rate,
                             emotion_state.science['chemicals'], t)

            # Glow pass
            glow_k  = (23, 23)
            organs_glow = cv2.GaussianBlur(organs, glow_k, 0)
            organs  = np.clip(organs * 0.75 + organs_glow * 0.90, 0, 255)

            # Biometric visibility fade (2-second decay)
            output = np.clip(output + organs * emotion_state.face_visible, 0, 255)

        return output.astype(np.uint8)

    # ── Brain Anatomy ──────────────────────────────────────────────

    def _draw_brain(self, canvas, cx, cy, face_w, face_h, col, t):
        """
        Draws an anatomically-shaped glowing brain inside the head region.
        Hemispheres, cerebellum, brain stem, gyri folds, active synapses.
        """
        bw = max(6, int(face_w * 0.44))
        bh = max(4, int(face_h * 0.36))

        dark   = tuple(int(c * 0.30) for c in col)
        bright = tuple(min(255, int(c * 1.55)) for c in col)

        # ── Filled base shapes ────────────────────────────────────
        # Left hemisphere
        cv2.ellipse(canvas, (int(cx - bw * 0.22), int(cy - bh * 0.12)),
                    (int(bw * 0.62), int(bh * 0.52)), -15, 0, 360, dark, -1, cv2.LINE_AA)
        # Right hemisphere
        cv2.ellipse(canvas, (int(cx + bw * 0.22), int(cy - bh * 0.12)),
                    (int(bw * 0.62), int(bh * 0.52)),  15, 0, 360, dark, -1, cv2.LINE_AA)
        # Cerebellum
        cv2.ellipse(canvas, (cx, int(cy + bh * 0.36)),
                    (int(bw * 0.46), int(bh * 0.26)), 0, 0, 360, dark, -1, cv2.LINE_AA)
        # Brain stem
        cv2.ellipse(canvas, (cx, int(cy + bh * 0.68)),
                    (int(bw * 0.14), int(bh * 0.34)), 0, 0, 360, dark, -1, cv2.LINE_AA)

        # ── Gyri & Sulci (organic folds that wiggle) ──────────────
        pulse_scale = 1.0 + 0.07 * math.sin(t * 7.5)

        # Fold paths as relative (rx, ry) fractions of brain dimensions
        fold_paths = [
            # Left hemisphere folds
            [(-0.25,-0.42),(-0.40,-0.30),(-0.44,-0.10),(-0.28, 0.02),(-0.10,-0.10)],
            [(-0.18,-0.30),(-0.32,-0.18),(-0.28, 0.04),(-0.10, 0.10)],
            [(-0.44,-0.10),(-0.52, 0.10),(-0.38, 0.22),(-0.18, 0.12)],
            [(-0.28, 0.08),(-0.38, 0.18),(-0.28, 0.28),(-0.10, 0.20)],
            [(-0.10,-0.22),(-0.20,-0.10),(-0.18, 0.04)],
            # Right hemisphere folds (mirrored)
            [( 0.25,-0.42),( 0.40,-0.30),( 0.44,-0.10),( 0.28, 0.02),( 0.10,-0.10)],
            [( 0.18,-0.30),( 0.32,-0.18),( 0.28, 0.04),( 0.10, 0.10)],
            [( 0.44,-0.10),( 0.52, 0.10),( 0.38, 0.22),( 0.18, 0.12)],
            [( 0.28, 0.08),( 0.38, 0.18),( 0.28, 0.28),( 0.10, 0.20)],
            [( 0.10,-0.22),( 0.20,-0.10),( 0.18, 0.04)],
            # Corpus callosum median fold
            [(-0.10,-0.20),( 0.00,-0.28),( 0.10,-0.20)],
            [(-0.10,-0.10),( 0.00,-0.16),( 0.10,-0.10)],
            [(-0.12, 0.00),( 0.00,-0.04),( 0.12, 0.00)],
            # Cerebellum folds
            [(-0.34, 0.28),( 0.00, 0.26),( 0.34, 0.28)],
            [(-0.28, 0.34),( 0.00, 0.32),( 0.28, 0.34)],
            [(-0.20, 0.40),( 0.00, 0.38),( 0.20, 0.40)],
        ]

        for path in fold_paths:
            pts = []
            for rx, ry in path:
                wx = 0.024 * math.sin(t * 5.8 + rx * 13.0 + ry * 7.0)
                wy = 0.024 * math.cos(t * 4.9 + ry * 11.0 + rx * 8.0)
                px = int(cx + (rx + wx) * bw * pulse_scale)
                py = int(cy + (ry + wy) * bh * pulse_scale)
                pts.append((px, py))
            cv2.polylines(canvas, [np.array(pts, dtype=np.int32)],
                          False, bright, 2, cv2.LINE_AA)

        # ── Active synapses (blinking nodes) ──────────────────────
        synapse_locs = [
            (-0.30,-0.22),(-0.10,-0.32),( 0.30,-0.22),( 0.10,-0.32),
            (-0.22, 0.06),( 0.22, 0.06),( 0.00,-0.16),( 0.00, 0.06),
            (-0.16, 0.30),( 0.16, 0.30),( 0.00, 0.40),
            (-0.44,-0.10),( 0.44,-0.10),
        ]
        for sx, sy in synapse_locs:
            phase = t * 10.8 + sx * 22.0 + sy * 14.0
            blink = 0.4 + 0.6 * abs(math.sin(phase))
            r     = max(1, int(3.5 * blink))
            px    = int(cx + sx * bw * pulse_scale)
            py    = int(cy + sy * bh * pulse_scale)
            cv2.circle(canvas, (px, py), r,     (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(canvas, (px, py), r + 2, bright,          1,  cv2.LINE_AA)

    # ── Somatic Heart Core ─────────────────────────────────────────

    def _draw_heart(self, canvas, cx, cy, face_w, col, heart_rate, chems, t):
        """
        Draws a pulsing somatic heart/core in the chest region.
        Pulse frequency and amplitude are driven by Adrenaline/Cortisol.
        GABA slows the beat. The core radiates concentric aura rings.
        """
        adr = chems.get('Adrenaline', 0.2)
        cor = chems.get('Cortisol',   0.3)
        gab = chems.get('GABA',       0.5)

        amp  = 0.10 + adr * 0.32 + cor * 0.10
        hb   = 1.0 + amp * math.sin(t * heart_rate)
        r0   = max(3, int(face_w * 0.145 * hb))

        bright = tuple(min(255, int(c * 1.5)) for c in col)
        mid    = tuple(min(255, int(c * 0.8)) for c in col)

        # Inner core glow
        cv2.circle(canvas, (cx, cy), r0, bright, -1, cv2.LINE_AA)

        # Radiating rings (4 rings, fading outward)
        for ring in range(1, 5):
            rr   = int(r0 * (1.0 + ring * 0.45))
            fade = max(0.0, 1.0 - ring * 0.22)
            rc   = tuple(int(c * fade) for c in col)
            thickness = max(1, 3 - ring)
            cv2.circle(canvas, (cx, cy), rr, rc, thickness, cv2.LINE_AA)

        # Neural connection lines from heart to brain region direction
        num_spokes = 6
        spoke_len  = int(face_w * 0.18 * (1.0 + adr * 0.4))
        for i in range(num_spokes):
            angle = (i / num_spokes) * math.pi * 2 + t * 0.8
            ex2   = int(cx + math.cos(angle) * spoke_len)
            ey2   = int(cy + math.sin(angle) * spoke_len)
            alpha = 0.5 + 0.5 * math.sin(t * 9.0 + i * 1.1)
            sc    = tuple(int(c * alpha * 0.9) for c in mid)
            cv2.line(canvas, (cx, cy), (ex2, ey2), sc, 1, cv2.LINE_AA)


# ═══════════════════════════════════════════════════════════════════
#  GHOST RENDERER  (LINE / SMOKE / FUSION)
# ═══════════════════════════════════════════════════════════════════

class GhostRenderer:
    def __init__(self, width, height):
        self.width  = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.float32)
        self.mode   = RenderMode.LINE
        self.sensitivity_scale = 1.0

    def cycle_mode(self):
        modes     = list(RenderMode)
        self.mode = modes[(modes.index(self.mode) + 1) % len(modes)]
        print(f"[Renderer] Mode -> {self.mode.name}")

    def reset(self):
        self.canvas[:] = 0

    def adjust_sensitivity(self, delta):
        self.sensitivity_scale = max(0.1, self.sensitivity_scale + delta)
        print(f"[Renderer] Sensitivity -> {self.sensitivity_scale:.2f}")

    def update(self, flow, pulse=0.0):
        fade = Config.FUSION_FADE_ALPHA + pulse * 0.04 \
               if self.mode == RenderMode.FUSION else Config.FADE_ALPHA
        self.canvas *= fade
        if flow is not None:
            if   self.mode == RenderMode.LINE:   self._lines(flow)
            elif self.mode == RenderMode.SMOKE:  self._smoke(flow)
            elif self.mode == RenderMode.FUSION: self._fusion(flow, pulse)
        return np.clip(self.canvas, 0, 255).astype(np.uint8)

    def _thr(self, s=1.0):
        return Config.VELOCITY_THRESHOLD * self.sensitivity_scale * s

    def _lines(self, flow):
        step = Config.STEP; h, w = flow.shape[:2]
        ys, xs = np.mgrid[step//2:h:step, step//2:w:step]
        fx, fy  = flow[ys, xs, 0], flow[ys, xs, 1]
        mag = np.sqrt(fx**2 + fy**2); mask = mag > self._thr()
        x0  = xs[mask].astype(np.int32); y0 = ys[mask].astype(np.int32)
        x1  = np.clip(x0 + fx[mask] * Config.VELOCITY_SCALE, 0, w - 1).astype(np.int32)
        y1  = np.clip(y0 + fy[mask] * Config.VELOCITY_SCALE, 0, h - 1).astype(np.int32)
        mags = mag[mask]
        for i in range(len(x0)):
            v  = mags[i]; br = min(255.0, 80 + v * 12)
            b  = Config.ACCENT_COLOR if v > Config.VELOCITY_ACCENT_THR else Config.GHOST_COLOR_BASE
            cv2.line(self.canvas, (x0[i], y0[i]), (x1[i], y1[i]),
                     (int(b[0]*br/255), int(b[1]*br/255), int(b[2]*br/255)),
                     Config.LINE_THICKNESS, cv2.LINE_AA)

    def _smoke(self, flow):
        step = Config.STEP; h, w = flow.shape[:2]
        s = np.zeros((h, w), dtype=np.float32)
        ys, xs = np.mgrid[step//2:h:step, step//2:w:step]
        fx, fy  = flow[ys, xs, 0], flow[ys, xs, 1]
        mag = np.sqrt(fx**2 + fy**2); mask = mag > self._thr()
        px  = xs[mask].astype(np.int32); py = ys[mask].astype(np.int32); mags = mag[mask]
        for i in range(len(px)):
            cv2.circle(s, (px[i], py[i]),
                       Config.PARTICLE_RADIUS + int(mags[i] * 0.5),
                       int(min(255, mags[i] / 10 * 255)), -1)
        s = cv2.GaussianBlur(s, Config.SMOKE_BLUR_KSIZE, Config.SMOKE_BLUR_SIGMA)
        self.canvas = np.clip(self.canvas + np.stack([(s / 255) * 200] * 3, axis=-1), 0, 255)

    def _fusion(self, flow, pulse):
        step = Config.FUSION_STEP; h, w = flow.shape[:2]
        ys, xs = np.mgrid[step//2:h:step, step//2:w:step]
        fx, fy  = flow[ys, xs, 0], flow[ys, xs, 1]
        mag = np.sqrt(fx**2 + fy**2); mask = mag > self._thr(0.7)
        x0  = xs[mask].astype(np.int32); y0 = ys[mask].astype(np.int32)
        sc  = Config.FUSION_VEL_SCALE * (1 + pulse * 0.5)
        x1  = np.clip(x0 + fx[mask] * sc, 0, w - 1).astype(np.int32)
        y1  = np.clip(y0 + fy[mask] * sc, 0, h - 1).astype(np.int32)
        mags  = mag[mask]; boost = 1 + pulse * 1.8
        for i in range(len(x0)):
            v = mags[i]; tc = min(1.0, v / 14); br = min(255, (50 + v * 16) * boost)
            cv2.line(self.canvas, (x0[i], y0[i]), (x1[i], y1[i]),
                     (int(min(255, (160 + tc * 95) * br / 255)),
                      int(min(255, tc * 220 * br / 255)),
                      int(min(255, (80 - tc * 60) * br / 255))),
                     Config.LINE_THICKNESS, cv2.LINE_AA)


# ═══════════════════════════════════════════════════════════════════
#  HALLUCINATION CLOCK
# ═══════════════════════════════════════════════════════════════════

class HallucinationClock:
    def __init__(self):
        self._t0      = time.perf_counter()
        self.strength = Config.HALLUCINATION_STRENGTH
        self.period   = Config.HALLUCINATION_PERIOD

    def factor(self):
        t  = (time.perf_counter() - self._t0) % self.period
        ph = t / self.period
        raw = ph / 0.15 if ph < 0.15 else max(0.0, 1 - (ph - 0.15) / 0.85) ** 2
        return raw * self.strength

    def adjust(self, d):
        self.strength = max(0.0, min(1.0, self.strength + d))
        print(f"[Hallucination] -> {self.strength:.2f}")


# ═══════════════════════════════════════════════════════════════════
#  BRAIN HUD  (live neurotransmitter chemistry panel)
# ═══════════════════════════════════════════════════════════════════

class BrainHUD:
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    MONO = cv2.FONT_HERSHEY_PLAIN

    CHEM_COLORS = {
        'Dopamine':   (255, 140,  30),
        'Serotonin':  ( 80, 220, 255),
        'Endorphins': ( 50, 255, 150),
        'Cortisol':   ( 40,  40, 220),
        'Adrenaline': ( 20, 100, 255),
        'GABA':       (180, 180,  40),
    }

    def draw(self, frame: np.ndarray, state: EmotionState, show: bool) -> np.ndarray:
        if not show:
            return frame

        h, w = frame.shape[:2]
        sci  = state.science

        pw, ph = 320, 328
        px, py = w - pw - 18, h - ph - 18
        panel  = frame.copy()
        cv2.rectangle(panel, (px, py), (px + pw, py + ph), (8, 8, 8), -1)
        frame = cv2.addWeighted(panel, 0.78, frame, 0.22, 0)

        em_col   = state.color
        conf_pct = int(state.confidence * 100)

        # Emotion label
        cv2.putText(frame, sci['label'], (px + 12, py + 30),
                    self.FONT, 0.80, em_col, 2, cv2.LINE_AA)
        cv2.putText(frame, f"{conf_pct}% confidence", (px + 12, py + 52),
                    self.FONT, 0.38, (130, 130, 130), 1, cv2.LINE_AA)

        # Confidence bar
        bw2 = int((pw - 24) * state.confidence)
        cv2.rectangle(frame, (px + 12, py + 58), (px + 12 + bw2, py + 64), em_col, -1)
        cv2.rectangle(frame, (px + 12, py + 58), (px + pw - 12,  py + 64), (50, 50, 50), 1)

        cv2.line(frame, (px + 8, py + 74), (px + pw - 8, py + 74), (40, 40, 40), 1)

        # Neurotransmitter bars
        cv2.putText(frame, "BRAIN CHEMISTRY", (px + 12, py + 90),
                    self.FONT, 0.36, (80, 80, 80), 1, cv2.LINE_AA)

        bar_x_label = px + 12
        bar_x_fill  = px + 120
        bar_max_w   = pw - 135
        row_h       = 26
        y0          = py + 108

        for i, chem in enumerate(CHEMICAL_ORDER):
            level = sci['chemicals'].get(chem, 0.0)
            cy2   = y0 + i * row_h
            col   = self.CHEM_COLORS.get(chem, (200, 200, 200))
            cv2.putText(frame, chem, (bar_x_label, cy2 + 10),
                        self.FONT, 0.34, (140, 140, 140), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (bar_x_fill, cy2), (bar_x_fill + bar_max_w, cy2 + 12), (30, 30, 30), -1)
            fill = int(bar_max_w * level)
            cv2.rectangle(frame, (bar_x_fill, cy2), (bar_x_fill + fill, cy2 + 12), col, -1)
            cv2.putText(frame, f"{int(level * 100)}%",
                        (bar_x_fill + bar_max_w + 4, cy2 + 10),
                        self.FONT, 0.30, (100, 100, 100), 1, cv2.LINE_AA)

        div_y = y0 + len(CHEMICAL_ORDER) * row_h + 4
        cv2.line(frame, (px + 8, div_y), (px + pw - 8, div_y), (40, 40, 40), 1)

        cv2.putText(frame, "ACTIVE REGION", (px + 12, div_y + 16),
                    self.FONT, 0.34, (80, 80, 80), 1, cv2.LINE_AA)
        region = sci['brain_region']
        parts  = region.split(' · ')
        for j, part in enumerate(parts):
            cv2.putText(frame, part.strip(), (px + 12, div_y + 30 + j * 14),
                        self.FONT, 0.33, em_col, 1, cv2.LINE_AA)

        cm_y = div_y + 30 + len(parts) * 14 + 8
        cv2.putText(frame, "COLOR PSYCHOLOGY", (px + 12, cm_y),
                    self.FONT, 0.34, (80, 80, 80), 1, cv2.LINE_AA)
        cv2.putText(frame, sci['color_name'], (px + 12, cm_y + 14),
                    self.FONT, 0.36, em_col, 1, cv2.LINE_AA)
        for j, mp in enumerate(sci['color_meaning'].split('  ·  ')):
            cv2.putText(frame, mp.strip(), (px + 12, cm_y + 28 + j * 13),
                        self.FONT, 0.30, (100, 100, 100), 1, cv2.LINE_AA)

        return frame


# ═══════════════════════════════════════════════════════════════════
#  STANDARD HUD
# ═══════════════════════════════════════════════════════════════════

class HUD:
    FONT  = cv2.FONT_HERSHEY_SIMPLEX
    SCALE = 0.44

    _COL = {
        RenderMode.LINE:    (55,  55,  55),
        RenderMode.SMOKE:   (55,  55,  55),
        RenderMode.FUSION:  (60,  80, 200),
        RenderMode.QUANTUM: (200, 200,  60),
        RenderMode.EMOTION: (60,  220, 200),
    }

    def __init__(self):
        self._buf  = []
        self._last = time.perf_counter()

    def fps(self):
        now = time.perf_counter(); dt = now - self._last; self._last = now
        self._buf.append(1 / dt if dt > 0 else 0)
        if len(self._buf) > 30: self._buf.pop(0)
        return sum(self._buf) / len(self._buf)

    def draw(self, frame, fps_val, mode, sens, pulse, bloom, n_part, show):
        if not show:
            return frame
        ov  = frame.copy()
        col = self._COL.get(mode, (55, 55, 55))
        lines = [
            "void.lumin — The Somatic Ghost v4",
            f"FPS: {fps_val:5.1f}  Mode: {mode.name}",
            f"Sens: {sens:.2f}x   Particles: {n_part:,}",
        ]
        if mode == RenderMode.FUSION:
            lines.append(f"Bloom: {bloom:.2f}   Pulse: {pulse:.2f}")
        lines += ["", "SPACE cycle modes", "R reset", "F HUD",
                  "B bloom", "H hallucination", "+/- sensitivity", "Q/ESC quit"]
        x, y = 14, 24
        for line in lines:
            c = col if line.startswith("void") else (45, 45, 45)
            cv2.putText(ov, line, (x, y), self.FONT, self.SCALE, c, 1, cv2.LINE_AA)
            y += 17
        return cv2.addWeighted(ov, 0.85, frame, 0.15, 0)


# ═══════════════════════════════════════════════════════════════════
#  APPLICATION
# ═══════════════════════════════════════════════════════════════════

class SomaticGhost:
    def __init__(self):
        print("=" * 56)
        print("  void.lumin — The Somatic Ghost v4")
        print("  VOID LUMIN 2.0 — Cognitive Instrument")
        print("=" * 56)
        print("  You are the conductor.")
        print("  Your calm builds the cathedral.")
        print("  Your chaos shatters the cosmos.")
        print("=" * 56)

        self.cam       = CameraManager(Config.CAMERA_INDEX, Config.FRAME_WIDTH, Config.FRAME_HEIGHT)
        self.flow      = FlowEngine()
        self.renderer  = GhostRenderer(self.cam.width, self.cam.height)
        self.somatic   = SomaticRenderer(self.cam.width, self.cam.height)
        self.human_fx  = HumanFX()
        self.emotion   = EmotionEngine()
        self.hallucine = HallucinationClock()
        self.hud       = HUD()
        self.brain_hud = BrainHUD()
        self.show_hud  = Config.SHOW_FPS_DEFAULT
        self.bloom     = Config.BLOOM_STRENGTH
        self.running   = False

    def _keys(self, key):
        if key in (ord('q'), ord('Q'), 27): return False
        if key == ord(' '):
            self.renderer.cycle_mode()
        if key in (ord('r'), ord('R')):
            self.renderer.reset(); self.somatic.reset()
            print("[App] Reset.")
        if key in (ord('f'), ord('F')):
            self.show_hud = not self.show_hud
        if key == ord('+'):
            self.renderer.adjust_sensitivity(-0.1)
            self.somatic.sensitivity_scale = self.renderer.sensitivity_scale
        if key == ord('-'):
            self.renderer.adjust_sensitivity(+0.1)
            self.somatic.sensitivity_scale = self.renderer.sensitivity_scale
        if key in (ord('b'), ord('B')):
            self.bloom = max(0, min(2, self.bloom + 0.05))
            print(f"[Bloom] {self.bloom:.2f}")
        if key in (ord('h'), ord('H')):
            self.hallucine.adjust(0.05)
        return True

    def run(self):
        cv2.namedWindow(Config.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(Config.WINDOW_NAME, self.cam.width, self.cam.height)
        self.running = True
        print("[App] Running — press SPACE to cycle through modes.")
        print("[App] EMOTION mode is mode 5 (press SPACE x4).")
        if not EMOTION_AVAILABLE:
            print("[App] EMOTION mode needs:  py -m pip install fer")

        while self.running:
            frame = self.cam.read()
            if frame is None:
                continue
            frame  = cv2.flip(frame, 1)
            pulse  = self.hallucine.factor()
            fl     = self.flow.update(frame)
            mode   = self.renderer.mode

            # Always feed emotion engine (async, non-blocking)
            self.emotion.submit(frame)
            self.emotion.tick()
            e_state = self.emotion.get_state()

            # ── Render ────────────────────────────────────────────
            if mode == RenderMode.EMOTION:
                if EMOTION_AVAILABLE:
                    output = self.somatic.update(frame, fl, pulse, emotion_state=e_state)
                else:
                    output = self.somatic.update(frame, fl, pulse)

            elif mode == RenderMode.QUANTUM:
                output = self.somatic.update(frame, fl, pulse)

            elif mode == RenderMode.FUSION:
                ghost  = self.renderer.update(fl, pulse)
                human  = self.human_fx.apply(frame, pulse, self.bloom)
                output = np.clip(
                    ghost.astype(np.float32) * Config.GHOST_ALPHA
                    + human.astype(np.float32) * Config.HUMAN_ALPHA,
                    0, 255).astype(np.uint8)

            else:
                output = self.renderer.update(fl, pulse)

            # ── Overlays ──────────────────────────────────────────
            fps_v  = self.hud.fps()
            output = self.hud.draw(output, fps_v, mode,
                                   self.renderer.sensitivity_scale,
                                   pulse, self.bloom,
                                   len(self.somatic.particles), self.show_hud)
            if mode == RenderMode.EMOTION and self.show_hud and EMOTION_AVAILABLE:
                output = self.brain_hud.draw(output, e_state, True)

            cv2.imshow(Config.WINDOW_NAME, output)
            key = cv2.waitKey(1) & 0xFF
            if key != 255:
                self.running = self._keys(key)

        self.emotion.stop()
        self.cam.release()
        cv2.destroyAllWindows()
        print("[App] Done.")


# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = SomaticGhost()
    app.run()
