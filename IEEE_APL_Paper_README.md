# 📄 IEEE Paper — Automatic Pantograph Lifter (APL)

## Title
**Design and Implementation of an Automatic Pantograph Lifter Using Programmable Logic Controller**

---

## 📁 File: `IEEE_APL_Paper.tex`
This is the full IEEE-format LaTeX source file for the APL research paper.

---

## 🛠️ How to Compile

### Option 1: Online (Recommended — No Installation)
1. Go to [Overleaf.com](https://www.overleaf.com)
2. Click **New Project → Upload Project**
3. Upload `IEEE_APL_Paper.tex`
4. Click **Compile** — your PDF will appear instantly

### Option 2: Local (TeX Live / MikTeX)
```bash
pdflatex IEEE_APL_Paper.tex
pdflatex IEEE_APL_Paper.tex   # Run twice for cross-references
```

---

## 📐 Paper Structure (IEEE Double-Column Format)

| Section | Title |
|---------|-------|
| Abstract | System summary, contributions, results |
| I | Introduction |
| II | Literature Review |
| III | System Architecture + Block Diagram |
| IV | Hardware Components (PLC, VFD, Sensor, Actuator) |
| V | Ladder Logic Programs (4 Rungs + Timing Table) |
| VI | Results and Discussion |
| VII | Conclusion |
| — | References (7 citations) |

---

## 🔧 Ladder Logic Summary

| Rung | Purpose | Key I/O |
|------|---------|---------|
| Rung 1 | UP Motion Control (self-latching) | X0→Y0 |
| Rung 2 | DOWN Motion Control (self-latching) | X1→Y1 |
| Rung 3 | Fault / Emergency Stop indication | X5,X6→Y4 |
| Rung 4 | Status Indicator Lamps | Y0→Y2, Y1→Y3 |

---

## ✏️ Before Submitting — Replace Placeholders

Search and replace the following in `IEEE_APL_Paper.tex`:

| Placeholder | Replace With |
|------------|-------------|
| `[Author Name]` | Your full name |
| `[Institution Name, City, Country]` | Your college/university |
| `[email@institution.edu]` | Your institutional email |

---

## 📊 Key Results

- **Positioning Accuracy:** Mean error = 0.0 mm, σ = 0.13 mm
- **Cycle Time:** 5.02 ± 0.03 s (500 mm stroke)
- **Power Consumption:** ~450 W at rated 50 kg load
- **Energy Efficiency:** 85% (vs 60% hydraulic, 55% pneumatic)

---

## 📦 Repository Files

| File | Description |
|------|-------------|
| `IEEE_APL_Paper.tex` | Full IEEE LaTeX source |
| `APL.pdf` | Original project report |
| `paper.pdf` | Reference paper |
| `Conference-APL-A4.doc` | Conference draft (Word) |
| `pantograph_lifter.jpg` | Pantograph mechanism photo |
| `delta14ss2-series-plc.jpg` | Delta PLC photo |
| `control pannel.jpeg` | Control panel photo |
| `speed_controller.jpeg` | VFD/Speed controller photo |
| `zpactuator.jpeg` | Zip-chain actuator photo |
| `zipchain.png` | Zip-chain diagram |
| `IMG_Product_E2FQ-X2x1_xM_corner_JPG_001.jpg` | Omron E2FQ sensor |

---

*Generated for IEEE conference/journal submission — ECE Department*