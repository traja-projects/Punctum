#!/usr/bin/env python3
"""Static-site generator for the Punctum website.

Shared templates + per-language content -> plain static HTML under
/{de,en,es,fr}/. No build step is needed to SERVE the site (GitHub Pages
serves the emitted files directly); run this only to regenerate after
editing content or templates:

    python3 _build/generate.py

When the app goes live on the App Store, set APP_STORE_URL below to the
real product URL: the coming-soon badge then becomes a real link.
"""
import os

BASE = "https://traja-projects.github.io/Punctum/"
LANGS = ["de", "en", "es", "fr"]
# ("page key", "file name"); "" means the folder index.
PAGES = [("index", ""), ("privacy", "privacy.html"), ("terms", "terms.html"),
         ("imprint", "imprint.html"), ("support", "support.html")]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Flip to the real App Store URL on launch (None = coming-soon badge).
APP_STORE_URL = None

# Apple logo (recognisable silhouette).
APPLE = ('<svg class="badge__apple" width="22" height="22" viewBox="0 0 24 24" '
         'fill="#fff" aria-hidden="true"><path d="M16.36 1.43c0 1.14-.42 2.2-1.12 '
         '2.98-.85.94-2.22 1.66-3.36 1.57-.14-1.1.43-2.27 1.1-3 .76-.84 2.07-1.46 '
         '3.13-1.5.02.22.03.43.05.65zM20.5 17.2c-.55 1.27-.82 1.83-1.53 2.95-.99 '
         '1.56-2.39 3.5-4.12 3.51-1.54.02-1.93-1-4.02-.99-2.09.01-2.52 1.01-4.06.99'
         '-1.73-.01-3.04-1.77-4.03-3.32C-.38 16.6-.74 11.9 1.24 9.4c1.18-1.5 '
         '2.78-2.38 4.46-2.38 1.71 0 2.79 1 4.2 1 1.36 0 2.2-1 4.18-1 1.5 0 3.08.82 '
         '4.21 2.23-3.7 2.03-3.09 7.31 1.21 7.95z"/></svg>')

ICO = {
 "privacy": ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFCE6B" '
             'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M12 3l7 3v5c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z"/></svg>'),
 "purchase": ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFCE6B" '
              'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M3 11V4h7l10 10-7 7z"/><circle cx="7" cy="8" r="1.3"/></svg>'),
 "quiet": ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFCE6B" '
           'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           '<path d="M20 14.5A8 8 0 1 1 9.5 4 6.5 6.5 0 0 0 20 14.5z"/></svg>'),
}

# ---------------------------------------------------------------- templates
SHELL = """<!DOCTYPE html>
<html lang="{htmllang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Punctum">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{root}assets/favicon.png">
<link rel="apple-touch-icon" href="{root}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<div class="cosmos" aria-hidden="true"><div class="cosmos__blob cosmos__blob--p"></div><div class="cosmos__blob cosmos__blob--t"></div><canvas id="starfield"></canvas></div>
{header}
{main}
{footer}
<script src="{root}cosmos.js" defer></script>
</body>
</html>
"""

HEADER = """<header class="site-header"><div class="site-header__in">
<a class="brand" href="index.html">Punctum</a>
<nav class="nav" aria-label="{nav_aria}">
<div class="nav__links"><a href="index.html#lenses">{nav_features}</a><a href="support.html">{nav_support}</a></div>
<div class="langs">{langswitch}</div>
</nav>
</div></header>"""

FOOTER = """<footer class="site-footer">
<div class="site-footer__in">
<div><a class="brand" href="index.html">Punctum</a><p class="site-footer__tag">{foot_tag}</p></div>
<nav class="footer-nav" aria-label="{footnav_aria}"><a href="privacy.html">{foot_privacy}</a><a href="terms.html">{foot_terms}</a><a href="imprint.html">{foot_imprint}</a><a href="support.html">{foot_support}</a></nav>
</div>
<div class="site-footer__base"><span>{foot_rights}</span><a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a><div class="langs">{langswitch}</div></div>
</footer>"""

LANDING = """<main>
<section class="hero">
<div class="hero__grid">
<div class="hero__copy">
<p class="eyebrow">{eyebrow}</p>
<h1 class="hero__title">{hero_title}</h1>
<p class="hero__sub">{hero_sub}</p>
<div class="hero__cta">{badge}<a class="ghost-link" href="#lenses">{hero_ghost}</a></div>
<p class="hero__note">{hero_note}</p>
</div>
<div class="device"><div class="device__glow"></div><img class="device__img" src="{root}assets/screens/{code}_board.jpg" width="600" height="1303" alt="{alt_board}" loading="eager" fetchpriority="high"></div>
</div>
</section>

<section class="section concept" id="concept">
<div class="wrap">
<p class="eyebrow">{concept_eyebrow}</p>
<h2 class="section__title">{concept_title}</h2>
<p class="section__lead">{concept_lead}</p>
<div class="legend">
<span class="legend__item"><span class="dot dot--past"></span>{legend_past}</span>
<span class="legend__item"><span class="dot dot--now"></span>{legend_now}</span>
<span class="legend__item"><span class="dot dot--future"></span>{legend_future}</span>
</div>
</div>
</section>

<section class="section lenses" id="lenses">
<div class="wrap center"><p class="eyebrow">{lenses_eyebrow}</p><h2 class="section__title">{lenses_title}</h2><p class="section__lead">{lenses_lead}</p></div>
<div class="wrap"><div class="cards">
<article class="lens"><h3>{lens1_h}</h3><p>{lens1_p}</p><img class="lens__shot" src="{root}assets/screens/{code}_phases.jpg" width="600" height="1303" alt="{lens1_h}" loading="lazy"></article>
<article class="lens"><h3>{lens2_h}</h3><p>{lens2_p}</p><img class="lens__shot" src="{root}assets/screens/{code}_life.jpg" width="600" height="1303" alt="{lens2_h}" loading="lazy"></article>
<article class="lens"><h3>{lens3_h}</h3><p>{lens3_p}</p><img class="lens__shot" src="{root}assets/screens/{code}_thisyear.jpg" width="600" height="1303" alt="{lens3_h}" loading="lazy"></article>
</div></div>
</section>

<section class="section" id="values">
<div class="wrap center"><p class="eyebrow">{values_eyebrow}</p><h2 class="section__title">{values_title}</h2></div>
<div class="wrap"><div class="values">
<div class="value"><div class="value__ico">{ico_privacy}</div><h3>{val1_h}</h3><p>{val1_p}</p></div>
<div class="value"><div class="value__ico">{ico_purchase}</div><h3>{val2_h}</h3><p>{val2_p}</p></div>
<div class="value"><div class="value__ico">{ico_quiet}</div><h3>{val3_h}</h3><p>{val3_p}</p></div>
</div></div>
</section>

<section class="section closing"><div class="wrap">
<p class="closing__quote">{closing_quote}</p>
<div class="hero__cta cta--center">{badge}</div>
</div></section>
</main>"""

