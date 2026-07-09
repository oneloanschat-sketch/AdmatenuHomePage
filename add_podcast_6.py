import os
import subprocess
import sys

def install_and_compress():
    print("Installing imageio-ffmpeg...")
    subprocess.run([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"], check=True)
    
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    input_file = 'העלות_הנסתרת_של_משכנתא_מיושנת.mp4'
    output_file = 'assets/videos/hidden-costs.mp4'
    
    print(f"Compressing {input_file} to {output_file}...")
    # Compress video: scale to 720p (if larger), adjust bitrate
    cmd = [
        ffmpeg_exe, '-y', '-i', input_file,
        '-vf', "scale='min(1280,iw)':-2",
        '-c:v', 'libx264', '-crf', '28', '-preset', 'fast',
        '-c:a', 'aac', '-b:a', '128k',
        output_file
    ]
    subprocess.run(cmd, check=True)
    print("Compression finished successfully!")

def update_html():
    with open('podcasts.html', 'r', encoding='utf-8') as f:
        c = f.read()

    new_js = '''    'no-tabu': {
      title: 'משכנתא ללא טאבו: שוברים את המיתוס',
      desc: 'חושבים שאי אפשר לקבל משכנתא בלי רישום בטאבו? בואו לגלות איך אנחנו משיגים פתרונות מימון גם לנכסים בהליכי הסדרה.',
      file: 'assets/videos/no-tabu.mp4'
    },
    'hidden-costs': {
      title: 'העלות הנסתרת של משכנתא מיושנת',
      desc: 'מתי בפעם האחרונה בדקתם את תנאי המשכנתא שלכם? גלו כיצד מחזור נכון יכול למנוע הפסד של עשרות אלפי שקלים.',
      file: 'assets/videos/hidden-costs.mp4'
    }'''

    new_html = '''        <div class="playlist-item" data-id="hidden-costs">
          <div class="item-icon">
            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div class="item-content">
            <div class="item-title">העלות הנסתרת של משכנתא מיושנת</div>
            <div class="item-duration">צפו עכשיו</div>
          </div>
        </div>

      </div>
    </div>'''

    if "'hidden-costs': {" not in c:
        # Update JS dictionary
        c = c.replace('''    'no-tabu': {
      title: 'משכנתא ללא טאבו: שוברים את המיתוס',
      desc: 'חושבים שאי אפשר לקבל משכנתא בלי רישום בטאבו? בואו לגלות איך אנחנו משיגים פתרונות מימון גם לנכסים בהליכי הסדרה.',
      file: 'assets/videos/no-tabu.mp4'
    }''', new_js)

        # Update Playlist HTML
        search_html = '''        <div class="playlist-item" data-id="no-tabu">
          <div class="item-icon">
            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div class="item-content">
            <div class="item-title">משכנתא ללא טאבו: שוברים את המיתוס</div>
            <div class="item-duration">צפו עכשיו</div>
          </div>
        </div>

      </div>
    </div>'''
        
        c = c.replace(search_html, search_html.replace('      </div>\n    </div>', new_html))

    with open('podcasts.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("HTML updated!")

try:
    install_and_compress()
except Exception as e:
    print(f"Compression failed: {e}")
    print("Falling back to moving the uncompressed file...")
    import shutil
    shutil.move('העלות_הנסתרת_של_משכנתא_מיושנת.mp4', 'assets/videos/hidden-costs.mp4')

update_html()
print("Process completed.")
