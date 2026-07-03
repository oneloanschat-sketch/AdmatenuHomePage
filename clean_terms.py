import json
import re

with open('extracted_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

cleaned_terms = []
for term, dfn in terms:
    # Remove all <div> and </div> tags
    dfn = re.sub(r'<div[^>]*>', '', dfn)
    dfn = re.sub(r'</div>', '', dfn)
    
    # Also clean any stray <a> tags that might be unbalanced
    dfn = re.sub(r'<a[^>]*>', '', dfn)
    dfn = re.sub(r'</a>', '', dfn)
    
    # And empty <p></p>
    dfn = re.sub(r'<p>\s*</p>', '', dfn)
    
    cleaned_terms.append([term, dfn])

with open('extracted_terms.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_terms, f, ensure_ascii=False, indent=2)
print("Cleaned extracted_terms.json")
