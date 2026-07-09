import re

with open('articles_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

parts = re.split(r'--- (.*?) ---', content)
# parts[0] is empty
# parts[1] is name1
# parts[2] is content1
# parts[3] is name2
# parts[4] is content2
# parts[5] is name3
# parts[6] is content3

def create_article_html(id, title, badge, excerpt, tag, html_content):
    return f"""
    <!-- ===== ARTICLE CARD {id} ===== -->
    <article class="article-card" id="article-{id}">
      <div class="article-card-inner">
        <div class="article-card-badge">{badge}</div>
        <h2 class="article-card-title">{title}</h2>
        <p class="article-card-excerpt">{excerpt}</p>
        <div class="article-card-meta">
          <span class="meta-tag">{tag}</span>
        </div>
      </div>
      <div class="article-expand" hidden>
        <div class="article-full-content">
{html_content}
        </div>
      </div>
      <button class="article-toggle-btn" aria-expanded="false">קראו את המאמר המלא ←</button>
    </article>
"""

# Process Article 1: מילון
lines1 = [x.strip() for x in parts[2].strip().split('\n') if x.strip()]
title1 = lines1[0]
html_content1 = ""
for i in range(1, len(lines1)):
    if i == 1:
        html_content1 += f"          <p>{lines1[i]}</p>\n"
    else:
        if i % 2 == 0:
            html_content1 += f"          <div class=\"insight-block\"><h3>{lines1[i]}</h3>\n"
        else:
            html_content1 += f"          <p>{lines1[i]}</p></div>\n"

# Fix unclosed div if needed
if len(lines1) % 2 == 1:
    html_content1 += "</div>\n"

article1_html = create_article_html(6, title1, "📖 מילון", "מילון מונחים מפורט לשירותכם בו תוכלו לקבל הסבר למונחים ותשובות לשאלות נפוצות.", "מושגים", html_content1)

# Process Article 2: בית ללא טאבו
lines2 = [x.strip() for x in parts[4].strip().split('\n') if x.strip()]
title2 = lines2[0]
html_content2 = ""
for line in lines2[1:]:
    html_content2 += f"          <p>{line}</p>\n"
article2_html = create_article_html(7, title2, "🏠 טאבו", "אם אתם שוקלים לקחת משכנתא על בית במגזר הערבי ואין לכם טאבו מוסדר, המאמר הזה בשבילכם.", "משכנתא", html_content2)

# Process Article 3: מסחרי
lines3 = [x.strip() for x in parts[6].strip().split('\n') if x.strip()]
title3 = lines3[0]
html_content3 = ""
for line in lines3[1:]:
    if len(line) < 60 and not line.endswith('.'):
        html_content3 += f"          <h3>{line}</h3>\n"
    else:
        html_content3 += f"          <p>{line}</p>\n"
article3_html = create_article_html(8, title3, "🏢 מסחרי", "על משכנתא מסחרית ומגמות בשוק הנדל״ן המניב. איפה כדאי להשקיע ב-2026?", "השקעות", html_content3)


with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Insert the articles before the end of the container in the main
insert_pos = html.find('  </div>\n</main>')
if insert_pos != -1:
    new_html = html[:insert_pos] + article1_html + article2_html + article3_html + html[insert_pos:]
else:
    print("Could not find insertion point for articles!")
    exit(1)

# Add banner notification right after <header ...>
# Banner logic: Check if within a week from today (approx June 22, 2026 -> valid until June 29, 2026)
banner_html = """
<!-- ============================ NOTIFICATION BANNER ============================ -->
<div id="new-articles-banner" style="background: linear-gradient(135deg, #0E3A5F, #195283); color: #fff; text-align: center; padding: 12px; position: relative; z-index: 1000; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: none;">
  <span style="font-size: 1.1rem;">🎉 הוספנו 3 מאמרים חדשים ומרתקים במיוחד בשבילכם! <a href="#article-6" style="color: #FFD700; text-decoration: underline; font-weight: bold; margin-right: 10px;">קראו עכשיו</a></span>
  <button onclick="document.getElementById('new-articles-banner').style.display='none';" style="background: none; border: none; color: white; cursor: pointer; float: left; margin-left: 10px; font-size: 1.2rem;" aria-label="סגור התראה">✖</button>
</div>
<script>
  // Hide the banner after 7 days from now
  const publishDate = new Date('2026-06-22T00:00:00');
  const expirationDate = new Date(publishDate.getTime() + 7 * 24 * 60 * 60 * 1000);
  if (new Date() < expirationDate) {
    document.getElementById('new-articles-banner').style.display = 'block';
  }
</script>
"""

# Insert banner after header open
header_pos = new_html.find('<header class="site-header" id="top">')
if header_pos != -1:
    new_html = new_html[:header_pos] + banner_html + new_html[header_pos:]

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated articles.html successfully.")
