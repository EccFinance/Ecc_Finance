# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


OUT = Path("assets/partner-pack-ecc-finance.pdf")
SITE_URL = "https://hamzasennah.github.io/Ecc-Finance/"
PARTNER_URL = "https://hamzasennah.github.io/Ecc-Finance/partenaires.html"
CLUB_EMAIL = "club.finance@centrale-casablanca.ma"
LINKEDIN = "https://www.linkedin.com/company/ecc-finance"

W, H = A4
M = 18 * mm

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))

INK = colors.HexColor("#111614")
INK_SOFT = colors.HexColor("#25312D")
PAPER = colors.HexColor("#F4EFE6")
WHITE = colors.HexColor("#FFFFFF")
TEAL = colors.HexColor("#1C8A78")
TEAL_DARK = colors.HexColor("#0E5F55")
GOLD = colors.HexColor("#C49A4A")
WINE = colors.HexColor("#7D2032")
MUTED = colors.HexColor("#64706A")
LINE = colors.HexColor("#DCD2BF")
PALE = colors.HexColor("#FFF8EA")
GREEN_PALE = colors.HexColor("#EAF4F1")


styles = {
    "eyebrow": ParagraphStyle("eyebrow", fontName="Arial-Bold", fontSize=8.5, leading=11, textColor=GOLD, uppercase=True),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=34, leading=36, textColor=WHITE),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=22, leading=25, textColor=INK),
    "h3": ParagraphStyle("h3", fontName="Arial-Bold", fontSize=13, leading=15, textColor=INK),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=9.3, leading=13.2, textColor=INK_SOFT),
    "body_white": ParagraphStyle("body_white", fontName="Arial", fontSize=10.5, leading=15, textColor=colors.HexColor("#FFF7E8")),
    "small": ParagraphStyle("small", fontName="Arial", fontSize=7.8, leading=10, textColor=MUTED),
    "small_white": ParagraphStyle("small_white", fontName="Arial", fontSize=7.8, leading=10, textColor=colors.HexColor("#D9E0DC")),
    "metric": ParagraphStyle("metric", fontName="Arial-Bold", fontSize=18, leading=20, textColor=TEAL_DARK),
    "metric_white": ParagraphStyle("metric_white", fontName="Arial-Bold", fontSize=18, leading=20, textColor=GOLD),
}


def p(c, text, style, x, y, w, h=None):
    para = Paragraph(text, style)
    _, used_h = para.wrap(w, 1000)
    if h is not None:
        used_h = min(used_h, h)
    para.drawOn(c, x, y - used_h)
    return used_h


def section_title(c, eyebrow, title, x, y, width=170 * mm):
    c.setFillColor(GOLD)
    c.setFont("Arial-Bold", 8)
    c.drawString(x, y, eyebrow.upper())
    y -= 9
    used = p(c, title, styles["h2"], x, y, width)
    return y - used - 10


