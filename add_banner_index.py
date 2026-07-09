with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

banner_html = """
<!-- ============================ NOTIFICATION BANNER ============================ -->
<div id="new-articles-banner" style="background: linear-gradient(135deg, #0E3A5F, #195283); color: #fff; text-align: center; padding: 12px; position: relative; z-index: 1000; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: none;">
  <span style="font-size: 1.1rem;">🎉 הוספנו 3 מאמרים חדשים ומרתקים בעמוד המאמרים שלנו! <a href="articles.html" style="color: #FFD700; text-decoration: underline; font-weight: bold; margin-right: 10px;">קראו עכשיו</a></span>
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

if "new-articles-banner" not in html:
    header_pos = html.find('<header class="site-header" id="top">')
    if header_pos != -1:
        new_html = html[:header_pos] + banner_html + html[header_pos:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("Updated index.html successfully.")
    else:
        print("Header not found in index.html")
else:
    print("Banner already in index.html")
