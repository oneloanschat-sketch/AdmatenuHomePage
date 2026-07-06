import os
import re
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# =========================================================================
# כותב המאמרים האוטומטי (מופעל בענן דרך GitHub Actions)
# =========================================================================

def generate_article_html():
    """קורא ל-API של Gemini ומבקש מאמר חדש בפורמט HTML תואם לאתר"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ שגיאה: לא נמצא מפתח GEMINI_API_KEY")
        return None
        
    genai.configure(api_key=api_key)
    
    # נושאים אפשריים לבחירה אקראית (או לפי יום)
    topics = ["איחוד הלוואות ואיך זה מציל ממשבר", "מה עושים אם הבנק מסרב למשכנתא", "איך לקבל מימון לנכס ללא טאבו או היתר בנייה"]
    topic = topics[datetime.datetime.now().day % len(topics)]
    
    prompt = f"""
    כתוב מאמר שיווקי מקצועי, קצר וקולע (כ-150 מילים) לאתר 'אדמתנו ביתנו' שעוסק בייעוץ משכנתאות ופיננסים למגזר הערבי והדרוזי.
    הנושא: {topic}.
    
    עליך להחזיר **רק** קוד HTML (ללא טקסט מקדים וללא תגיות markdown) שבנוי בדיוק במבנה הבא:
    <article class="article-card" id="article-NEW">
      <div class="article-card-inner">
        <div class="article-card-badge">💼 פיננסים</div>
        <h2 class="article-card-title">[כותרת מושכת]</h2>
        <p class="article-card-excerpt">[תקציר של שורה אחת המעורר סקרנות]</p>
        <div class="article-card-meta">
          <span class="meta-tag">[תגית רלוונטית]</span>
        </div>
      </div>
      <div class="article-expand" hidden>
        <div class="article-full-content">
          <p>[פסקה 1 של המאמר]</p>
          <p>[פסקה 2 של המאמר]</p>
          <blockquote class="article-quote">[משפט הדגשה מרכזי מהמאמר]</blockquote>
          <p>מומחי אדמתנו ביתנו כאן עבורכם לבדיקה וייעוץ. השאירו פרטים או חייגו אלינו.</p>
        </div>
      </div>
    </article>
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        html_content = response.text.strip()
        
        # ניקוי פורמט קוד אם קפץ
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
            
        return html_content.strip()
    except Exception as e:
        print(f"❌ שגיאה בהפעלת המודל: {e}")
        return None

def inject_to_website(new_html):
    """שותל את המאמר החדש בראש רשימת המאמרים בקובץ articles.html"""
    file_path = "articles.html"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # החלפת ה-ID למזהה ייחודי מבוסס זמן
        unique_id = f"article-{int(datetime.datetime.now().timestamp())}"
        new_html = new_html.replace('id="article-NEW"', f'id="{unique_id}"')
        
        # מחפש את המאמר הראשון כדי להשתיל לפניו
        match = re.search(r'<article class="article-card"', content)
        if match:
            insert_pos = match.start()
            updated_content = content[:insert_pos] + new_html + "\n\n      " + content[insert_pos:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("✅ המאמר הושתל בהצלחה באתר!")
        else:
            print("❌ לא נמצאה נקודת השתלה באתר.")
    except Exception as e:
        print(f"❌ שגיאה בעריכת הקובץ: {e}")

if __name__ == "__main__":
    print("מתחיל תהליך כתיבה אוטומטי (Auto Writer)...")
    article_html = generate_article_html()
    if article_html:
        inject_to_website(article_html)
