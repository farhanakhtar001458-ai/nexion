#!/usr/bin/env python3
"""
2026 Prediction engine.

Kya karta hai:
 1. prediction_data.py ke topics par frequency + recency + streak weight lagakar
    har question ki probability (%) nikalta hai aur bucket deta hai.
 2. "PREDICTION-2026.md" report likhta hai (repeat champions + predicted paper).
 3. index.html me "🔮 2026 Prediction" section inject karta hai.
 4. Ek PDF banata hai: papers/RGPV-2026-Most-Probable-Questions.pdf

Usage: python3 tools/build_prediction.py
"""
import os, re, sys, datetime, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from prediction_data import TOPICS, PREDICTED_PAPER, END_SEM
import build_pdfs as bp  # fonts + styles reuse (module import sirf fonts register karta hai)

from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

TODAY = datetime.date.today().strftime("%d %b %Y")
EXAM_YEAR = "2026"

# ---------------- probability engine ----------------
# observed sessions (Nov2022 se Jun2026 tak) -> order index
SESSIONS = {"Nov2022": 1, "Dec2022": 2, "Jun2023": 3, "Dec2023": 4, "Jun2024": 5,
            "Dec2024": 6, "Jun2025": 7, "Dec2025": 8, "Jun2026": 9}
RECENCY = {"2026": 1.00, "2025": 0.90, "2024": 0.78, "2023": 0.62, "2022": 0.55}

# Evidence-gap correction:
# Jun2023 / Dec2023 / Dec2024 ke papers publicly available nahi the, isliye raw score un
# "evergreen" topics ko under-rate kar deta hai jo actually lagataar aate hain (jaise levelling
# numerical, Newton's rings, OS functions). Ye chhota bonus us gap ko correct karta hai.
BOOST = {
 "BT-201": {"Heisenberg": 8, "Particle in one-dimensional": 8, "Newton's rings": 10,
            "Michelson": 12, "Plane transmission grating": 6, "Fraunhofer": 6, "Rayleigh": 6,
            "phase velocity": 5, "de Broglie": 6},
 "BT-202": {"Method of variation": 4, "Cauchy": 4, "Complementary function": 5,
            "Series solution": 5, "Bernoulli": 6, "Homogeneous / variable": 5},
 "BT-203": {"Stress": 6, "Mechanical properties": 5, "Iron": 4, "Lathe": 4,
            "Temperature measurement": 4, "Vernier": 5, "Viscosity": 5, "Hooke": 5},
 "BT-204": {"Levelling numerical": 16, "Cement": 16, "Theodolite": 14, "Contouring": 10,
            "Remote sensing": 8, "Bricks & stones": 8, "Stone masonry": 8, "Foundations": 8,
            "Staircases": 6, "Mortar": 6, "Plastering": 5},
 "BT-205": {"Operating system": 6, "CPU organization": 10, "Computer": 4, "Memory & storage": 6,
            "System software": 8, "MS-Word": 8, "Inheritance": 6, "Polymorphism": 8,
            "Algorithm": 5, "OOP characteristics": 6, "Scope resolution": 5,
            "Constructors": 5, "Looping": 4, "Instruction set": 6},
}

def year_of(tag):
    m = re.search(r"(19|20)\d{2}", tag)
    return m.group(0) if m else None

def session_index(tag):
    for name, idx in SESSIONS.items():
        if name.lower() in tag.lower():
            return idx
    return 0

def streak_bonus(idxs):
    """Latest sessions me lagataar aana = sabse strong signal."""
    s = set(idxs)
    if not s: return 0
    m = max(s)
    if m < 8: return 0
    run = 0
    while m - run in s: run += 1
    return min(run, 3) * (4 if m == 9 else 3)

def boost_for(code, topic):
    for key, val in BOOST.get(code, {}).items():
        if key.lower() in topic.lower():
            return val
    return 0

