import re

def wrap_insight_blocks(html_fragment):
    # This function takes the HTML inside <div class="article-full-content"> 
    # and wraps consecutive <h3> and <p> elements into <div class="insight-block"> ... </div>
    # Actually, we can split by \n
    lines = html_fragment.split('\n')
    new_lines = []
    in_block = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('<h3>'):
            if in_block:
                new_lines.append('      </div>')
            new_lines.append('      <div class="insight-block">')
            new_lines.append(line)
            in_block = True
        elif stripped.startswith('<p>') or stripped.startswith('</p>'):
            # If we see a paragraph, it either belongs to an open block, or it's a standalone paragraph
            new_lines.append(line)
        else:
            # For other tags, just append. But if we are in a block and hit a non-p non-h3 tag, we might want to close it?
            # Actually, let's keep it simple. Only h3 starts a block.
            new_lines.append(line)
            
    if in_block:
        new_lines.append('      </div>')
        
    return '\n'.join(new_lines)

def process_file():
    with open('articles.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Process Card 8
    start_8 = html.find('<!-- ===== ARTICLE CARD 8 ===== -->')
    start_7 = html.find('<!-- ===== ARTICLE CARD 7 ===== -->')
    
    if start_8 != -1 and start_7 != -1:
        card_8 = html[start_8:start_7]
        content_start = card_8.find('<div class="article-full-content">') + len('<div class="article-full-content">\n')
        content_end = card_8.find('    </div>\n  </div>\n  <button class="article-toggle-btn"')
        
        inner_html = card_8[content_start:content_end]
        wrapped_inner = wrap_insight_blocks(inner_html)
        
        card_8_new = card_8[:content_start] + wrapped_inner + '\n' + card_8[content_end:]
        html = html[:start_8] + card_8_new + html[start_7:]
        
    # Process Card 7
    start_7 = html.find('<!-- ===== ARTICLE CARD 7 ===== -->')
    start_1 = html.find('<!-- ===== ARTICLE CARD 1 ===== -->')
    
    if start_7 != -1 and start_1 != -1:
        card_7 = html[start_7:start_1]
        content_start = card_7.find('<div class="article-full-content">') + len('<div class="article-full-content">\n')
        content_end = card_7.find('    </div>\n  </div>\n  <button class="article-toggle-btn"')
        
        inner_html = card_7[content_start:content_end]
        wrapped_inner = wrap_insight_blocks(inner_html)
        
        card_7_new = card_7[:content_start] + wrapped_inner + '\n' + card_7[content_end:]
        html = html[:start_7] + card_7_new + html[start_1:]
        
    with open('articles.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
if __name__ == '__main__':
    process_file()
