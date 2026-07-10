import os
import requests
import json
import logging
from dotenv import load_dotenv

# =========================================================================
# פריסת פרסומים אוטומטית לפייסבוק ואינסטגרם (כולל תמיכה בתמונות מקומיות)
# =========================================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')

GRAPH_API_VERSION = "v19.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def post_to_facebook(message, local_image_path=None):
    """מפרסם פוסט (ותמונה במידה ויש) לדף העסקי בפייסבוק."""
    if not PAGE_ID or not ACCESS_TOKEN:
        logger.error("חסרים פרטי גישה לפייסבוק בקובץ .env")
        return
        
    url = f"{BASE_URL}/{PAGE_ID}/photos" if local_image_path else f"{BASE_URL}/{PAGE_ID}/feed"
    
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    
    try:
        if local_image_path and os.path.exists(local_image_path):
            with open(local_image_path, 'rb') as f:
                files = {'source': f}
                response = requests.post(url, data=payload, files=files)
        else:
            # אם רץ בענן ואין את התמונה המקומית, יפרסם רק טקסט (feed)
            url_feed = f"{BASE_URL}/{PAGE_ID}/feed"
            response = requests.post(url_feed, data=payload)
            
        if response.status_code == 200:
            logger.info(f"✅ פוסט פייסבוק פורסם בהצלחה! מזהה: {response.json().get('id', response.json().get('post_id'))}")
        else:
            logger.error(f"❌ שגיאה בפרסום לפייסבוק: {response.text}")
            
    except Exception as e:
        logger.error(f"שגיאת מערכת בזמן השליחה: {e}")

if __name__ == "__main__":
    print("---------------------------------------------------------")
    print("מריץ אוטומציית פרסום לעמוד הפייסבוק 🚀")
    print("---------------------------------------------------------")
    
    post_file = "latest_facebook_post.txt"
    if os.path.exists(post_file):
        with open(post_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
            
        if text:
            # We no longer use a local image, Facebook will fetch the og:image from the link
            post_to_facebook(text, local_image_path=None)
        else:
            logger.error("❌ הקובץ latest_facebook_post.txt ריק!")
    else:
        logger.error(f"❌ לא נמצא הקובץ {post_file}. יש להריץ את auto_writer.py קודם.")

