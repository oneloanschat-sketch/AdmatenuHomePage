with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()
idx = html.find('/* ---------- טאבים למילון ---------- */')
end_idx = html.find('</script>', idx)
print(html[idx:end_idx].encode('ascii', 'ignore').decode())
