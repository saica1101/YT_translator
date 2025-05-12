from app.transcript import get_transcript
from app.summarizer import summarize_and_translate
from app.youtube_client import get_videos_in_playlist_without_shorts
from app.notion_uploader import upload_to_notion
import time

GENERATE_SUMMARY = True  # Trueにすると要約を生成してNotionにアップロードします

playlist_id = "PLjxrf2q8roU1nbstACpBBSwHa-BuOILlM"

videos = get_videos_in_playlist_without_shorts(playlist_id)
for video in videos:
    try:
        print(f"\n処理開始: {video['title']} (ID: {video['videoId']})")
    except Exception as e:
        continue
    transcript = get_transcript(video["videoId"])
    if transcript:
        try:
            if GENERATE_SUMMARY:
                summary = summarize_and_translate(transcript)
                upload_to_notion(video["videoId"], video["title"], summary)
            else:
                upload_to_notion(video["videoId"], video["title"])
            print(f"動画{video['videoId']}の要約をNotionにアップロードしました。")
            time.sleep(5)
        except Exception as e:
            print(f"エラー: 動画 {video['videoId']}の要約またはアップロード中に問題が発生しました。 : {e}")
    else:
        print(f"エラー: 動画 {video['videoId']}の字幕を取得できませんでした。")