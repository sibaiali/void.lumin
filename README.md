# VOID LUMIN 3.0 // Biometric Neural Render Engine
> An interactive cognitive instrument and real-time graphics pipeline connecting human biometric signals to dynamic physics simulations and high-precision mark-making.

[![Crytek Engine Architecture](https://img.shields.io/badge/Architecture-Data--Oriented%20(DoD)-00f0ff.svg)](#)
[![Performance](https://img.shields.io/badge/Target-60%2F120%20FPS%20Locked-10b981.svg)](#)
[![Resolution](https://img.shields.io/badge/Export-4K%20UHD%20(3840x2160)-ffd700.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#)

---

## 🇩🇪 Zusammenfassung (German Engineering Summary)
**Void Lumin 3.0** ist eine interaktive Echtzeit-Grafik- und Biometrie-Pipeline, entwickelt nach modernen Grundsätzen des **Data-Oriented Design (DoD)**, wie sie in High-End-Engines (z. B. **CryEngine**, Unreal Engine) eingesetzt werden.

Das System verzichtet vollständig auf träge externe Laufzeit-Abhängigkeiten und realisiert:
1. **Cache-freundliche Partikelsimulation:** 8.192 simultane Partikel in kontinuierlichen `Float32Array`-Puffern (Structure of Arrays).
2. **Subpixel-Präzisionszeichnung:** Catmull-Rom- und Bézier-Interpolation für detaillierte anatomische Porträt-Skizzen mit dynamischer Drucksensitivität.
3. **Biometrisch gesteuerte physikalische Vektorfelder:** Affektive Zustände modulieren Auftrieb, Wirbelstärke (Curl Noise) und viskose Dämpfung in Echtzeit.
4. **Deterministische Telemetrie-Überwachung:** Crytek-inspirierter Profiler für Frame-Zeiten, Vektordivergenz und Pufferbelegung.

---

## ⚡ Quick Start
### Local Execution
```bash
# Clone the repository
git clone https://github.com/sibaiali/void.lumin.git
cd void.lumin

# Run with standard Python local server
python -m http.server 3000
```
Open **[http://localhost:3000](http://localhost:3000)** in any modern browser.

---

## 🎮 Engine Controls & Hotkeys

| Input | Action | Subsystem |
| :--- | :--- | :--- |
| **Mouse / Touch Drag** | Draw with active brush & pressure | High-DPI Spline Pipeline |
| **Hotkeys `[1]` – `[6]`** | Instant Biometric State Override (Joy, Zen, Rage, Fear, Focus, GOAT) | Neural Signal Deck |
| **Key `[C]`** | Clear canvas / Reset neural state | Render Buffer Reset |
| **Key `[S]`** | Export 4K UHD Masterpiece with Biometric Watermark | 3840x2160 Canvas Pipeline |
| **Camera Toggle** | Switch between live optical tracking & simulation deck | Computer Vision Hook |

---

## 🔬 Mathematical & Biometric Mapping

```math
\mathbf{v}_{t+1} = \left(\mathbf{v}_t + \nabla \times \mathbf{\Psi}(\mathbf{x}) \cdot \omega_{\text{Serotonin}}\right) \cdot (1 - \gamma_{\text{GABA}}) - \mathbf{g}_{\text{Dopamine}} + \mathbf{\eta}_{\text{Cortisol}}
```

- **$\mathbf{g}_{\text{Dopamine}}$ (Buoyancy):** Euphoria and dopamine spikes generate upward particle drift and logarithmic spiral tendencies.
- **$\mathbf{\eta}_{\text{Cortisol}}$ (Turbulence):** Volatile states introduce high-frequency stochastic noise, fracturing geometric coherence.
- **$\gamma_{\text{GABA}}$ (Viscous Damping):** Focus and calm stabilize velocity vectors, producing crystal-clear harmonic filaments.

---

## 💼 Application Dossier for Crytek & German AAA Studios
For hiring managers, technical leads, and recruiters at **Crytek (Frankfurt)**:  
Please review the complete architectural whitepaper in [CRYTEK_PORTFOLIO_CASE_STUDY.md](CRYTEK_PORTFOLIO_CASE_STUDY.md).
