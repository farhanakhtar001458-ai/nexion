# RGPV B.Tech 1st Year · AI/ML (AIML) · Mid-Sem PYQ Research

**Deliverables:**
1. [`index.html`](./index.html) — interactive study guide (subject tabs, search, progress tracking, print/PDF support).
2. [`papers/`](./papers/README.md) — **78 PDF files**: 62 original RGPV papers (2009–2019) + 16 reconstructed English papers (2022–2026).
3. Ye `README.md` — poora research report sources ke saath.

Ek hi zip me sab kuch: repo ke **Releases** section se `rgpv-btech-first-year-pyq.zip` download kar lo (guide + saare PDFs).

Ye research RGPV ke public question-paper archives se banaya gaya hai, jisme **actual papers (2022 → June 2026)** ke questions extract kiye gaye hain aur **2018–2026** ke year-tags ke saath repeat-analysis di gayi hai.

---

## 1. Kaunse subjects? (AIML first year)

RGPV first year me branch-specific paper nahi hota — sab branches ko 2 sets me baant ke 10 common subjects padhaye jaate hain:

| Set | Subjects | Kaunsi branch | Sem |
|---|---|---|---|
| **SET-B** | BT-201 Engineering Physics, BT-202 Mathematics-II, BT-203 Basic Mechanical Engg., BT-204 Basic Civil Engg. & Mechanics, BT-205 Basic Computer Engg. | ME, CE, EC, **AIML (AL)**, CY, IP, AU | AIML ka **Sem-1** |
| SET-A | BT-101 Engineering Chemistry, BT-102 Mathematics-I, BT-103 English for Communication, BT-104 BEEE, BT-105 Engineering Graphics | CS, CSIT, EE, EX | AIML ka Sem-2 |

> AIML ke core papers (AL-304 Artificial Intelligence, AL-405 Machine Learning) **3rd–4th sem** me start hote hain. 1st year purely common subjects hai.
> Note: agar aapke college me AIML ko SET-A me rakha gaya ho, to Sem-1 me BT-101…BT-105 honge — unke saare paper links bhi guide ke "Sem-2 / SET-A" tab me diye hain.

## 2. Mid-sem (MSE) scheme

- RGPV scheme: **End-Sem 70 + Mid-Sem 20 + Quiz/Assignment 10 = 100** marks per theory subject.
- Har semester me **kam se kam 2 mid-sem tests** conduct karne hote hain (MSE-1, MSE-2).
- MSE-1 ka syllabus lagbhag sab college me **Unit 1 + Unit 2** hota hai; paper **college-level internal** hota hai (RGPV publish nahi karta).
- Isliye yahan ka repeat-analysis RGPV ke **end-sem papers** se banaya gaya hai — wahi questions colleges MSE me reuse karte hain.

## 3. Research method (kya-kya dekha gaya)

1. **Verbatim extraction:** 11 papers ke asli PDFs (Jun 2026, Dec 2025, Jun 2025, Jun 2024, Nov 2022 — 5 subjects) parse karke Unit 1-2 ke questions word-by-word nikale gaye.
   - Source index: <https://www.rgpvonline.com/rgpv-first-year.html> (B.TECH → ALL Branch 1st Year)
2. **Year-tagging (2018–2023):** unit-wise "Important Questions" compilations se purane saal ke tags liye gaye —
   - BT-201: <https://career-shiksha.com/post/important-rgpv-question-bt-201-engineering-physics-1styear/>
   - BT-203: <https://career-shiksha.com/post/important-rgpv-question-bt-203-basic-mechanical-engineering-1st-year/>
   - BT-205: <https://career-shiksha.com/post/important-rgpv-question-bt-205-basic-computer-engineering-1st-year/>
   - BT-205 (unit-wise, year-tagged PDF): <https://www.studocu.com/in/document/rajiv-gandhi-proudyogiki-vishwavidyalaya/basic-computer-engg/bce-computer-imp-important-privious-years-important-questions/101697818>
3. **Syllabus/unit mapping:**
   - BT-204: <https://www.rgpvnotes.in/btech/grading-system-old/qp/2018/12/basic-civil-engineering-mechanics-bt-204>
   - 1st year all-subject syllabus: <https://career-shiksha.com/post/syllabus-of-i-year-all-branch-all-subjects-rgpv/>
   - Scheme tables (70-20-10): RGPV scheme-of-examination PDFs + <https://indorestudents.com/rgpv-credit-based-grading-system-for-bachelor-of-engineering-b-e/>

## 4. Unit 1-2 (Mid-Sem) unit structure

| Subject | Unit 1 | Unit 2 |
|---|---|---|
| BT-201 Physics | Wave nature of particles & Schrödinger equation | Wave Optics |
| BT-202 Maths-II | ODE-I (first order) | ODE-II (higher order, variation of parameters, series) |
| BT-203 BME | Materials | Measurement & Production Engineering |
| BT-204 BCEM | Building Materials & Construction | Surveying & Positioning |
| BT-205 BCE | Computer & Operating System | Introduction to Algorithms & C++ |

(Unit 3-5 = MSE-2 / end-sem: Physics → solid state, lasers, electrostatics; Maths-II → PDE, complex variables, vector calculus; BME → fluids, thermodynamics, reciprocating machines; BCEM → mapping & sensing, forces & equilibrium, centroid/SFD-BMD; BCE → OOP/DS, networking & security, DBMS & cloud.)

