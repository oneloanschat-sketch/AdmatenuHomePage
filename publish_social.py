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
        if local_image_path:
            with open(local_image_path, 'rb') as f:
                files = {'source': f}
                response = requests.post(url, data=payload, files=files)
        else:
            response = requests.post(url, data=payload)
            
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
    
    text = (
        "איך המשכנתא שלכם יכולה להציל אתכם ממינוס תמידי? 🤔\n"
        "הרבה אנשים לא יודעים את זה, אבל הנכס שלכם יכול לחלץ אתכם מהלוואות קטנות, ריביות מטורפות בכרטיסי אשראי והלוואות צרכניות.\n"
        "הפתרון נקרא \"איחוד הלוואות תחת משכנתא\" – מחזירים הלוואה אחת גדולה עם ריבית של משכנתא (שהיא נמוכה יותר מכל הלוואה רגילה בבנק), והתזרים החודשי שלכם קופץ פלאים!\n"
        "רוצים לדעת אם זה מתאים לכם? דברו איתנו בפרטי או בתגובות ⬇️\n"
        "#משכנתא #איחודהלוואות #אדמתנוביתנו #פיננסים"
    )
    
    # מיקום התמונה המקומית בתיקיית ה-artifacts
    image_path = r"C:\Users\1\.gemini\antigravity-ide\brain\57a1f589-9981-4950-99df-58b621d9e3f8\debt_consolidation_ad_1783072858495.png"
    
    post_to_facebook(text, local_image_path=image_path)
