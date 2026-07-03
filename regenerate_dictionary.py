import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read original raw text
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
    
    # Heuristic for detecting a term vs definition
    if len(line) < 60 and not line.endswith('.') and not line.endswith(':'):
        if current_term:
            terms_list.append((current_term, "<br>".join(current_def)))
        current_term = line
        current_def = []
    else:
        current_def.append(line)

if current_term:
    terms_list.append((current_term, "<br>".join(current_def)))

print(f"Extracted {len(terms_list)} terms from source.")

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
    
    html_term = f'''            <div class="acc-item">
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

def build_card(card_num, title, group_html):
    joined_html = "\n".join(group_html)
    return f'''<!-- ===== ARTICLE CARD {card_num} ===== -->
      <article class="article-card">
        <div class="article-card-inner">
          <div class="article-card-body">
            <h2 class="article-card-title">{title}</h2>
            <p class="article-card-excerpt">חלק מתוך מילון מונחים מפורט לשירותכם בו תוכלו לקבל הסבר למונחים.</p>
          </div>
          <button class="article-toggle-btn" aria-expanded="false">
            <span class="btn-text">קרא עוד</span>
            <svg viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7"/></svg>
          </button>

          <div class="article-expand" hidden>
            <div class="article-full-content">
              <p>מילון מונחים מפורט לשירותכם בו תוכלו לקבל הסבר למונחים ותשובות לשאלות נפוצות. לחצו על המונח להצגת ההגדרה המלאה.</p>
              <div class="accordion">
{joined_html}
              </div>
            </div>
          </div>
        </div>
      </article>'''

new_cards = []
new_cards.append(build_card("6 (מילון א'-ה')", "מילון מונחים א'-ה'", groups['א-ה']))
new_cards.append(build_card("6.1 (מילון ו'-י')", "מילון מונחים ו'-י'", groups['ו-י']))
new_cards.append(build_card("6.2 (מילון כ'-ע')", "מילון מונחים כ'-ע'", groups['כ-ע']))
new_cards.append(build_card("6.3 (מילון פ'-ת')", "מילון מונחים פ'-ת'", groups['פ-ת']))

new_cards_html = "\n\n      ".join(new_cards) + "\n\n"

# Now read articles.html and replace the 4 dictionary cards
with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<!-- ===== ARTICLE CARD 6 (מילון א\'-ה\') ===== -->')

card63_start = html.find('<!-- ===== ARTICLE CARD 6.3 (מילון פ\'-ת\') ===== -->')
end_idx = html.find('</article>', card63_start) + len('</article>')


if start_idx == -1 or end_idx == -1:
    print("Could not find the bounds to replace in articles.html")
    sys.exit(1)

html = html[:start_idx] + new_cards_html + html[end_idx:]

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Dictionary rebuilt as accordions successfully!")
