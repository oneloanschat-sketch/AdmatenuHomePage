import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('extracted_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

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

for term, dfn in terms:
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

new_tabs_html = f'''<div class="dictionary-tabs">
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
              </div>'''

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<div class="dictionary-tabs">')
end_idx = html.find('</div>\n            </div>\n          </div>', start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_tabs_html + "\n            " + html[end_idx:]
    with open('articles.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Replaced dictionary content successfully!")
else:
    print("Could not find dictionary-tabs block.")
