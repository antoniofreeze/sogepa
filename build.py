#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore statico del sito So.Ge.Pa. Facility Management.
Uso:  python3 build.py        → scrive le pagine HTML, sitemap.xml e robots.txt nella cartella del progetto.
Tutti i contenuti (testi, servizi, recapiti) vivono qui: modifica e rilancia.
"""
import os, json, datetime, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://antoniofreeze.github.io/sogepa"   # ← cambiare quando il sito va sul dominio definitivo
ANNO = datetime.date.today().year
VERSIONE = "3"   # ← aumentare a ogni modifica di CSS o JS (evita la cache dei browser)
OGGI = datetime.date.today().isoformat()

AZIENDA = {
    "nome": "So.Ge.Pa.",
    "nome_esteso": "So.Ge.Pa. Facility Management",
    "ragione_sociale": "So.Ge.P.A. S.n.c. Ambiente Global Service",   # da confermare (in home Wix compare "S.r.l.")
    "indirizzo": "Via Roma 17",
    "cap": "95037",
    "citta": "San Giovanni La Punta",
    "provincia": "CT",
    "piva": "02158910873",
    "tel_fisso": "095 525642",
    "tel_fisso_link": "+39095525642",
    "cell": "392 995 7941",
    "cell_link": "+393929957941",
    "whatsapp": "393929957941",
    "email": "sogepasnc@libero.it",
    "google_maps": "https://www.google.com/maps/search/?api=1&query=So.Ge.Pa.+San+Giovanni+La+Punta",
    "mappa_embed": "https://www.google.com/maps?q=Via+Roma+17,+95037+San+Giovanni+La+Punta+CT&output=embed",
}
ENDPOINT_MODULO = "https://formsubmit.co/ajax/" + AZIENDA["email"]
ACTION_MODULO = "https://formsubmit.co/" + AZIENDA["email"]

# ---------------------------------------------------------------- servizi
CATEGORIE = [
    {
        "id": "pulizie", "nome": "Pulizie", "colore": "teal", "icona": "scopa", "foto": "pulizie",
        "alt": "Operatore che pulisce una grande vetrata dall'interno di un ufficio",
        "breve": "Uffici, condomini, negozi, hotel e ambienti industriali: pulizie ordinarie e interventi speciali, dai vetri ai pannelli fotovoltaici.",
        "intro": "Pulizie professionali per uffici, condomini, negozi, strutture ricettive e ambienti industriali: interventi programmati o straordinari, con squadre formate e attrezzature dedicate.",
        "servizi": [
            ("Pulizie speciali per ambienti sensibili", "scudo", "Protocolli dedicati per strutture sanitarie, laboratori, scuole e ambienti che richiedono standard igienici elevati."),
            ("Pulizia pannelli fotovoltaici", "sole", "Rimozione di polvere, guano e depositi dai moduli per recuperare il rendimento dell’impianto, senza graffiare le superfici."),
            ("Pulizia post cantiere", "cantiere", "Rimozione di polveri, residui di cemento, colla e vernice a fine lavori: consegniamo l’ambiente pronto da usare."),
            ("Pulizia e decalcificazione vetri e vetrate", "finestra", "Servizio specializzato per finestre, vetri e vetrate: rimuoviamo calcare e aloni per una trasparenza perfetta. Rendiamo brillanti i tuoi vetri."),
            ("Ripristino pavimentazione", "pavimento", "Pulizia di fondo e recupero di pavimenti usurati o macchiati, per riportarli all’aspetto originale."),
            ("Pulizie piscine", "onde", "Pulizia di vasche, bordi e aree solarium per piscine di condomini, hotel e strutture sportive."),
            ("Pulizia grondaie", "grondaia", "Rimozione di foglie, detriti e ostruzioni da grondaie e pluviali, per prevenire infiltrazioni e ristagni."),
            ("Shampoo rinnovante moquette", "moquette", "Lavaggio profondo di moquette e tappeti per rimuovere sporco, macchie e odori e rinnovare le fibre."),
        ],
    },
    {
        "id": "trattamenti", "nome": "Trattamenti", "colore": "blu", "icona": "cera", "foto": "trattamenti",
        "alt": "Operatore con lavasciuga professionale su un pavimento industriale",
        "breve": "Ceratura, levigatura, lucidatura e protezione di pavimenti e superfici: recuperiamo i materiali e ne allunghiamo la vita.",
        "intro": "Trattamenti specialistici per pavimenti e superfici: proteggono i materiali, li rinnovano e ne allungano la vita, riducendo i costi di manutenzione nel tempo.",
        "servizi": [
            ("Ceratura e deceratura pavimenti", "cera", "Rimozione delle vecchie cere e applicazione di nuovi strati protettivi, per pavimenti brillanti e più resistenti."),
            ("Trattamento antiscivolo", "grip", "Trattamento delle superfici per aumentare l’aderenza e ridurre il rischio di cadute in aree bagnate o ad alto passaggio."),
            ("Vetrificazione permanente superfici", "goccia", "Protezione a lunga durata che sigilla la superficie e la rende più facile da pulire e mantenere."),
            ("Rimozione graffiti", "gomma", "Eliminazione di scritte e vernici da muri, serrande e superfici in pietra, rispettando il materiale di base."),
            ("Trattamento pavimenti in PVC e linoleum", "pavimento", "Pulizia di fondo e protezione specifica per pavimenti resilienti, molto diffusi in scuole, uffici e strutture sanitarie."),
            ("Levigatura pavimenti", "pietra", "Levigatura meccanica di marmo, pietra e cemento per eliminare graffi e dislivelli e recuperare la superficie."),
            ("Trattamento cotto e pietre naturali", "pietra", "Pulizia, impregnazione e protezione di cotto e pietre naturali contro macchie e umidità."),
            ("Lucidatura e sigillatura pavimenti", "cera", "Lucidatura a specchio e sigillatura dei pori, per pavimenti protetti e più semplici da pulire."),
        ],
    },
    {
        "id": "disinfestazioni", "nome": "Disinfestazioni e sanificazioni", "colore": "magenta", "icona": "insetto", "foto": "disinfestazioni",
        "alt": "Sanificazione a vapore di un pavimento con guanti gialli",
        "breve": "Derattizzazione, deblattizzazione, cimici, colombi e sanificazione ambientale, con monitoraggio anche per il settore alimentare.",
        "intro": "Disinfestazione, derattizzazione e sanificazione con procedure controllate e monitoraggio degli infestanti, anche per ristoranti e industrie alimentari.",
        "servizi": [
            ("Sanificazione e disinfezione ambientale", "spray", "Interventi professionali per eliminare batteri, virus e agenti contaminanti, garantendo ambienti igienizzati e sicuri."),
            ("Disinfestazione caditoie e fognature", "scarico", "Trattamento di caditoie, pozzetti e reti fognarie contro blatte e insetti, con interventi programmati."),
            ("Controllo infestanti per locali food", "cibo", "Monitoraggio e controllo degli infestanti per ristoranti, bar e industrie alimentari, in linea con i piani HACCP."),
            ("Allontanamento colombi", "uccello", "Sistemi dissuasori e interventi per allontanare i colombi da tetti, cornicioni e balconi, con pulizia del guano."),
            ("Disinfestazione termiti", "legno", "Individuazione e trattamento delle colonie di termiti per proteggere legno e strutture."),
            ("Disinfestazione e deblattizzazione", "insetto", "Eliminazione di blatte e insetti striscianti con trattamenti mirati e monitoraggio dei risultati."),
            ("Disinfestazione cimici dei letti", "letto", "Trattamenti specifici per hotel, B&B e abitazioni, con verifica degli ambienti dopo l’intervento."),
            ("Derattizzazione", "topo", "Piani di derattizzazione con esche in sicurezza, postazioni controllate e monitoraggio periodico."),
        ],
    },
]
TOT_SERVIZI = sum(len(c["servizi"]) for c in CATEGORIE)

CLIENTI = [
    ("benetton", "United Colors of Benetton"), ("geox", "Geox"), ("sheraton", "Sheraton"),
    ("belmond-grand-hotel-timeo", "Belmond Grand Hotel Timeo, Taormina"), ("regione-siciliana", "Regione Siciliana"),
    ("save-the-children", "Save the Children"), ("zanichelli", "Zanichelli"), ("sisley", "Sisley Paris"),
    ("bricocity", "Bricocity"), ("sidra", "Sidra S.p.A."), ("acoset", "Acoset S.p.A."), ("agrosan", "Agrosan Sicilia"),
    ("campus", "eCampus Università"),
]

RECENSIONI = [
    ("Puntualità, professionalità, cortesia. Ci siamo trovati benissimo e il lavoro fatto è stato impeccabile. Il personale è gentile e molto disponibile. Impresa consigliatissima.", "Anna Monosi"),
    ("Personale affidabile, serio ed esperto. L’intervento è stato tempestivo e super efficiente. Lo consiglio vivamente! Complimenti e grazie ancora… finalmente il mio incubo è finito!!!", "Angela Russo"),
    ("Massima professionalità, cordialità e precisione nei lavori, cosa che non sempre è evidente in questo settore. 5 stelle, più che da consigliare!!!!", "Maurizio Verdone"),
]

CERTIFICAZIONI = [
    ("ISO 45001", "scudo", "Sistema di gestione della salute e sicurezza sul lavoro: ambienti operativi sicuri e rispetto delle normative per la tutela di lavoratori e clienti."),
    ("UNI EN 13549", "medaglia", "Standard europeo per i servizi di pulizia: definisce come misurare e controllare la qualità del servizio erogato."),
    ("ISO 14001", "foglia", "Sistema di gestione ambientale: processi e prodotti a basso impatto, nel rispetto dell’ambiente e della sostenibilità."),
    ("Protocolli di sanificazione", "spray", "Interventi professionali di sanificazione per eliminare batteri, virus e agenti contaminanti, garantendo ambienti igienizzati e sicuri."),
]

# ---------------------------------------------------------------- icone svg
_S = 'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"'
ICONE = {
    "wa": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2m.01 1.67c4.55 0 8.24 3.7 8.24 8.24 0 4.55-3.69 8.24-8.24 8.24-1.49 0-2.94-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24M8.53 7.33c-.16 0-.43.06-.66.31-.22.25-.87.86-.87 2.07 0 1.22.89 2.39 1 2.56.14.17 1.76 2.67 4.25 3.73.59.27 1.05.42 1.41.53.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.07-.1-.23-.16-.48-.27-.25-.14-1.47-.74-1.69-.82-.23-.08-.37-.12-.56.12-.16.25-.64.81-.78.97-.15.17-.29.19-.53.07-.26-.13-1.06-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.12-.24-.01-.39.11-.5.11-.11.27-.29.37-.44.13-.14.17-.25.25-.41.08-.17 0-.31-.05-.43-.06-.12-.56-1.36-.78-1.85-.19-.5-.4-.42-.55-.43-.14 0-.3-.01-.47-.01"/></svg>',
    "mail": f'<svg {_S}><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "tel": f'<svg {_S}><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "pin": f'<svg {_S}><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>',
    "check": f'<svg {_S}><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
    "freccia": f'<svg {_S}><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "lente": f'<svg {_S}><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg>',
    "x": f'<svg {_S}><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "scopa": f'<svg {_S}><path d="m14 3 7 7"/><path d="m9.5 8.5 6 6"/><path d="M3 21c1-5 4-8 6.5-9.5l4 4C12 18 9 21 3 21z"/></svg>',
    "spray": f'<svg {_S}><rect x="7" y="9" width="8" height="12" rx="2"/><path d="M9 9V6h4v3"/><path d="M13 6h3"/><path d="m18 4.5 1.5-1M19 7h2M18 9.5l1.5 1"/></svg>',
    "scudo": f'<svg {_S}><path d="M12 3l8 3v6c0 4.5-3.2 7.8-8 9-4.8-1.2-8-4.5-8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>',
    "sole": f'<svg {_S}><rect x="3" y="11" width="18" height="9" rx="1"/><path d="M3 15.5h18M9 11v9M15 11v9"/><path d="M12 3v3M6.5 5l1.5 1.5M17.5 5 16 6.5"/></svg>',
    "cantiere": f'<svg {_S}><path d="M4 15a8 8 0 0 1 16 0"/><path d="M2 15h20v3H2z"/><path d="M10 7v5M14 7v5"/></svg>',
    "finestra": f'<svg {_S}><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M12 3v18M4 12h16"/><path d="m7 7 2-2"/></svg>',
    "pavimento": f'<svg {_S}><path d="m3 9 9-5 9 5-9 5z"/><path d="m3 14 9 5 9-5"/></svg>',
    "onde": f'<svg {_S}><path d="M2 8c2 0 3-1.5 5-1.5S10 8 12 8s3-1.5 5-1.5S20 8 22 8"/><path d="M2 13c2 0 3-1.5 5-1.5S10 13 12 13s3-1.5 5-1.5S20 13 22 13"/><path d="M2 18c2 0 3-1.5 5-1.5S10 18 12 18s3-1.5 5-1.5S20 18 22 18"/></svg>',
    "grondaia": f'<svg {_S}><path d="m3 11 9-7 9 7"/><path d="M5 11v3h14v-3"/><path d="M8 17v2M12 17v3M16 17v2"/></svg>',
    "moquette": f'<svg {_S}><path d="M4 8h13a3 3 0 0 1 0 6H4"/><circle cx="4" cy="11" r="3"/><path d="M8 17h10M8 20h7"/></svg>',
    "cera": f'<svg {_S}><path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="m19 17 .8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/></svg>',
    "grip": f'<svg {_S}><path d="m4 18 4-9 3 6 3-4 6 7z"/><path d="M4 21h16"/></svg>',
    "goccia": f'<svg {_S}><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></svg>',
    "gomma": f'<svg {_S}><path d="m3 17 9.5-9.5a2 2 0 0 1 2.8 0l3.2 3.2a2 2 0 0 1 0 2.8L13 19H7z"/><path d="M6 20h15"/><path d="m9 11 6 6"/></svg>',
    "pietra": f'<svg {_S}><path d="M8 3h8l4 7-4 7H8l-4-7z"/><path d="m8 3 4 7h8M12 10l-4 7"/></svg>',
    "insetto": f'<svg {_S}><ellipse cx="12" cy="13" rx="5" ry="7"/><path d="M12 6V3M9 4 7 2M15 4l2-2"/><path d="M7 10H3M7 14H3M17 10h4M17 14h4M7 18l-2 2M17 18l2 2"/></svg>',
    "scarico": f'<svg {_S}><rect x="3" y="10" width="18" height="10" rx="1"/><path d="M6 13v4M10 13v4M14 13v4M18 13v4"/><path d="M12 3v4M9 5l3 3 3-3"/></svg>',
    "cibo": f'<svg {_S}><path d="M7 3v18"/><path d="M5 3v5a2 2 0 0 0 4 0V3"/><path d="M16 3c-2 2-2 6-2 8h4V3z"/><path d="M16 11v10"/></svg>',
    "uccello": f'<svg {_S}><path d="M3 12c4 0 6-2 8-5 1 3 3 5 6 5l-1 2h-4c-2 3-5 4-9 4z"/><path d="m16 12 5-2-2 4"/></svg>',
    "legno": f'<svg {_S}><path d="m3 16 18-6"/><path d="m3 19 18-6"/><circle cx="14" cy="8" r="3"/><path d="M14 5V3M11.5 6 10 5M16.5 6 18 5"/></svg>',
    "letto": f'<svg {_S}><path d="M3 18V8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v10"/><path d="M3 14h18"/><path d="M6 10h5v4H6z"/></svg>',
    "topo": f'<svg {_S}><path d="M4 15c0-4 4-7 9-7s7 3 7 6-2 5-6 5H8a4 4 0 0 1-4-4z"/><circle cx="16" cy="12" r="1"/><path d="M13 8c0-3 3-4 5-2"/><path d="M20 15c2 1 1 4-1 4"/></svg>',
    "foglia": f'<svg {_S}><path d="M5 20c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 20c4-5 7-8 11-11"/></svg>',
    "medaglia": f'<svg {_S}><circle cx="12" cy="9" r="5"/><path d="m9 13-1 8 4-2.5L16 21l-1-8"/></svg>',
    "lista": f'<svg {_S}><path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/></svg>',
    "chat": f'<svg {_S}><path d="M4 5h16v11H9l-5 4z"/></svg>',
    "documento": f'<svg {_S}><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
    "orologio": f'<svg {_S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}
def ico(n): return ICONE[n]

# ---------------------------------------------------------------- helper html
def e(s): return H.escape(s, quote=True)

def _dim(nome, w):
    """Dimensioni reali dei file (per width/height e srcset)."""
    try:
        from PIL import Image
        with Image.open(os.path.join(ROOT, "assets/img", f"{nome}-{w}.jpg")) as im:
            return im.size
    except Exception:
        return (w, None)

def pic(nome, alt, widths, sizes="100vw", priority=False, cls=""):
    ws = sorted(widths)
    webp = ", ".join(f"assets/img/{nome}-{w}.webp {_dim(nome,w)[0]}w" for w in ws)
    jpg = ", ".join(f"assets/img/{nome}-{w}.jpg {_dim(nome,w)[0]}w" for w in ws)
    big = ws[-1]
    W, Hh = _dim(nome, big)
    dims = f' width="{W}" height="{Hh}"' if Hh else ""
    attrs = ' fetchpriority="high"' if priority else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture{c}><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="assets/img/{nome}-{big}.jpg" srcset="{jpg}" sizes="{sizes}" alt="{e(alt)}"{dims}{attrs} decoding="async"></picture>')

def hexicon(icona, colore="", extra=""):
    c = f" {colore}" if colore else ""
    x = f" {extra}" if extra else ""
    return f'<span class="hexicon{c}{x}">{ico(icona)}</span>'

def cta(testo, servizio="", cls="btn-primario", extra="", testo_mobile="Scrivici su WhatsApp"):
    """Pulsante adattivo: da telefono apre WhatsApp, da PC apre il modulo (vedi sito.js)."""
    s = f' data-servizio="{e(servizio)}"' if servizio else ""
    return (f'<a class="btn {cls}{(" "+extra) if extra else ""}" href="contatti.html#richiesta" data-cta{s} data-testo-mobile="{e(testo_mobile)}">'
            f'<span class="ico-wa">{ico("wa")}</span><span class="ico-form">{ico("mail")}</span><span class="testo">{e(testo)}</span></a>')

def btn_tel(cls="btn-secondario", testo=None):
    t = testo or f'Chiama {AZIENDA["tel_fisso"]}'
    return f'<a class="btn {cls}" href="tel:{AZIENDA["tel_fisso_link"]}">{ico("tel")}<span>{e(t)}</span></a>'

def btn_wa(testo="Apri WhatsApp", cls="btn-wa", servizio=""):
    s = f' data-servizio="{e(servizio)}"' if servizio else ""
    return f'<a class="btn {cls}" href="https://wa.me/{AZIENDA["whatsapp"]}" data-wa{s}>{ico("wa")}<span>{e(testo)}</span></a>'

NAV = [("index.html", "Home"), ("servizi.html", "Servizi"), ("chi-siamo.html", "Chi siamo"),
       ("parlano-di-noi.html", "Parlano di noi"), ("contatti.html", "Contatti")]

def testata(pagina):
    def cur(h): return ' aria-current="page"' if h == pagina else ''
    voci = "".join(f'<li><a href="{h}"{cur(h)}>{t}</a></li>' for h, t in NAV)
    voci_m = "".join(f'<a class="voce" href="{h}"{cur(h)}>{t}</a>' for h, t in NAV)
    return f'''
<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="testata">
  <div class="contenitore">
    <a class="marchio" href="index.html" aria-label="So.Ge.Pa. Facility Management, torna alla home">
      <img src="assets/logo/logo-orizzontale.png" alt="So.Ge.Pa. Facility Management" width="1200" height="245">
    </a>
    <nav class="nav" aria-label="Principale"><ul>{voci}</ul></nav>
    <div class="azioni-testata">
      {cta("Richiedi un preventivo", cls="btn-primario btn-piccolo", testo_mobile="WhatsApp")}
      <button class="burger" aria-expanded="false" aria-controls="menu-mobile" aria-label="Apri il menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<nav class="menu-mobile" id="menu-mobile" aria-label="Menu mobile">
  {voci_m}
  <div class="azioni">
    {btn_wa("Scrivici su WhatsApp")}
    {btn_tel()}
  </div>
  <p class="recapiti-mini">{e(AZIENDA["ragione_sociale"])}<br>{e(AZIENDA["indirizzo"])}, {AZIENDA["cap"]} {e(AZIENDA["citta"])} ({AZIENDA["provincia"]})<br><a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a></p>
</nav>'''

def pie():
    return f'''
<footer class="pie">
  <div class="contenitore">
    <div class="griglia-pie">
      <div class="marchio-pie">
        <img src="assets/logo/logo-orizzontale-bianco.png" alt="So.Ge.Pa. Facility Management" width="1200" height="245">
        <p>Impresa di pulizie, trattamenti, disinfestazioni e facility management. Oltre 35 anni di igiene professionale per aziende, condomini, enti e privati in tutta la Sicilia.</p>
      </div>
      <div>
        <h4>Contatti</h4>
        <ul>
          <li class="recapito-pie">{ico("tel")}<a href="tel:{AZIENDA["tel_fisso_link"]}">{AZIENDA["tel_fisso"]}</a></li>
          <li class="recapito-pie">{ico("wa")}<a href="https://wa.me/{AZIENDA["whatsapp"]}" data-wa>{AZIENDA["cell"]} · WhatsApp</a></li>
          <li class="recapito-pie">{ico("mail")}<a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a></li>
          <li class="recapito-pie">{ico("pin")}<span>{e(AZIENDA["indirizzo"])}<br>{AZIENDA["cap"]} {e(AZIENDA["citta"])} ({AZIENDA["provincia"]})</span></li>
        </ul>
      </div>
      <div>
        <h4>Pagine</h4>
        <ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}
          <li><a href="servizi.html#pulizie">Pulizie</a></li>
          <li><a href="servizi.html#trattamenti">Trattamenti</a></li>
          <li><a href="servizi.html#disinfestazioni">Disinfestazioni</a></li>
        </ul>
      </div>
      <div>
        <h4>Informazioni legali</h4>
        <ul>
          <li>{e(AZIENDA["ragione_sociale"])}</li>
          <li>P. IVA {AZIENDA["piva"]}</li>
          <li><a href="privacy.html">Informativa sulla privacy</a></li>
          <li><a href="cookie.html">Informativa sui cookie</a></li>
        </ul>
      </div>
    </div>
    <div class="fondo">
      <span>© {ANNO} {e(AZIENDA["ragione_sociale"])} · Tutti i diritti riservati</span>
      <span>Sito realizzato da <a href="https://www.freezestudio.it" rel="noopener" target="_blank">Freeze Studio</a></span>
    </div>
  </div>
</footer>
<a class="wa-flottante" href="https://wa.me/{AZIENDA["whatsapp"]}" data-wa aria-label="Scrivici su WhatsApp">{ico("wa")}</a>'''

def opzioni_servizi():
    out = ['<option value="">Scegli un servizio…</option>']
    for c in CATEGORIE:
        out.append(f'<optgroup label="{e(c["nome"])}">' + "".join(f'<option value="{e(n)}">{e(n)}</option>' for n, _, _ in c["servizi"]) + "</optgroup>")
    out.append('<option value="Altro / non so ancora">Altro / non so ancora</option>')
    return "".join(out)

def modulo(prefisso="m", in_pagina=False):
    p = prefisso
    return f'''
<form class="richiesta" action="{ACTION_MODULO}" method="POST" novalidate="" aria-labelledby="{p}-titolo">
  <input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off" aria-hidden="true">
  <input type="hidden" name="_next" value="{BASE}/grazie.html">
  <input type="hidden" name="_subject" value="Richiesta dal sito So.Ge.Pa.">
  <div class="campi">
    <div class="campo"><label for="{p}-nome">Nome *</label><input id="{p}-nome" name="nome" required autocomplete="given-name"></div>
    <div class="campo"><label for="{p}-cognome">Cognome *</label><input id="{p}-cognome" name="cognome" required autocomplete="family-name"></div>
    <div class="campo"><label for="{p}-email">Email *</label><input id="{p}-email" type="email" name="email" required autocomplete="email" inputmode="email"></div>
    <div class="campo"><label for="{p}-tel">Telefono</label><input id="{p}-tel" type="tel" name="telefono" autocomplete="tel" inputmode="tel"></div>
    <div class="campo intero"><label for="{p}-servizio">Servizio richiesto *</label><select id="{p}-servizio" name="servizio" required>{opzioni_servizi()}</select></div>
    <div class="campo intero"><label for="{p}-msg">Messaggio</label><textarea id="{p}-msg" name="messaggio" placeholder="Descrivi l’ambiente, la superficie indicativa e quando ti servirebbe l’intervento."></textarea></div>
    <div class="campo intero consenso"><input type="checkbox" id="{p}-privacy" name="privacy" value="accettata" required><label for="{p}-privacy">Ho letto l’<a href="privacy.html">informativa sulla privacy</a> e acconsento al trattamento dei dati per essere ricontattato. *</label></div>
    <div class="campo intero">
      <button class="btn btn-primario btn-grande" type="submit">{ico("mail")}<span>Invia la richiesta</span></button>
      <p class="nota">Sopralluogo e preventivo sono gratuiti e senza impegno. La richiesta arriva direttamente a {AZIENDA["email"]}.</p>
    </div>
  </div>
  <div class="esito" role="status" aria-live="polite"></div>
</form>'''

def modale():
    return f'''
<dialog class="modale" id="modale-richiesta" aria-labelledby="mod-titolo">
  <div class="interno">
    <header>
      <div><h2 id="mod-titolo">Richiedi un preventivo</h2><p>Compila il modulo: la richiesta arriva direttamente in azienda e ti ricontattiamo per il sopralluogo gratuito.</p></div>
      <button class="chiudi" type="button" aria-label="Chiudi">{ico("x")}</button>
    </header>
    {modulo("mod")}
  </div>
</dialog>'''

def banda_cta(titolo="Hai bisogno di un intervento?", testo="Raccontaci di cosa hai bisogno: ti rispondiamo con un sopralluogo gratuito e un preventivo chiaro.", servizio=""):
    return f'''
<section class="banda-cta" aria-labelledby="cta-titolo">
  <span class="deco-hex deco-a" aria-hidden="true"></span>
  <div class="contenitore">
    <div><h2 id="cta-titolo">{e(titolo)}</h2><p>{e(testo)}</p></div>
    <div class="azioni">{cta("Richiedi un preventivo", servizio=servizio)}{btn_tel("btn-contorno-chiaro")}</div>
  </div>
</section>'''

def sezione_certificazioni(reveal=True):
    cards = "".join(f'''<article class="cert reveal r{i+1}">{hexicon(ic)}<h3>{e(t)}</h3><p>{e(d)}</p></article>''' for i, (t, ic, d) in enumerate(CERTIFICAZIONI))
    return f'''
<section class="sezione scura" aria-labelledby="cert-titolo">
  <span class="deco-hex deco-a" aria-hidden="true"></span><span class="deco-hex deco-b" aria-hidden="true"></span>
  <div class="contenitore">
    <div class="intesta centro reveal"><p class="etichetta">Qualità e sicurezza</p><h2 id="cert-titolo">Certificazioni e standard che seguiamo</h2><p class="sotto">Lavoriamo con procedure controllate, per la sicurezza di chi lavora con noi e di chi ci affida i propri spazi.</p></div>
    <div class="griglia-4">{cards}</div>
  </div>
</section>'''

def google_pill():
    return f'''<a class="google" href="{AZIENDA["google_maps"]}" target="_blank" rel="noopener"><span class="g">G</span><span><span class="voto">5,0</span> <span class="stelle" aria-label="5 stelle su 5">★★★★★</span><br><small>129 recensioni su Google</small></span></a>'''

def sezione_recensioni():
    cards = "".join(f'''<article class="recensione reveal r{i+1}"><div class="stelle" aria-label="5 stelle su 5">★★★★★</div><blockquote>“{e(t)}”</blockquote><footer><span class="avatar" aria-hidden="true">{n[0]}</span>{e(n)}</footer></article>''' for i, (t, n) in enumerate(RECENSIONI))
    return f'''
<section class="sezione tinta" aria-labelledby="rec-titolo">
  <div class="contenitore">
    <div class="testa-recensioni reveal">
      <div class="intesta"><p class="etichetta">Dicono di noi</p><h2 id="rec-titolo">Una reputazione immacolata</h2><p class="sotto">Le parole di chi ha scelto So.Ge.Pa. per i propri spazi.</p></div>
      {google_pill()}
    </div>
    <div class="griglia-3">{cards}</div>
  </div>
</section>'''

def documento(pagina, titolo, descrizione, corpo, con_modale=True, jsonld=None, og_img="assets/img/hero-home-1600.jpg", tipo="website"):
    canon = f"{BASE}/" if pagina == "index.html" else f"{BASE}/{pagina}"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    cfg = json.dumps({"whatsapp": AZIENDA["whatsapp"], "email": AZIENDA["email"], "endpoint": ENDPOINT_MODULO})
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="format-detection" content="telephone=no">
<title>{e(titolo)}</title>
<meta name="description" content="{e(descrizione)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#125C4D">
<meta property="og:type" content="{tipo}">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="So.Ge.Pa. Facility Management">
<meta property="og:title" content="{e(titolo)}">
<meta property="og:description" content="{e(descrizione)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="assets/logo/favicon-32.png">
<link rel="apple-touch-icon" href="assets/logo/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/stile.css?v={VERSIONE}">
<script>window.SOGEPA={cfg};</script>
{ld}
</head>
<body>
{testata(pagina)}
<main id="contenuto">
{corpo}
</main>
{pie()}
{modale() if con_modale else ""}
<script src="assets/js/sito.js?v={VERSIONE}" defer></script>
</body>
</html>'''

JSONLD_AZIENDA = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "@id": f"{BASE}/#azienda",
    "name": AZIENDA["nome_esteso"], "legalName": AZIENDA["ragione_sociale"], "url": f"{BASE}/",
    "logo": f"{BASE}/assets/logo/logo-orizzontale.png", "image": f"{BASE}/assets/img/hero-home-1600.jpg",
    "description": "Impresa di pulizie, trattamenti, disinfestazioni, sanificazioni e facility management a Catania e in tutta la Sicilia. Oltre 35 anni di esperienza, sopralluogo e preventivo gratuiti.",
    "telephone": AZIENDA["tel_fisso_link"], "email": AZIENDA["email"], "vatID": "IT" + AZIENDA["piva"],
    "address": {"@type": "PostalAddress", "streetAddress": AZIENDA["indirizzo"], "addressLocality": AZIENDA["citta"],
                "addressRegion": AZIENDA["provincia"], "postalCode": AZIENDA["cap"], "addressCountry": "IT"},
    "areaServed": ["Catania", "Provincia di Catania", "Sicilia"],
    "contactPoint": [{"@type": "ContactPoint", "telephone": AZIENDA["cell_link"], "contactType": "customer service", "availableLanguage": "it"}],
}

# ---------------------------------------------------------------- pagine
def pagina_home():
    hero_pic = f'''<picture>
  <source media="(min-width:901px)" type="image/webp" srcset="assets/img/hero-home-p-640.webp 640w, assets/img/hero-home-p-1000.webp 1000w" sizes="(min-width:1200px) 540px, 45vw">
  <source media="(min-width:901px)" srcset="assets/img/hero-home-p-640.jpg 640w, assets/img/hero-home-p-1000.jpg 1000w" sizes="(min-width:1200px) 540px, 45vw">
  <source type="image/webp" srcset="assets/img/hero-home-640.webp 640w, assets/img/hero-home-1000.webp 1000w, assets/img/hero-home-1600.webp 1600w" sizes="100vw">
  <img src="assets/img/hero-home-1000.jpg" srcset="assets/img/hero-home-640.jpg 640w, assets/img/hero-home-1000.jpg 1000w, assets/img/hero-home-1600.jpg 1600w" sizes="100vw" alt="Operatrice So.Ge.Pa. al lavoro con il carrello delle pulizie nel corridoio di un ufficio" width="1000" height="666" fetchpriority="high" decoding="async">
</picture>'''
    loghi = "".join(f'<img src="assets/clienti/{f}.png" alt="{e(n)}" loading="lazy" height="44">' for f, n in CLIENTI)
    loghi_dup = "".join(f'<img class="dup" src="assets/clienti/{f}.png" alt="" aria-hidden="true" loading="lazy" height="44">' for f, n in CLIENTI)
    pilastri = "".join(f'''
      <a class="pilastro reveal r{i+1}" href="servizi.html#{c["id"]}">
        <div class="foto">{pic(c["foto"], c["alt"], [640,1000] if c["foto"]!="disinfestazioni" else [780], "(min-width:1000px) 380px, (min-width:640px) 50vw, 100vw")}{hexicon(c["icona"], c["colore"])}</div>
        <div class="corpo"><span class="conteggio">{len(c["servizi"])} servizi</span><h3>{e(c["nome"])}</h3><p>{e(c["breve"])}</p><span class="link">Vedi i servizi {ico("freccia")}</span></div>
      </a>''' for i, c in enumerate(CATEGORIE))
    interventi = [("vetri", "Pulizia e decalcificazione vetri e vetrate", "Operatrice che lava una finestra dietro una veneziana"),
                  ("fotovoltaico", "Pulizia pannelli fotovoltaici", "Spazzola rotante che pulisce pannelli fotovoltaici"),
                  ("piscine", "Pulizie piscine", "Operatore che spazzola il fondo di una piscina vuota"),
                  ("moquette", "Shampoo rinnovante moquette", "Lavaggio di una moquette con macchina a estrazione")]
    galleria = "".join(f'''<figure class="intervento reveal r{i+1}">{pic(f, a, [640,1000] if f not in ("moquette",) else [900], "(min-width:1000px) 25vw, 50vw")}<figcaption>{e(t)}</figcaption></figure>''' for i, (f, t, a) in enumerate(interventi))
    passi = [("Scegli il servizio", f"Trova quello che ti serve tra i nostri {TOT_SERVIZI} servizi, oppure descrivici il problema: ti indirizziamo noi.", "lista", "teal"),
             ("Scrivici", "Da telefono ci raggiungi su WhatsApp con un tocco; da computer compili il modulo e la richiesta arriva direttamente in azienda.", "chat", "blu"),
             ("Sopralluogo e preventivo", "Un nostro tecnico valuta gli ambienti e ti propone tempi, modalità e costi. Poi interveniamo.", "documento", "magenta")]
    passi_html = "".join(f'''<article class="passo reveal r{i+1}"><span class="numero" style="background:var(--{col})">{i+1}</span><h3>{e(t)}</h3><p>{e(d)}</p></article>''' for i, (t, d, ic, col) in enumerate(passi))
    corpo = f'''
<section class="hero" aria-labelledby="hero-titolo">
  <span class="deco-hex deco-a" aria-hidden="true"></span><span class="deco-hex deco-b" aria-hidden="true"></span>
  <div class="contenitore">
    <div class="hero-testo">
      <p class="etichetta">Impresa di pulizie · San Giovanni La Punta, Catania</p>
      <h1 id="hero-titolo">Impresa di pulizie e facility management a Catania</h1>
      <p class="sotto">Pulizie, trattamenti, sanificazioni e disinfestazioni per aziende, condomini, strutture ricettive e privati. Oltre 35 anni di esperienza, personale formato e sopralluogo gratuito.</p>
      <div class="azioni">{cta("Richiedi un preventivo", extra="btn-grande")}<a class="btn btn-secondario btn-grande" href="servizi.html">{ico("lista")}<span>Scopri i servizi</span></a></div>
      <ul class="prove">
        <li><span class="hexdot teal"></span>Oltre 35 anni di attività</li>
        <li><span class="hexdot blu"></span>5,0 su Google · 129 recensioni</li>
        <li><span class="hexdot magenta"></span>ISO 45001 · ISO 14001</li>
      </ul>
    </div>
    <div class="hero-foto">
      <div class="cornice">{hero_pic}</div>
      <div class="badge-flottante">{hexicon("check", "menta", "piccolo")}<span>Sopralluogo e preventivo gratuiti<small>Senza impegno, in tutta la Sicilia</small></span></div>
    </div>
  </div>
</section>

<section class="loghi" aria-label="Aziende e enti che hanno scelto So.Ge.Pa.">
  <div class="contenitore">
    <p class="titolo-loghi">Hanno scelto So.Ge.Pa.</p>
    <div class="nastro"><div class="nastro-track">{loghi}{loghi_dup}</div></div>
  </div>
</section>

<section class="sezione" aria-labelledby="cosa-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">Cosa facciamo</p><h2 id="cosa-titolo">Tre aree, un solo interlocutore</h2><p class="sotto">Dalle pulizie quotidiane ai trattamenti specialistici, fino a disinfestazioni e sanificazioni: gestiamo ogni aspetto dell’igiene dei tuoi spazi.</p></div>
    <div class="griglia-3">{pilastri}</div>
  </div>
</section>

<section class="sezione tinta" aria-labelledby="campo-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">Sul campo</p><h2 id="campo-titolo">Dalle vetrate ai pannelli fotovoltaici</h2><p class="sotto">Ogni superficie ha la sua tecnica: attrezzature dedicate e prodotti specifici per ciascun materiale.</p></div>
    <div class="interventi">{galleria}</div>
  </div>
</section>

<section class="sezione" aria-labelledby="come-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">Come funziona</p><h2 id="come-titolo">Dal primo contatto all’intervento</h2><p class="sotto">Tre passaggi, nessuna complicazione.</p></div>
    <div class="passi">{passi_html}</div>
    <div class="nota-gratis reveal">{hexicon("check", "menta", "piccolo")}<span>Consulenze e sopralluoghi sono sempre gratuiti e senza impegno.</span></div>
  </div>
</section>

{sezione_certificazioni()}
{sezione_recensioni()}
{banda_cta()}'''
    return documento("index.html", "So.Ge.Pa. | Impresa di pulizie e facility management a Catania",
                     "Impresa di pulizie a Catania: pulizie, trattamenti pavimenti, sanificazioni e disinfestazioni per aziende, condomini e privati. Oltre 35 anni di esperienza, sopralluogo e preventivo gratuiti.",
                     corpo, jsonld=JSONLD_AZIENDA)

def pagina_servizi():
    chips = "".join(f'<a class="chip {c["colore"]}" href="#{c["id"]}">{e(c["nome"])} · {len(c["servizi"])}</a>' for c in CATEGORIE)
    sezioni = ""
    for i, c in enumerate(CATEGORIE):
        cards = "".join(f'''
        <article class="servizio reveal">{hexicon(ic, c["colore"])}<h3>{e(n)}</h3><p>{e(d)}</p>{cta("Richiedi", servizio=n, cls="btn-secondario btn-piccolo", testo_mobile="WhatsApp")}</article>''' for n, ic, d in c["servizi"])
        foto = pic(c["foto"], c["alt"], [640,1000] if c["foto"]!="disinfestazioni" else [780], "(min-width:900px) 440px, 90vw")
        sezioni += f'''
<section class="categoria{" tinta" if i % 2 else ""}" id="{c["id"]}" aria-labelledby="cat-{c["id"]}">
  <div class="contenitore">
    <div class="testa">
      <div class="reveal"><p class="etichetta {c["colore"]}">{len(c["servizi"])} servizi</p><h2 id="cat-{c["id"]}">{e(c["nome"])}</h2><p>{e(c["intro"])}</p></div>
      <div class="foto-hex reveal r2">{foto}</div>
    </div>
    <div class="griglia-servizi">{cards}</div>
  </div>
</section>'''
    galleria = [("facciata", "Pulizia vetrate e facciate", "Operatore che pulisce una grande facciata vetrata al tramonto"),
                ("grondaie", "Pulizia grondaie e tetti", "Idropulitrice su un tetto di tegole"),
                ("piscine", "Pulizie piscine", "Operatore che spazzola il fondo di una piscina"),
                ("fotovoltaico", "Pulizia pannelli fotovoltaici", "Spazzola rotante su pannelli fotovoltaici"),
                ("moquette", "Shampoo rinnovante moquette", "Macchina a estrazione su una moquette")]
    gal = "".join(f'''<figure class="intervento reveal r{(i%4)+1}">{pic(f, a, [640,1000] if f in ("facciata","piscine","fotovoltaico") else ([800] if f=="grondaie" else [900]), "(min-width:1000px) 20vw, 50vw")}<figcaption>{e(t)}</figcaption></figure>''' for i, (f, t, a) in enumerate(galleria))
    corpo = f'''
<section class="hero-pagina" aria-labelledby="pg-titolo">
  <div class="sfondo">{pic("servizi-hero", "", [1000,1800], "100vw", priority=True)}</div>
  <div class="contenitore">
    <nav class="briciole" aria-label="Percorso"><a href="index.html">Home</a><span aria-hidden="true">›</span><span>Servizi</span></nav>
    <p class="etichetta">I nostri servizi</p>
    <h1 id="pg-titolo">{TOT_SERVIZI} servizi per ogni spazio di lavoro e di vita</h1>
    <p class="sotto">Scegli il servizio che ti serve e richiedilo in un tocco: da telefono su WhatsApp, da computer con il modulo che arriva direttamente in azienda.</p>
    <div class="chips">{chips}</div>
  </div>
</section>
<div class="barra-servizi">
  <div class="contenitore">
    <label class="filtro" for="filtro-servizi">{ico("lente")}<span class="sr-only">Cerca un servizio</span><input id="filtro-servizi" type="search" placeholder="Cerca un servizio: vetri, cimici, pavimenti…" autocomplete="off"></label>
    <div class="chips" style="margin:0">{chips}</div>
  </div>
</div>
{sezioni}
<p class="nessuno">Nessun servizio corrisponde alla ricerca. Descrivici il problema: {btn_wa("Scrivici su WhatsApp", cls="btn-wa btn-piccolo solo-mobile")}{cta("Scrivici", cls="btn-primario btn-piccolo", extra="solo-desktop")}</p>
<section class="sezione" aria-labelledby="gal-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">In azione</p><h2 id="gal-titolo">Attrezzature e tecniche per ogni superficie</h2></div>
    <div class="galleria">{gal}</div>
  </div>
</section>
{banda_cta("Non trovi il servizio che cerchi?", "Descrivici il problema: valutiamo insieme la soluzione più adatta, con sopralluogo gratuito.")}'''
    return documento("servizi.html", "Servizi di pulizia, trattamenti e disinfestazioni a Catania | So.Ge.Pa.",
                     f"{TOT_SERVIZI} servizi professionali: pulizie speciali, vetri, pannelli fotovoltaici, trattamenti pavimenti, sanificazioni, derattizzazione e disinfestazioni a Catania e in Sicilia.",
                     corpo, og_img="assets/img/servizi-hero-1800.jpg")

def pagina_chi_siamo():
    valori = [("Lealtà", "Verso tutti: clienti, collaboratori e fornitori. I rapporti sono l’anima della nostra azienda.", "check", "teal"),
              ("Qualità", "Il nostro lavoro di pulizie viene svolto senza mai perdere di vista l’obiettivo: la soddisfazione del cliente.", "cera", "blu"),
              ("Curiosità", "Cerchiamo il meglio dei prodotti offerti dal mercato, individuiamo nuovi bisogni e inventiamo i servizi per soddisfarli.", "lente", "magenta"),
              ("Garanzia", "Garantiamo sulla condotta dei nostri dipendenti e sulla sicurezza durante l’esecuzione dei lavori di pulizia.", "scudo", "navy")]
    valori_html = "".join(f'''<article class="valore reveal r{i+1}">{hexicon(ic, col)}<h3>{e(t)}</h3><p>{e(d)}</p></article>''' for i, (t, d, ic, col) in enumerate(valori))
    superfici = "".join(f"<li>{s}</li>" for s in ["Cotto", "Gres", "Marmo", "Linoleum", "Cemento", "Moquette", "Parquet", "Vetro"])
    corpo = f'''
<section class="hero-pagina" aria-labelledby="pg-titolo">
  <div class="sfondo">{pic("chisiamo-hero", "", [1000,1800], "100vw", priority=True)}</div>
  <div class="contenitore">
    <nav class="briciole" aria-label="Percorso"><a href="index.html">Home</a><span aria-hidden="true">›</span><span>Chi siamo</span></nav>
    <p class="etichetta">Chi siamo</p>
    <h1 id="pg-titolo">Oltre 35 anni di lavoro pulito</h1>
    <p class="sotto">So.Ge.Pa. è un’impresa di pulizie e facility management di San Giovanni La Punta, Catania, che lavora in tutta la Sicilia per aziende, condomini, enti e privati.</p>
  </div>
</section>

<section class="sezione" aria-labelledby="storia-titolo">
  <div class="contenitore">
    <div class="due-colonne">
      <div class="prosa reveal">
        <p class="etichetta">La nostra storia</p>
        <h2 id="storia-titolo">Esperienza che si vede nei dettagli</h2>
        <p>Da oltre 35 anni operiamo nel settore offrendo servizi professionali di pulizia e manutenzione per ambienti civili e industriali. Grazie a un team qualificato, gestiamo anche interventi di facchinaggio e manutenzioni tecniche, garantendo affidabilità, efficienza e soluzioni su misura per ogni esigenza.</p>
        <p>Ci rivolgiamo a <strong>privati, aziende, esercizi commerciali, enti e istituzioni</strong>: dal singolo intervento ai contratti continuativi di facility management. Validi collaboratori sono sempre a disposizione per consulenze e sopralluoghi completamente gratuiti e senza impegno.</p>
        <div class="numeri">
          <div><span class="numero-grande">35+</span><small>anni di attività</small></div>
          <div><span class="numero-grande">{TOT_SERVIZI}</span><small>servizi specialistici</small></div>
          <div><span class="numero-grande">3</span><small>certificazioni</small></div>
          <div><span class="numero-grande">5,0</span><small>valutazione Google</small></div>
        </div>
      </div>
      <div class="foto-tonda reveal r2">{pic("team-uniforme", "Divisa So.Ge.Pa. con il logo sulla manica", [640,1000], "(min-width:900px) 45vw, 100vw")}</div>
    </div>
  </div>
</section>

<section class="sezione tinta" aria-labelledby="mission-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">Mission</p><h2 id="mission-titolo">Un rapporto di fiducia fatto di esperienza, feeling e intuizione</h2><p class="sotto">È ciò che lega la nostra impresa ai suoi clienti: attenzione alle loro esigenze, elemento chiave del nostro lavoro.</p></div>
    <div class="griglia-4">{valori_html}</div>
  </div>
</section>

<section class="sezione" aria-labelledby="tecnica-titolo">
  <div class="contenitore">
    <div class="due-colonne">
      <div class="foto-hex reveal">{pic("facciata", "Operatore che pulisce una grande facciata vetrata", [640,1000], "(min-width:900px) 440px, 90vw")}</div>
      <div class="prosa reveal r2">
        <p class="etichetta">Tecnica</p>
        <h2 id="tecnica-titolo">Tecniche all’avanguardia e prodotti naturali</h2>
        <p>La ditta impiega tecniche molto all’avanguardia e prodotti naturali: sempre efficaci e mai nocivi per l’ambiente o per la salute dell’uomo.</p>
        <p>Trattiamo superfici di ogni natura, manualmente o con macchinari, con prodotti certificati e specifici, in grado di agire nel migliore dei modi su ciascun materiale:</p>
        <ul class="superfici">{superfici}</ul>
      </div>
    </div>
    <div class="citazione reveal mt-3">
      <span class="virgolette" aria-hidden="true">“</span>
      <blockquote>I rapporti con i nostri clienti sono basati su un rapporto di fiducia fatto di esperienza, feeling e intuizione.<cite>Daiko Morello, amministratore So.Ge.Pa.</cite></blockquote>
    </div>
  </div>
</section>

{sezione_certificazioni()}
{banda_cta("Vuoi conoscerci di persona?", "Chiedi un sopralluogo gratuito: veniamo a vedere i tuoi spazi e ti proponiamo la soluzione più adatta.")}'''
    return documento("chi-siamo.html", "Chi siamo | So.Ge.Pa. Facility Management, Catania",
                     "Oltre 35 anni di pulizie professionali, trattamenti e disinfestazioni in Sicilia. Mission, valori e tecniche di So.Ge.Pa., impresa di San Giovanni La Punta (Catania).",
                     corpo, og_img="assets/img/chisiamo-hero-1800.jpg")

def pagina_parlano():
    loghi = "".join(f'<div class="logo-card reveal"><img src="assets/clienti/{f}.png" alt="" loading="lazy"><span>{e(n)}</span></div>' for f, n in CLIENTI)
    corpo = f'''
<section class="hero-pagina semplice" aria-labelledby="pg-titolo">
  <div class="contenitore">
    <nav class="briciole" aria-label="Percorso"><a href="index.html">Home</a><span aria-hidden="true">›</span><span>Parlano di noi</span></nav>
    <p class="etichetta">Parlano di noi</p>
    <h1 id="pg-titolo">Interviste, recensioni, clienti e partner</h1>
    <p class="sotto">Leggi e scopri il nostro mondo, lasciati consigliare da chi ha già scelto i nostri servizi: i partner strategici, le sponsorizzazioni e gli articoli che parlano della nostra azienda.</p>
  </div>
</section>

<section class="sezione" aria-labelledby="stampa-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">Sulla stampa</p><h2 id="stampa-titolo">Siamo stati citati in molte testate e non solo</h2></div>
    <div class="stampa">
      <button class="collage reveal" type="button" data-luce="assets/img/stampa-1600.jpg" aria-label="Ingrandisci la rassegna stampa">{pic("stampa", "Rassegna stampa So.Ge.Pa.: copertine e articoli di Paesi Etnei Oggi, Sicilia Magazine e ANSA", [1000,1600], "(min-width:900px) 60vw, 100vw")}<span class="lente">{ico("lente")} Ingrandisci</span></button>
      <article class="articolo reveal r2">
        <span class="fonte">Paesi Etnei Oggi · 8 luglio 2021</span>
        <h3>«Igiene e pulizia la nostra mission». Parola di Daiko Morello</h3>
        <p>Un’intervista all’amministratore di So.Ge.Pa. su oltre 35 anni di attività, i servizi di sanificazione, derattizzazione e trattamento dei pavimenti e il rapporto di fiducia con i clienti.</p>
        <a class="btn btn-secondario btn-piccolo" href="https://www.paesietneioggi.it/promotions/sogepa-igiene-e-pulizia-la-nostra-mission-parola-di-daiko-morello/" target="_blank" rel="noopener">Leggi l’articolo {ico("freccia")}</a>
        <div class="testate"><span>Paesi Etnei Oggi</span><span>Sicilia Magazine</span><span>ANSA</span></div>
      </article>
    </div>
  </div>
</section>

<section class="sezione tinta" aria-labelledby="clienti-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">Clienti e partner</p><h2 id="clienti-titolo">Hanno lavorato con noi</h2><p class="sotto">Grandi aziende, catene, enti e strutture ricettive che ci hanno affidato i loro spazi.</p></div>
    <div class="griglia-loghi">{loghi}</div>
  </div>
</section>

{sezione_recensioni().replace('class="sezione tinta"', 'class="sezione"')}
{banda_cta()}
<dialog class="luce" id="luce" aria-label="Rassegna stampa ingrandita"><img src="" alt="Rassegna stampa So.Ge.Pa."><button class="chiudi" type="button" aria-label="Chiudi">{ico("x")}</button></dialog>'''
    return documento("parlano-di-noi.html", "Parlano di noi: stampa, clienti e recensioni | So.Ge.Pa.",
                     "Rassegna stampa, interviste, clienti e partner di So.Ge.Pa.: Benetton, Geox, Sheraton, Regione Siciliana, Save the Children e molti altri. Recensioni 5,0 su Google.",
                     corpo, og_img="assets/img/stampa-1600.jpg")

def pagina_contatti():
    corpo = f'''
<section class="hero-pagina" aria-labelledby="pg-titolo">
  <div class="sfondo">{pic("contatti-hero", "", [1000,1800], "100vw", priority=True)}</div>
  <div class="contenitore">
    <nav class="briciole" aria-label="Percorso"><a href="index.html">Home</a><span aria-hidden="true">›</span><span>Contatti</span></nav>
    <p class="etichetta">Contatti</p>
    <h1 id="pg-titolo">Chiedi un preventivo gratuito</h1>
    <p class="sotto">Da telefono scrivici su WhatsApp, da computer compila il modulo: la richiesta arriva direttamente in azienda. Sopralluogo e consulenza sono gratuiti e senza impegno.</p>
  </div>
</section>

<section class="sezione" aria-label="Recapiti e modulo di richiesta">
  <div class="contenitore">
    <div class="wa-card solo-mobile">
      <h2>Scrivici su WhatsApp</h2>
      <p>Ti rispondiamo dal numero aziendale {AZIENDA["cell"]}. Se preferisci, chiamaci.</p>
      <div class="azioni">{btn_wa("Apri WhatsApp")}{btn_tel()}</div>
    </div>
    <div class="contatti-griglia">
      <div class="reveal">
        <p class="etichetta">Recapiti</p>
        <h2>Siamo a San Giovanni La Punta, operiamo in tutta la Sicilia</h2>
        <div class="recapito">{hexicon("tel", "teal", "piccolo")}<div><small>Telefono</small><a href="tel:{AZIENDA["tel_fisso_link"]}">{AZIENDA["tel_fisso"]}</a></div></div>
        <div class="recapito">{hexicon("wa", "blu", "piccolo")}<div><small>Cellulare e WhatsApp</small><a href="https://wa.me/{AZIENDA["whatsapp"]}" data-wa>{AZIENDA["cell"]}</a><span class="sub">Scrivici anche su WhatsApp</span></div></div>
        <div class="recapito">{hexicon("mail", "magenta", "piccolo")}<div><small>Email</small><a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a></div></div>
        <div class="recapito">{hexicon("pin", "navy", "piccolo")}<div><small>Sede</small><strong>{e(AZIENDA["indirizzo"])}, {AZIENDA["cap"]} {e(AZIENDA["citta"])} ({AZIENDA["provincia"]})</strong><span class="sub">{e(AZIENDA["ragione_sociale"])} · P. IVA {AZIENDA["piva"]}</span></div></div>
      </div>
      <div class="modulo reveal r2" id="richiesta">
        <h2 id="c-titolo">Richiedi un servizio o un preventivo</h2>
        <p class="intro-modulo">Compila il modulo: la richiesta arriva direttamente alla nostra email e ti ricontattiamo per il sopralluogo gratuito.</p>
        {modulo("c", in_pagina=True)}
      </div>
    </div>
  </div>
</section>

<section class="sezione tinta" aria-labelledby="mappa-titolo">
  <div class="contenitore">
    <div class="intesta reveal"><p class="etichetta">Dove siamo</p><h2 id="mappa-titolo">La nostra sede</h2></div>
    <div class="mappa reveal" data-mappa="{AZIENDA["mappa_embed"]}">
      <span class="deco-hex" aria-hidden="true"></span>
      <div>{hexicon("pin", "navy")}<p class="mt-1">{e(AZIENDA["indirizzo"])}, {AZIENDA["cap"]} {e(AZIENDA["citta"])} ({AZIENDA["provincia"]}). La mappa di Google si carica solo se lo desideri: può impostare cookie di terze parti.</p><button class="btn btn-primario" type="button">{ico("pin")}<span>Mostra la mappa</span></button></div>
    </div>
  </div>
</section>'''
    return documento("contatti.html", "Contatti e preventivo gratuito | So.Ge.Pa. Catania",
                     "Contatta So.Ge.Pa.: telefono 095 525642, WhatsApp 392 995 7941, modulo di richiesta servizi. Sede a San Giovanni La Punta (Catania), interventi in tutta la Sicilia.",
                     corpo, con_modale=False, jsonld=JSONLD_AZIENDA, og_img="assets/img/contatti-hero-1800.jpg")

def pagina_testo(file, titolo, descrizione, h1, contenuto):
    corpo = f'''
<section class="hero-pagina semplice" aria-labelledby="pg-titolo">
  <div class="contenitore">
    <nav class="briciole" aria-label="Percorso"><a href="index.html">Home</a><span aria-hidden="true">›</span><span>{e(h1)}</span></nav>
    <h1 id="pg-titolo">{e(h1)}</h1>
  </div>
</section>
<section class="sezione pagina-testo"><div class="contenitore">{contenuto}</div></section>'''
    return documento(file, titolo, descrizione, corpo)

PRIVACY = f'''
<p><em>Ultimo aggiornamento: {datetime.date.today().strftime("%d/%m/%Y")}</em></p>
<p>La presente informativa descrive come vengono trattati i dati personali dei visitatori di questo sito, ai sensi del Regolamento (UE) 2016/679 (GDPR) e del D.Lgs. 196/2003 e successive modifiche.</p>
<h2>Titolare del trattamento</h2>
<p>{e(AZIENDA["ragione_sociale"])}, {e(AZIENDA["indirizzo"])}, {AZIENDA["cap"]} {e(AZIENDA["citta"])} ({AZIENDA["provincia"]}), P. IVA {AZIENDA["piva"]}, email <a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a>, telefono {AZIENDA["tel_fisso"]}.</p>
<h2>Quali dati trattiamo</h2>
<ul>
<li><strong>Dati forniti volontariamente</strong> tramite il modulo di richiesta: nome, cognome, email, telefono, servizio di interesse e contenuto del messaggio.</li>
<li><strong>Dati di navigazione</strong>: il servizio di hosting può registrare in modo automatico dati tecnici (indirizzo IP, tipo di browser, pagine visitate) per finalità di sicurezza e statistiche aggregate.</li>
<li><strong>Contatto via WhatsApp o telefono</strong>: se scegli di contattarci con questi canali, i dati sono trattati secondo le condizioni dei rispettivi fornitori e utilizzati da noi solo per rispondere alla richiesta.</li>
</ul>
<h2>Finalità e base giuridica</h2>
<p>I dati sono trattati per rispondere alle richieste di informazioni e di preventivo e per organizzare il sopralluogo (esecuzione di misure precontrattuali richieste dall’interessato, art. 6, par. 1, lett. b GDPR) e, ove necessario, per adempiere a obblighi di legge (lett. c). Non svolgiamo attività di marketing né di profilazione sulla base dei dati raccolti dal sito.</p>
<h2>Modalità e conservazione</h2>
<p>Il trattamento avviene con strumenti informatici, adottando misure adeguate di sicurezza. I dati delle richieste sono conservati per il tempo necessario a gestirle e, in caso di successivo rapporto contrattuale, per la durata prevista dagli obblighi civilistici e fiscali.</p>
<h2>Destinatari</h2>
<ul>
<li>Il modulo del sito è inviato tramite il servizio <a href="https://formsubmit.co" target="_blank" rel="noopener">FormSubmit</a>, che recapita il messaggio alla nostra casella email e agisce come fornitore tecnico.</li>
<li>Il sito è pubblicato su un servizio di hosting di terze parti che tratta i dati tecnici di navigazione.</li>
<li>La mappa della sede si carica solo su tua richiesta e utilizza servizi Google (vedi <a href="cookie.html">informativa sui cookie</a>).</li>
</ul>
<p>Alcuni fornitori possono avere sede fuori dall’Unione europea: in tal caso il trasferimento avviene sulla base di decisioni di adeguatezza o di garanzie appropriate ai sensi degli artt. 44 e seguenti del GDPR. I dati non sono comunicati ad altri soggetti né diffusi.</p>
<h2>I tuoi diritti</h2>
<p>Puoi chiedere in ogni momento l’accesso ai dati, la rettifica, la cancellazione, la limitazione del trattamento, la portabilità e opporti al trattamento (artt. 15–22 GDPR) scrivendo a <a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a>. Hai inoltre il diritto di proporre reclamo al Garante per la protezione dei dati personali (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">www.garanteprivacy.it</a>).</p>
<h2>Minori</h2>
<p>Il sito non è destinato a minori di 14 anni e non raccoglie consapevolmente i loro dati.</p>
<h2>Aggiornamenti</h2>
<p>La presente informativa può essere aggiornata: la versione in vigore è sempre quella pubblicata su questa pagina.</p>'''

COOKIE = f'''
<p><em>Ultimo aggiornamento: {datetime.date.today().strftime("%d/%m/%Y")}</em></p>
<div class="avviso"><p><strong>In breve:</strong> questo sito non utilizza cookie di profilazione né strumenti di analisi statistica. Nessun cookie viene impostato durante la navigazione, salvo quanto descritto qui sotto per la mappa di Google, che si carica solo su tua richiesta.</p></div>
<h2>Cosa sono i cookie</h2>
<p>I cookie sono piccoli file di testo che i siti inviano al dispositivo dell’utente, dove vengono memorizzati per essere ritrasmessi alla visita successiva. Possono essere tecnici (necessari al funzionamento) oppure di profilazione (usati per tracciare l’utente e proporre pubblicità mirata).</p>
<h2>Cookie utilizzati da questo sito</h2>
<ul>
<li><strong>Cookie tecnici propri:</strong> nessuno. Il sito è composto da pagine statiche e non richiede autenticazione.</li>
<li><strong>Cookie di analisi o profilazione:</strong> nessuno.</li>
</ul>
<h2>Servizi di terze parti</h2>
<ul>
<li><strong>Google Maps</strong>: nella pagina Contatti la mappa della sede viene caricata soltanto dopo il click sul pulsante «Mostra la mappa». Da quel momento Google può impostare cookie e trattare dati secondo la propria <a href="https://policies.google.com/privacy?hl=it" target="_blank" rel="noopener">informativa sulla privacy</a>.</li>
<li><strong>Google Fonts</strong>: i caratteri tipografici sono caricati dai server di Google; il browser trasmette a Google i dati tecnici necessari (tra cui l’indirizzo IP). Google dichiara di non utilizzare cookie per questo servizio.</li>
<li><strong>WhatsApp</strong>: i pulsanti WhatsApp sono semplici link; nessun dato viene trasmesso finché non decidi di aprire la conversazione.</li>
</ul>
<h2>Come gestire i cookie</h2>
<p>Puoi bloccare o cancellare i cookie dalle impostazioni del tuo browser (Chrome, Safari, Firefox, Edge). La disattivazione dei cookie di terze parti non compromette la navigazione di questo sito.</p>
<p>Per ogni informazione sul trattamento dei dati consulta l’<a href="privacy.html">informativa sulla privacy</a> o scrivi a <a href="mailto:{AZIENDA["email"]}">{AZIENDA["email"]}</a>.</p>'''

def pagina_grazie():
    corpo = f'''
<section class="pagina-errore"><div class="contenitore">
  <img class="marchio-grande" src="assets/logo/marchio-colore.png" alt="" width="600" height="519">
  <p class="etichetta" style="justify-content:center">Richiesta ricevuta</p>
  <h1>Grazie, ti ricontattiamo presto</h1>
  <p class="sotto" style="color:var(--ink-2);max-width:40rem;margin:0 auto 1.5rem">La tua richiesta è arrivata in azienda. Ti risponderemo per fissare il sopralluogo gratuito. Se hai urgenza chiama il <a href="tel:{AZIENDA["tel_fisso_link"]}">{AZIENDA["tel_fisso"]}</a>.</p>
  <a class="btn btn-primario" href="index.html">Torna alla home</a>
</div></section>'''
    return documento("grazie.html", "Richiesta ricevuta | So.Ge.Pa.", "Grazie: la tua richiesta è arrivata a So.Ge.Pa.", corpo, con_modale=False)

def pagina_404():
    corpo = f'''
<section class="pagina-errore"><div class="contenitore">
  <img class="marchio-grande" src="assets/logo/marchio-colore.png" alt="" width="600" height="519">
  <p class="etichetta" style="justify-content:center">Errore 404</p>
  <h1>Pagina non trovata</h1>
  <p class="sotto" style="color:var(--ink-2);max-width:40rem;margin:0 auto 1.5rem">La pagina che cerchi non esiste o è stata spostata. Torna alla home oppure sfoglia i servizi.</p>
  <div class="azioni" style="justify-content:center"><a class="btn btn-primario" href="index.html">Torna alla home</a><a class="btn btn-secondario" href="servizi.html">Vedi i servizi</a></div>
</div></section>'''
    return documento("404.html", "Pagina non trovata | So.Ge.Pa.", "La pagina richiesta non esiste.", corpo, con_modale=False)

# ---------------------------------------------------------------- scrittura
PAGINE = {
    "index.html": pagina_home,
    "servizi.html": pagina_servizi,
    "chi-siamo.html": pagina_chi_siamo,
    "parlano-di-noi.html": pagina_parlano,
    "contatti.html": pagina_contatti,
    "privacy.html": lambda: pagina_testo("privacy.html", "Informativa sulla privacy | So.Ge.Pa.", "Come So.Ge.Pa. tratta i dati personali dei visitatori del sito e di chi invia una richiesta.", "Informativa sulla privacy", PRIVACY),
    "cookie.html": lambda: pagina_testo("cookie.html", "Informativa sui cookie | So.Ge.Pa.", "Quali cookie e servizi di terze parti utilizza il sito So.Ge.Pa.", "Informativa sui cookie", COOKIE),
    "grazie.html": pagina_grazie,
    "404.html": pagina_404,
}

def main():
    for nome, fn in PAGINE.items():
        with open(os.path.join(ROOT, nome), "w", encoding="utf-8") as f:
            f.write(fn())
        print("scritto", nome)
    pubbliche = ["index.html", "servizi.html", "chi-siamo.html", "parlano-di-noi.html", "contatti.html", "privacy.html", "cookie.html"]
    urls = "".join(f"<url><loc>{BASE}/{'' if p=='index.html' else p}</loc><lastmod>{OGGI}</lastmod></url>" for p in pubbliche)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /grazie.html\nSitemap: {BASE}/sitemap.xml\n")
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    print("scritti sitemap.xml, robots.txt, .nojekyll")

if __name__ == "__main__":
    main()
