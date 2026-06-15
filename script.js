/* ============================================================
   אדמתנו ביתנו — script.js
   scroll-reveal · count-up · אקורדיון · קרוסלה · ולידציה ושליחת טופס
   Vanilla JS, ללא תלויות.
   ============================================================ */
(function () {
  "use strict";

  /* ---------- עזר ---------- */
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* מעטפת מדידה — שולחת event לפיקסל/GTM אם מותקנים (לא חובה) */
  function track(name) {
    try { if (window.fbq) window.fbq("trackCustom", name); } catch (e) {}
    try { if (window.dataLayer) window.dataLayer.push({ event: name }); } catch (e) {}
  }

  /* ---------- שנה נוכחית בפוטר ---------- */
  var yEl = $("#year");
  if (yEl) yEl.textContent = new Date().getFullYear();

  /* ---------- צל להדר בגלילה ---------- */
  var header = $(".site-header");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- תפריט מובייל ---------- */
  var toggle = $(".nav-toggle");
  var mobileNav = $("#mobile-nav");
  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mobileNav.hidden = open;
    });
    $$("a", mobileNav).forEach(function (a) {
      a.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        mobileNav.hidden = true;
      });
    });
  }

  /* ---------- לחיצה על הלוגו = חזרה לראש העמוד ---------- */
  var brandHome = $("#brandHome");
  if (brandHome) {
    brandHome.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, left: 0, behavior: reduceMotion ? "auto" : "smooth" });
      if (history.replaceState) history.replaceState(null, "", location.pathname + location.search);
    });
  }

  /* ---------- קוביית וידאו בהירו — מעבר אוטומטי בין סרטונים ---------- */
  (function heroVideo() {
    var v = $("#heroVideo");
    if (!v) return;
    var list = (v.getAttribute("data-playlist") || "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    var i = 0;
    var hasPlayed = false;
    var userWantsSound = false;
    function play() { 
      if (!userWantsSound) {
        v.muted = true;
      } else {
        v.muted = false;
        v.volume = 1;
      }
      v.setAttribute("playsinline", "");
      var p = v.play(); 
      if (p && p.catch) {
        p.then(function(){ hasPlayed = true; }).catch(function () { hasPlayed = false; });
      } else {
        hasPlayed = true;
      }
    }
    document.addEventListener("touchstart", function() {
      if (!hasPlayed) { play(); }
    }, { once: true, passive: true });
    document.addEventListener("click", function() {
      if (!hasPlayed) { play(); }
    }, { once: true, passive: true });
    if (list.length > 1) {
      v.addEventListener("ended", function () {
        i = (i + 1) % list.length;
        v.src = list[i];
        v.load();
        play();
      });
    } else {
      v.loop = true;
    }
    play();

    /* כפתור הפעלת/השתקת קול */
    var soundBtn = $("#videoSound");
    if (soundBtn) {
      soundBtn.addEventListener("click", function (e) {
        if (e) { e.preventDefault(); e.stopPropagation(); }
        userWantsSound = !userWantsSound;
        var on = userWantsSound;
        
        // פתרון קסם ל-iOS: חייבים לעצור, לשנות מצב השתקה, ואז לנגן שוב
        if (!v.paused) v.pause();
        
        v.muted = !on;
        if (on) v.volume = 1;
        
        soundBtn.setAttribute("aria-pressed", String(on));
        var t = soundBtn.querySelector(".vs-text");
        if (t) t.textContent = on ? "השתק" : "הפעל קול";
        
        play();
      });
    }
  })();

  /* ---------- מעקב קליקים על ערוצי המרה ---------- */
  $$("[data-track]").forEach(function (el) {
    el.addEventListener("click", function () { track(el.getAttribute("data-track")); });
  });

  /* ---------- Scroll Reveal ---------- */
  var revealEls = $$(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (entry.isIntersecting) {
          var sibs = $$(".reveal", entry.target.parentElement);
          var idx = sibs.indexOf(entry.target);
          entry.target.style.transitionDelay = Math.min(idx, 6) * 80 + "ms";
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Count-Up ---------- */
  function formatNum(n, fmt) {
    if (fmt === "year") return String(n);
    return n.toLocaleString("en-US");
  }
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10) || 0;
    var fmt = el.getAttribute("data-format");
    if (reduceMotion) { el.textContent = formatNum(target, fmt); return; }
    var start = (fmt === "year") ? Math.max(target - 18, 1990) : 0;
    var dur = 1500, t0 = null;
    function tick(ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = Math.round(start + (target - start) * eased);
      el.textContent = formatNum(val, fmt);
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = formatNum(target, fmt);
    }
    requestAnimationFrame(tick);
  }
  var counters = $$("[data-count]");
  if (!("IntersectionObserver" in window)) {
    counters.forEach(countUp);
  } else {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { countUp(entry.target); cio.unobserve(entry.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- אקורדיון FAQ ---------- */
  $$(".acc-head").forEach(function (head) {
    head.addEventListener("click", function () {
      var open = head.getAttribute("aria-expanded") === "true";
      head.setAttribute("aria-expanded", String(!open));
      var body = head.nextElementSibling;
      body.style.maxHeight = open ? null : body.scrollHeight + "px";
    });
  });

  /* ---------- קרוסלת סיפורי הצלחה ---------- */
  (function carousel() {
    var track = $(".stories-track");
    var dotsWrap = $(".carousel-dots");
    if (!track || !dotsWrap) return;
    var slides = $$(".story", track);
    var index = 0;

    function perView() { return window.innerWidth >= 768 ? 2 : 1; }
    function maxIndex() { return Math.max(0, slides.length - perView()); }

    function buildDots() {
      dotsWrap.innerHTML = "";
      for (var i = 0; i <= maxIndex(); i++) {
        var b = document.createElement("button");
        b.setAttribute("role", "tab");
        b.setAttribute("aria-label", "מעבר לסיפור " + (i + 1));
        (function (i) { b.addEventListener("click", function () { go(i); }); })(i);
        dotsWrap.appendChild(b);
      }
    }
    function update() {
      var slideW = slides[0].getBoundingClientRect().width + 20; /* + gap */
      track.style.transform = "translateX(" + (index * slideW) + "px)"; /* RTL: חיובי = ימינה */
      $$("button", dotsWrap).forEach(function (d, i) {
        d.setAttribute("aria-selected", String(i === index));
      });
    }
    function go(i) {
      index = Math.max(0, Math.min(i, maxIndex()));
      update();
    }

    $$(".carousel-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        go(index + (btn.getAttribute("data-dir") === "next" ? 1 : -1));
      });
    });

    var timer = null;
    function autoplay() {
      if (reduceMotion) return;
      stop();
      timer = setInterval(function () { go(index >= maxIndex() ? 0 : index + 1); }, 5000);
    }
    function stop() { if (timer) clearInterval(timer); }
    var region = $(".stories-carousel");
    if (region) { region.addEventListener("mouseenter", stop); region.addEventListener("mouseleave", autoplay); }

    window.addEventListener("resize", function () { buildDots(); go(Math.min(index, maxIndex())); });
    buildDots(); update(); autoplay();
  })();

  /* ---------- טופס לידים: ולידציה + שליחה ---------- */
  (function leadForm() {
    var form = $("#leadForm");
    if (!form) return;
    var status = $("#formStatus");
    var leadIdField = $("#leadId");

    /* יצירת LeadID ייחודי (תואם לפורמט הלידים הקיים) */
    if (leadIdField) {
      var d = new Date();
      leadIdField.value = "WEB-" + d.getFullYear() + ("0" + (d.getMonth() + 1)).slice(-2) +
        ("0" + d.getDate()).slice(-2) + "-" + Math.random().toString(36).slice(2, 7).toUpperCase();
    }

    function setError(id, msg) {
      var input = $("#" + id);
      var err = $('.err[data-for="' + id + '"]');
      if (input) input.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg || "";
    }

    function validPhone(v) {
      var digits = v.replace(/[^0-9]/g, "");
      return /^0(5\d|[2-489])\d{7}$/.test(digits); /* טלפון ישראלי כללי + נייד */
    }

    function validate() {
      var ok = true;
      var name = $("#fullname").value.trim();
      var phone = $("#phone").value.trim();
      if (name.length < 2) { setError("fullname", "נא להזין שם מלא"); ok = false; } else setError("fullname", "");
      if (!validPhone(phone)) { setError("phone", "נא להזין מספר טלפון תקין"); ok = false; } else setError("phone", "");
      return ok;
    }

    $("#fullname").addEventListener("blur", validate);
    $("#phone").addEventListener("blur", validate);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (status) { status.textContent = ""; status.className = "form-status"; }
      if (!validate()) {
        var firstErr = $('input[aria-invalid="true"]');
        if (firstErr) firstErr.focus();
        return;
      }

      var btn = $('button[type="submit"]', form);
      var orig = btn.textContent;
      btn.disabled = true; btn.textContent = "שולח...";

      var action = form.getAttribute("action") || "";
      var keyField = form.querySelector('input[name="access_key"]');
      var key = keyField ? keyField.value : "";
      var configured = action && key && key.indexOf("YOUR_") === -1;

      track("Lead"); /* אירוע המרה לפיקסל */

      if (configured) {
        /* שליחה אמיתית ל-Formspree / Web3Forms / webhook */
        var data = new FormData(form);
        fetch(action, { method: "POST", body: data, headers: { Accept: "application/json" } })
          .then(function (res) {
            if (res.ok) { onSuccess(); }
            else { throw new Error("send failed"); }
          })
          .catch(function () { onFallback(); })
          .finally(function () { btn.disabled = false; btn.textContent = orig; });
      } else {
        /* טרם הוגדר endpoint — מציגים הצלחה ומפעילים fallback לוואטסאפ */
        btn.disabled = false; btn.textContent = orig;
        onSuccess();
        setTimeout(openWhatsApp, 600);
      }
    });

    function summary() {
      var get = function (id) { var el = $("#" + id); return el ? el.value.trim() : ""; };
      var owner = (form.querySelector('input[name="בעל נכס"]:checked') || {}).value || "";
      return "ליד חדש מהאתר:\n" +
        "שם: " + get("fullname") + "\n" +
        "טלפון: " + get("phone") + "\n" +
        "עיר: " + get("city") + "\n" +
        "צורך: " + ($("#need") ? $("#need").value : "") + "\n" +
        "בעל נכס: " + owner + "\n" +
        "סכום מבוקש: " + get("amount") + "\n" +
        "הערה: " + get("note") + "\n" +
        "מזהה: " + (leadIdField ? leadIdField.value : "");
    }

    function openWhatsApp() {
      var url = "https://wa.me/972587554588?text=" + encodeURIComponent(summary());
      window.open(url, "_blank", "noopener");
    }

    function onSuccess() {
      if (status) {
        status.textContent = "תודה! קיבלנו את הפרטים — ניצור איתך קשר בהקדם. אפשר גם להתקשר 054-555-4588.";
        status.className = "form-status ok";
      }
      form.reset();
      status.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    }

    function onFallback() {
      if (status) {
        status.innerHTML = 'אירעה תקלה בשליחה. אפשר לשלוח לנו את הפרטים בוואטסאפ או להתקשר 054-555-4588.';
        status.className = "form-status bad";
      }
      openWhatsApp();
    }
  })();

})();
