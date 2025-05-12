from notion_client import Client
from app.config import NOTION_API_KEY, NOTION_DATABASE_ID
from typing import Optional

notion = Client(auth=NOTION_API_KEY)

def upload_to_notion(video_id, title, summary=None):
    page = notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties={
            "ID": { # "ID" プロパティを title 型に合わせる
                "title": [
                    {
                        "text": {
                            "content": video_id
                        }
                    }
                ]
            },
            "タイトル": { # "タイトル" プロパティを rich_text 型に合わせる
                "rich_text": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "URL": {
                "url": f"https://www.youtube.com/watch?v={video_id}"
            },
            "視聴済み": {
                "checkbox": False
            }
        }
    )

    page_id = page["id"]

    notion.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": summary if summary else "要約はありません",
                            },
                        }
                    ]
                }
            }
        ]
    )