with open('temp_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.strip().split('\n')
lines = [l.strip() for l in lines if l.strip()]

start_idx = lines.index('==== CARD 6 ====')

title = lines[start_idx+1]
desc = lines[start_idx+2]
terms = lines[start_idx+3:]

html_output = '<p>' + desc + '</p>\n<dl class="dictionary-list">\n'

i = 0
while i < len(terms):
    term = terms[i]
    if i + 1 < len(terms):
        definition = terms[i+1]
        
        # Check if the next line is actually a definition or another term?
        # A simple heuristic: terms are short, definitions are usually longer or we just assume strict alternation.
        # Strict alternation was the structure in temp_dump.txt
        html_output += f'  <div class="dictionary-term">\n    <dt>{term}</dt>\n    <dd>{definition}</dd>\n  </div>\n'
    i += 2

html_output += '</dl>\n'

with open('card6_inner.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

# Now inject it into articles.html
with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_tag = '<!-- ===== ARTICLE CARD 6 ===== -->'
end_tag = '<!-- ===== ARTICLE CARD 5 ===== -->'

start_idx = html.find(start_tag)
end_idx = html.find(end_tag)

if start_idx != -1 and end_idx != -1:
    card = html[start_idx:end_idx]
    
    content_start = card.find('<div class="article-full-content">') + len('<div class="article-full-content">\n')
    content_end = card.find('    </div>\n  </div>\n  <button class="article-toggle-btn"')
    
    new_card = card[:content_start] + html_output + '\n' + card[content_end:]
    html = html[:start_idx] + new_card + html[end_idx:]
    
    with open('articles.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated articles.html for Card 6")
