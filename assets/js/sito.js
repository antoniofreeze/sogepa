/* So.Ge.Pa. — comportamenti del sito (nessuna dipendenza) */
(function () {
  'use strict';
  var html = document.documentElement;
  html.classList.add('js');

  /* Configurazione: numeri e recapiti in un punto solo (vedi anche build.py) */
  var CFG = window.SOGEPA || {};
  var WA = CFG.whatsapp || '393929957941';
  var EMAIL = CFG.email || 'sogepasnc@libero.it';
  var ENDPOINT = CFG.endpoint || ('https://formsubmit.co/ajax/' + EMAIL);
  var INTRO = CFG.introWa || 'Ciao So.Ge.Pa., vorrei';
  function pixel(evento) { if (typeof window.fbq === 'function') { try { window.fbq('track', evento); } catch (e) {} } }

  /* Dispositivo: da telefono/tablet si va su WhatsApp, da PC si apre il modulo */
  var mobile = (function () {
    var ua = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    var coarse = window.matchMedia && matchMedia('(pointer:coarse)').matches;
    var stretto = window.matchMedia && matchMedia('(max-width:1024px)').matches;
    return ua || (coarse && stretto);
  })();
  html.classList.add(mobile ? 'is-mobile' : 'is-desktop');

  function linkWhatsApp(servizio) {
    var testo = servizio
      ? INTRO + ' informazioni e un preventivo per: ' + servizio + '.'
      : INTRO + ' richiedere un preventivo.';
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(testo);
  }

  /* Link WhatsApp espliciti */
  Array.prototype.forEach.call(document.querySelectorAll('[data-wa]'), function (a) {
    a.setAttribute('href', linkWhatsApp(a.getAttribute('data-servizio') || ''));
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener');
    a.addEventListener('click', function () { pixel('Contact'); });
  });

  /* Origine della richiesta (UTM delle campagne) nel campo nascosto "origine" */
  var params = new URLSearchParams(location.search);
  var utm = [];
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
    if (params.get(k)) utm.push(k.replace('utm_', '') + '=' + params.get(k));
  });
  Array.prototype.forEach.call(document.querySelectorAll('input[name="origine"]'), function (i) {
    if (utm.length) i.value = (i.value || 'Sito') + ' · ' + utm.join(' ');
  });

  /* Modulo: preselezione servizio, apertura modale o scroll al modulo in pagina */
  var modale = document.getElementById('modale-richiesta');
  function preseleziona(root, servizio) {
    if (!root || !servizio) return;
    var sel = root.querySelector('select[name="servizio"]');
    if (!sel) return;
    for (var i = 0; i < sel.options.length; i++) {
      if (sel.options[i].value === servizio) { sel.value = servizio; return; }
    }
  }
  function apriModulo(servizio) {
    var inPagina = document.getElementById('richiesta');
    if (inPagina) {
      preseleziona(inPagina, servizio);
      inPagina.scrollIntoView({ behavior: 'smooth', block: 'start' });
      var primo = inPagina.querySelector('input[name="nome"]');
      if (primo) setTimeout(function () { primo.focus({ preventScroll: true }); }, 500);
      return;
    }
    if (!modale) return;
    preseleziona(modale, servizio);
    if (typeof modale.showModal === 'function') modale.showModal();
    else modale.setAttribute('open', '');
  }
  if (modale) {
    modale.addEventListener('click', function (e) { if (e.target === modale) modale.close(); });
    var chiudi = modale.querySelector('.chiudi');
    if (chiudi) chiudi.addEventListener('click', function () { modale.close(); });
  }

  /* CTA adattive */
  Array.prototype.forEach.call(document.querySelectorAll('[data-cta]'), function (el) {
    var servizio = el.getAttribute('data-servizio') || '';
    if (mobile) {
      el.setAttribute('href', linkWhatsApp(servizio));
      el.setAttribute('target', '_blank');
      el.setAttribute('rel', 'noopener');
      var tm = el.getAttribute('data-testo-mobile');
      var span = el.querySelector('.testo');
      if (tm && span) span.textContent = tm;
      el.addEventListener('click', function () { pixel('Contact'); });
    } else {
      el.setAttribute('href', el.getAttribute('data-href') || '#richiesta');
      el.addEventListener('click', function (e) {
        e.preventDefault();
        apriModulo(servizio);
      });
    }
  });

  /* Invio modulo (FormSubmit via AJAX, con ripiego su mailto) */
  Array.prototype.forEach.call(document.querySelectorAll('form.richiesta'), function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var honey = form.querySelector('[name="_honey"]');
      if (honey && honey.value) return;
      if (!form.reportValidity()) return;
      var esito = form.querySelector('.esito');
      var btn = form.querySelector('button[type="submit"]');
      var fd = new FormData(form);
      var dati = {};
      fd.forEach(function (v, k) { if (k !== '_honey' && k !== '_next') dati[k] = v; });
      var soggetto = (dati.origine ? '[Ads] ' : '') + 'Richiesta dal sito: ' + (dati.servizio || 'informazioni') + ' - ' + (dati.nome || '') + ' ' + (dati.cognome || '');
      dati._subject = soggetto;
      dati._template = 'table';
      dati._captcha = 'false';
      btn.disabled = true;
      btn.setAttribute('data-testo', btn.textContent);
      btn.textContent = 'Invio in corso…';
      esito.className = 'esito';
      esito.textContent = '';
      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(dati)
      }).then(function (r) {
        return r.json().then(function (j) { return { ok: r.ok, j: j }; }, function () { return { ok: r.ok, j: {} }; });
      }).then(function (res) {
        if (res.ok && String(res.j.success) === 'true') {
          form.querySelector('.campi').hidden = true;
          esito.className = 'esito ok';
          esito.innerHTML = '<strong>Richiesta inviata, grazie.</strong> Ti ricontattiamo al più presto per il sopralluogo gratuito. Se hai urgenza chiama il <a href="tel:+39095525642">095 525642</a>.';
          esito.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          pixel('Lead');
        } else {
          throw new Error(res.j && res.j.message ? res.j.message : 'Invio non riuscito');
        }
      }).catch(function () {
        var corpo = 'Nome: ' + (dati.nome || '') + ' ' + (dati.cognome || '') + '\nEmail: ' + (dati.email || '') + '\nTelefono: ' + (dati.telefono || '') + '\nServizio: ' + (dati.servizio || '') + '\n\n' + (dati.messaggio || '');
        var mailto = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(soggetto) + '&body=' + encodeURIComponent(corpo);
        esito.className = 'esito errore';
        esito.innerHTML = 'Non siamo riusciti a inviare la richiesta dal sito. Puoi <a href="' + mailto + '">inviarla via email</a> con un click oppure chiamare il <a href="tel:+39095525642">095 525642</a>.';
      }).then(function () {
        btn.disabled = false;
        btn.textContent = btn.getAttribute('data-testo') || 'Invia la richiesta';
      });
    });
  });

  /* Menu mobile */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu-mobile');
  function chiudiMenu() {
    if (!menu) return;
    menu.removeAttribute('data-aperto');
    if (burger) burger.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-aperto');
  }
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var aperto = menu.hasAttribute('data-aperto');
      if (aperto) { chiudiMenu(); return; }
      menu.setAttribute('data-aperto', '');
      burger.setAttribute('aria-expanded', 'true');
      document.body.classList.add('menu-aperto');
    });
    Array.prototype.forEach.call(menu.querySelectorAll('a'), function (a) { a.addEventListener('click', chiudiMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') chiudiMenu(); });
  }

  /* Ombra della testata allo scroll */
  var testata = document.querySelector('.testata');
  if (testata) {
    var aggiorna = function () { testata.classList.toggle('scorso', window.scrollY > 10); };
    window.addEventListener('scroll', aggiorna, { passive: true });
    aggiorna();
  }

  /* Animazioni di ingresso */
  var ridotto = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var reveal = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !ridotto) {
    var io = new IntersectionObserver(function (voci) {
      voci.forEach(function (v) {
        if (v.isIntersecting) { v.target.classList.add('visibile'); io.unobserve(v.target); }
      });
    }, { threshold: 0.05, rootMargin: '0px 0px -4% 0px' });
    Array.prototype.forEach.call(reveal, function (el) { io.observe(el); });
    /* failsafe: se l'observer non scatta (ambienti particolari), tutto visibile dopo 4 s */
    setTimeout(function () { Array.prototype.forEach.call(reveal, function (el) { el.classList.add('visibile'); }); }, 4000);
  } else {
    Array.prototype.forEach.call(reveal, function (el) { el.classList.add('visibile'); });
  }

  /* Filtro servizi */
  var filtro = document.getElementById('filtro-servizi');
  if (filtro) {
    var cards = Array.prototype.slice.call(document.querySelectorAll('.servizio'));
    var sezioni = Array.prototype.slice.call(document.querySelectorAll('.categoria'));
    var nessuno = document.querySelector('.nessuno');
    var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    filtro.addEventListener('input', function () {
      var q = norm(filtro.value.trim());
      var tot = 0;
      cards.forEach(function (c) {
        var ok = !q || norm(c.textContent).indexOf(q) !== -1;
        c.hidden = !ok;
        if (ok) tot++;
      });
      sezioni.forEach(function (s) {
        var visibili = Array.prototype.some.call(s.querySelectorAll('.servizio'), function (c) { return !c.hidden; });
        s.hidden = !!q && !visibili;
        var testa = s.querySelector('.testa');
        if (testa) testa.classList.toggle('compatta', !!q);
      });
      if (nessuno) nessuno.classList.toggle('mostra', tot === 0);
    });
  }

  /* Mappa: si carica solo dopo il click (nessun cookie Google senza consenso) */
  Array.prototype.forEach.call(document.querySelectorAll('[data-mappa]'), function (box) {
    var b = box.querySelector('button');
    if (!b) return;
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = box.getAttribute('data-mappa');
      f.loading = 'lazy';
      f.title = 'Mappa della sede So.Ge.Pa.';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      f.allowFullscreen = true;
      box.innerHTML = '';
      box.appendChild(f);
    });
  });

  /* Lightbox rassegna stampa */
  var luce = document.getElementById('luce');
  if (luce) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-luce]'), function (b) {
      b.addEventListener('click', function () {
        luce.querySelector('img').src = b.getAttribute('data-luce');
        if (typeof luce.showModal === 'function') luce.showModal();
      });
    });
    luce.addEventListener('click', function () { luce.close(); });
  }
})();
