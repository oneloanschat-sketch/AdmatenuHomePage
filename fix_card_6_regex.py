import re

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_tag = '<!-- ===== ARTICLE CARD 6 ===== -->'
start_idx = html.find(start_tag)

if start_idx != -1:
    card6_html = html[start_idx:]
    html_before = html[:start_idx]

    pattern = re.compile(r'<div class="insight-block">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>', re.DOTALL)
    
    def repl(m):
        dt = m.group(1).strip()
        dd = m.group(2).strip()
        return f'<div class="dictionary-term">\n        <dt>{dt}</dt>\n        <dd>{dd}</dd>\n      </div>'
    
    new_card6, count = pattern.subn(repl, card6_html)
    print(f'Replaced {count} items!')
    
    if count > 0:
        new_card6 = new_card6.replace('<div class="dictionary-term">', '!!!START!!!<div class="dictionary-term">', 1)
        
        end_idx = new_card6.find('    </div>\n  </div>\n  <button class="article-toggle-btn"')
        if end_idx != -1:
            new_card6 = new_card6[:end_idx] + '      </dl>\n' + new_card6[end_idx:]
            
        new_card6 = new_card6.replace('!!!START!!!', '<dl class="dictionary-list">\n      ')
        
        with open('articles.html', 'w', encoding='utf-8') as f:
            f.write(html_before + new_card6)
        print('Saved articles.html successfully.')
else:
    print('Card 6 not found!')
