import os

def fix_styles():
    with open('styles.css', 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Fix the gap and add white-space: nowrap to main-nav
    c = c.replace('.main-nav { display: none; gap: 22px; margin-inline-start: auto; }',
                  '.main-nav { display: none; gap: 14px; margin-inline-start: auto; }')
    c = c.replace('.main-nav a { color: var(--navy); font-weight: 600; font-size: .98rem; position: relative; }',
                  '.main-nav a { color: var(--navy); font-weight: 600; font-size: .95rem; position: relative; white-space: nowrap; }')
    
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(c)

def fix_podcasts():
    with open('podcasts.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Replace the broken mobile nav HTML
    old_mobile_nav = '''<!-- ============================ MOBILE NAV ============================ -->
<div class="mobile-nav-overlay" id="mobile-nav">
  <div class="mobile-nav-content">
    <button class="close-nav" aria-label="סגירת תפריט">✖</button>
    <a href="index.html#about">מי אנחנו</a>
    <a href="index.html#services">השירותים</a>
    <a href="index.html#how">איך זה עובד</a>
    <a href="index.html#stories">סיפורי הצלחה</a>
    <a href="articles.html">מאמרים</a>
    <a href="podcasts.html" class="active">פודקאסטים</a>
    <a href="tel:0545554588" class="btn btn-primary" style="margin-top:20px;">התקשרו עכשיו</a>
  </div>
</div>'''
    
    new_mobile_nav = '''<!-- תפריט מובייל -->
<nav class="mobile-nav" id="mobile-nav-podcasts" aria-label="ניווט מובייל" hidden>
  <a href="index.html">דף הבית</a>
  <a href="index.html#about">מי אנחנו</a>
  <a href="index.html#services">השירותים</a>
  <a href="articles.html">מאמרים</a>
  <a href="podcasts.html" class="active">פודקאסטים</a>
  <a href="index.html#lead-form">צור קשר</a>
</nav>'''
    
    if old_mobile_nav in c:
        c = c.replace(old_mobile_nav, new_mobile_nav)
    
    # Also update aria-controls on nav-toggle
    c = c.replace('aria-controls="mobile-nav"', 'aria-controls="mobile-nav-podcasts"')

    # 2. Update JS for mobile nav
    old_js = '''  // Mobile Nav Logic
  const navToggle = document.querySelector('.nav-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  const closeNav = document.querySelector('.close-nav');

  navToggle.addEventListener('click', () => {
    mobileNav.classList.add('active');
  });
  closeNav.addEventListener('click', () => {
    mobileNav.classList.remove('active');
  });'''
    
    new_js = '''  // Mobile Nav Logic
  const navToggle = document.querySelector('.nav-toggle');
  const mobileNav = document.getElementById('mobile-nav-podcasts');
  
  navToggle.addEventListener('click', () => {
    const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', !isExpanded);
    mobileNav.hidden = isExpanded;
  });'''
    
    if old_js in c:
        c = c.replace(old_js, new_js)

    # 3. Change Autoplay to True on load
    c = c.replace("loadPodcast(videoParam || 'vision', false);", "loadPodcast(videoParam || 'vision', true);")

    # 4. Add moving WOW elements (particles) to podcasts main section
    if '<div class="particles">' not in c:
        c = c.replace('<main class="podcasts-main">', '''<main class="podcasts-main">
  <div class="particles">
    <div class="particle"></div><div class="particle"></div><div class="particle"></div><div class="particle"></div><div class="particle"></div>
  </div>''')

    # 5. Add Chatbot widget HTML before footer
    chatbot_html = '''
<!-- WOW Chatbot -->
<div class="wow-chatbot">
  <div class="chatbot-bubble">
    היי! 👋<br>
    צריכים עזרה בחישוב המשכנתא או מימון מותאם אישית? אני כאן!
  </div>
  <a href="https://wa.me/972587554588" class="chatbot-avatar" target="_blank" aria-label="לשיחה בוואטסאפ עם מומחה">
    <img src="assets/logo.png" alt="בוט אדמתנו ביתנו">
    <span class="pulse-ring"></span>
  </a>
</div>
'''
    if 'wow-chatbot' not in c:
        c = c.replace('<!-- Whatsapp Float Button -->', chatbot_html + '\n<!-- Whatsapp Float Button -->')

    with open('podcasts.html', 'w', encoding='utf-8') as f:
        f.write(c)

def fix_podcasts_css():
    with open('podcasts.css', 'r', encoding='utf-8') as f:
        c = f.read()

    css_additions = '''
/* ===== PARTICLES (MOVING ELEMENTS) ===== */
.podcasts-main { position: relative; overflow: hidden; }
.particles { position: absolute; bottom: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
.particle { position: absolute; background: radial-gradient(circle, rgba(212,175,55,0.4) 0%, transparent 70%); border-radius: 50%; opacity: 0; animation: floatUp 8s infinite ease-in; }
.particle:nth-child(1) { width: 150px; height: 150px; left: 10%; bottom: -150px; animation-duration: 12s; animation-delay: 0s; }
.particle:nth-child(2) { width: 80px; height: 80px; left: 30%; bottom: -80px; animation-duration: 9s; animation-delay: 2s; }
.particle:nth-child(3) { width: 200px; height: 200px; left: 60%; bottom: -200px; animation-duration: 15s; animation-delay: 4s; }
.particle:nth-child(4) { width: 120px; height: 120px; left: 80%; bottom: -120px; animation-duration: 11s; animation-delay: 1s; }
.particle:nth-child(5) { width: 90px; height: 90px; left: 50%; bottom: -90px; animation-duration: 10s; animation-delay: 3s; }

@keyframes floatUp {
  0% { transform: translateY(0) scale(0.8); opacity: 0; }
  20% { opacity: 0.6; }
  80% { opacity: 0.6; }
  100% { transform: translateY(-800px) scale(1.2); opacity: 0; }
}

/* ===== WOW CHATBOT ===== */
.wow-chatbot {
  position: fixed;
  bottom: 120px;
  right: 26px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 15px;
}

@media (max-width: 768px) {
  .wow-chatbot { bottom: 100px; right: 20px; }
}

.chatbot-bubble {
  background: white;
  color: #0e3a5f;
  padding: 15px 20px;
  border-radius: 20px 20px 0 20px;
  box-shadow: 0 10px 25px rgba(14, 58, 95, 0.15);
  font-size: 0.95rem;
  line-height: 1.5;
  max-width: 250px;
  text-align: right;
  border: 1px solid rgba(212,175,55,0.3);
  animation: bounceIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  transform-origin: bottom right;
  opacity: 0;
  animation-delay: 2s; /* Show after 2s */
}

.chatbot-avatar {
  position: relative;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  border: 2px solid #0e3a5f;
  transition: transform 0.3s ease;
}

.chatbot-avatar:hover {
  transform: scale(1.1);
}

.chatbot-avatar img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.pulse-ring {
  position: absolute;
  top: -5px; left: -5px; right: -5px; bottom: -5px;
  border-radius: 50%;
  border: 2px solid #ffd700;
  animation: pulse 2s infinite cubic-bezier(0.215, 0.61, 0.355, 1);
  pointer-events: none;
}

@keyframes pulse {
  0% { transform: scale(0.9); opacity: 1; }
  100% { transform: scale(1.5); opacity: 0; }
}

@keyframes bounceIn {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
'''
    if 'WOW CHATBOT' not in c:
        c += '\n' + css_additions
        
    with open('podcasts.css', 'w', encoding='utf-8') as f:
        f.write(c)

fix_styles()
fix_podcasts()
fix_podcasts_css()
print("Done styling and fixes")
