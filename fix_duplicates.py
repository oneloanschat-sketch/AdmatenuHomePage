import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix literal \n
html = html.replace('\\n', '\n')
print("Fixed literal \\n.")

# Remove duplicates
# Find the second occurrence of ARTICLE CARD 7
idx1 = html.find('<!-- ===== ARTICLE CARD 7 ===== -->')
idx2 = html.find('<!-- ===== ARTICLE CARD 7 ===== -->', idx1 + 1)

if idx2 != -1:
    # Find the second occurrence of ARTICLE CARD 5
    card5_idx1 = html.find('<!-- ===== ARTICLE CARD 5 ===== -->')
    card5_idx2 = html.find('<!-- ===== ARTICLE CARD 5 ===== -->', card5_idx1 + 1)
    
    if card5_idx2 != -1:
        # Find the end of this article card
        end_idx = html.find('</article>', card5_idx2)
        if end_idx != -1:
            end_idx += len('</article>')
            html = html[:idx2] + html[end_idx:]
            print("Removed duplicated cards.")

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("articles.html cleaned up!")
