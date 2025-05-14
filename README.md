# Ensemble Data Analysis – Adidas Social Media

**Author:** Olivia Pivovar  
**Project:** Analysis of Adidas' social media engagement on TikTok and Instagram using data collected via the Ensemble API.

This repository contains Python scripts, visualizations, and cleaned datasets used to examine trends in social media performance across TikTok and Instagram.

---

## Features

- Parses raw TikTok and Instagram data using the Ensemble API format
- Cleans, structures, and extracts post-level metrics
- Computes engagement rates and analyzes patterns (hour, emoji usage, caption length, etc.)
- Generates comparative visualizations across platforms
- Exports clean datasets to CSV for further analysis

---

## Project Structure

```
Adidas-Ensemble-Data/
├── tiktok_data/
│   ├── cleaned_tiktok.csv
│   ├── tiktok_analysis.py
│   └── TikTok Charted Data/
├── instagram_data/
│   ├── cleaned_instagram.csv
│   ├── instagram_analysis.py
│   └── Instagram Charted Data/
├── compare_platforms/
│   ├── compare_platforms.py
│   └── Compare Charted Data/
├── docs/
│   └── Ensemble_API_Report.pdf # Full project write-up and methodology
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/olivovar/Adidas-Ensemble-Data.git
cd Adidas-Ensemble-Data
```

### 2. Install dependencies

Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

> Required packages: pandas, matplotlib, emoji

### 3. Prepare the environment

Update any file paths in the scripts if needed — some reference local directories such as:

/Users/oliviapivovar/Desktop/ensemble_data/

### 4. Run the analysis scripts

In this order:

```bash
python3 tiktok_analysis.py
python3 instagram_analysis.py
python3 compare_platforms.py
```

---

## 📊 Output Overview

### Data Files
- cleaned_tiktok.csv: Post-level metrics and derived features from TikTok.
- cleaned_instagram.csv: Post-level metrics and derived features from Instagram.

### Visualizations
- Exported PNGs include:
  - Engagement trends by hour and day
  - Caption length vs. engagement
  - Emoji usage impact
  - Top hashtags in high-performing posts
- Organized into:
  - TikTok Charted Data/
  - Instagram Charted Data/
  - Compare Charted Data/

---

## Notes

- All code, data cleaning, and visualizations were independently written.
- File parsing was customized to handle nested Ensemble API formats and to skip malformed or empty data files.
- Visuals were generated using matplotlib; no external dashboards/tools used.
- A full write-up of the data processing pipeline, engagement metric design, and visualization decisions is available in:

**`docs/Ensemble_API_Report.pdf`**

---

## Author

**Olivia Pivovar**  
📍 Boston, MA  
GitHub: https://github.com/olivovar  
LinkedIn: https://linkedin.com/in/oliviapivovar

---

## Disclaimer

This project is for educational and research purposes only. Please ensure you comply with platform-specific data policies and ethical guidelines when working with social media data.