def score(code, topic, topic_years):
    """
    probability = frequency(recent sessions) 40%
                + recency(latest appearance)  40%
                + evergreen(old papers me bhi) 20%
                + streak(lagataar recent sessions) + gap-correction
    """
    idxs = [session_index(t) for t in topic_years]
    recent = sorted({i for i in idxs if i > 0})
    years = [year_of(t) for t in topic_years if year_of(t)]
    freq_recent = min(len(recent) / 4.0, 1.0)
    recency = max([RECENCY.get(y, 0.34) for y in years] or [0.34])
    old_years = {y for y in years if int(y) <= 2021}
    old_bonus = min(len(old_years) / 4.0, 1.0)
    p = 100 * (0.40 * freq_recent + 0.40 * recency + 0.20 * old_bonus)
    p += streak_bonus(idxs) + boost_for(code, topic)
    return int(max(28, min(97, round(p))))

def bucket(p):
    if p >= 82: return ("🔴 SURE-SHOT", "SURE")
    if p >= 68: return ("🟠 HIGH", "HIGH")
    if p >= 55: return ("🟡 MEDIUM", "MED")
    return ("⚪ SLEEPER (rotation)", "SLEEP")

def unit_label(u, code):
    if u.startswith("U4") and code == "BT-201":
        return "Unit 4 (Lasers & Fibre Optics)"
    return {"U1": "Unit 1", "U2": "Unit 2", "U3": "Unit 3", "U4": "Unit 4", "U5": "Unit 5"}.get(u, u)

# compute table
ROWS = {}
for code, items in TOPICS.items():
    out = []
    for unit, topic, years, kind in items:
        p = score(code, topic, years)
        b, key = bucket(p)
        out.append(dict(unit=unit, ulabel=unit_label(unit, code), topic=topic, years=years,
                        p=p, bucket=b, key=key, kind=kind))
    out.sort(key=lambda r: -r["p"])
    ROWS[code] = out

# ---------------- markdown report ----------------
SUBJ_NAME = {c: PREDICTED_PAPER[c]["name"] if c in PREDICTED_PAPER else c for c in TOPICS}

def md():
    L = []
    L.append(f"# 🔮 RGPV 1st Year (AI/ML) — {EXAM_YEAR} Exam: Most-Probable Questions\n")
    L.append(f"_Ye prediction 2022 → Jun 2026 ke **asli papers** (verbatim) + 2018-2023 ke year-tagged data par "
             f"frequency + recency + streak analysis se banaya gaya hai. Report date: {TODAY}._\n")
    L.append("## Kaise padho\n")
    L.append("- 🔴 **SURE-SHOT (82%+)**: ye chhoote to exam me gadbad. Pehle ye.\n"
             "- 🟠 **HIGH (68-81%)**: 5 me 3-4 baar aata hai.\n"
             "- 🟡 **MEDIUM (55-69%)**: choice wale questions me ghus jata hai.\n"
             "- ⚪ **SLEEPER**: 1-2 saal se nahi aaya, par history me repeat hua — rotation me wapas aa sakta hai.\n")
    for code, rows in ROWS.items():
        L.append(f"\n## {code} — {SUBJ_NAME.get(code, '')}\n")
        L.append("| Unit | Question/Topic | Kis-kis session me aaya | Probability | Level |")
        L.append("|---|---|---|---|---|")
        for r in rows:
            yrs = ", ".join(r["years"][-6:]) if r["years"] else "old"
            L.append(f"| {r['ulabel']} | {r['topic']} | {yrs} | **{r['p']}%** | {r['bucket']} |")
    L.append("\n## Predicted paper (Mid-Sem, Unit 1-2)\n")
    for code, pp in PREDICTED_PAPER.items():
        L.append(f"\n### {pp['code']} — {pp['name']} · {pp['exam']}\n_basis: {pp['basis']}_\n")
        for qno, parts in pp["qs"]:
            for part, text, lvl in parts:
                lbl = f"**{qno}{f'({part})' if part else ''}**"
                L.append(f"- {lbl} {text}  \n  `{ {'SURE':'🔴 SURE-SHOT','HIGH':'🟠 HIGH','MED':'🟡 MEDIUM'}[lvl] }`")
    L.append("\n## End-sem (Unit 3-5) most-probable topics\n")
    for code, items in END_SEM.items():
        L.append(f"\n### {code} — {SUBJ_NAME.get(code, '')}\n")
        for unit, topic, lvl in items:
            icon = {"SURE": "🔴", "HIGH": "🟠", "MED": "🟡"}[lvl]
            L.append(f"- {icon} `{unit}` {topic}")
    L.append("\n---\n")
    L.append("**Note:** Mid-sem papers college-level internal hote hain (public nahi). Ye prediction RGPV ke end-sem "
             "papers ke repeat-pattern par based hai — isliye probability 'aane ke chances' batati hai, guarantee nahi. "
             "Apne college ka syllabus/circular ek baar check kar lena.\n")
    return "\n".join(L)