LEGAL = """<main><div class="wrap">
<div class="page-head"><h1>{h1}</h1>{lede}</div>
<div class="prose">
{body}
<a class="back" href="index.html">{back}</a>
</div>
</div></main>"""

# ---------------------------------------------------------------- content
C = {
"de": {
 "htmllang":"de", "nav_aria":"Navigation", "footnav_aria":"Rechtliches",
 "nav_features":"Funktionen", "nav_support":"Support",
 "eyebrow":"Dein Leben als Punkt",
 "hero_title":"Jeder Punkt war<br>einmal <em>das Jetzt.</em>",
 "hero_sub":"Dein Leben als Brett aus Punkten. Die meisten sind schon gefüllt. Punctum zeigt dir ruhig, wie viele bleiben — und macht aus dem Gedanken an das Ende einen Kompass.",
 "hero_ghost":"So funktioniert’s",
 "hero_note":"Einmaliger Kauf · keine Werbung · kein Tracking",
 "badge_small":"Bald verfügbar im", "badge_store":"App Store", "badge_tag":"Bald",
 "alt_board":"Punctum-Brett: die Wochen, die dir bleiben, als Gitter aus Punkten",
 "concept_eyebrow":"Das Brett",
 "concept_title":"Die meisten deiner Punkte sind schon gefüllt.",
 "concept_lead":"Punctum zeigt dir dein ganzes Leben als ein Brett aus Punkten. Was hinter dir liegt, ist gefüllt. Was bleibt, ist offen. Ein einziger, leuchtender Punkt ist das Jetzt — der Moment, in dem du gerade liest.",
 "legend_past":"Gelebt", "legend_now":"Jetzt", "legend_future":"Was bleibt",
 "lenses_eyebrow":"Drei Linsen", "lenses_title":"Wähle, wie nah du hinsiehst.",
 "lenses_lead":"Wochen, Monate oder Jahre — und drei Blickwinkel auf dieselbe Zeit.",
 "lens1_h":"Lebensphasen", "lens1_p":"Deine Phasen als Milchstraße — was war, was ist, was kommt.",
 "lens2_h":"Dein ganzes Leben", "lens2_p":"Jahr für Jahr, auf einen Blick.",
 "lens3_h":"Dieses Jahr", "lens3_p":"Näher heran — die Wochen dieses einen Jahres.",
 "values_eyebrow":"Ruhig und privat", "values_title":"Deine Zeit gehört dir. Deine Daten auch.",
 "val1_h":"Alles bleibt lokal", "val1_p":"Kein Server, keine Cloud, kein Tracking, kein Konto. Nichts verlässt dein Gerät.",
 "val2_h":"Einmaliger Kauf", "val2_p":"Kein Abo, keine In-App-Käufe, keine versteckten Kosten. Einmal gekauft, gehört es dir.",
 "val3_h":"Still, nicht laut", "val3_p":"Heimbildschirm-Widgets erden dich — ohne eine einzige Benachrichtigung.",
 "closing_quote":"Jeder Punkt war einmal das Jetzt.",
 "foot_tag":"Punctum — lateinisch für den Punkt und den Augenblick.",
 "foot_privacy":"Datenschutz", "foot_terms":"Nutzungsbedingungen", "foot_imprint":"Impressum", "foot_support":"Support",
 "foot_rights":"© 2026 Bao Anh Tran",
 "back":"← Zur Startseite",
 "meta_desc":"Punctum zeigt dein Leben als Brett aus Punkten — ruhig, lokal, ohne Tracking. Wähle Wochen, Monate oder Jahre und finde das Jetzt.",
 "priv_lede":"Deine Zeit gehört dir. Deine Daten auch.",
 "sup_lede":"Eine Frage, ein Problem oder eine Idee? Schreib mir — ich antworte persönlich.",
 "body_privacy":'''<p class="stand">Stand: Juni 2026 · gilt für die App Punctum (iOS &amp; Android).</p>
<h2>Was die App speichert</h2>
<p>Geburtsdatum, Lebenserwartung, Anzeigeeinstellung — lokal, auf diesem Gerät. Nichts davon verlässt es. Kein Server. Keine Cloud. Kein Tracking. Gespeichert wird über die geräteeigene Schlüssel-Wert-Ablage. Der Anbieter hat darauf zu keinem Zeitpunkt Zugriff.</p>
<h2>Bewegungssensor</h2>
<p>Für den dezenten Parallax-Effekt liest die App kurzzeitig den Beschleunigungssensor. Die Werte werden nicht gespeichert und nirgends übertragen.</p>
<h2>Widgets (optional)</h2>
<p>Die Heimbildschirm-Widgets werden täglich im Hintergrund aktualisiert — ausschließlich aus deinen lokal gespeicherten Angaben. Keine Netzwerkverbindung, keine Benachrichtigungen.</p>
<h2>Deine Daten löschen</h2>
<p>Einstellungen → „Von vorn beginnen“. Oder die App deinstallieren. Dann sind alle Angaben unwiderruflich weg.</p>
<h2>App-Store-Anbieter</h2>
<p>Apple und Google verarbeiten beim Download Daten in eigener Verantwortung, unabhängig von Punctum.</p>
<h2>Rechtsgrundlage</h2>
<p>Da Punctum keine personenbezogenen Daten verarbeitet, ist eine Rechtsgrundlage nach Art. 6 DSGVO nicht erforderlich. Diese Erklärung dient der Transparenz.</p>
<h2>Deine Rechte</h2>
<p>Auskunft, Berichtigung, Löschung, Einschränkung, Portabilität, Widerspruch (Art. 15–21 DSGVO) sowie Beschwerderecht bei einer Aufsichtsbehörde (Art. 77 DSGVO). In der Praxis: lokal löschen (s. o.) oder den Verantwortlichen kontaktieren.</p>
<h2>Verantwortlicher</h2>
<p>Bao Anh Tran · Friedenstr. 61 · 90409 Nürnberg · Deutschland<br>E-Mail: <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>''',
 "body_terms":'''<p class="stand">Stand: Juni 2026</p>
<h2>1. Geltungsbereich</h2>
<p>Diese Nutzungsbedingungen gelten für die App „Punctum“ (nachfolgend „App“), bereitgestellt von Bao Anh Tran (Kontaktdaten siehe <a href="imprint.html">Impressum</a>). Mit dem Download und der Nutzung der App stimmst du diesen Bedingungen zu.</p>
<h2>2. Was die App ist</h2>
<p>Punctum ist eine App zur Reflexion über die eigene Lebenszeit. Sie stellt deine Lebenszeit als Feld aus Punkten dar und funktioniert vollständig lokal auf deinem Gerät.</p>
<h2>3. Kauf und Preis</h2>
<p>Punctum ist eine kostenpflichtige App: einmaliger Kauf, kein Abonnement, keine In-App-Käufe. Kauf, Abwicklung und etwaige Erstattungen erfolgen ausschließlich über den jeweiligen App-Store (Apple App Store bzw. Google Play) nach deren Bedingungen. Der Anbieter wickelt keine Zahlungen direkt ab.</p>
<h2>4. Nutzungsrecht</h2>
<p>Du erhältst ein einfaches, nicht übertragbares Recht, die App für private Zwecke auf den von dir kontrollierten Geräten zu nutzen. Reverse Engineering, Dekompilierung oder Weiterverbreitung sind nur im gesetzlich zwingend zulässigen Rahmen gestattet.</p>
<h2>5. Wichtiger Hinweis — keine medizinische Vorhersage</h2>
<p>Die dargestellte Lebenserwartung und die daraus berechnete „verbleibende Zeit“ sind eine rein statistische, beispielhafte Veranschaulichung auf Grundlage der von dir eingegebenen Werte. Sie sind ausdrücklich <strong>keine</strong> medizinische Vorhersage, keine Diagnose und keine Gesundheits- oder Behandlungsempfehlung. Punctum ist kein Medizinprodukt im Sinne der Verordnung (EU) 2017/745. Triff keine gesundheitlichen Entscheidungen allein auf Grundlage der angezeigten Werte.</p>
<h2>6. Haftung</h2>
<p>Die App wird mit größtmöglicher Sorgfalt bereitgestellt. Der Anbieter haftet unbeschränkt bei Vorsatz und grober Fahrlässigkeit sowie bei der Verletzung von Leben, Körper oder Gesundheit. Bei leicht fahrlässiger Verletzung wesentlicher Vertragspflichten ist die Haftung auf den vertragstypischen, vorhersehbaren Schaden begrenzt. Im Übrigen ist die Haftung ausgeschlossen. Die Haftung nach dem Produkthaftungsgesetz bleibt unberührt.</p>
<h2>7. Verfügbarkeit und Änderungen</h2>
<p>Der Anbieter darf die App weiterentwickeln, ändern oder den Betrieb einstellen. Diese Bedingungen können angepasst werden; maßgeblich ist die zum Zeitpunkt der Nutzung veröffentlichte Fassung.</p>
<h2>8. Anwendbares Recht</h2>
<p>Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts. Zwingende verbraucherschützende Vorschriften deines Wohnsitzstaates bleiben unberührt.</p>
<h2>9. Kontakt</h2>
<p>Anbieter und verantwortlicher Ansprechpartner: siehe <a href="imprint.html">Impressum</a>.</p>''',
 "body_imprint":'''<p class="stand">Angaben gemäß § 5 DDG (Digitale-Dienste-Gesetz)</p>
<address>Bao Anh Tran
Friedenstr. 61
90409 Nürnberg
Deutschland</address>
<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>
<h2>Verantwortlich für den Inhalt</h2>
<p>Bao Anh Tran, Anschrift wie oben</p>
<p class="note">Plattform der EU-Kommission zur Online-Streitbeilegung: <a href="https://ec.europa.eu/consumers/odr/">https://ec.europa.eu/consumers/odr/</a>. Wir sind nicht verpflichtet und nicht bereit, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>''',
 "body_support":'''<a class="mail" href="mailto:traja.projects@gmail.com?subject=Punctum%20Support">traja.projects@gmail.com</a>
<h2>Häufige Fragen</h2>
<p><strong>Wie lösche ich meine Daten?</strong><br>In der App: Einstellungen → „Von vorn beginnen“. Oder die App deinstallieren. Alles wird unwiderruflich lokal gelöscht.</p>
<p><strong>Gibt es ein Abo oder versteckte Kosten?</strong><br>Nein. Punctum ist ein einmaliger Kauf — kein Abo, kein Konto, keine In-App-Käufe.</p>
<p><strong>Neues Gerät — muss ich erneut zahlen?</strong><br>Nein. Lade die App mit derselben Apple-ID bzw. demselben Google-Konto kostenlos erneut.</p>
<p><strong>Werden meine Daten gespeichert?</strong><br>Nur lokal auf deinem Gerät. Kein Server, keine Cloud, kein Tracking. Details in der <a href="privacy.html">Datenschutzerklärung</a>.</p>
<p><strong>Welche Sprachen gibt es?</strong><br>Deutsch, Englisch, Spanisch und Französisch.</p>''',
},

"en": {
 "htmllang":"en", "nav_aria":"Navigation", "footnav_aria":"Legal",
 "nav_features":"Features", "nav_support":"Support",
 "eyebrow":"Your life as a dot",
 "hero_title":"Every dot was<br>once <em>the now.</em>",
 "hero_sub":"Your life as a board of dots. Most are already filled. Punctum shows you, calmly, how many remain — and turns the thought of the end into a compass for the present.",
 "hero_ghost":"See how it works",
 "hero_note":"One-time purchase · no ads · no tracking",
 "badge_small":"Coming soon to the", "badge_store":"App Store", "badge_tag":"Soon",
 "alt_board":"Punctum board: the weeks you have left, as a grid of dots",
 "concept_eyebrow":"The board",
 "concept_title":"Most of your dots are already filled.",
 "concept_lead":"Punctum shows your whole life as a board of dots. What is behind you is filled. What remains is open. And one bright dot is the now — the moment you are reading this.",
 "legend_past":"Lived", "legend_now":"Now", "legend_future":"What remains",
 "lenses_eyebrow":"Three lenses", "lenses_title":"Choose how close you look.",
 "lenses_lead":"Weeks, months or years — and three ways to see the same time.",
 "lens1_h":"Life phases", "lens1_p":"Your phases as a Milky Way — what was, what is, what comes.",
 "lens2_h":"Your whole life", "lens2_p":"Year by year, at a glance.",
 "lens3_h":"This year", "lens3_p":"Closer in — the weeks of this one year.",
 "values_eyebrow":"Calm and private", "values_title":"Your time is yours. So is your data.",
 "val1_h":"Everything stays local", "val1_p":"No server, no cloud, no tracking, no account. Nothing leaves your device.",
 "val2_h":"One-time purchase", "val2_p":"No subscription, no in-app purchases, no hidden costs. Buy it once and it’s yours.",
 "val3_h":"Quiet, not loud", "val3_p":"Home-screen widgets ground you — without a single notification.",
 "closing_quote":"Every dot was once the now.",
 "foot_tag":"Punctum — Latin for the point and the moment.",
 "foot_privacy":"Privacy", "foot_terms":"Terms", "foot_imprint":"Imprint", "foot_support":"Support",
 "foot_rights":"© 2026 Bao Anh Tran",
 "back":"← Back to home",
 "meta_desc":"Punctum shows your life as a board of dots — calm, local, no tracking. Choose weeks, months or years and find the now.",
 "priv_lede":"Your time is yours. So is your data.",
 "sup_lede":"A question, a problem, or an idea? Write to me — I reply personally.",
 "body_privacy":'''<p class="stand">Last updated: June 2026 · applies to the Punctum app (iOS &amp; Android).</p>
<h2>What the app stores</h2>
<p>Date of birth, life expectancy, display setting — locally, on this device. None of it leaves the device. No server. No cloud. No tracking. Storage uses the device’s own key-value store. The provider has no access to it at any time.</p>
<h2>Motion sensor</h2>
<p>For the subtle parallax effect, the app briefly reads the accelerometer. The values are not stored and are never transmitted.</p>
<h2>Widgets (optional)</h2>
<p>The home-screen widgets refresh once a day in the background — solely from your locally stored entries. No network connection, no notifications.</p>
<h2>Deleting your data</h2>
<p>Settings → “Start over”. Or uninstall the app. All entries are then irrevocably gone.</p>
<h2>App-store providers</h2>
<p>When you download the app, Apple and Google process data under their own responsibility, independently of Punctum.</p>
<h2>Legal basis</h2>
<p>Since Punctum processes no personal data, a legal basis under Art. 6 GDPR is not required. This statement is provided for transparency.</p>
<h2>Your rights</h2>
<p>Access, rectification, erasure, restriction, portability, objection (Art. 15–21 GDPR), and the right to lodge a complaint with a supervisory authority (Art. 77 GDPR). In practice: delete locally (see above) or contact the controller.</p>
<h2>Controller</h2>
<p>Bao Anh Tran · Friedenstr. 61 · 90409 Nürnberg · Germany<br>E-mail: <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>''',
 "body_terms":'''<p class="stand">Last updated: June 2026</p>
<h2>1. Scope</h2>
<p>These Terms of Use apply to the “Punctum” app (the “App”), provided by Bao Anh Tran (contact details in the <a href="imprint.html">Imprint</a>). By downloading and using the App, you agree to these terms.</p>
<h2>2. What the App is</h2>
<p>Punctum is an app for reflecting on your own lifetime. It depicts your lifetime as a field of dots and runs entirely locally on your device.</p>
<h2>3. Purchase and price</h2>
<p>Punctum is a paid app: a one-time purchase, no subscription, no in-app purchases. Purchase, processing and any refunds are handled exclusively by the respective app store (Apple App Store or Google Play) under their terms. The provider does not process any payments directly.</p>
<h2>4. Licence</h2>
<p>You receive a non-exclusive, non-transferable right to use the App for private purposes on devices you control. Reverse engineering, decompilation or redistribution are permitted only within the limits of mandatory law.</p>
<h2>5. Important notice — not a medical prediction</h2>
<p>The life expectancy shown and the “remaining time” derived from it are a purely statistical, illustrative depiction based on the values you enter. They are expressly <strong>not</strong> a medical prediction, not a diagnosis, and not a health or treatment recommendation. Punctum is not a medical device within the meaning of Regulation (EU) 2017/745. Do not make health decisions based on the displayed values alone.</p>
<h2>6. Liability</h2>
<p>The App is provided with the greatest possible care. The provider is liable without limitation for intent and gross negligence and for injury to life, body or health. For slightly negligent breach of essential contractual obligations, liability is limited to the foreseeable damage typical for this type of contract. Otherwise liability is excluded. Liability under the German Product Liability Act remains unaffected.</p>
<h2>7. Availability and changes</h2>
<p>The provider may further develop, change or discontinue the App. These terms may be amended; the version published at the time of use applies.</p>
<h2>8. Governing law</h2>
<p>German law applies, excluding the UN Convention on Contracts for the International Sale of Goods. Mandatory consumer-protection provisions of your country of residence remain unaffected.</p>
<h2>9. Contact</h2>
<p>Provider and responsible contact: see the <a href="imprint.html">Imprint</a>.</p>''',
 "body_imprint":'''<p class="stand">Information pursuant to § 5 DDG (German Digital Services Act)</p>
<address>Bao Anh Tran
Friedenstr. 61
90409 Nürnberg
Germany</address>
<h2>Contact</h2>
<p>E-mail: <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>
<h2>Responsible for content</h2>
<p>Bao Anh Tran, address as above</p>
<p class="note">EU Commission online dispute resolution platform: <a href="https://ec.europa.eu/consumers/odr/">https://ec.europa.eu/consumers/odr/</a>. We are neither obliged nor willing to participate in dispute resolution proceedings before a consumer arbitration board.</p>''',
 "body_support":'''<a class="mail" href="mailto:traja.projects@gmail.com?subject=Punctum%20Support">traja.projects@gmail.com</a>
<h2>Frequently asked</h2>
<p><strong>How do I delete my data?</strong><br>In the app: Settings → “Start over”. Or uninstall the app. Everything is irrevocably deleted locally.</p>
<p><strong>Is there a subscription or hidden cost?</strong><br>No. Punctum is a one-time purchase — no subscription, no account, no in-app purchases.</p>
<p><strong>New device — do I pay again?</strong><br>No. Re-download for free with the same Apple ID or Google account.</p>
<p><strong>Is my data stored anywhere?</strong><br>Only locally on your device. No server, no cloud, no tracking. Details in the <a href="privacy.html">privacy policy</a>.</p>
<p><strong>Which languages are supported?</strong><br>German, English, Spanish, and French.</p>''',
},

"es": {
 "htmllang":"es", "nav_aria":"Navegación", "footnav_aria":"Legal",
 "nav_features":"Funciones", "nav_support":"Soporte",
 "eyebrow":"Tu vida como un punto",
 "hero_title":"Cada punto fue<br>una vez <em>el ahora.</em>",
 "hero_sub":"Tu vida como un tablero de puntos. La mayoría ya están llenos. Punctum te muestra, con calma, cuántos quedan — y convierte pensar en el final en una brújula para el presente.",
 "hero_ghost":"Cómo funciona",
 "hero_note":"Compra única · sin anuncios · sin rastreo",
 "badge_small":"Pronto en la", "badge_store":"App Store", "badge_tag":"Pronto",
 "alt_board":"Tablero de Punctum: las semanas que te quedan, como una rejilla de puntos",
 "concept_eyebrow":"El tablero",
 "concept_title":"La mayoría de tus puntos ya están llenos.",
 "concept_lead":"Punctum muestra toda tu vida como un tablero de puntos. Lo que queda atrás está lleno. Lo que queda por venir está abierto. Y un único punto brillante es el ahora — el momento en el que lees esto.",
 "legend_past":"Vivido", "legend_now":"Ahora", "legend_future":"Lo que queda",
 "lenses_eyebrow":"Tres lentes", "lenses_title":"Elige cuánto te acercas.",
 "lenses_lead":"Semanas, meses o años — y tres miradas al mismo tiempo.",
 "lens1_h":"Etapas de vida", "lens1_p":"Tus etapas como una Vía Láctea — lo que fue, lo que es, lo que viene.",
 "lens2_h":"Toda tu vida", "lens2_p":"Año tras año, de un vistazo.",
 "lens3_h":"Este año", "lens3_p":"Más cerca — las semanas de este año.",
 "values_eyebrow":"Sereno y privado", "values_title":"Tu tiempo es tuyo. Tus datos también.",
 "val1_h":"Todo es local", "val1_p":"Sin servidor, sin nube, sin rastreo, sin cuenta. Nada sale de tu dispositivo.",
 "val2_h":"Compra única", "val2_p":"Sin suscripción, sin compras dentro de la app, sin costes ocultos. Cómpralo una vez y es tuyo.",
 "val3_h":"Sereno, no ruidoso", "val3_p":"Widgets en la pantalla de inicio que te centran — sin una sola notificación.",
 "closing_quote":"Cada punto fue una vez el ahora.",
 "foot_tag":"Punctum — latín para el punto y el instante.",
 "foot_privacy":"Privacidad", "foot_terms":"Términos", "foot_imprint":"Aviso legal", "foot_support":"Soporte",
 "foot_rights":"© 2026 Bao Anh Tran",
 "back":"← Volver al inicio",
 "meta_desc":"Punctum muestra tu vida como un tablero de puntos — sereno, local, sin rastreo. Elige semanas, meses o años y encuentra el ahora.",
 "priv_lede":"Tu tiempo es tuyo. Tus datos también.",
 "sup_lede":"¿Una pregunta, un problema o una idea? Escríbeme — respondo personalmente.",
 "body_privacy":'''<p class="stand">Última actualización: junio de 2026 · se aplica a la app Punctum (iOS y Android).</p>
<h2>Qué almacena la app</h2>
<p>Fecha de nacimiento, esperanza de vida, ajuste de visualización — de forma local, en este dispositivo. Nada de esto sale de él. Sin servidor. Sin nube. Sin rastreo. El almacenamiento usa el almacén clave-valor propio del dispositivo. El proveedor no tiene acceso a él en ningún momento.</p>
<h2>Sensor de movimiento</h2>
<p>Para el sutil efecto de paralaje, la app lee brevemente el acelerómetro. Los valores no se almacenan ni se transmiten a ningún sitio.</p>
<h2>Widgets (opcional)</h2>
<p>Los widgets de la pantalla de inicio se actualizan una vez al día en segundo plano — únicamente a partir de tus datos guardados localmente. Sin conexión de red, sin notificaciones.</p>
<h2>Eliminar tus datos</h2>
<p>Ajustes → «Empezar de nuevo». O desinstala la app. Entonces todos los datos desaparecen de forma irreversible.</p>
<h2>Proveedores de la tienda</h2>
<p>Al descargar la app, Apple y Google tratan datos bajo su propia responsabilidad, de forma independiente de Punctum.</p>
<h2>Base jurídica</h2>
<p>Como Punctum no trata datos personales, no se requiere una base jurídica según el art. 6 del RGPD. Esta declaración se ofrece por transparencia.</p>
<h2>Tus derechos</h2>
<p>Acceso, rectificación, supresión, limitación, portabilidad y oposición (art. 15–21 del RGPD), así como el derecho a presentar una reclamación ante una autoridad de control (art. 77 del RGPD). En la práctica: elimina localmente (ver arriba) o contacta al responsable.</p>
<h2>Responsable</h2>
<p>Bao Anh Tran · Friedenstr. 61 · 90409 Núremberg · Alemania<br>Correo: <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>''',
 "body_terms":'''<p class="stand">Última actualización: junio de 2026</p>
<h2>1. Ámbito de aplicación</h2>
<p>Estas condiciones de uso se aplican a la app «Punctum» (la «App»), ofrecida por Bao Anh Tran (datos de contacto en el <a href="imprint.html">Aviso legal</a>). Al descargar y usar la App, aceptas estas condiciones.</p>
<h2>2. Qué es la app</h2>
<p>Punctum es una app para reflexionar sobre la propia vida. Representa tu tiempo de vida como un campo de puntos y funciona por completo de forma local en tu dispositivo.</p>
<h2>3. Compra y precio</h2>
<p>Punctum es una app de pago: una compra única, sin suscripción, sin compras dentro de la app. La compra, su tramitación y cualquier reembolso se gestionan exclusivamente a través de la tienda correspondiente (Apple App Store o Google Play) según sus condiciones. El proveedor no procesa ningún pago directamente.</p>
<h2>4. Licencia</h2>
<p>Recibes un derecho no exclusivo e intransferible de usar la App con fines privados en los dispositivos que controlas. La ingeniería inversa, la descompilación o la redistribución solo se permiten dentro de los límites de la ley imperativa.</p>
<h2>5. Aviso importante — no es una predicción médica</h2>
<p>La esperanza de vida mostrada y el «tiempo restante» derivado de ella son una representación puramente estadística e ilustrativa basada en los valores que introduces. No son, de forma expresa, <strong>ninguna</strong> predicción médica, ni un diagnóstico, ni una recomendación de salud o tratamiento. Punctum no es un producto sanitario en el sentido del Reglamento (UE) 2017/745. No tomes decisiones de salud basándote únicamente en los valores mostrados.</p>
<h2>6. Responsabilidad</h2>
<p>La App se ofrece con el mayor cuidado posible. El proveedor responde sin limitación por dolo y negligencia grave, así como por lesiones a la vida, el cuerpo o la salud. En caso de incumplimiento por negligencia leve de obligaciones contractuales esenciales, la responsabilidad se limita al daño previsible y típico de este tipo de contrato. Por lo demás, queda excluida la responsabilidad. La responsabilidad conforme a la Ley alemana de responsabilidad por productos no se ve afectada.</p>
<h2>7. Disponibilidad y cambios</h2>
<p>El proveedor puede seguir desarrollando, modificar o descontinuar la App. Estas condiciones pueden modificarse; rige la versión publicada en el momento del uso.</p>
<h2>8. Ley aplicable</h2>
<p>Se aplica el Derecho alemán, con exclusión de la Convención de las Naciones Unidas sobre los Contratos de Compraventa Internacional de Mercaderías. Las disposiciones imperativas de protección al consumidor de tu país de residencia no se ven afectadas.</p>
<h2>9. Contacto</h2>
<p>Proveedor y persona de contacto responsable: véase el <a href="imprint.html">Aviso legal</a>.</p>''',
 "body_imprint":'''<p class="stand">Información según el art. 5 de la DDG (Ley alemana de servicios digitales)</p>
<address>Bao Anh Tran
Friedenstr. 61
90409 Núremberg
Alemania</address>
<h2>Contacto</h2>
<p>Correo: <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>
<h2>Responsable del contenido</h2>
<p>Bao Anh Tran, dirección como arriba</p>
<p class="note">Plataforma de resolución de litigios en línea de la Comisión Europea: <a href="https://ec.europa.eu/consumers/odr/">https://ec.europa.eu/consumers/odr/</a>. No estamos obligados ni dispuestos a participar en procedimientos de resolución de litigios ante un organismo de arbitraje de consumo.</p>''',
 "body_support":'''<a class="mail" href="mailto:traja.projects@gmail.com?subject=Punctum%20Support">traja.projects@gmail.com</a>
<h2>Preguntas frecuentes</h2>
<p><strong>¿Cómo elimino mis datos?</strong><br>En la app: Ajustes → «Empezar de nuevo». O desinstala la app. Todo se elimina localmente de forma irreversible.</p>
<p><strong>¿Hay suscripción o costes ocultos?</strong><br>No. Punctum es una compra única — sin suscripción, sin cuenta, sin compras dentro de la app.</p>
<p><strong>Nuevo dispositivo, ¿pago otra vez?</strong><br>No. Vuelve a descargarla gratis con el mismo ID de Apple o la misma cuenta de Google.</p>
<p><strong>¿Se guardan mis datos en algún sitio?</strong><br>Solo localmente en tu dispositivo. Sin servidor, sin nube, sin rastreo. Detalles en la <a href="privacy.html">política de privacidad</a>.</p>
<p><strong>¿Qué idiomas admite?</strong><br>Alemán, inglés, español y francés.</p>''',
},

"fr": {
 "htmllang":"fr", "nav_aria":"Navigation", "footnav_aria":"Mentions légales",
 "nav_features":"Fonctions", "nav_support":"Support",
 "eyebrow":"Ta vie comme un point",
 "hero_title":"Chaque point fut<br>un jour <em>l’instant.</em>",
 "hero_sub":"Ta vie comme un tableau de points. La plupart sont déjà remplis. Punctum te montre, avec calme, combien il en reste — et fait de la pensée de la fin une boussole pour le présent.",
 "hero_ghost":"Comment ça marche",
 "hero_note":"Achat unique · sans publicité · sans pistage",
 "badge_small":"Bientôt sur l’", "badge_store":"App Store", "badge_tag":"Bientôt",
 "alt_board":"Tableau Punctum : les semaines qu’il te reste, en grille de points",
 "concept_eyebrow":"Le tableau",
 "concept_title":"La plupart de tes points sont déjà remplis.",
 "concept_lead":"Punctum montre ta vie entière comme un tableau de points. Ce qui est derrière toi est rempli. Ce qui reste est ouvert. Et un seul point lumineux est l’instant présent — le moment où tu lis ceci.",
 "legend_past":"Vécu", "legend_now":"Maintenant", "legend_future":"Ce qui reste",
 "lenses_eyebrow":"Trois focales", "lenses_title":"Choisis ta distance.",
 "lenses_lead":"Semaines, mois ou années — et trois regards sur le même temps.",
 "lens1_h":"Phases de vie", "lens1_p":"Tes phases en Voie lactée — ce qui fut, ce qui est, ce qui vient.",
 "lens2_h":"Ta vie entière", "lens2_p":"Année après année, d’un coup d’œil.",
 "lens3_h":"Cette année", "lens3_p":"Plus près — les semaines de cette année.",
 "values_eyebrow":"Calme et privé", "values_title":"Ton temps t’appartient. Tes données aussi.",
 "val1_h":"Tout reste local", "val1_p":"Aucun serveur, aucun cloud, aucun pistage, aucun compte. Rien ne quitte ton appareil.",
 "val2_h":"Achat unique", "val2_p":"Sans abonnement, sans achats intégrés, sans frais cachés. Achète-le une fois et il est à toi.",
 "val3_h":"Discret, pas bruyant", "val3_p":"Des widgets d’écran d’accueil qui t’ancrent — sans la moindre notification.",
 "closing_quote":"Chaque point fut un jour l’instant présent.",
 "foot_tag":"Punctum — le latin pour le point et l’instant.",
 "foot_privacy":"Confidentialité", "foot_terms":"Conditions", "foot_imprint":"Mentions légales", "foot_support":"Support",
 "foot_rights":"© 2026 Bao Anh Tran",
 "back":"← Retour à l’accueil",
 "meta_desc":"Punctum montre ta vie comme un tableau de points — calme, local, sans pistage. Choisis semaines, mois ou années et trouve l’instant.",
 "priv_lede":"Ton temps t’appartient. Tes données aussi.",
 "sup_lede":"Une question, un problème ou une idée ? Écris-moi — je réponds personnellement.",
 "body_privacy":'''<p class="stand">Dernière mise à jour : juin 2026 · s’applique à l’app Punctum (iOS et Android).</p>
<h2>Ce que l’app enregistre</h2>
<p>Date de naissance, espérance de vie, réglage d’affichage — en local, sur cet appareil. Rien de tout cela ne le quitte. Aucun serveur. Aucun cloud. Aucun pistage. Le stockage utilise le magasin clé-valeur propre à l’appareil. Le fournisseur n’y a accès à aucun moment.</p>
<h2>Capteur de mouvement</h2>
<p>Pour le discret effet de parallaxe, l’app lit brièvement l’accéléromètre. Les valeurs ne sont ni enregistrées ni transmises.</p>
<h2>Widgets (facultatif)</h2>
<p>Les widgets de l’écran d’accueil se mettent à jour une fois par jour en arrière-plan — uniquement à partir de tes données enregistrées localement. Aucune connexion réseau, aucune notification.</p>
<h2>Supprimer tes données</h2>
<p>Réglages → « Recommencer ». Ou désinstalle l’app. Toutes les données sont alors irrévocablement effacées.</p>
<h2>Fournisseurs des stores</h2>
<p>Lors du téléchargement, Apple et Google traitent des données sous leur propre responsabilité, indépendamment de Punctum.</p>
<h2>Base légale</h2>
<p>Comme Punctum ne traite aucune donnée personnelle, aucune base légale au sens de l’art. 6 du RGPD n’est requise. Cette déclaration est fournie par souci de transparence.</p>
<h2>Tes droits</h2>
<p>Accès, rectification, effacement, limitation, portabilité, opposition (art. 15–21 du RGPD), ainsi que le droit d’introduire une réclamation auprès d’une autorité de contrôle (art. 77 du RGPD). En pratique : supprime en local (voir ci-dessus) ou contacte le responsable.</p>
<h2>Responsable</h2>
<p>Bao Anh Tran · Friedenstr. 61 · 90409 Nuremberg · Allemagne<br>E-mail : <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>''',
 "body_terms":'''<p class="stand">Dernière mise à jour : juin 2026</p>
<h2>1. Champ d’application</h2>
<p>Les présentes conditions d’utilisation s’appliquent à l’app « Punctum » (l’« App »), fournie par Bao Anh Tran (coordonnées dans les <a href="imprint.html">Mentions légales</a>). En téléchargeant et en utilisant l’App, tu acceptes ces conditions.</p>
<h2>2. Ce qu’est l’app</h2>
<p>Punctum est une app de réflexion sur sa propre vie. Elle représente ton temps de vie comme un champ de points et fonctionne entièrement en local sur ton appareil.</p>
<h2>3. Achat et prix</h2>
<p>Punctum est une app payante : un achat unique, sans abonnement, sans achats intégrés. L’achat, son traitement et tout remboursement sont gérés exclusivement par la boutique concernée (Apple App Store ou Google Play) selon leurs conditions. Le fournisseur ne traite aucun paiement directement.</p>
<h2>4. Licence</h2>
<p>Tu reçois un droit non exclusif et non transférable d’utiliser l’App à des fins privées sur les appareils que tu contrôles. L’ingénierie inverse, la décompilation ou la redistribution ne sont autorisées que dans les limites du droit impératif.</p>
<h2>5. Avis important — pas une prédiction médicale</h2>
<p>L’espérance de vie affichée et le « temps restant » qui en découle sont une représentation purement statistique et illustrative fondée sur les valeurs que tu saisis. Elles ne constituent expressément <strong>pas</strong> une prédiction médicale, ni un diagnostic, ni une recommandation de santé ou de traitement. Punctum n’est pas un dispositif médical au sens du règlement (UE) 2017/745. Ne prends pas de décisions de santé sur la seule base des valeurs affichées.</p>
<h2>6. Responsabilité</h2>
<p>L’App est fournie avec le plus grand soin possible. Le fournisseur est responsable sans limitation en cas de dol et de faute lourde, ainsi qu’en cas d’atteinte à la vie, au corps ou à la santé. En cas de manquement par négligence légère à des obligations contractuelles essentielles, la responsabilité est limitée au dommage prévisible et typique de ce type de contrat. Pour le reste, la responsabilité est exclue. La responsabilité au titre de la loi allemande sur la responsabilité du fait des produits demeure inchangée.</p>
<h2>7. Disponibilité et modifications</h2>
<p>Le fournisseur peut faire évoluer, modifier ou arrêter l’App. Ces conditions peuvent être modifiées ; la version publiée au moment de l’utilisation fait foi.</p>
<h2>8. Droit applicable</h2>
<p>Le droit allemand s’applique, à l’exclusion de la Convention des Nations Unies sur les contrats de vente internationale de marchandises. Les dispositions impératives de protection des consommateurs de ton pays de résidence demeurent inchangées.</p>
<h2>9. Contact</h2>
<p>Fournisseur et interlocuteur responsable : voir les <a href="imprint.html">Mentions légales</a>.</p>''',
 "body_imprint":'''<p class="stand">Informations conformément à l’art. 5 de la DDG (loi allemande sur les services numériques)</p>
<address>Bao Anh Tran
Friedenstr. 61
90409 Nuremberg
Allemagne</address>
<h2>Contact</h2>
<p>E-mail : <a href="mailto:traja.projects@gmail.com">traja.projects@gmail.com</a></p>
<h2>Responsable du contenu</h2>
<p>Bao Anh Tran, adresse comme ci-dessus</p>
<p class="note">Plateforme de règlement en ligne des litiges de la Commission européenne : <a href="https://ec.europa.eu/consumers/odr/">https://ec.europa.eu/consumers/odr/</a>. Nous ne sommes ni obligés ni disposés à participer à une procédure de règlement des litiges devant un organe de médiation des consommateurs.</p>''',
 "body_support":'''<a class="mail" href="mailto:traja.projects@gmail.com?subject=Punctum%20Support">traja.projects@gmail.com</a>
<h2>Questions fréquentes</h2>
<p><strong>Comment supprimer mes données ?</strong><br>Dans l’app : Réglages → « Recommencer ». Ou désinstalle l’app. Tout est supprimé localement de façon irréversible.</p>
<p><strong>Y a-t-il un abonnement ou des coûts cachés ?</strong><br>Non. Punctum est un achat unique — sans abonnement, sans compte, sans achats intégrés.</p>
<p><strong>Nouvel appareil — dois-je repayer ?</strong><br>Non. Retélécharge-la gratuitement avec le même identifiant Apple ou le même compte Google.</p>
<p><strong>Mes données sont-elles stockées quelque part ?</strong><br>Uniquement en local sur ton appareil. Aucun serveur, aucun cloud, aucun pistage. Détails dans la <a href="privacy.html">politique de confidentialité</a>.</p>
<p><strong>Quelles langues sont prises en charge ?</strong><br>Allemand, anglais, espagnol et français.</p>''',
},
}

