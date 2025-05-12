import isodate
from googleapiclient.discovery import build
from app.config import YOUTUBE_API_KEY
from app.config import GEMINI_API_KEY

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_video_ids_in_playlist(playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in request["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = request.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

def get_video_id(video_url):
    if "youtube.com/watch?v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("/")[-1]
    else:
        raise ValueError("Invalid YouTube URL format.")

def filter_out_shorts(video_ids):
    filtered = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i + 50]
        request = youtube.videos().list(
            part="contentDetails,snippet",
            id=",".join(chunk)
        ).execute()

        for item in request["items"]:
            duration = isodate.parse_duration(
                item["contentDetails"]["duration"])
            title = item["snippet"]["title"]
            if duration.total_seconds() >= 60:
                filtered.append({
                    "videoId": item["id"],
                    "title": title,
                    "duration": duration.total_seconds()
                })
    return filtered

def get_video_id_without_shorts(video_url):
    video_ids = get_video_id(video_url)
    filtered_videos = filter_out_shorts([video_ids])
    return filtered_videos

def get_videos_in_playlist_without_shorts(playlist_id):
    video_ids = get_video_ids_in_playlist(playlist_id)
    filtered_videos = filter_out_shorts(video_ids)
    return filtered_videos