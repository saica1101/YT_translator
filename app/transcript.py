from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        if "en" not in [t.language_code for t in transcript_list]:
            print(f"警告：動画{video_id}には英語字幕(en)が存在しません。")
            return None
        
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["en"])
        
        transcript_text = " ".join(entry["text"] for entry in transcript)
        return transcript_text
    
    except Exception as e:
        print(f"動画の取得に失敗しました。: {e}")
        return None