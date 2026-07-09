import os
import re

with open('articles_content.txt', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

content_lines = []
title = 'בנק ישראל מוריד את הריבית... ואתם עדיין משלמים כאילו כלום לא קרה?'
excerpt = 'יכול להיות שהבנק שלכם מרוויח אלפי שקלים על חשבונכם – בכל שנה. בואו נדבר דוגרי.'

html = f"""
<article class="article-card" id="article-refinance-manual">
  <div class="article-card-inner">
    <div class="article-card-badge">💰 פיננסים ומשכנתא</div>
    <h2 class="article-card-title">{title}</h2>
    <p class="article-card-excerpt">{excerpt}</p>
    <div class="article-card-meta">
      <span class="meta-tag">מיחזור משכנתא</span>
    </div>
  </div>
  <div class="article-expand" hidden>
    <div class="article-full-content">
"""

for line in lines[4:]:
    line = line.strip()
    if not line: continue
    if line.startswith('# '):
        html += f'      <h3 class="article-section-title">{line[2:]}</h3>\n'
    elif line.startswith('## '):
        html += f'      <h3 class="article-section-title">{line[3:]}</h3>\n'
    elif line.startswith('**') and line.endswith('**'):
        html += f'      <p><strong>{line[2:-2]}</strong></p>\n'
    elif line.startswith('* '):
        html += f'      <ul><li>{line[2:]}</li></ul>\n'
    else:
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        html += f'      <p>{line}</p>\n'

html = html.replace('</ul>\n      <ul>', '')

html += """
      <div class="article-cta-box">
        <p>📞 מומחי אדמתנו ביתנו כאן עבורכם לבדיקה וייעוץ אישי. השאירו פרטים או חייגו אלינו לשיחת התייעצות ללא התחייבות.</p>
        <a href="https://wa.me/972587554588" target="_blank" rel="noopener" class="btn btn-primary">דברו איתנו בוואטסאפ</a>
      </div>
    </div>
  </div>
  <button class="article-toggle-btn" aria-expanded="false">קראו את המאמר המלא &larr;</button>
</article>
"""

html_file = 'articles.html'
with open(html_file, 'r', encoding='utf-8') as f:
    page_content = f.read()

page_content = page_content.replace('<!-- ===== ARTICLE CARD 8 ===== -->', '<!-- ===== ARTICLE CARD 8 ===== -->\n' + html)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(page_content)

os.remove('מיחזור משכנתא.docx')
os.remove('articles_content.txt')
print('Article added and docx removed!')
