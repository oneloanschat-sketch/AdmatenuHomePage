import os

def replace_email():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'office@ourland.co.il' in content:
            content = content.replace('office@ourland.co.il', 'admateinu.beitenu@gmail.com')
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)

def extract_lead_form():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_str = '<section class="lead" id="lead-form"'
    end_str = '</section>\n</main>'
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx != -1 and end_idx != -1:
        # Extract the entire section (excluding </main>)
        return content[start_idx:end_idx] + '</section>'
    return None

def add_lead_to_podcasts(lead_form_html):
    if not lead_form_html:
        print("Lead form not found!")
        return

    with open('podcasts.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'id="lead-form"' not in content:
        # Insert before </main>
        content = content.replace('</main>', f'\n{lead_form_html}\n</main>')
        with open('podcasts.html', 'w', encoding='utf-8') as f:
            f.write(content)
            
replace_email()
lead_form = extract_lead_form()
add_lead_to_podcasts(lead_form)
print("Done modifying email and CTA")
