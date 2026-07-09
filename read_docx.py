import zipfile
import xml.etree.ElementTree as ET
import sys

def extract_text(path):
    try:
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paragraphs = []
        for p in tree.findall('.//w:p', namespaces):
            texts = [node.text for node in p.findall('.//w:t', namespaces) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)
    except Exception as e:
        return str(e)

with open('articles_content.txt', 'w', encoding='utf-8') as out:
    for f in sys.argv[1:]:
        out.write(f"--- {f} ---\n")
        out.write(extract_text(f) + "\n\n")
