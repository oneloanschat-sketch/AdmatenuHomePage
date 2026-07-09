import os

def fix_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        c = f.read()
    
    search_mobile = '    <a href="articles.html">מאמרים</a>\n    <a href="tel:0545554588"'
    replace_mobile = '    <a href="articles.html">מאמרים</a>\n    <a href="podcasts.html">פודקאסטים</a>\n    <a href="tel:0545554588"'
    if 'href="podcasts.html">פודקאסטים</a>\n    <a href="tel:0545554588"' not in c:
        c = c.replace(search_mobile, replace_mobile)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)

def fix_articles():
    with open('articles.html', 'r', encoding='utf-8') as f:
        c = f.read()
    
    search_main = '      <a href="articles.html" class="active">מאמרים</a>'
    replace_main = '      <a href="articles.html" class="active">מאמרים</a>\n      <a href="podcasts.html">פודקאסטים</a>'
    if 'href="podcasts.html">פודקאסטים</a>' not in c:
        c = c.replace(search_main, replace_main)
        
    search_mobile = '    <a href="articles.html" class="active">מאמרים</a>\n    <a href="tel:0545554588"'
    replace_mobile = '    <a href="articles.html" class="active">מאמרים</a>\n    <a href="podcasts.html">פודקאסטים</a>\n    <a href="tel:0545554588"'
    if 'href="podcasts.html">פודקאסטים</a>\n    <a href="tel:0545554588"' not in c:
        c = c.replace(search_mobile, replace_mobile)

    with open('articles.html', 'w', encoding='utf-8') as f:
        f.write(c)

fix_index()
fix_articles()