def logo_mark(c, x, y, size=28):
    c.setFillColor(INK)
    c.roundRect(x, y, size, size, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", size * 0.42)
    c.drawString(x + size * 0.19, y + size * 0.33, "E")
    c.setFillColor(GOLD)
    c.rect(x + size * 0.56, y + size * 0.24, size * 0.11, size * 0.48, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.circle(x + size * 0.74, y + size * 0.56, size * 0.06, fill=1, stroke=0)


def footer(c, page):
    c.setStrokeColor(colors.HexColor("#D7CBB7"))
    c.setLineWidth(0.5)
    c.line(M, 14 * mm, W - M, 14 * mm)
    c.setFillColor(MUTED)
    c.setFont("Arial", 7.5)
    c.drawString(M, 9 * mm, f"{SITE_URL}  |  {CLUB_EMAIL}")
    c.drawRightString(W - M, 9 * mm, f"ECC Finance Partner Pack 2026 - {page}")


def draw_icon(c, kind, x, y, color):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.4)
    if kind == "chart":
        c.line(x, y, x + 26, y)
        c.line(x, y, x, y + 22)
        c.line(x + 3, y + 5, x + 10, y + 11)
        c.line(x + 10, y + 11, x + 17, y + 8)
        c.line(x + 17, y + 8, x + 25, y + 18)
        for px, py in [(3, 5), (10, 11), (17, 8), (25, 18)]:
            c.circle(x + px, y + py, 1.8, fill=1, stroke=0)
    elif kind == "network":
        pts = [(x + 4, y + 5), (x + 18, y + 16), (x + 28, y + 7), (x + 12, y + 24)]
        for a, b in [(0, 1), (1, 2), (1, 3), (0, 3)]:
            c.line(*pts[a], *pts[b])
        for px, py in pts:
            c.circle(px, py, 3.2, fill=1, stroke=0)
    elif kind == "brief":
        c.roundRect(x + 2, y + 4, 27, 18, 3, stroke=1, fill=0)
        c.roundRect(x + 10, y + 20, 11, 5, 2, stroke=1, fill=0)
        c.line(x + 2, y + 14, x + 29, y + 14)
    else:
        c.circle(x + 15, y + 15, 13, stroke=1, fill=0)
        c.line(x + 15, y + 4, x + 15, y + 26)
        c.line(x + 4, y + 15, x + 26, y + 15)


def metric_card(c, x, y, w, h, value, title, body, fill=WHITE):
    c.setFillColor(fill)
    c.roundRect(x, y - h, w, h, 8, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - h, w, h, 8, fill=0, stroke=1)
    p(c, value, styles["metric"], x + 10, y - 11, w - 20)
    p(c, f"<b>{title}</b>", styles["body"], x + 10, y - 33, w - 20)
    p(c, body, styles["small"], x + 10, y - 52, w - 20)


def offer_row(c, y, need, answer, icon_kind, color):
    x = M
    row_h = 47
    c.setFillColor(WHITE)
    c.roundRect(x, y - row_h, W - 2 * M, row_h, 7, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - row_h, W - 2 * M, row_h, 7, fill=0, stroke=1)
    draw_icon(c, icon_kind, x + 12, y - 34, color)
    p(c, f"<b>{need}</b>", styles["body"], x + 52, y - 13, 54 * mm)
    p(c, answer, styles["body"], x + 52 + 62 * mm, y - 13, 88 * mm)
    return y - row_h - 8


def pack_card(c, x, y, w, h, title, items, color):
    c.setFillColor(WHITE)
    c.roundRect(x, y - h, w, h, 8, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.roundRect(x, y - h, w, h, 8, fill=0, stroke=1)
    c.setFillColor(color)
    c.roundRect(x, y - 28, w, 28, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 12)
    c.drawString(x + 10, y - 18, title)
    item_y = y - 43
    for item in items:
        used = p(c, f"- {item}", styles["small"], x + 10, item_y, w - 20)
        item_y -= used + 7


def qr_code(c, url, x, y, size):
    quiet_zone = 8
    c.setFillColor(WHITE)
    c.roundRect(x - quiet_zone, y - quiet_zone, size + 2 * quiet_zone, size + 2 * quiet_zone, 6, fill=1, stroke=0)
    qr = QrCodeWidget(url)
    bounds = qr.getBounds()
    qr_w = bounds[2] - bounds[0]
    qr_h = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / qr_w, 0, 0, size / qr_h, 0, 0])
    drawing.add(qr)
    renderPDF.draw(drawing, c, x, y)


