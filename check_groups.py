with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

for i in range(1, 6):
    group_str = f'id="dict-group-{i}"'
    idx = html.find(group_str)
    if idx == -1:
        print(f'Group {i} not found!')
        continue
        
    next_idx = html.find('id="dict-group-', idx + 10)
    if next_idx == -1:
        next_idx = len(html)
        
    content = html[idx:next_idx]
    count = content.count('class="acc-item"')
    print(f'Group {i} has {count} items.')
