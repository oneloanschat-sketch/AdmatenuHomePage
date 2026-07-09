import os
import subprocess
import sys
import shutil

def compress_file(ffmpeg_exe, input_file, output_file, is_new=False):
    print(f"Compressing {input_file}...")
    cmd = [
        ffmpeg_exe, '-y', '-i', input_file,
        '-vf', "scale='min(854,iw)':-2", # scale to 480p to save space
        '-c:v', 'libx264', '-crf', '32', '-preset', 'fast',
        '-c:a', 'aac', '-b:a', '96k',
        output_file
    ]
    subprocess.run(cmd, check=True)

def update_html():
    with open('podcasts.html', 'r', encoding='utf-8') as f:
        c = f.read()

    new_js = '''    'hidden-costs': {
      title: 'העלות הנסתרת של משכנתא מיושנת',
      desc: 'מתי בפעם האחרונה בדקתם את תנאי המשכנתא שלכם? גלו כיצד מחזור נכון יכול למנוע הפסד של עשרות אלפי שקלים.',
      file: 'assets/videos/hidden-costs.mp4'
    },
    'mortgage-refusals': {
      title: 'פתרון לסירובי משכנתא',
      desc: 'סורבתם למשכנתא בבנק? זה לא סוף הסיפור. גלו את הפתרונות החוץ-בנקאיים והיצירתיים שיעזרו לכם להגשים חלום.',
      file: 'assets/videos/mortgage-refusals.mp4'
    }'''

    new_html = '''        <div class="playlist-item" data-id="mortgage-refusals">
          <div class="item-icon">
            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div class="item-content">
            <div class="item-title">פתרון לסירובי משכנתא</div>
            <div class="item-duration">צפו עכשיו</div>
          </div>
        </div>

      </div>
    </div>'''

    if "'mortgage-refusals': {" not in c:
        c = c.replace('''    'hidden-costs': {
      title: 'העלות הנסתרת של משכנתא מיושנת',
      desc: 'מתי בפעם האחרונה בדקתם את תנאי המשכנתא שלכם? גלו כיצד מחזור נכון יכול למנוע הפסד של עשרות אלפי שקלים.',
      file: 'assets/videos/hidden-costs.mp4'
    }''', new_js)

        search_html = '''        <div class="playlist-item" data-id="hidden-costs">
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
        
        c = c.replace(search_html, search_html.replace('      </div>\n    </div>', new_html))

        with open('podcasts.html', 'w', encoding='utf-8') as f:
            f.write(c)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    # 1. Compress the new video
    input_file = 'פתרון_לסירובי_משכנתא.mp4.mp4'
    output_file = 'assets/videos/mortgage-refusals.mp4'
    if os.path.exists(input_file):
        try:
            compress_file(ffmpeg_exe, input_file, output_file)
            print("Successfully compressed new video.")
            os.remove(input_file)
        except Exception as e:
            print(f"Failed to compress {input_file}: {e}")
            shutil.move(input_file, output_file)

    # 2. Update HTML
    update_html()
    print("HTML updated.")
    
    # 3. Compress other videos if > 20MB
    videos_dir = 'assets/videos'
    for f in os.listdir(videos_dir):
        if f.endswith('.mp4') and f != 'mortgage-refusals.mp4':
            path = os.path.join(videos_dir, f)
            size_mb = os.path.getsize(path) / (1024 * 1024)
            if size_mb > 20:
                print(f"Compressing {f} (Size: {size_mb:.2f}MB)")
                tmp_path = path + ".tmp.mp4"
                try:
                    compress_file(ffmpeg_exe, path, tmp_path)
                    shutil.move(tmp_path, path)
                except Exception as e:
                    print(f"Failed to compress {f}: {e}")
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

if __name__ == '__main__':
    main()
