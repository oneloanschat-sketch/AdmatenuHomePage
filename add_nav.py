import os

def insert_podcast_link(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nav
    content = content.replace(
        '<a href="articles.html">מאמרים</a>\n    </nav>', 
        '<a href="articles.html">מאמרים</a>\n      <a href="podcasts.html">פודקאסטים</a>\n    </nav>'
    )
    # Mobile nav
    content = content.replace(
        '<a href="articles.html">מאמרים</a>\n    <a href="tel:0545554588" class="btn btn-primary"',
        '<a href="articles.html">מאמרים</a>\n    <a href="podcasts.html">פודקאסטים</a>\n    <a href="tel:0545554588" class="btn btn-primary"'
    )
    # Footer
    content = content.replace(
        '<li><a href="articles.html">מאמרים</a></li>\n        </ul>', 
        '<li><a href="articles.html">מאמרים</a></li>\n          <li><a href="podcasts.html">פודקאסטים</a></li>\n        </ul>'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

insert_podcast_link('index.html')
insert_podcast_link('articles.html')
print("Done")
