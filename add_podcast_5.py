import os

def add_new_podcast():
    with open('podcasts.html', 'r', encoding='utf-8') as f:
        c = f.read()

    new_js = '''    'real-estate': {
      title: 'מימון נדל״ן: אדמתנו ביתנו',
      desc: 'המדריך המלא לקבלת מימון לעסקאות נדל״ן מורכבות בחברה הערבית - ירושות, בנייה בשלבים ופתרונות חוץ-בנקאיים.',
      file: 'assets/videos/real-estate.mp4'
    },
    'no-tabu': {
      title: 'משכנתא ללא טאבו: שוברים את המיתוס',
      desc: 'חושבים שאי אפשר לקבל משכנתא בלי רישום בטאבו? בואו לגלות איך אנחנו משיגים פתרונות מימון גם לנכסים בהליכי הסדרה.',
      file: 'assets/videos/no-tabu.mp4'
    }'''

    new_html = '''        <div class="playlist-item" data-id="no-tabu">
          <div class="item-icon">
            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div class="item-content">
            <div class="item-title">משכנתא ללא טאבו: שוברים את המיתוס</div>
            <div class="item-duration">צפו עכשיו</div>
          </div>
        </div>

      </div>
    </div>'''

    if "'no-tabu': {" not in c:
        # Update JS dictionary
        c = c.replace('''    'real-estate': {
      title: 'מימון נדל״ן: אדמתנו ביתנו',
      desc: 'המדריך המלא לקבלת מימון לעסקאות נדל״ן מורכבות בחברה הערבית - ירושות, בנייה בשלבים ופתרונות חוץ-בנקאיים.',
      file: 'assets/videos/real-estate.mp4'
    }''', new_js)

        # Update Playlist HTML (inject before closing div)
        # Search for real-estate item and replace the end
        search_html = '''        <div class="playlist-item" data-id="real-estate">
          <div class="item-icon">
            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div class="item-content">
            <div class="item-title">מימון נדל״ן: אדמתנו ביתנו</div>
            <div class="item-duration">צפו עכשיו</div>
          </div>
        </div>

      </div>
    </div>'''
        
        # In case the whitespace differs slightly, use string splitting or just regex.
        # But this should be exact.
        c = c.replace(search_html, search_html.replace('      </div>\n    </div>', new_html))

    with open('podcasts.html', 'w', encoding='utf-8') as f:
        f.write(c)

add_new_podcast()
print("Podcast added")