# ---------------- HTML section ----------------
def htm():
    def table(code):
        rows = ROWS[code]
        tr = "".join(
            f'<tr><td>{r["ulabel"]}</td><td>{_html.escape(r["topic"])}</td>'
            f'<td class="yrs">{", ".join(r["years"][-6:])}</td>'
            f'<td><b class="p{"1" if r["p"]>=82 else "2" if r["p"]>=68 else "3" if r["p"]>=55 else "4"}">{r["p"]}%</b></td>'
            f'<td>{r["bucket"]}</td></tr>' for r in rows)
        return (f'<table class="pred"><thead><tr><th>Unit</th><th>Question / Topic</th><th>Sessions</th>'
                f'<th>Probability</th><th>Level</th></tr></thead><tbody>{tr}</tbody></table>')

    def paper(code):
        pp = PREDICTED_PAPER[code]
        out = [f'<div class="unit"><h4>{pp["code"]} — {pp["name"]} <span class="pill">{pp["exam"]}</span></h4>',
               f'<div class="hint">basis: {pp["basis"]} · Total 8 questions, "attempt any five" · har question 14 marks</div><ul class="q">']
        for qno, parts in pp["qs"]:
            for part, text, lvl in parts:
                badge = {"SURE": "🔴 SURE", "HIGH": "🟠 HIGH", "MED": "🟡 MED"}[lvl]
                lbl = f'{qno}{f"({part})" if part else ""}'
                out.append(f'<li><span></span><div><div class="qtext"><b>{lbl}</b> {_html.escape(text)}</div>'
                           f'<div class="meta"><span class="yr">{badge}</span></div></div></li>')
        out.append("</ul></div>")
        return "".join(out)

    def endsem(code):
        items = END_SEM.get(code, [])
        li = "".join(f'<li><span></span><div><div class="qtext">{ {"SURE":"🔴","HIGH":"🟠","MED":"🟡"}[lvl] } '
                     f'<b>{u}</b> — {_html.escape(t)}</div></div></li>' for u, t, lvl in items)
        return f'<ul class="q">{li}</ul>'

    legend = ('<div class="trend"><b>Legend:</b> 🔴 <b>SURE-SHOT (85%+)</b> — ye chhoote to gadbad · '
              '🟠 <b>HIGH (68-81%)</b> · 🟡 <b>MEDIUM (55-69%)</b> · ⚪ <b>SLEEPER</b> — 1-2 saal se nahi aaya, '
              'rotation me wapas aa sakta hai.</div>')

    how = ('<div class="warn"><b>Ye prediction kaise bani?</b> 2022 → Jun 2026 ke asli papers (verbatim) + 2018-2023 ke '
           'year-tagged data, teen weight ke saath: <b>frequency</b> (kitne saal aaya) + <b>recency</b> (last appearance '
           'kitni recent) + <b>streak</b> (lagataar aa raha hai ya nahi). Isliye "90%+" = 4+ saal me repeat + haal hi me '
           'aaya. Mid-sem papers college-level internal hote hain, isliye ye end-sem pattern par based prediction hai — '
           'guide ka "probability" = aa jaane ke chances, guarantee nahi.</div>')

    subj_tabs = "".join(
        f'<div class="unit"><h4>{code} — {SUBJ_NAME.get(code,"")}</h4>{table(code)}</div>' for code in ROWS)

    sec = f'''  <!-- PREDICT:START -->
  <section class="subject" id="predict">
    <div class="panel">
      <h2>🔮 {EXAM_YEAR} Exam — Most-Probable Questions <span class="pill b">frequency + recency + streak analysis</span></h2>
      <p class="sub">Neeche har subject ke questions <b>probability %</b> ke saath hain. Phir poora
      <b>predicted paper</b> (mid-sem, Unit 1-2) aur <b>end-sem ke Unit 3-5 topics</b> diye hain.
      Report date: {TODAY}.</p>
      {legend}
      {how}

      <h3>1️⃣ Repeat-champions — kaun baar-baar aa raha hai (subject-wise probability table)</h3>
      <div class="grid2">{subj_tabs}</div>

      <h3>2️⃣ Predicted Paper — Mid-Sem (Unit 1-2), "attempt any five"</h3>
      <p class="sub">Ye wahi 8 questions hain jo sabse zyada repeat ho rahe hain — inhe exam se pehle likh ke practice karo.
      Har subject me a/b parts ko usi tarah combine kiya gaya hai jaise RGPV karta hai.</p>
      <div class="grid2">{"".join(paper(c) for c in PREDICTED_PAPER)}</div>

      <h3>3️⃣ End-Sem ke liye (Unit 3, 4, 5) most-probable topics</h3>
      <p class="sub">Mid-sem ke baad ka syllabus — same analysis se top topics.</p>
      <div class="grid2">{"".join(f'<div class="unit"><h4>{c} — {SUBJ_NAME.get(c,"")}</h4>{endsem(c)}</div>' for c in END_SEM)}</div>

      <h3>4️⃣ 10-din ka final revision plan (prediction-first)</h3>
      <table>
        <tr><th>Din</th><th>Kaam</th></tr>
        <tr><td>Day 1-2</td><td>BT-201 Physics: uncertainty principle, TISE, 1-D box (numerical), Newton's rings numerical — 🔴 wale 5 topics ke answers likho.</td></tr>
        <tr><td>Day 3</td><td>BT-201 Unit 2: Michelson, grating resolving power, Fraunhofer 4.5%, NA/acceptance angle.</td></tr>
        <tr><td>Day 4</td><td>BT-202: variation of parameters + Cauchy–Euler (dono 🔴, lagataar 3 papers me) + linear/Bernoulli.</td></tr>
        <tr><td>Day 5</td><td>BT-202: Frobenius series + CF/PI + Bessel identity; predicted paper ke Q1-Q8 solve.</td></tr>
        <tr><td>Day 6</td><td>BT-205: OS functions, block diagram/CPU, algorithm+flowchart, OOP vs POP, inheritance, polymorphism.</td></tr>
        <tr><td>Day 7</td><td>BT-203: Fe–Fe₃C diagram (3 baar draw karo), stress-strain + numerical, lathe parts, optical pyrometer.</td></tr>
        <tr><td>Day 8</td><td>BT-204: cement/bricks/stones, footings, levelling numerical (HI + Rise-Fall), theodolite, remote sensing.</td></tr>
        <tr><td>Day 9</td><td>Predicted paper ka <b>mock</b>: 5 questions 3 ghante me, bina notes.</td></tr>
        <tr><td>Day 10</td><td>Sleeper (⚪) topics sirf short-note level par; formula sheet revise.</td></tr>
      </table>
      <div class="warn">
        <b>Sabse important 10 "lagbhag pakka" (sab subjects milakar):</b> Fe–Fe₃C diagram ·
        variation of parameters · Cauchy–Euler · uncertainty principle · TISE + 1-D box ·
        Newton's rings numerical · OS functions + file/process/memory · algorithm + flowchart ·
        POP vs OOP · levelling numerical (HI/Rise-Fall). <b>Inme se har subject ka kam se kam 2 question
        aana hi aana hai</b> — pehle inhe 100% karo.
      </div>
      <p class="sub">PDF version: <code>papers/RGPV-2026-Most-Probable-Questions.pdf</code> (is repo me) — print karke
      wall par chipka lo. Poora markdown report: <code>PREDICTION-2026.md</code>.</p>
    </div>
  </section>
  <!-- PREDICT:END -->

'''
    return sec

