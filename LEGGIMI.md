# Sito So.Ge.Pa. Facility Management

Sito statico (HTML/CSS/JS, nessun framework) generato da `build.py`.
Fonti: contenuti e foto del vecchio sito Wix (sogepasnc.com), loghi clienti forniti da Antonio, logo definitivo Sogepa.

## Struttura
- `build.py` — tutti i testi, i 24 servizi, i recapiti e le pagine. **Modifica qui e rilancia** `python3 build.py`.
- `assets/css/stile.css` — stile (palette Wix menta/verde + accenti del marchio teal/blu/magenta/navy, esagono ricorrente).
- `assets/js/sito.js` — CTA adattiva (telefono → WhatsApp, PC → modulo), menu mobile, filtro servizi, mappa su click, invio modulo.
- `assets/img` (foto WebP+JPG), `assets/logo`, `assets/clienti` (13 loghi).
- Pagine generate: index, servizi, chi-siamo, parlano-di-noi, contatti, privacy, cookie, grazie, 404 + sitemap.xml, robots.txt.

## Parametri da tenere d'occhio (in `build.py`, dizionario `AZIENDA`)
- `whatsapp`: 393929957941 (numero che riceve i messaggi WhatsApp).
- `email`: sogepasnc@libero.it (riceve le richieste del modulo).
- `ragione_sociale`, `indirizzo`, `piva`: presi dai registri pubblici, **da confermare col cliente**.
- `BASE`: URL pubblico (ora GitHub Pages). Al cambio dominio basta cambiarlo e rilanciare la build (canonical, sitemap, og:image, JSON-LD si aggiornano).

## Modulo richieste (FormSubmit)
Il modulo invia a `https://formsubmit.co/ajax/sogepasnc@libero.it`.
**Prima richiesta dal sito pubblicato:** FormSubmit manda una mail di attivazione a sogepasnc@libero.it; va cliccato "Activate Form" una volta sola. Da quel momento le richieste arrivano in casella (oggetto "Richiesta dal sito: <servizio> - Nome Cognome").
Se l'invio fallisce, il sito mostra un link "invia via email" (mailto) e il telefono.
Alternativa: Formspree (come freezestudio) → cambiare `ENDPOINT_MODULO`/`ACTION_MODULO` in build.py.

## Tag Google (misurazione delle campagne Google Ads)
- In build.py: `GOOGLE_TAG_ID` = ID conversione Google Ads (formato `AW-1234567890`, da Google Ads → Obiettivi → Conversioni → Riepilogo → "Configurazione tag"); `GA4_ID` facoltativo (`G-…`); `GOOGLE_ADS_ETICHETTE` = etichette delle 3 azioni di conversione create in Google Ads (Sito web, configurazione manuale): `lead_modulo`, `contatto_whatsapp`, `chiamata`. Vuoto = niente tag né banner.
- Con l'ID impostato la build attiva: Consent Mode v2 (tutto "denied" di default, solo segnali anonimi senza cookie), banner Accetta/Rifiuta (scelta in localStorage `sogepa-consenso`), link "Gestisci cookie" nel footer, sezioni Google nelle informative cookie e privacy.
- Eventi: `contatto_whatsapp` (click WhatsApp), `chiamata` (click sui numeri), `lead_modulo` (modulo inviato). Ogni evento è anche un evento GA4; se c'è l'etichetta, viene inviata la conversione Google Ads `AW-…/ETICHETTA`.
- Verifica: Google Tag Assistant (tagassistant.google.com) o Google Ads → Conversioni → stato dopo il primo click.
- Landing `preventivo.html`: non linkata, `noindex`, WhatsApp con testo "ho visto la vostra inserzione", campo nascosto `origine` con gli UTM (con Google Ads: tagging automatico gclid attivo e `?utm_source=google&utm_medium=cpc&utm_campaign=…`), oggetto mail con prefisso [Ads]. Barra fissa WhatsApp/Chiama su mobile.

## Anteprima locale
`python3 -m http.server 4231 --directory <cartella>` (macOS: servire una copia fuori da Downloads se il server non legge la cartella).
Nel desktop Claude: entry `sogepa` in `Downloads/.claude/launch.json` (porta 4231, serve la copia in scratchpad: risincronizzare con rsync dopo le modifiche).

## Pubblicazione (GitHub Pages, come gli altri siti Freeze)
1. `git init && git add -A && git commit -m "Sito So.Ge.Pa."`
2. Repo `antoniofreeze/sogepa` → push su `main` → Settings ▸ Pages ▸ Deploy from branch `main` / root.
3. Il sito risponde su https://antoniofreeze.github.io/sogepa/ (BASE già impostato così).
4. Dominio definitivo (sogepasnc.com, oggi su Wix): aggiungere il file `CNAME`, puntare il DNS, cambiare `BASE` e rilanciare la build.
