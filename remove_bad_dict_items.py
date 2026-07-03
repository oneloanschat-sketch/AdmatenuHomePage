import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern to find acc-item blocks
# We'll use a regex that matches the full acc-item div
# <div class="acc-item">...</div>
# Because regex with HTML is tricky, let's use string operations

parts = html.split('<div class="acc-item">')
new_parts = [parts[0]]

removed_count = 0

for p in parts[1:]:
    # extract the strong tag
    strong_match = re.search(r'<strong>(.*?)</strong>', p)
    if strong_match:
        title = strong_match.group(1).strip()
        # condition to remove: title is a digit, or is the specific string
        if title.isdigit() or 'דוגמא ללוח סילוקין לפי שיטת' in title:
            removed_count += 1
            print(f"Removing item: {title}")
            continue
            
    new_parts.append('<div class="acc-item">' + p)

if removed_count > 0:
    new_html = "".join(new_parts)
    with open('articles.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"Removed {removed_count} items and saved.")
else:
    print("No items removed.")
