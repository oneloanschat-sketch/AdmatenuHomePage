import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix literal \n
html = html.replace('\\n', '\n')
print("Fixed literal \\n.")

# Also let's check if dict-group-3 and dict-group-4 have any terms
idx3 = html.find('id="dict-group-3"')
end3 = html.find('id="dict-group-4"')
print(f"Group 3 length in chars: {end3 - idx3}")
print("Group 3 count of acc-item:", html[idx3:end3].count('class="acc-item"'))

end4 = html.find('</div>\n              </div>', end3)
print(f"Group 4 length in chars: {end4 - end3}")
print("Group 4 count of acc-item:", html[end3:end4].count('class="acc-item"'))

with open('articles.html', 'w', encoding='utf-8') as f:
    f.write(html)