# ---------------- PDF ----------------
def pdf():
    out = os.path.join(BASE, "papers", "RGPV-2026-Most-Probable-Questions.pdf")
    S = dict(bp.S)
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=13*mm, rightMargin=13*mm,
                          topMargin=12*mm, bottomMargin=16*mm,
                          title=f"RGPV 1st Year (AI/ML) — {EXAM_YEAR} Most-Probable Questions",
                          author="RGPV PYQ study archive")
    doc.subject_code, doc.session = "PREDICTION", EXAM_YEAR
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=bp.footer)])

    F = [Paragraph(f"RGPV B.Tech 1st Year (AI/ML) — {EXAM_YEAR}", bp.S["h1"]),
         Paragraph("MOST-PROBABLE QUESTIONS (Unit-wise probability analysis)", bp.S["h2"]),
         Paragraph(f"Based on actual papers Nov 2022 → Jun 2026 · Generated {TODAY} · unofficial study material", bp.S["meta"]),
         Spacer(1, 5), HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#888888")), Spacer(1, 5),
         Paragraph("<b>Legend:</b> 🔴 SURE-SHOT 82%+ · 🟠 HIGH 68-81% · 🟡 MEDIUM 55-69% · ⚪ SLEEPER (rotation). "
                   "Probability = frequency + recency + streak weight (2022-2026 papers se).", bp.S["note"]),
         Spacer(1, 8)]

    for code, rows in ROWS.items():
        F.append(Paragraph(f"{code} — {SUBJ_NAME.get(code,'')}", bp.S["h3"]))
        F.append(Spacer(1, 3))
        data = [[Paragraph("<b>Unit</b>", bp.S["q"]), Paragraph("<b>Question / Topic</b>", bp.S["q"]),
                 Paragraph("<b>Sessions</b>", bp.S["q"]), Paragraph("<b>Prob.</b>", bp.S["q"]),
                 Paragraph("<b>Level</b>", bp.S["q"])]]
        for r in rows:
            data.append([Paragraph(r["ulabel"].replace("Unit ", "U"), bp.S["q"]),
                         Paragraph(_html.escape(r["topic"]), bp.S["q"]),
                         Paragraph(", ".join(r["years"][-5:]), bp.S["q"]),
                         Paragraph(f"<b>{r['p']}%</b>", bp.S["q"]),
                         Paragraph(r["bucket"], bp.S["q"])])
        t = Table(data, colWidths=[13*mm, doc.width-13*mm-52*mm-15*mm-30*mm, 52*mm, 15*mm, 30*mm], repeatRows=1)
        t.setStyle(TableStyle([("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#999999")),
                               ("VALIGN", (0,0), (-1,-1), "TOP"),
                               ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#eeeeee")),
                               ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 2),
                               ("FONTSIZE", (0,0), (-1,-1), 7.6), ("LEFTPADDING", (0,0), (-1,-1), 3)]))
        F.append(t); F.append(Spacer(1, 7))

    for code, pp in PREDICTED_PAPER.items():
        F.append(Paragraph(f"Predicted Paper — {pp['code']} {pp['name']} ({pp['exam']})", bp.S["h3"]))
        F.append(Paragraph(f"<i>{pp['basis']}</i> · attempt any five · 14 marks each", bp.S["meta"]))
        F.append(Spacer(1, 3))
        rows = []
        for qno, parts in pp["qs"]:
            first = True
            for part, text, lvl in parts:
                badge = {"SURE": "🔴", "HIGH": "🟠", "MED": "🟡"}[lvl]
                rows.append([Paragraph(f"{qno}." if first else "", bp.S["qn"]),
                             Paragraph(f"{badge} {f'({part}) ' if part else ''}{_html.escape(text)}", bp.S["q"])])
                first = False
            rows.append([Spacer(1, 5), ""])
        t = Table(rows, colWidths=[10*mm, doc.width-10*mm])
        t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("TOPPADDING", (0,0), (-1,-1), 2),
                               ("BOTTOMPADDING", (0,0), (-1,-1), 2)]))
        F.append(t); F.append(Spacer(1, 6))

    F.append(Paragraph("End-Sem (Unit 3-5) — Most-probable topics", bp.S["h2"])); F.append(Spacer(1, 4))
    for code, items in END_SEM.items():
        F.append(Paragraph(f"{code} — {SUBJ_NAME.get(code,'')}", bp.S["h3"]))
        li = "".join(f"{ {'SURE':'🔴','HIGH':'🟠','MED':'🟡'}[lvl] } <b>{u}</b> {_html.escape(t)}<br/>" for u, t, lvl in items)
        F.append(Paragraph(li, bp.S["q"])); F.append(Spacer(1, 5))

    F.append(Spacer(1, 6)); F.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    F.append(Spacer(1, 4))
    F.append(Paragraph("Mid-sem papers college-level internal hote hain (public nahi) — ye prediction RGPV ke end-sem papers ke "
                       "repeat-pattern par based hai, isliye probability 'chances' batati hai, guarantee nahi. Exam se pehle apne "
                       "college ka syllabus/circular verify karein. Papers RGPV ki property hain — free study use only.", bp.S["small"]))
    doc.build(F)
    return out

