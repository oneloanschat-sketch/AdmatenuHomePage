import re
with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<svg viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7"/></svg>', '', html)

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Removed arrows!")
