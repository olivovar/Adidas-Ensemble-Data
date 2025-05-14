# -----------------------------------------
# Instagram Engagement Analysis
# -----------------------------------------

import zipfile
import os
import json
import emoji
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# -----------------------------------------
# Unzip the Instagram Data
# -----------------------------------------
main_zip_path = "/Users/oliviapivovar/Desktop/ensemble_data/ensemble_data.zip"
extract_dir = "ensemble_data"

with zipfile.ZipFile(main_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Unzip the Instagram-specific ZIP
instagram_zip_path = os.path.join(extract_dir, "raw_instagram.zip")
instagram_data_dir = os.path.join(extract_dir, "instagram_data")

with zipfile.ZipFile(instagram_zip_path, 'r') as zip_ref:
    zip_ref.extractall(instagram_data_dir)

# -----------------------------------------
# Load and Filter Usable Instagram Files
# -----------------------------------------

# List all JSON files in the instagram raw folder
raw_folder = os.path.join(instagram_data_dir, "raw")
file_list = []
for root, dirs, files in os.walk(raw_folder):
    for file in files:
        if file.endswith(".json"):
            file_list.append(os.path.join(root, file))

# Load posts from files using the structure:
# {
#   "data": {
#       "count": <...>,
#       "posts": [ { "node": { ...post info... } }, ... ]
#   }
# }
insta_posts = []
for file_path in file_list:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Ensure we have the expected structure:
        if (
            isinstance(data, dict) and
            "data" in data and
            isinstance(data["data"], dict) and
            "posts" in data["data"] and
            isinstance(data["data"]["posts"], list)
        ):
            # From each post item, extract the "node" (if available)
            for item in data["data"]["posts"]:
                if isinstance(item, dict) and "node" in item:
                    insta_posts.append(item["node"])
    except Exception as e:
        print(f"⚠️ Skipping {file_path}: {e}")

print(f" Total valid Instagram posts loaded: {len(insta_posts)}")

# -----------------------------------------
# Extract Key Fields from Each Post
# -----------------------------------------

def extract_instagram_post(node):
    """
    Extracts post-level fields from an Instagram node.
    Expected node fields (for GraphQL responses) include:
      - id
      - taken_at_timestamp : unix timestamp
      - edge_media_to_caption: { "edges": [ { "node": { "text": "..." } } ] }
      - edge_liked_by: { "count": ... }
      - edge_media_to_comment: { "count": ... }
      - video_view_count: (if video)
      - __typename: media type
    """
    # Post ID
    post_id = node.get("id")
    
    # Caption: Instagram GraphQL posts typically nest the caption
    caption = ""
    if "edge_media_to_caption" in node:
        caption_edges = node["edge_media_to_caption"].get("edges", [])
        if caption_edges:
            caption = caption_edges[0]["node"].get("text", "")
    # Fallback: sometimes the caption might be at a top level as a string
    if not caption and isinstance(node.get("caption"), str):
        caption = node.get("caption")
    
    # Timestamp: Convert unix timestamp to datetime.
    timestamp = pd.to_datetime(node.get("taken_at_timestamp"), unit='s', errors='coerce')
    
    # Engagement metrics: likes and comments
    likes = node.get("edge_liked_by", {}).get("count", 0)
    comments = node.get("edge_media_to_comment", {}).get("count", 0)
    
    # Views: only applicable for videos; may be missing for images.
    views = node.get("video_view_count", 0)
    
    # Media type: given in __typename
    media_type = node.get("__typename")
    
    # Extract hashtags from caption
    hashtags = [word.strip("#") for word in caption.split() if word.startswith("#")]
    
    return {
        "post_id": post_id,
        "caption": caption,
        "timestamp": timestamp,
        "likes": likes,
        "comments": comments,
        "views": views,
        "media_type": media_type,
        "hashtags": hashtags
    }

# Build a DataFrame from all extracted posts
df = pd.DataFrame([extract_instagram_post(p) for p in insta_posts])
df = df[df["timestamp"].notna()]  # Remove any posts with invalid timestamps

print(f"Posts with valid timestamps: {len(df)}")
if len(df) == 0:
    print("No usable Instagram posts found.")
else:
    print(df.head())

# -----------------------------------------
# Calculate Engagement and Visualize
# -----------------------------------------

# Define an engagement rate.
# For Instagram, since many posts are images, we don't have a "views" field.
# Define engagement rate as (likes + comments) / (views + 1) to avoid division by zero.
df["engagement_rate"] = (df["likes"] + df["comments"]) / (df["views"] + 1)

# Extract posting hour from timestamp
df["hour"] = df["timestamp"].dt.hour

#Print Engagement by Hour
print("\nAverage Engagement Rate by Hour:")
print(df.groupby("hour")["engagement_rate"].mean().round(2).sort_index())

# Plot: Engagement Rate Over Time
plt.figure(figsize=(10, 4))
df.sort_values("timestamp").plot(x="timestamp", y="engagement_rate", marker="o", legend=False)
plt.title("Instagram Engagement Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Engagement Rate")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot: Average Engagement by Hour
df.groupby("hour")["engagement_rate"].mean().plot(kind="bar", figsize=(10, 4), title="Avg Engagement by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Engagement Rate")
plt.grid(True)
plt.tight_layout()
plt.show()

# Caption Length vs. Engagement
df["caption_length"] = df["caption"].fillna("").apply(len)
#Print caption length vs Engagement
print("\nCaption Length Analysis:")
print(f"Average caption length: {df['caption_length'].mean():.1f} characters")
correlation = df[["caption_length", "engagement_rate"]].corr().iloc[0, 1]
print(f"Correlation between caption length and engagement rate: {correlation:.4f}")
#Bin-wise report
df["caption_bin"] = pd.cut(df["caption_length"], bins=[0, 50, 100, 150, 300], labels=["0–50", "51–100", "101–150", "151+"])
print("\nEngagement Rate by Caption Length Bin:")
print(df.groupby("caption_bin")["engagement_rate"].mean().round(2))
#Plot Caption Length vs Engagement
plt.figure(figsize=(10, 5))
plt.scatter(df["caption_length"], df["engagement_rate"], alpha=0.5)
plt.title("Caption Length vs Engagement Rate (Instagram)")
plt.xlabel("Caption Length (characters)")
plt.ylabel("Engagement Rate")
plt.grid(True)
plt.tight_layout()
plt.show()

# Engagement by Day of the Week
df["weekday"] = df["timestamp"].dt.day_name()
weekday_avg = df.groupby("weekday")["engagement_rate"].mean().sort_values()
#Print Week Day Avg
print("\nAverage Engagement Rate by Day of Week:")
print(weekday_avg.round(2))
#Plot Week day avg
weekday_avg.plot(kind="bar", figsize=(10, 4), title="Avg Engagement by Day of Week (Instagram)")
plt.ylabel("Engagement Rate")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Top Hashtags (High-Engagement)
top_posts = df[df["engagement_rate"] >= df["engagement_rate"].quantile(0.75)]
hashtags = [tag for tags in top_posts["hashtags"] if isinstance(tags, list) for tag in tags]
top_tags = Counter(hashtags).most_common(10)
print("\nTop Hashtags in High-Engagement Instagram Posts:")
for tag, count in top_tags:
    print(f"{tag}: {count}")

# Plot the top hashtags
if top_tags:
    tags, counts = zip(*top_tags)
    plt.figure(figsize=(10, 4))
    plt.bar(tags, counts)
    plt.title("Top Hashtags in High Engagement Posts (Instagram)")
    plt.xticks(rotation=45)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.grid(True)
    plt.show()


# Function to detect if any emoji is in the caption
def contains_emoji(text):
    return any(char in emoji.EMOJI_DATA for char in str(text))

# Apply emoji detection
df["has_emoji"] = df["caption"].apply(contains_emoji)

# Compare average engagement
emoji_avg = df.groupby("has_emoji")["engagement_rate"].mean()

print("\nInstagram Engagement by Emoji Use:")
print(f"With Emojis:    {emoji_avg.get(True, 'N/A'):.4f}")
print(f"Without Emojis: {emoji_avg.get(False, 'N/A'):.4f}")

#Plot emoji findings
emoji_avg.plot(kind="bar", figsize=(6, 4), title="Engagement Rate by Emoji Use (Instagram)")
plt.xticks([0, 1], ["No Emoji", "Has Emoji"], rotation=0)
plt.ylabel("Engagement Rate")
plt.grid(True)
plt.tight_layout()
plt.show()


df.to_csv("cleaned_instagram.csv", index=False)