# ---------------- run ----------------
if __name__ == "__main__":
    # 1) markdown
    open(os.path.join(BASE, "PREDICTION-2026.md"), "w", encoding="utf-8").write(md())

    # 2) inject into index.html
    p = os.path.join(BASE, "index.html")
    h = open(p, encoding="utf-8").read()
    section = htm()
    if "<!-- PREDICT:START -->" in h:
        h = re.sub(r"<!-- PREDICT:START -->.*?<!-- PREDICT:END -->\n\n", section, h, flags=re.S)
    else:
        h = h.replace('  <section class="subject" id="sources">', section + '  <section class="subject" id="sources">', 1)

    # tab button + activation (idempotent)
    if 'data-t="predict"' not in h:
        h = h.replace("""'<button data-t="pdfs">📄 PDF Archive</button>' +""",
                      """'<button data-t="pdfs">📄 PDF Archive</button>' +\n  '<button data-t="predict">🔮 2026 Prediction</button>' +""")
    h = h.replace('if(id === "guide" || id === "plan" || id === "seta" || id === "sources" || id === "pdfs"){',
                  'if(id === "guide" || id === "plan" || id === "seta" || id === "sources" || id === "pdfs" || id === "predict"){')

    # prediction tables ke liye chhota CSS
    if ".pred{" not in h:
        css = """
  table.pred{width:100%;border-collapse:collapse;font-size:12.6px;margin-top:8px}
  table.pred th,table.pred td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
  table.pred th{background:#ffffff0f;color:#fff}
  table.pred td.yrs{color:var(--muted);font-size:11.5px}
  table.pred b.p1{color:#4ade80} table.pred b.p2{color:#fbbf24}
  table.pred b.p3{color:#7dd3fc} table.pred b.p4{color:var(--muted)}
"""
        h = h.replace("  footer{", css + "  footer{", 1)

    open(p, "w", encoding="utf-8").write(h)

    # 3) PDF
    fp = pdf()
    print("wrote PREDICTION-2026.md, index.html section, and", os.path.relpath(fp, BASE))
    print("\nTop probabilities per subject (top 4):")
    for code, rows in ROWS.items():
        print(f"  {code}: " + " | ".join(f"{r['p']}% {r['topic'][:42]}" for r in rows[:4]))
