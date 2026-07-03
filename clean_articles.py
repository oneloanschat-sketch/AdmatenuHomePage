import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the old 4 dictionary cards
start_idx = html.find('<!-- ===== ARTICLE CARD 6 (מילון א\'-ה\') ===== -->')
card_63 = html.find('<!-- ===== ARTICLE CARD 6.3 (מילון פ\'-ת\') ===== -->')
if start_idx != -1 and card_63 != -1:
    end_idx = html.find('</article>', card_63)
    if end_idx != -1:
        end_idx += len('</article>')
        # Remove this section completely
        html = html[:start_idx] + html[end_idx:]
        print("Removed the old duplicate dictionary cards.")
else:
    print("Old duplicate cards not found (already removed?).")

# 2. Fix the javascript button toggle arrow issue
# Old JS: btn.textContent = isOpen ? 'קראו את המאמר המלא ←' : 'סגרו את המאמר ↑';
# New JS: btn.querySelector('.btn-text').textContent = isOpen ? 'קראו את המאמר המלא' : 'סגרו את המאמר';

html = html.replace(
    "btn.textContent = isOpen ? 'קראו את המאמר המלא ←' : 'סגרו את המאמר ↑';",
    "btn.querySelector('.btn-text').textContent = isOpen ? 'קראו את המאמר המלא' : 'סגרו את המאמר';"
)

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("articles.html cleaned and fixed successfully!")
