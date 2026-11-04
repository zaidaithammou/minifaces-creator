# ⚡ EA Sports FC & FIFA MiniFaces Creator

An automated Python utility designed for EA Sports FC and FIFA modders to batch-process, clean, and remove backgrounds from player face images (minifaces), featuring automated team folder and ID organization.
---

## 📌 Overview

When building custom squad updates or league expansion mods for EA FC and FIFA, player minifaces often come with inconsistent or solid white backgrounds that clash with in-game UI aesthetics. **MiniFaces Creator** provides dual processing pipelines to instantly strip backgrounds, preserve transparency, and export clean PNG assets mapped directly to team IDs.

---

## ✨ Features

* **Dual Processing Engines:**
  * **Fast Thresholding Mode:** Multi-threaded pixel color filtering for instant processing of clean white backgrounds.
  * **Optimized AI Mode:** Advanced background removal using `rembg` for complex or non-white photo backdrops.
* **Resource-Managed AI Pipeline:** Sequential execution paired with automated Python garbage collection (`gc.collect`) and customizable frame delays to prevent system lag during heavy batch jobs.
* **Automated Team Structure:** Automatically parses team directory naming conventions (`TeamID_TeamName`, e.g., `150100_ASFAR`) and generates corresponding structured export targets.
* **Transparent PNG Export:** Outputs clean 32-bit RGBA PNG files ready for injection via the FIFA Editor Tool.

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/minifaces-creator.git
   cd minifaces-creator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📂 Expected Directory Structure

Organize your working directory to match this structure before running batch operations:

```text
MiniFaces_Creator/
├── New/                    # Input folder containing team folders
│   ├── 150100_ASFAR/
│   │   └── minifaces/      # Raw player face images (.png/.jpg)
│   └── 150200_RCA/
│       └── minifaces/
├── Export folder/          # Auto-generated clean output directory
└── minifaces_creator.py    # Main script
```

---

## 💻 Usage

Run the script interactively or via command-line arguments:

```bash
python minifaces_creator.py
```

### Command-Line Arguments Reference

```bash
# Process all teams using fast color thresholding
python minifaces_creator.py 1

# Process all teams using optimized AI background removal
python minifaces_creator.py 2

# Process a specific team folder
python minifaces_creator.py 3 "150100_ASFAR"
python minifaces_creator.py 3 "150100_ASFAR" ai

# Process a single standalone image
python minifaces_creator.py 4 "path/to/input.png" "path/to/output.png" ai
```

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---
<div align="center">
  <p><b>Zaid Ait Hammou</b> (Zaid_Ath)</p>
  <p>Full-Stack Web Development Student @ NTIC Rabat | Ex-Bell & Nespresso Specialist</p>
  <p>
    <a href="https://zaidath-portfolio.netlify.app/">🌐 Portfolio</a> • 
    <a href="https://github.com/zaidaithammou">📦 GitHub</a>
  </p>
</div>
