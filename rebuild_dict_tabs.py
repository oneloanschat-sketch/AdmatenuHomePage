import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('articles_content.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.strip() == 'אזור':
        start_idx = i
    if 'ליעוץ ראשוני ללא עלות' in line:
        if start_idx != -1:
            end_idx = i
            break

dict_lines = lines[start_idx:end_idx]
terms_list = []
current_term = ""
current_def = []

for line in dict_lines:
    line = line.strip()
    if not line:
        continue
    
    if len(line) < 60 and not line.endswith('.') and not line.endswith(':'):
        if current_term:
            terms_list.append((current_term, "<br>".join(current_def)))
        current_term = line
        current_def = []
    else:
        current_def.append(line)

if current_term:
    terms_list.append((current_term, "<br>".join(current_def)))

groups = {
    'א-ה': [],
    'ו-י': [],
    'כ-ע': [],
    'פ-ת': []
}

letters_1 = ['א', 'ב', 'ג', 'ד', 'ה']
letters_2 = ['ו', 'ז', 'ח', 'ט', 'י']
letters_3 = ['כ', 'ך', 'ל', 'מ', 'ם', 'נ', 'ן', 'ס', 'ע']
letters_4 = ['פ', 'ף', 'צ', 'ץ', 'ק', 'ר', 'ש', 'ת']

for term, dfn in terms_list:
    clean_term = term.strip()
    if not clean_term:
        continue
        
    first_letter = clean_term[0]
    match = re.search(r'[א-ת]', clean_term)
    if match:
        first_letter = match.group(0)
    
    html_term = f'''              <div class="acc-item">
                <button class="acc-head" aria-expanded="false">
                  <strong>{clean_term}</strong>
                  <span class="acc-icon" aria-hidden="true"></span>
                </button>
                <div class="acc-body">
                  <p>{dfn.strip()}</p>
                </div>
              </div>'''
    
    if first_letter in letters_1:
        groups['א-ה'].append(html_term)
    elif first_letter in letters_2:
        groups['ו-י'].append(html_term)
    elif first_letter in letters_3:
        groups['כ-ע'].append(html_term)
    elif first_letter in letters_4:
        groups['פ-ת'].append(html_term)
    else:
        groups['א-ה'].append(html_term)

card_html = f'''<!-- ===== ARTICLE CARD 6 (מילון מונחים עם טאבים) ===== -->
      <article class="article-card">
        <div class="article-card-inner">
          <div class="article-card-body">
            <h2 class="article-card-title">מילון מונחים</h2>
            <p class="article-card-excerpt">מילון מונחים מפורט לשירותכם בו תוכלו לקבל הסבר למונחים ותשובות לשאלות נפוצות.</p>
          </div>
          <button class="article-toggle-btn" aria-expanded="false">
            <span class="btn-text">קרא עוד</span>
            <svg viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7"/></svg>
          </button>

          <div class="article-expand" hidden>
            <div class="article-full-content">
              <p>לחיפוש מושג, בחרו באות המתאימה בסרגל, ולחצו על המונח להצגת ההגדרה המלאה.</p>
              
              <div class="dictionary-tabs">
                <div class="dict-tab-links">
                  <button class="dict-tab-btn active" data-target="dict-group-1">א' - ה'</button>
                  <button class="dict-tab-btn" data-target="dict-group-2">ו' - י'</button>
                  <button class="dict-tab-btn" data-target="dict-group-3">כ' - ע'</button>
                  <button class="dict-tab-btn" data-target="dict-group-4">פ' - ת'</button>
                </div>
                
                <div class="dict-tab-content active" id="dict-group-1">
                  <div class="accordion">
{"\\n".join(groups['א-ה'])}
                  </div>
                </div>
                
                <div class="dict-tab-content" id="dict-group-2" hidden>
                  <div class="accordion">
{"\\n".join(groups['ו-י'])}
                  </div>
                </div>
                
                <div class="dict-tab-content" id="dict-group-3" hidden>
                  <div class="accordion">
{"\\n".join(groups['כ-ע'])}
                  </div>
                </div>
                
                <div class="dict-tab-content" id="dict-group-4" hidden>
                  <div class="accordion">
{"\\n".join(groups['פ-ת'])}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </article>'''

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<!-- ===== ARTICLE CARD 6')
end_idx = html.find('<!-- ===== ARTICLE CARD 10 ===== -->')
if end_idx == -1:
    end_idx = html.find('<!-- ===== ARTICLE CARD 7') # fallback

if start_idx == -1 or end_idx == -1:
    print("Could not find bounds")
    sys.exit(1)

html = html[:start_idx] + card_html + "\\n\\n      " + html[end_idx:]

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Dictionary tabs successfully generated!")
