# -----------------------------------------
# TikTok Engagement Analysis - Adidas Data
# -----------------------------------------

import zipfile
import os
import json
import emoji
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# -------------------------------
# Unzip and Load Tiktok Data
# -------------------------------
#Zip path based on my local directory
main_zip_path = "/Users/oliviapivovar/Desktop/ensemble_data/ensemble_data.zip"
extract_dir = "ensemble_data"

with zipfile.ZipFile(main_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

tiktok_zip_path = os.path.join(extract_dir, "raw_tiktok.zip")
tiktok_data_dir = os.path.join(extract_dir, "tiktok_data")

with zipfile.ZipFile(tiktok_zip_path, 'r') as zip_ref:
    zip_ref.extractall(tiktok_data_dir)

# -------------------------------
# Load All Valid TikTok JSON Files
# -------------------------------
all_posts = []
raw_folder = os.path.join(tiktok_data_dir, "raw")

for filename in os.listdir(raw_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(raw_folder, filename)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            if "data" in data:
                all_posts.extend(data["data"])
        except Exception as e:
            print(f"Skipping {filename}: {e}")

# -------------------------------
# Extract and Clean the Data
# -------------------------------
def extract_post_info(post):
    return {
        "post_id": post.get("aweme_id"),
        "caption": post.get("desc"),
        "timestamp": pd.to_datetime(post.get("create_time"), unit="s", errors="coerce"),
        "likes": post.get("statistics", {}).get("digg_count"),
        "comments": post.get("statistics", {}).get("comment_count"),
        "shares": post.get("statistics", {}).get("share_count"),
        "views": post.get("statistics", {}).get("play_count"),
        "hashtags": [tag.get("hashtag_name") for tag in post.get("text_extra", []) if tag.get("hashtag_name")]
    }

df = pd.DataFrame([extract_post_info(p) for p in all_posts])
df = df[df["timestamp"].notna()]  # filter out bad timestamps
df = df[df["views"] > 0]  # avoid divide-by-zero

df["engagement_rate"] = (df["likes"] + df["comments"] + df["shares"]) / df["views"]
df["hour"] = df["timestamp"].dt.hour
# Print average engagement by hour
print("\nAverage Engagement Rate by Hour:")
print(df.groupby("hour")["engagement_rate"].mean().round(4).sort_index())

print(f"Loaded {len(df)} valid TikTok posts")

# -------------------------------
# Plot Engagement Trends
# -------------------------------

# Engagement over time
plt.figure(figsize=(10, 4))
df.sort_values("timestamp").plot(x="timestamp", y="engagement_rate", marker="o", legend=False)
plt.title("Engagement Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Engagement Rate")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()

# Engagement by hour
df.groupby("hour")["engagement_rate"].mean().plot(kind="bar", figsize=(10, 4), title="Avg Engagement by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Engagement Rate")
plt.grid(True)
plt.tight_layout()
plt.show()

# Caption length in characters
df["caption_length"] = df["caption"].fillna("").apply(len)

# Print caption length stats
print("\nCaption Length Analysis:")
print(f"Average caption length: {df['caption_length'].mean():.1f} characters")
correlation = df[["caption_length", "engagement_rate"]].corr().iloc[0, 1]
print(f"Correlation between caption length and engagement rate: {correlation:.4f}")

#Bin-wise analysis for caption length
df["caption_bin"] = pd.cut(df["caption_length"], bins=[0, 50, 100, 150, 300], labels=["0–50", "51–100", "101–150", "151+"])
print("\nEngagement Rate by Caption Length Bin:")
print(df.groupby("caption_bin")["engagement_rate"].mean().round(4))

# Scatter plot: Caption length vs engagement
plt.figure(figsize=(10, 5))
plt.scatter(df["caption_length"], df["engagement_rate"], alpha=0.5)
plt.title("Caption Length vs Engagement Rate")
plt.xlabel("Caption Length (characters)")
plt.ylabel("Engagement Rate")
plt.grid(True)
plt.tight_layout()
plt.show()

#Day of Week Trends (When is the best posting day?)
df["weekday"] = df["timestamp"].dt.day_name()
weekday_avg = df.groupby("weekday")["engagement_rate"].mean().sort_values()

#Print Week Day Avgs
print("\nAverage Engagement Rate by Day of Week:")
print(weekday_avg.round(4))

#Plot Week Day Avgs
weekday_avg.plot(kind="bar", figsize=(10, 4), title="Avg Engagement by Day of Week")
plt.ylabel("Engagement Rate")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

#Does having emojis help engagement?
def contains_emoji(text):
    return any(char in emoji.EMOJI_DATA for char in str(text))

df["has_emoji"] = df["caption"].apply(contains_emoji)

emoji_avg = df.groupby("has_emoji")["engagement_rate"].mean()

print("\n Average Engagement Rate:")
print(f"With Emojis:    {emoji_avg.get(True, 'N/A'):.4f}")
print(f"Without Emojis: {emoji_avg.get(False, 'N/A'):.4f}")

emoji_avg.plot(kind="bar", figsize=(6, 4), title="Engagement Rate by Emoji Use")
plt.xticks([0, 1], ["No Emoji", "Has Emoji"], rotation=0)
plt.ylabel("Engagement Rate")
plt.tight_layout()
plt.grid(True)
plt.show()

# Top Hashtags (High Engagement)
top_posts = df[df["engagement_rate"] >= df["engagement_rate"].quantile(0.75)]
hashtags = [tag for tags in top_posts["hashtags"] if isinstance(tags, list) for tag in tags]
top_tags = Counter(hashtags).most_common(10)

print("\n Top Hashtags in High-Engagement Posts:")
for tag, count in top_tags:
    print(f"{tag}: {count}")

# Convert top_tags list to a dictionary for plotting
hashtags_dict = dict(top_tags)
plt.figure(figsize=(10, 5))
plt.bar(hashtags_dict.keys(), hashtags_dict.values())
plt.title("Top Hashtags in High Engagement Posts")
plt.xticks(rotation=45)
plt.ylabel("Frequency in Top Posts")
plt.tight_layout()
plt.grid(True)
plt.show()

df.to_csv("cleaned_tiktok.csv", index=False)     