# ---------------------------------------------------------------- helpers
def badge(L):
    soon = ('<span class="badge__tag">%s</span>' % L["badge_tag"]) if APP_STORE_URL is None else ""
    inner = ('%s<span class="badge__tx"><small>%s</small><b>%s</b></span>%s'
             % (APPLE, L["badge_small"], L["badge_store"], soon))
    if APP_STORE_URL is None:
        return '<span class="badge is-soon" role="img" aria-label="%s %s">%s</span>' % (
            L["badge_small"], L["badge_store"], inner)
    return '<a class="badge" href="%s" aria-label="%s">%s</a>' % (APP_STORE_URL, L["badge_store"], inner)


def alts_for(pagefile):
    out = ['<link rel="alternate" hreflang="%s" href="%s%s/%s">' % (l, BASE, l, pagefile) for l in LANGS]
    out.append('<link rel="alternate" hreflang="x-default" href="%sen/%s">' % (BASE, pagefile))
    return "\n".join(out)


def langswitch(cur, pagefile):
    out = []
    for l in LANGS:
        cura = ' aria-current="true"' if l == cur else ''
        out.append('<a href="../%s/%s" hreflang="%s"%s>%s</a>' % (l, pagefile, l, cura, l.upper()))
    return "".join(out)


def render(tmpl, L, **extra):
    ctx = dict(L); ctx.update(extra)
    return tmpl.format(**ctx)


