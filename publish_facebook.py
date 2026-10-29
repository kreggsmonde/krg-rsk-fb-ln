"""
Facebook Page Video Publisher (Meta Graph API v20.0)
Single API Call Direct Upload Architecture
"""
import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()
GRAPH_API_VERSION = "v20.0"

def get_facebook_credentials():
    """
    Retrieves FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN from environment.
    If running locally and not set, seamlessly resolves them from META_LONG_LIVED_ACCESS_TOKEN.
    """
    page_id = (os.getenv('FB_PAGE_ID') or os.getenv('FACEBOOK_PAGE_ID') or '').strip()
    access_token = (os.getenv('FB_PAGE_ACCESS_TOKEN') or os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN') or '').strip()

    if page_id and access_token:
        return page_id, access_token

    # Local fallback via META_LONG_LIVED_ACCESS_TOKEN in Windows User Variables
    meta_user_token = os.getenv('META_LONG_LIVED_ACCESS_TOKEN')
    if not meta_user_token and sys.platform == 'win32':
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment')
            meta_user_token, _ = winreg.QueryValueEx(key, 'META_LONG_LIVED_ACCESS_TOKEN')
        except Exception:
            pass

    if meta_user_token:
        try:
            url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/accounts"
            params = {"access_token": meta_user_token, "limit": 100}
            target = None
            while url:
                resp = requests.get(url, params=params, timeout=15)
                if resp.status_code != 200:
                    break
                data = resp.json()
                for p in data.get("data", []):
                    if p.get("id") == "948526841675964" or "kreggsmonde" in p.get("name", "").lower():
                        target = p
                        break
                if target:
                    break
                url = data.get("paging", {}).get("next")
                params = None

            if target:
                return target.get("id"), target.get("access_token")
        except Exception as e:
            print(f"[facebook] Заметка при автораспознавании: {e}")

    print("[facebook] Данные FB_PAGE_ID или FB_PAGE_ACCESS_TOKEN не настроены.")
    return None, None

def upload_to_facebook(video_path: str, title: str, description: str):
    """
    Publishes a video to Facebook Page in strictly ONE single API call (multipart POST).
    """
    if not os.path.exists(video_path):
        print(f"[facebook] Ошибка: видеофайл не найден: {video_path}")
        return None

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    page_id, access_token = get_facebook_credentials()
    if not page_id or not access_token:
        print(f"[facebook] Ошибка: видеофайл не найден: {video_path}")
        return None

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/videos"
    print(f"[facebook] Начинаю загрузку на страницу {page_id} ({file_size_mb:.2f} MB)...")
    print("[facebook] Вызов Meta API: 1 единственный прямой POST...")

    t0 = time.time()
    try:
        with open(video_path, 'rb') as vf:
            files = {'source': (os.path.basename(video_path), vf, 'video/mp4')}
            data = {
                'title': title,
                'description': description,
                'access_token': access_token
            }
            # Strictly ONE single API call
            res = requests.post(url, files=files, data=data, timeout=600)

        elapsed = time.time() - t0
        if res.status_code == 200:
            result = res.json()
            vid_id = result.get('id')
            print(f"[facebook] УСПЕХ! Видео опубликовано за {elapsed:.1f}s одним вызовом API.")
            print(f"[facebook] ID видео Facebook: {vid_id}")
            return result
        else:
            print(f"[facebook] Ошибка Meta API ({res.status_code}): {res.text}")
            return None
    except Exception as e:
        print(f"[facebook] Исключение при публикации: {e}")
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Прямой тест загрузки видео на Facebook")
    parser.add_argument("video_path", type=str, help="Путь к MP4-видеофайлу")
    parser.add_argument("--title", type=str, default="Тестовый выпуск - Искусство отношений", help="Название видео")
    parser.add_argument("--desc", type=str, default="Автоматический тест прямой публикации (1 вызов API)", help="Описание")
    args = parser.parse_args()

    upload_to_facebook(args.video_path, args.title, args.desc)
