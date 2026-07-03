import re
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\1\.gemini\antigravity-ide\brain\57a1f589-9981-4950-99df-58b621d9e3f8\.system_generated\steps\660\content.md', 'r', encoding='utf-8') as f:
    html = f.read()

terms = []
parts = html.split('<div class="quest">')
for p in parts[1:]:
    # Find the title
    title_start = p.find('class="linky_title"')
    if title_start == -1: continue
    title_start = p.find('>', title_start) + 1
    title_end = p.find('</a>', title_start)
    if title_end == -1: continue
    title = p[title_start:title_end].strip()
    
    # Find the content
    content_start = p.find('class="content_p"', title_end)
    if content_start == -1: continue
    content_start = p.find('>', content_start) + 1
    content_end = p.find('</div>', content_start)
    if content_end == -1: continue
    content = p[content_start:content_end].strip()
    
    # Clean HTML tags from content but keep br
    content = re.sub(r'</?p>', '', content)
    content = re.sub(r'<br\s*/?>', '<br>', content)
    # also remove any style attributes or inner spans
    content = re.sub(r'<span[^>]*>', '', content)
    content = re.sub(r'</span>', '', content)
    content = re.sub(r'<strong[^>]*>', '<strong>', content)
    content = content.replace('&nbsp;', ' ')
    
    terms.append((title, content))

print(f"Extracted {len(terms)} terms.")
for t in terms[:3]:
    print(t[0])

with open('extracted_terms.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, ensure_ascii=False, indent=2)
