import requests
import pandas as pd
import time

# API_KEY = "AIzaSyCIddjWNtfkTzgjyojXwJj0oBO8ZM4PyeQ"
API_KEY = "AIzaSyD9ASbYJWsFNsgLFRmBBpeXEmeoq_9Z3bY"

# channel_ids = [
#     "UCzkTtH8IIccS11vP_8UINJQ",
#     "UCOq55Zy7QM_lBZRzgeuFIHw",
# ]  # Replace with your channel IDs

# Part 1
channel_ids = [
    "UCX6OQ3DkcsbYNE6H8uQQuVA",
    "UCbCmjCuTUZos6Inko4u57UQ",
    "UCbp9MyKCTEww4CxEzc_Tp0Q",
    "UCcdwLMPsaU2ezNSJU1nFoBQ",
    "UC2tsySbe9TNrI-xh2lximHA",
    "UCRijo3ddMTht_IHyNSNXpNQ",
    "UC5gxP-2QqIh_09djvlm9Xcg",
    "UCgyeJxD05YnoDquRMNBfBqw",
    "UCyEd6QBSgat5kkC6svyjudA",
    "UCBJycsmduvYEL83R_U4JriQ",
    "UC_DmOS_FBvO4H27U7X0OtRg",
    "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
    "UCcgVECVN4OKV6DH1jLkqmcA",
    "UCdoLeDxfcGwvj_PRl7TLTzQ",
    "UCBwSufNse8VMBvQM_rCSvgQ",
    "UCKGiTasUqLcZUuUjQiyKotw",
]  # Replace with your channel IDs

# Part 2
# channel_ids = [
#     "UChGJGhZ9SOOHvBB0Y4DOO_w",
#     "UC-SV8-bUJfXjrRMnp7F8Wzw",
#     "UCWXCrItCF6ZgXrdozUS-Idw",
#     "UCczFdwWpVEpoqb-eMm4c4dQ",
#     "UCGCPAOQDZa_TTTXDr5byjww",
#     "UCDogdKl7t7NHzQ95aEwkdMw",
#     "UCagjd6FJVi3nxR3HxH7KGQw",
#     "UCz4a7agVFr1TxU-mpAP8hkw",
#     "UCoOae5nYA7VqaXzerajD0lg",
#     "UCvK4bOhULCpmLabd2pDMtnA",
#     "UCWZZowzfDwihJ8VbQ3H8ivw",
#     "UCSAUGyc_xA8uYzaIVG6MESQ",
#     "UCFIRm1Fv1VC4DZxmYyvNOTQ",
#     "UCWoEpiHaC7LOQhaHFT8Rx7A",
#     "UCHa-hWHrTt4hqh-WiHry3Lw",
#     "UCiAq_SU0ED1C6vWFMnw8Ekg",
# ]  # Replace with your channel IDs

# published_after = "2019-01-01T00:00:00Z"  # Restrict to videos uploaded since 2019
published_after = "2024-08-06T00:00:00Z"  # Restrict to videos uploaded since 08-06-2024


def get_channel_videos(channel_id):
    # Initialize a list to hold video IDs
    video_ids = []
    search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=id&order=date&maxResults=50&publishedAfter={published_after}"

    while True:
        response = requests.get(search_url).json()
        if "items" not in response:
            break

        video_ids += [
            item["id"]["videoId"]
            for item in response["items"]
            if item["id"]["kind"] == "youtube#video"
        ]

        if "nextPageToken" in response:
            search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=id&order=date&maxResults=50&pageToken={response['nextPageToken']}&publishedAfter={published_after}"
        else:
            break

    return video_ids


def get_video_details(video_ids):
    video_details = []
    for video_id in video_ids:
        video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={API_KEY}"
        response = requests.get(video_url).json()

        if "items" in response and len(response["items"]) > 0:
            video_data = response["items"][0]
            video_details.append(
                {
                    "Video ID": video_id,
                    "Title": video_data["snippet"]["title"],
                    "Thumbnail": video_data["snippet"]["thumbnails"]["default"]["url"],
                    "Date": video_data["snippet"]["publishedAt"],
                    "Likes": video_data["statistics"].get("likeCount", 0),
                    "Favorites": video_data["statistics"].get("favoriteCount", 0),
                    "Views": video_data["statistics"].get("viewCount", 0),
                    "Comments": video_data["statistics"].get("commentCount", 0),
                }
            )

    return video_details


def get_channel_details(channel_id):
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={API_KEY}"
    response = requests.get(channel_url).json()

    if "items" in response and len(response["items"]) > 0:
        channel_data = response["items"][0]
        return {
            "Channel ID": channel_id,
            "Channel Title": channel_data["snippet"]["title"],
            "Subscribers": channel_data["statistics"].get("subscriberCount", 0),
        }
    return {}


# Initialize a list to hold the combined data
all_data = []

for channel_id in channel_ids:
    print(f"Fetching data for channel: {channel_id}")

    # Get channel details
    channel_details = get_channel_details(channel_id)

    # Get all video IDs for the channel
    video_ids = get_channel_videos(channel_id)

    # Get details for each video
    video_details = get_video_details(video_ids)

    # Combine channel and video details
    for video in video_details:
        video.update(channel_details)
        all_data.append(video)

    # Sleep to respect API rate limits
    time.sleep(1)

# Create a DataFrame and save to CSV
df = pd.DataFrame(all_data)
df.to_csv("../data/youtube_channel_data_test_1.csv", index=False)

print("Dataset created successfully!")