def redirect_page(suffix, title, desc, canonical):
    alts = alts_for(suffix)
    names = [("en", "Continue"), ("de", "Deutsch"), ("es", "Español"), ("fr", "Français")]
    links = " · ".join('<a href="%s/%s">%s</a>' % (l, suffix, n) for l, n in names)
    js = ("(function(){var m={de:1,en:1,es:1,fr:1};"
          "var l=(navigator.language||'en').slice(0,2).toLowerCase();"
          "var t=m[l]?l:'en';location.replace(t+'/%s');})();" % suffix)
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>%s</title>\n<meta name=\"description\" content=\"%s\">\n"
            "<link rel=\"canonical\" href=\"%s\">\n%s\n"
            "<link rel=\"icon\" type=\"image/png\" href=\"assets/favicon.png\">\n"
            "<style>html,body{height:100%%;margin:0;background:#04050F;color:#F4F6FF;"
            "font-family:system-ui,-apple-system,sans-serif;display:flex;align-items:center;"
            "justify-content:center;text-align:center}a{color:#FFCE6B;text-decoration:none}</style>\n"
            "<script>%s</script>\n</head>\n<body>\n<p>Punctum<br><br>%s</p>\n</body>\n</html>\n"
            ) % (title, desc, canonical, alts, js, links)


