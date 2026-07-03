import json
with open('extracted_terms.json', 'r', encoding='utf-8') as f:
    terms = json.load(f)

with open('unbalanced_output.txt', 'w', encoding='utf-8') as out:
    for term, dfn in terms:
        for tag in ['div', 'strong', 'ul', 'li', 'span', 'a']:
            opens = dfn.count(f'<{tag}')
            closes = dfn.count(f'</{tag}>')
            if opens != closes:
                out.write(f'Unbalanced {tag} ({opens} vs {closes}) in term: {term.strip()}\n')
