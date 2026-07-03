import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

card6_start = html.find('<!-- ===== ARTICLE CARD 6 ===== -->')
if card6_start == -1:
    print("Card 6 start not found")
    exit(1)

card6_end = html.find('</article>', card6_start)
if card6_end == -1:
    print("Card 6 end not found")
    exit(1)
card6_end += len('</article>')

card6_content = html[card6_start:card6_end]

# Extract all terms
terms = re.findall(r'<div class="dictionary-term">\s*<dt>(.*?)</dt>\s*<dd>(.*?)</dd>\s*</div>', card6_content, re.DOTALL)
print(f"Found {len(terms)} terms.")

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
    clean_term = term.strip().replace('<strong>', '').replace('</strong>', '')
    if not clean_term:
        continue
        
    first_letter = clean_term[0]
    
    # Strip non-hebrew characters from start to find real first letter if any
    match = re.search(r'[א-ת]', clean_term)
    if match:
        first_letter = match.group(0)
    
    html_term = f'            <div class="dictionary-term">\n              <dt><strong>{clean_term}</strong></dt>\n              <dd>{dfn.strip()}</dd>\n            </div>'
    
    if first_letter in letters_1:
        groups['א-ה'].append(html_term)
    elif first_letter in letters_2:
        groups['ו-י'].append(html_term)
    elif first_letter in letters_3:
        groups['כ-ע'].append(html_term)
    elif first_letter in letters_4:
        groups['פ-ת'].append(html_term)
    else:
        print(f"Unknown letter for term: {clean_term}")
        groups['א-ה'].append(html_term) # default

def build_card(card_num, title, group_html):
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
              <p>מילון מונחים מפורט לשירותכם בו תוכלו לקבל הסבר למונחים ותשובות לשאלות נפוצות. חלק זה מרכז מושגים באותיות אלו.</p>
              <dl class="dictionary-list">
{"\\n".join(group_html)}
              </dl>
            </div>
          </div>
        </div>
      </article>'''

new_cards = []
new_cards.append(build_card("6 (מילון א'-ה')", "מילון מונחים א'-ה'", groups['א-ה']))
new_cards.append(build_card("6.1 (מילון ו'-י')", "מילון מונחים ו'-י'", groups['ו-י']))
new_cards.append(build_card("6.2 (מילון כ'-ע')", "מילון מונחים כ'-ע'", groups['כ-ע']))
new_cards.append(build_card("6.3 (מילון פ'-ת')", "מילון מונחים פ'-ת'", groups['פ-ת']))

new_cards_html = "\n\n      ".join(new_cards)

html = html[:card6_start] + new_cards_html + html[card6_end:]

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Split and updated successfully!")
