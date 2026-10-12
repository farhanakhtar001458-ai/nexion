#!/usr/bin/env python3
"""
Build clean, readable PDF question papers from paper_data.py.

Output: ../papers/reconstructed-2022-2026/<subject>/<CODE>_<Session>.pdf
Usage:  python3 tools/build_pdfs.py
Requires: reportlab (pip install reportlab)
"""
import os, sys, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, HRFlowable)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_data import PAPERS, SET  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_ROOT = os.path.join(BASE, "papers", "reconstructed-2022-2026")
TODAY = datetime.date.today().strftime("%d %b %Y")

# ---------- fonts (DejaVu = unicode friendly: ², ³, ∂, ∫, θ, λ, √, ≤, Å …) ----------
def find_font_dir():
    """DejaVu faces (incl. Oblique) dhoondho — system fonts ya matplotlib ke bundled copy se."""
    cands = ["/usr/share/fonts/truetype/dejavu"]
    try:
        import matplotlib, os as _os
        cands.append(_os.path.join(_os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf"))
    except Exception:
        pass
    cands.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"))
    for d in cands:
        if os.path.exists(os.path.join(d, "DejaVuSans.ttf")):
            return d
    sys.exit("DejaVu fonts nahi mile. Install karo:  apt-get install fonts-dejavu-core  "
             "(ya pip install matplotlib)")

FDIR = find_font_dir()
def face(name, fallback=None):
    p = os.path.join(FDIR, name)
    if os.path.exists(p):
        return p
    if fallback:
        return os.path.join(FDIR, fallback)
    raise SystemExit(f"font missing: {p}")

pdfmetrics.registerFont(TTFont("DJ",   face("DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DJ-B", face("DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DJ-I", face("DejaVuSans-Oblique.ttf", "DejaVuSans.ttf")))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B", italic="DJ-I")

S = {
 "h1": ParagraphStyle("h1", fontName="DJ-B", fontSize=14.5, leading=19, alignment=TA_CENTER),
 "h2": ParagraphStyle("h2", fontName="DJ-B", fontSize=12, leading=16, alignment=TA_CENTER),
 "h3": ParagraphStyle("h3", fontName="DJ-B", fontSize=11.5, leading=15, alignment=TA_CENTER),
 "meta": ParagraphStyle("meta", fontName="DJ-I", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor("#333333")),
 "note": ParagraphStyle("note", fontName="DJ", fontSize=9.2, leading=13, alignment=TA_JUSTIFY),
 "q": ParagraphStyle("q", fontName="DJ", fontSize=10.3, leading=14.5, alignment=TA_JUSTIFY),
 "qn": ParagraphStyle("qn", fontName="DJ-B", fontSize=10.3, leading=14.5),
 "marks": ParagraphStyle("marks", fontName="DJ-B", fontSize=10, leading=14, alignment=TA_CENTER),
 "small": ParagraphStyle("small", fontName="DJ", fontSize=7.6, leading=10.5, alignment=TA_CENTER, textColor=colors.HexColor("#555555")),
}

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DJ", 7.4)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 12 * mm,
        f"Reconstructed English version · source: rgpvonline.com public archives · generated {TODAY} · unofficial study material")
    canvas.drawRightString(A4[0] - 14 * mm, 8 * mm, f"Page {doc.page}")
    canvas.drawString(14 * mm, 8 * mm, f"{doc.subject_code} · {doc.session}")
    canvas.setStrokeColor(colors.HexColor("#bbbbbb"))
    canvas.line(14 * mm, 15 * mm, A4[0] - 14 * mm, 15 * mm)
    canvas.restoreState()

def build(paper):
    folder = os.path.join(OUT_ROOT, f"{paper['code']}-{paper['name'].replace(' ', '-').replace('&', 'and')}")
    os.makedirs(folder, exist_ok=True)
    mon = {"June": "Jun", "December": "Dec", "November": "Nov", "May": "May"}.get(paper["session"].split()[0], paper["session"].split()[0])
    out = os.path.join(folder, f"{paper['code']}_{mon}-{paper['session'].split()[1]}.pdf")

    doc = BaseDocTemplate(out, pagesize=A4,
                          leftMargin=14 * mm, rightMargin=14 * mm, topMargin=13 * mm, bottomMargin=17 * mm,
                          title=f"{paper['code']} {paper['name']} — {paper['session']} (reconstructed)",
                          author="RGPV PYQ study archive")
    doc.subject_code, doc.session = paper["code"], paper["session"]
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])

    F = []
    F.append(Paragraph(f"{paper['code']} (GS)", S["h1"]))
    F.append(Paragraph(f"B.Tech., I &amp; II Semester Examination, {paper['session']}", S["h2"]))
    F.append(Paragraph("Grading System (GS)", S["h3"]))
    F.append(Paragraph(paper["name"].upper(), S["h1"]))
    F.append(Spacer(1, 3))
    F.append(Paragraph("Time : Three Hours &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Maximum Marks : 70", S["meta"]))
    F.append(Spacer(1, 3))
    F.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#888888")))
    F.append(Spacer(1, 6))
    F.append(Paragraph(
        "<b>Note :</b> (i) Attempt any five questions. &nbsp; (ii) All questions carry equal marks. &nbsp; "
        "(iii) Original paper bilingual (Hindi + English) tha; yahan sirf English version diya gaya hai.", S["note"]))
    F.append(Spacer(1, 4))
    F.append(Paragraph(f"<i>Coverage: {paper.get('coverage','Full paper')}</i>", S["note"]))
    F.append(Spacer(1, 8))

    rows = []
    for qno, parts in paper["questions"]:
        if parts is None:
            rows.append([Paragraph(f"{qno}.", S["qn"]),
                         Paragraph("<i>(source me ye question available nahi tha — original paper dekhein)</i>", S["q"]),
                         Paragraph("—", S["marks"])])
            rows.append([Spacer(1, 4), "", ""])
            continue
        first = True
        for i, (part, text, marks) in enumerate(parts):
            label = f"{qno}." if first else ""
            sub = f"({part}) " if part else ""
            rows.append([Paragraph(label, S["qn"]),
                         Paragraph(f"{sub}{text}", S["q"]),
                         Paragraph(str(marks) if marks else "", S["marks"])])
            first = False
        rows.append([Spacer(1, 6), "", ""])

    t = Table(rows, colWidths=[11 * mm, doc.width - 11 * mm - 13 * mm, 13 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    F.append(t)
    F.append(Spacer(1, 10))
    F.append(Paragraph("*******", S["h3"]))
    F.append(Spacer(1, 8))
    F.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    F.append(Spacer(1, 4))
    F.append(Paragraph(
        "<b>Yeh reconstructed paper kya hai?</b> RGPV ke 2022–2026 ke papers ka free official PDF internet par "
        "downloadable nahi hai (mirrors sirf ~2019 tak ke papers rakhte hain). Ye version un hi papers ke public web "
        "renders se word-by-word English questions lekar banaya gaya hai, tai ki students unhe PDF me padh/print kar sakein. "
        "Hindi version aur exact layout ke liye original paper dekhein. Ye unofficial study material hai.", S["small"]))
    doc.build(F)
    return out

if __name__ == "__main__":
    made = []
    for p in PAPERS:
        path = build(p)
        made.append(path)
    print(f"Generated {len(made)} PDFs in {OUT_ROOT}")
    for m in made:
        print("  ", os.path.relpath(m, BASE), f"({os.path.getsize(m)//1024} KB)")
