import json
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('extracted_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

# Group terms based on spiraly4u's 5 tabs
groups = {
    'א-ד': [],
    'ה-ח': [],
    'ט-ל': [],
    'מ-ע': [],
    'פ-ת': []
}

letters_1 = ['\u05d0', '\u05d1', '\u05d2', '\u05d3'] # א-ד
letters_2 = ['\u05d4', '\u05d5', '\u05d6', '\u05d7'] # ה-ח
letters_3 = ['\u05d8', '\u05d9', '\u05db', '\u05da', '\u05dc'] # ט-ל
letters_4 = ['\u05de', '\u05dd', '\u05e0', '\u05df', '\u05e1', '\u05e2'] # מ-ע
letters_5 = ['\u05e4', '\u05e3', '\u05e6', '\u05e5', '\u05e7', '\u05e8', '\u05e9', '\u05ea'] # פ-ת

for term, dfn in terms:
    clean_term = term.strip()
    if not clean_term: continue
    
    first_letter = clean_term[0]
    match = re.search(r'[\u05d0-\u05ea]', clean_term)
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
              
    if first_letter in letters_1: groups['א-ד'].append(html_term)
    elif first_letter in letters_2: groups['ה-ח'].append(html_term)
    elif first_letter in letters_3: groups['ט-ל'].append(html_term)
    elif first_letter in letters_4: groups['מ-ע'].append(html_term)
    elif first_letter in letters_5: groups['פ-ת'].append(html_term)
    else: groups['א-ד'].append(html_term) # fallback

new_tabs_html = f'''<div class="dictionary-tabs">
                <div class="dict-tab-links">
                  <button class="dict-tab-btn active" data-target="dict-group-1">א' - ד'</button>
                  <button class="dict-tab-btn" data-target="dict-group-2">ה' - ח'</button>
                  <button class="dict-tab-btn" data-target="dict-group-3">ט' - ל'</button>
                  <button class="dict-tab-btn" data-target="dict-group-4">מ' - ע'</button>
                  <button class="dict-tab-btn" data-target="dict-group-5">פ' - ת'</button>
                </div>
                
                <div class="dict-tab-content active" id="dict-group-1">
                  <div class="accordion">
{chr(10).join(groups['א-ד'])}
                  </div>
                </div>
                
                <div class="dict-tab-content" id="dict-group-2" hidden>
                  <div class="accordion">
{chr(10).join(groups['ה-ח'])}
                  </div>
                </div>
                
                <div class="dict-tab-content" id="dict-group-3" hidden>
                  <div class="accordion">
{chr(10).join(groups['ט-ל'])}
                  </div>
                </div>
                
                <div class="dict-tab-content" id="dict-group-4" hidden>
                  <div class="accordion">
{chr(10).join(groups['מ-ע'])}
                  </div>
                </div>
                
                <div class="dict-tab-content" id="dict-group-5" hidden>
                  <div class="accordion">
{chr(10).join(groups['פ-ת'])}
                  </div>
                </div>
              </div>'''

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<div class="dictionary-tabs">')
# Find the end of the last dict-group which is now currently 4 (or 5)
# Actually, let's just find the closing tags of the article card wrapper.
# We know the dictionary-tabs is right before:
#               </div>
#             </div>
#           </div>
end_idx = html.find('</div>\n            </div>\n          </div>', start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_tabs_html + "\n            " + html[end_idx:]
    with open('articles.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Rebuilt tabs perfectly!")
else:
    print("Could not find dictionary-tabs block.")
