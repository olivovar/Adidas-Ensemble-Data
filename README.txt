README.txt  
Olivia Pivovar | BACSS Lab Research Fellow Co-op Trial  
Ensemble Data Analysis – Code Repository

This repository contains the Python scripts, visualization outputs, and cleaned datasets used to analyze Adidas' social media engagement on TikTok and Instagram.

---

FILES INCLUDED:

1. tiktok_analysis.py  
   - Parses raw TikTok API data from Ensemble.  
   - Cleans, structures, and analyzes engagement metrics.  
   - Generates visualizations and exports cleaned TikTok data as CSV.

2. instagram_analysis.py  
   - Parses raw Instagram API data from Ensemble.  
   - Extracts nested post structures and computes engagement metrics.  
   - Includes logic to filter out malformed or empty files.

3. compare_platforms.py  
   - Loads cleaned TikTok and Instagram datasets.  
   - Compares engagement trends across platforms by hour, emoji use, and caption length.  
   - Creates comparative charts and summary statistics.

4. cleaned_tiktok.csv  
   - Cleaned TikTok dataset with post-level metrics and derived features.

5. cleaned_instagram.csv  
   - Cleaned Instagram dataset with post-level metrics and derived features.

6. PNG Visualizations (in folders):  
   - Exported bar charts, scatter plots, and engagement curves used in the final report.  
   - Stored in separate folders for TikTok, Instagram, and comparative analysis.

---

HOW TO RUN:

1. Open a terminal or code editor.  
2. Update file paths in the scripts if needed — some variables reference directories on the local machine (e.g., "/Users/oliviapivovar/Desktop/ensemble_data/").  
3. Ensure the following Python packages are installed:  
   - pandas, matplotlib, emoji, json, os, zipfile  
4. Run the scripts in the following order:  
   - python3 tiktok_analysis.py  
   - python3 instagram_analysis.py  
   - python3 compare_platforms.py  

---

NOTES:

- All code, data processing, and visualizations were written independently.  
- Generative AI (ChatGPT) was used for idea generation and language refinement only.  
  All insights were verified manually, and AI-generated suggestions were only used when supported by the data. Full documentation is provided in Appendix A of the report.