## 5. Key findings (top repeats)

**BT-201 Physics**
- ★★★★★ Heisenberg uncertainty principle (gamma-ray microscope) — Dec 2022, Jun 2022, May 2019, Nov 2018, Dec 2025
- ★★★★★ Time-independent Schrödinger equation — Dec 2022, Jun 2022, Jun 2020, May 2018, Jun 2026, Dec 2025
- ★★★★★ Particle in 1-D box (+ numerical) — Jun 2022, Jun 2020, Jun 2026, Dec 2025
- ★★★★★ Newton's rings (+ numerical) — Dec 2020 → Dec 2025 lagbhag har saal
- ★★★★★ Michelson interferometer — Jun 2022, Dec 2020, May 2019, Dec 2025
- ★★★★★ Grating ki resolving power / Rayleigh criterion — Dec 2025 me resolving vs dispersive power ke saath

**BT-202 Maths-II**
- ★★★★★ Variation of parameters (`y''+y = tan x`, `= cosec x`, `(D²+a²)y = tan ax`) — Jun 2025, Dec 2025, Jun 2026
- ★★★★★ Cauchy–Euler / reducible-to-homogeneous (`(1+x)²y''+…`) — Jun 2025, Dec 2025, Jun 2026
- ★★★★ First-order: linear (IF), Bernoulli, homogeneous — har paper ka Q1
- ★★★★ Frobenius/series solution — Dec 2025, Jun 2025 (naya favourite)
- ★★★ J₁/₂(x) identity (Jun 2026), simultaneous equations (Dec 2025)

**BT-203 BME**
- ★★★★★ Iron–Carbon / Fe-Fe₃C diagram (phases, invariant reactions, critical temperatures) — Jun 2024, Dec 2025, Jun 2026
- ★★★★★ Lathe machine parts + operations — Nov 2022, Jun 2024, Dec 2025, Jun 2026 (4/4 papers)
- ★★★★★ Temperature measurement + optical pyrometer — same 4 papers
- ★★★★ Mechanical properties, stress–strain curve, alloy steels, Hooke's law
- ★★★★ Vernier calliper / sine-bar / slip gauge; errors in measurement

**BT-204 BCEM**
- ★★★★★ Levelling numerical (HI method & Rise-Fall + arithmetic check) — Nov 2022, Jun 2026
- ★★★★ Cement properties & tests; bricks & stones; theodolite
- ★★★★ Remote sensing applications — Nov 2022, Jun 2025, Jun 2026 (3 saal me 3 baar)
- ★★★ Contouring, GPS positioning, area & volume, footings, masonry, mortar, staircases/windows

**BT-205 BCE**
- ★★★★★ Operating system — functions + file/process/memory management — Dec 2022, Jun 2020, Dec 2025, Jun 2026
- ★★★★★ Classification of computers + CPU organization/block diagram — 2011 se Dec 2025 tak
- ★★★★★ OOP characteristics / POP vs OOP — Jun 2024, Dec 2025, Jun 2026
- ★★★★ Algorithm + flowchart (largest of 3 numbers) — Jun 2026, Dec 2025
- ★★★★ System vs application software; memory hierarchy & I/O devices; arrays & functions
- 📈 **Naya trend (2024+):** MS-Word/Excel/PowerPoint, cloud computing, e-commerce/social media, IT applications (healthcare/GIS/bioinformatics) wale questions aa rahe hain.

## 5.1 Downloads (PDF)

- Subah-shaam ke liye sabse aasan: repo ke **Releases** page se **`rgpv-btech-first-year-pyq.zip`** (~7 MB) download karo —
  usme ye guide (`index.html`) + saare 78 question papers PDF me hain.
- Individual PDF: [`papers/original-archive/`](./papers/original-archive) (asli scans, 2009–2019) aur
  [`papers/reconstructed-2022-2026/`](./papers/reconstructed-2022-2026) (saaf English, 2022–2026).
- Poori index: [`papers/INDEX.csv`](./papers/INDEX.csv) · [`papers/README.md`](./papers/README.md)

## 6. PYQ PDF links (direct)

Sabhi links `index.html` ke andar subject-wise archive me hain. Pattern:
`https://www.rgpvonline.com/be/<subject-slug>-<jun|dec|nov>-<year>.pdf`
e.g. `bt-202-mathematics-2-jun-2026.pdf`, `bt-201-engineering-physics-dec-2025.pdf`.

Available sessions (first year, dono sets): Jun 2020, Dec 2020, Jun 2022, Nov 2022, Jun 2023, Dec 2023, Jun 2024, Dec 2024, Jun 2025, Dec 2025, **Jun 2026**.

## 7. Limitations (honest disclosure)

- Mid-sem papers **college-level internal** hote hain aur public nahi hote — is guide ka repeat-analysis RGPV end-sem papers par based hai (jo MSE ka best predictor hain, par 100% identical nahi).
- Kuch year-slugs (2023, 2024 ke kuch papers) mirror par har waqt live nahi rehte; link fail ho to index page se manually kholein.
- Ye unofficial community resource hai; kisi bhi official claim ke liye RGPV circular/apne college ka MSE syllabus check karein.
