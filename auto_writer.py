import os
import re
import datetime
import random
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
    
    # נושאים אפשריים לבחירה אקראית
    topics = [
        "איחוד הלוואות ואיך זה מציל ממשבר", 
        "מה עושים אם הבנק מסרב למשכנתא", 
        "איך לקבל מימון לנכס ללא טאבו או היתר בנייה",
        "המדריך המלא למחזור משכנתא וחיסכון בעלויות",
        "משכנתא לבנייה עצמית: כל מה שצריך לדעת",
        "איך לשפר את דירוג האשראי לפני בקשת משכנתא",
        "פתרונות מימון לעסקים קטנים בחברה הערבית",
        "משכנתא חוץ בנקאית: מתי זה הפתרון הנכון?"
    ]
    topic = random.choice(topics)
    
    prompt = f"""
    כתוב מאמר שיווקי מקצועי, מקיף ומעמיק (כ-450 עד 500 מילים) לאתר 'אדמתנו ביתנו' שעוסק בייעוץ משכנתאות ופיננסים בחברה הערבית.
    הנושא: {topic}.
    
    חשוב מאוד: המאמר חייב להיות משכנע מאוד, ולכלול לאורך הטקסט ובמיוחד בסופו הנעה ברורה וחד-משמעית לפעולה (CTA) - להשאיר פרטים לייעוץ או לעבור לשיחה עם הצ'אט-בוט/מומחה שלנו בוואטסאפ!
    
    עליך להחזיר **רק** קוד HTML (ללא טקסט מקדים וללא תגיות markdown) שבנוי בדיוק במבנה הבא:
    <article class="article-card" id="article-NEW">
      <div class="article-card-inner">
        <div class="article-card-badge">💼 פיננסים</div>
        <h2 class="article-card-title">[כותרת מושכת וחזקה]</h2>
        <p class="article-card-excerpt">[תקציר של שורה אחת המעורר סקרנות ומניע לקריאה]</p>
        <div class="article-card-meta">
          <span class="meta-tag">[תגית רלוונטית]</span>
        </div>
      </div>
      <div class="article-expand" hidden>
        <div class="article-full-content">
          <p>[פסקת מבוא שמושכת את הקורא]</p>
          
          <h3 class="article-section-title">[כותרת משנה 1]</h3>
          <p>[תוכן מפורט ומעמיק]</p>
          <p>[תוכן נוסף עם ערך מקצועי אמיתי]</p>
          
          <blockquote class="article-quote">[משפט הדגשה מרכזי מהמאמר שאי אפשר להתעלם ממנו]</blockquote>
          
          <h3 class="article-section-title">[כותרת משנה 2 - למה לבחור בנו?]</h3>
          <p>[הסבר למה המומחים של אדמתנו ביתנו הם הפתרון]</p>
          
          <p>אל תחכו שהמצב יחמיר! השאירו עכשיו פרטים בטופס באתר שלנו או לחצו על הכפתור למטה כדי לעבור לשיחה מיידית בוואטסאפ ולקבל פתרון מותאם אישית.</p>
          <div class="article-cta-box">
            <p>📞 מומחי אדמתנו ביתנו כאן עבורכם לבדיקה וייעוץ אישי. השאירו פרטים או חייגו אלינו לשיחת התייעצות ללא התחייבות.</p>
            <a href="https://wa.me/972587554588" target="_blank" rel="noopener" class="btn btn-primary">דברו איתנו בוואטסאפ</a>
          </div>
        </div>
      </div>
      <button class="article-toggle-btn" aria-expanded="false">קראו את המאמר המלא &larr;</button>
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
