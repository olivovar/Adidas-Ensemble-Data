import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df_tiktok = pd.read_csv("/Users/oliviapivovar/Desktop/ensemble_data/tiktok data/cleaned_tiktok.csv")
df_instagram = pd.read_csv("/Users/oliviapivovar/Desktop/ensemble_data/instagram data/cleaned_instagram.csv")

# Add platform column
df_tiktok["platform"] = "TikTok"
df_instagram["platform"] = "Instagram"

# Align column names if needed
shared_cols = ["platform", "engagement_rate", "caption_length", "has_emoji", "hour"]
df_tiktok = df_tiktok[shared_cols]
df_instagram = df_instagram[shared_cols]

# Combine datasets
combined_df = pd.concat([df_tiktok, df_instagram], ignore_index=True)

#  Average engagement rate per platform
print("\nAverage Engagement Rate by Platform:")
combined_df.groupby("platform")["engagement_rate"].mean().plot(
    kind="bar", figsize=(6, 4), title="Average Engagement Rate by Platform"
)
plt.ylabel("Engagement Rate")
plt.xticks(rotation=0)
plt.tight_layout()
plt.grid(True)
plt.show()

print(combined_df.groupby("platform")["engagement_rate"].mean())

# Impact of emojis by platform
print("\nEngagement Rate by Platform and Emoji Use:")
combined_df.groupby(["platform", "has_emoji"])["engagement_rate"].mean().unstack().plot(
    kind="bar", figsize=(8, 4), title="Engagement Rate by Emoji Use"
)
plt.ylabel("Engagement Rate")
plt.xticks(rotation=0)
plt.legend(["No Emoji", "Has Emoji"], title="Emoji Used")
plt.tight_layout()
plt.grid(True)
plt.show()

print(combined_df.groupby(["platform", "has_emoji"])["engagement_rate"].mean())

# Engagement by hour
combined_df.groupby(["platform", "hour"])["engagement_rate"].mean().unstack().T.plot(
    figsize=(10, 5), title="Engagement by Hour of Day"
)
plt.ylabel("Avg Engagement Rate")
plt.grid(True)
plt.tight_layout()
plt.show()

# Engagement vs Caption Length (comparison scatter plot)
plt.figure(figsize=(10, 5))
for platform in combined_df["platform"].unique():
    subset = combined_df[combined_df["platform"] == platform]
    plt.scatter(subset["caption_length"], subset["engagement_rate"], alpha=0.4, label=platform)

plt.title("Caption Length vs Engagement Rate by Platform")
plt.xlabel("Caption Length (characters)")
plt.ylabel("Engagement Rate")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print("\nAvg Caption Length and Engagement Rate:")
print(combined_df.groupby("platform")[["caption_length", "engagement_rate"]].mean())


