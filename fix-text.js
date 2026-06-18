const fs = require('fs');
const path = require('path');

const spiralyDir = path.join(__dirname, 'spiraly');
const files = fs.readdirSync(spiralyDir).filter(f => f.endsWith('.html'));

const targetText = 'לקבלת ייעוץ מקצועי במקור לחצו כאן';
const newText = 'לקבל ייעוץ מקצועי לחצו כאן';

let count = 0;
for (const file of files) {
  const filePath = path.join(spiralyDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  if (html.includes(targetText)) {
    html = html.replace(new RegExp(targetText, 'g'), newText);
    fs.writeFileSync(filePath, html, 'utf8');
    count++;
  }
}
console.log(`Updated ${count} files.`);
