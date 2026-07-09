import re
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\1\.gemini\antigravity-ide\brain\57a1f589-9981-4950-99df-58b621d9e3f8\.system_generated\steps\660\content.md', 'r', encoding='utf-8') as f:
    html = f.read()

# The terms are usually inside <div class="quest">
# Title is in <a ... class="linky_title">TITLE</a>
# Definition is in <div class="content_p">...</div>

terms = []
matches = re.finditer(r'<div class="quest">(.*?)</div>\s*</div>', html, re.DOTALL)
for m in matches:
    block = m.group(1)
    title_match = re.search(r'class="linky_title"[^>]*>(.*?)</a>', block)
    content_match = re.search(r'<div class="content_p"[^>]*>(.*?)</div>', block, re.DOTALL)
    
    if title_match and content_match:
        title = title_match.group(1).strip()
        # Clean HTML from title if any
        title = re.sub(r'<[^>]+>', '', title)
        
        content = content_match.group(1).strip()
        # Clean paragraph tags from content but keep br
        content = re.sub(r'</?p>', '', content)
        content = re.sub(r'<br\s*/?>', '<br>', content)
        
        terms.append((title, content))

print(f"Extracted {len(terms)} terms.")
for t in terms[:5]:
    print(t[0])
    
with open('extracted_terms.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, ensure_ascii=False, indent=2)
