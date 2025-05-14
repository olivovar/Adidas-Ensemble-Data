# Ensemble Data Analysis – Adidas Social Media

**Author:** Olivia Pivovar  
**Project:** Analysis of Adidas' social media engagement on TikTok and Instagram.

This repository contains the Python scripts, visualization outputs, and cleaned datasets used to analyze engagement trends on both platforms using data collected via the Ensemble API.

---

## Included Files

### 1. `tiktok_analysis.py`
- Parses raw TikTok API data from Ensemble.
- Cleans, structures, and analyzes engagement metrics.
- Generates visualizations and exports a cleaned TikTok dataset as CSV.

### 2. `instagram_analysis.py`
- Parses raw Instagram API data from Ensemble.
- Extracts nested post structures and computes engagement metrics.
- Includes error handling for malformed or empty files.

### 3. `compare_platforms.py`
- Loads cleaned TikTok and Instagram datasets.
- Compares engagement trends by hour, emoji use, caption length, and more.
- Outputs comparative charts and summary statistics.

### 4. `cleaned_tiktok.csv`
- Final, cleaned TikTok dataset with post-level metrics and derived features.

### 5. `cleaned_instagram.csv`
- Final, cleaned Instagram dataset with post-level metrics and derived features.

### 6. 📈 Visualization Outputs (in folders)
- Bar charts, scatter plots, and engagement curves.
- Organized by platform: `TikTok Charted Data`, `Instagram Charted Data`, and `Compare Charted Data`.

---

## 🛠 How to Run the Scripts

1. Open a terminal or code editor.
2. Update any file paths in the scripts — some reference local directories (e.g., `/Users/oliviapivovar/Desktop/ensemble_data/`).
3. Ensure the following Python packages are installed:
   - `pandas`, `matplotlib`, `emoji`, `json`, `os`, `zipfile`
4. Run the scripts in the following order:
   ```bash
   python3 tiktok_analysis.py
   python3 instagram_analysis.py
   python3 compare_platforms.py