def cover(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#18221F"))
    c.roundRect(M, 86, W - 2 * M, H - 132, 18, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(M, H - 150, 8, 96, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(M + 10, H - 188, 8, 134, fill=1, stroke=0)
    c.setFillColor(WINE)
    c.rect(M + 20, H - 114, 8, 60, fill=1, stroke=0)

    logo_mark(c, M + 35, H - 108, 34)
    c.setFillColor(WHITE)
    c.setFont("Arial-Bold", 13)
    c.drawString(M + 78, H - 88, "ECC Finance")
    c.setFont("Arial", 8.5)
    c.setFillColor(colors.HexColor("#C9D2CE"))
    c.drawString(M + 78, H - 101, "École Centrale Casablanca - Club finance étudiant")

    p(c, "ECC Finance<br/>Partner Pack 2026", styles["h1"], M + 35, H - 235, 125 * mm)
    p(c, "Former, connecter et révéler les talents finance de Centrale Casablanca", styles["body_white"], M + 35, H - 318, 112 * mm)

    c.setFillColor(colors.HexColor("#22302B"))
    c.roundRect(M + 35, 156, W - 2 * M - 70, 128, 12, fill=1, stroke=0)
    p(c, "Document de présentation destiné aux partenaires académiques et professionnels. Les chiffres indiqués correspondent aux objectifs de structuration 2026 et pourront évoluer selon le calendrier académique.", styles["small_white"], M + 55, 255, W - 2 * M - 110)
    p(c, "Notre ambition est de rendre la finance accessible sans perdre en rigueur, à travers des formats pédagogiques, des analyses structurées et des échanges directs avec les professionnels.", styles["body_white"], M + 55, 217, W - 2 * M - 110)

    x0 = M + 35
    for i, (value, label) in enumerate([("+100", "étudiants ciblés"), ("5", "événements visés"), ("1", "Research Desk")]):
        x = x0 + i * 52 * mm
        c.setFillColor(colors.HexColor("#101513"))
        c.roundRect(x, 108, 45 * mm, 38, 7, fill=1, stroke=0)
        p(c, value, styles["metric_white"], x + 8, 138, 40 * mm)
        p(c, label, styles["small_white"], x + 8, 118, 38 * mm)


def page_two(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    logo_mark(c, M, H - 54, 26)
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 11)
    c.drawString(M + 34, H - 43, "ECC Finance")
    y = section_title(c, "Audience", "Pourquoi collaborer avec des élèves ingénieurs de Centrale Casablanca ?", M, H - 88)
    body = "Les élèves de Centrale Casablanca disposent d'une formation généraliste orientée ingénierie, data, analyse quantitative, gestion de projet et résolution de problèmes complexes. ECC Finance connecte ces profils à l'écosystème financier à travers des formats pédagogiques, professionnels et ciblés."
    y -= p(c, body, styles["body"], M, y, W - 2 * M) + 14

    c.setFillColor(INK)
    c.setFont("Arial-Bold", 16)
    c.drawString(M, y, "Preuves de structuration 2026")
    y -= 18
    card_w = (W - 2 * M - 16) / 3
    metric_card(c, M, y, card_w, 92, "+100", "étudiants ciblés", "Élèves ingénieurs intéressés par finance, data, conseil, marché et corporate finance.", WHITE)
    metric_card(c, M + card_w + 8, y, card_w, 92, "5", "événements visés", "Conférences, workshops, simulations d'entretien et rencontres métiers.", WHITE)
    metric_card(c, M + 2 * (card_w + 8), y, card_w, 92, "1", "Research Desk étudiant", "Production de notes pédagogiques, analyses de marché et contenus éducatifs.", WHITE)
    y -= 110
    metric_card(c, M, y, card_w, 82, "4", "pôles de travail", "Marché, corporate finance, data et carrière.", GREEN_PALE)
    metric_card(c, M + card_w + 8, y, card_w, 82, "3", "formats de formation", "Initiation, outils et préparation aux entretiens.", GREEN_PALE)
    metric_card(c, M + 2 * (card_w + 8), y, card_w, 82, "2026", "programme structuré", "Calendrier progressif aligné avec le rythme académique.", GREEN_PALE)

    y -= 116
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 16)
    c.drawString(M, y, "Contacts officiels")
    y -= 18
    contact_h = 138
    c.setFillColor(WHITE)
    c.roundRect(M, y - contact_h, W - 2 * M, contact_h, 8, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.roundRect(M, y - contact_h, W - 2 * M, contact_h, 8, fill=0, stroke=1)
    p(c, "<b>Équipe partenariats</b><br/>Ikram Boulouqat - Oumaima Nadour - Fatima Machrafi<br/>Ahmed Zhiri - Jean Paul Gbatto - Douae Amghar - Felix Camara", styles["body"], M + 14, y - 16, 98 * mm)
    p(c, f"<b>Contact officiel</b><br/>{CLUB_EMAIL}<br/>LinkedIn: ECC Finance<br/>Site: {SITE_URL}", styles["small"], M + 14, y - 78, 98 * mm)
    qr_x = W - M - 82
    qr_y = y - 114
    qr_code(c, PARTNER_URL, qr_x, qr_y, 72)
    p(c, "Scannez pour proposer<br/>une collaboration.", styles["small"], qr_x - 4, y - 10, 82)


def page_three(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    y = section_title(c, "Offre partenaire", "Ce que nous offrons au partenaire", M, H - 64)
    rows = [
        ("Visibilité campus", "Communication ciblée auprès des élèves ingénieurs.", "network", TEAL),
        ("Recrutement", "Accès à des profils finance, data et ingénierie.", "brief", GOLD),
        ("Image employeur", "Conférence, workshop ou intervention métier.", "chart", WINE),
        ("Contenu éducatif", "Article, note ou publication co-construite.", "market", TEAL_DARK),
        ("Interaction directe", "Session Q&amp;A avec les étudiants, simulation d'entretien ou challenge.", "network", GOLD),
    ]
    for need, answer, icon, color in rows:
        y = offer_row(c, y, need, answer, icon, color)

    y -= 22
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 16)
    c.drawString(M, y, "Formats packagés")
    y -= 22
    card_w = (W - 2 * M - 18) / 3
    pack_card(c, M, y, card_w, 166, "Pack Découverte", ["1 conférence métier", "communication campus", "inscription des participants", "publication LinkedIn après événement"], TEAL_DARK)
    pack_card(c, M + card_w + 9, y, card_w, 166, "Pack Workshop", ["1 atelier technique ou métier", "support pédagogique", "interaction avec les étudiants", "retour qualitatif après l'événement"], GOLD)
    pack_card(c, M + 2 * (card_w + 9), y, card_w, 166, "Pack Talent", ["présentation entreprise", "simulation d'entretiens", "recueil de profils intéressés via formulaire dédié", "accès à des profils finance, data et conseil"], WINE)

    p(c, "Les packs peuvent être combinés selon le calendrier académique, le niveau technique attendu et l'objectif du partenaire.", styles["body"], M, 112, W - 2 * M)


def page_four(c):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    y = section_title(c, "Activation", "Calendrier indicatif et prochaine étape", M, H - 64)

    steps = [
        ("T1 2026", "Atelier Finance de marché 101<br/><b>Partenaire idéal:</b> analyste marché, banque, alumni finance."),
        ("T2 2026", "Workshop Excel / Python finance<br/><b>Partenaire idéal:</b> cabinet, banque, fintech, data analyst."),
        ("T3 2026", "Publication sectorielle et contenus éducatifs<br/><b>Partenaire idéal:</b> média spécialisé, analyste, alumni."),
        ("T4 2026", "Conférence métiers: M&amp;A, Trading, Private Equity<br/><b>Partenaire idéal:</b> banque d'affaires, trading, PE, alumni."),
    ]
    for i, (period, desc) in enumerate(steps):
        x = M + (i % 2) * ((W - 2 * M) / 2 + 5)
        yy = y - (i // 2) * 96
        w = (W - 2 * M) / 2 - 5
        c.setFillColor(WHITE)
        c.roundRect(x, yy - 76, w, 76, 8, fill=1, stroke=0)
        c.setStrokeColor(LINE)
        c.roundRect(x, yy - 76, w, 76, 8, fill=0, stroke=1)
        p(c, f"<b>{period}</b>", styles["h3"], x + 12, yy - 12, w - 24)
        p(c, desc, styles["small"], x + 12, yy - 35, w - 24)

    y -= 216
    c.setFillColor(INK)
    c.roundRect(M, y - 142, W - 2 * M, 142, 10, fill=1, stroke=0)
    p(c, "Intéressé par une collaboration ?", ParagraphStyle("white_h2", fontName="Arial-Bold", fontSize=18, leading=22, textColor=WHITE), M + 18, y - 22, W - 2 * M - 36)
    p(c, "Contactez-nous pour définir le format le plus adapté à vos objectifs: conférence, workshop, publication, challenge ou rencontre talents.<br/><br/><b>Prochaine étape:</b> planifier un échange de 20 minutes pour identifier le format le plus pertinent.", styles["body_white"], M + 18, y - 56, W - 2 * M - 36)

    y -= 176
    c.setFillColor(WHITE)
    c.roundRect(M, y - 158, W - 2 * M, 158, 8, fill=1, stroke=0)
    c.setStrokeColor(LINE)
    c.roundRect(M, y - 158, W - 2 * M, 158, 8, fill=0, stroke=1)
    p(c, "<b>Pourquoi nous faire confiance ?</b>", styles["h3"], M + 14, y - 15, 110 * mm)
    p(c, "ECC Finance s'engage à préparer chaque collaboration avec un brief clair, une communication organisée, une inscription suivie et un retour qualitatif après l'événement.", styles["body"], M + 14, y - 40, 112 * mm)
    p(c, "<b>Cadre responsable</b><br/>Contenus éducatifs, sans recommandation d'investissement.", styles["small"], M + 14, y - 88, 112 * mm)
    p(c, f"<b>Contact officiel</b><br/>{CLUB_EMAIL}<br/>LinkedIn: ECC Finance<br/>Site: {SITE_URL}", styles["small"], M + 14, y - 108, 112 * mm)
    qr_code(c, PARTNER_URL, W - M - 86, y - 124, 70)
    p(c, "Scannez pour proposer une collaboration.", styles["small"], W - M - 92, y - 24, 84)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("ECC Finance Partner Pack 2026")
    c.setAuthor("ECC Finance")
    pages = [cover, page_two, page_three, page_four]
    for index, page in enumerate(pages, start=1):
        page(c)
        footer(c, index)
        c.showPage()
    c.save()


if __name__ == "__main__":
    build()