# ---------------------------------------------------------------- build
def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.relpath(path, ROOT))


def build():
    namekey = {"privacy": "foot_privacy", "terms": "foot_terms",
               "imprint": "foot_imprint", "support": "foot_support"}
    for lang in LANGS:
        L = C[lang]
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        for key, pagefile in PAGES:
            ls = langswitch(lang, pagefile)
            header = render(HEADER, L, langswitch=ls)
            footer = render(FOOTER, L, langswitch=ls)
            if key == "index":
                main = render(LANDING, L, badge=badge(L), root="../", code=lang,
                              ico_privacy=ICO["privacy"], ico_purchase=ICO["purchase"], ico_quiet=ICO["quiet"])
                title = "Punctum · " + L["eyebrow"]
                desc = L["meta_desc"]
                canonical = BASE + lang + "/"
            else:
                h1 = L[namekey[key]]
                if key == "privacy":
                    lede = '<p class="lede">%s</p>' % L["priv_lede"]; desc = L["priv_lede"]
                elif key == "support":
                    lede = '<p class="lede">%s</p>' % L["sup_lede"]; desc = L["sup_lede"]
                else:
                    lede = ""; desc = "%s — Punctum." % h1
                main = render(LEGAL, L, h1=h1, lede=lede, body=L["body_" + key])
                title = h1 + " · Punctum"
                canonical = BASE + lang + "/" + pagefile
            html = SHELL.format(htmllang=lang, title=title, desc=desc, canonical=canonical,
                                alts=alts_for(pagefile), og=BASE + "assets/og_" + lang + ".jpg",
                                root="../", header=header, main=main, footer=footer)
            out = os.path.join(ROOT, lang, pagefile if pagefile else "index.html")
            write(out, html)

    # root redirect + legacy stubs (preserve old /Punctum/<page> URLs)
    write(os.path.join(ROOT, "index.html"),
          redirect_page("", "Punctum",
                        "Punctum — your life as a board of dots. Calm, local, no tracking.", BASE))
    for key, pagefile in PAGES:
        if not pagefile:
            continue
        write(os.path.join(ROOT, pagefile),
              redirect_page(pagefile, "Punctum", "Punctum", BASE + "en/" + pagefile))

    # remove the old single-page assets that the new structure replaces
    for old in ["site.js"]:
        p = os.path.join(ROOT, old)
        if os.path.exists(p):
            os.remove(p); print("removed", old)


if __name__ == "__main__":
    build()
    print("done")
