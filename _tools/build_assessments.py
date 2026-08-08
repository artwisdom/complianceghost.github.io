#!/usr/bin/env python3
"""Rebuild the four gap-assessment PDFs (ticket A0 + A1).

Why this exists: the originals were produced on the old Windows machine with no
generator in the repo, and they carried three defects that a lead magnet must
not have —

  1. a "30-day money-back guarantee" we do not offer (site terms say all sales
     are final). An advertised guarantee is enforceable; this one went out to
     every checklist lead.
  2. claims that do not survive checking: a $10M Travis County verdict that was
     actually a hospitalist group suing its management company (and is on
     appeal), an unsourced "less than half of dental offices are fully HIPAA
     compliant" (which also uses the "fully compliant" phrasing our own rules
     forbid), and an OCR "risk management" expansion that is really the Risk
     Analysis Initiative.
  3. a substantive legal error: the tattoo sheet told studios a notarized
     parental consent lets them tattoo a minor. Notarized consent is the BODY
     PIERCING rule. Tattooing under 18 is barred except to cover an existing
     tattoo, and then only with an affidavit, proof of identity and
     relationship, and a photo kept permanently (HSC 146.012; 25 TAC 229.406).

Plus the fourth sheet was an "Aesthetic Clinic" checklist about physician
delegation handed to leads who clicked "Esthetician Studio" — the wrong
regulator entirely. Its content is rebuilt from the esthetician question bank.

Every row here is sourced from assets/assessment.js, which was researched and
cited when the quiz was built, so the PDFs and the quiz now say the same thing.
Penalty figures re-verified 2026-08-07: OSHA $16,550 (serious, eff. Jan 15
2026), HIPAA $145-$73,011 per violation with a $2,190,294 annual cap (eff. Jan
28 2026), TMB/TSBDE/TDLR/DSHS $5,000 per violation with each day separate.

Usage:  python3 build_assessments.py <outdir>
"""
import sys
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, Spacer, Flowable, KeepTogether)

REPO = os.path.expanduser("~/Sites/complianceghost")
MARK = os.path.join(REPO, "assets", "mark.png")

NAVY = colors.HexColor("#1a2744")
INK = colors.HexColor("#1c2433")
INK2 = colors.HexColor("#4a5568")
INK3 = colors.HexColor("#8592ab")
RED = colors.HexColor("#b3261e")
GREEN = colors.HexColor("#0f6b47")
AMBER_BG = colors.HexColor("#fdf6e3")
AMBER_LN = colors.HexColor("#e0b400")
LINE = colors.HexColor("#d7deea")


def tint(c, frac):
    """Blend toward white; frac 0 = white, 1 = full colour."""
    return colors.Color(1 - (1 - c.red) * frac,
                        1 - (1 - c.green) * frac,
                        1 - (1 - c.blue) * frac)


class CheckBox(Flowable):
    """An empty box you can actually tick with a pen."""
    def __init__(self, size=9):
        Flowable.__init__(self)
        self.width = self.height = size

    def draw(self):
        c = self.canv
        c.setStrokeColor(colors.HexColor("#93a1b8"))
        c.setFillColor(colors.HexColor("#fbfcfe"))
        c.setLineWidth(0.9)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=1)


# ---- shared paragraph styles ------------------------------------------------
S_Q = ParagraphStyle("q", fontName="Helvetica", fontSize=8.7, leading=11.2, textColor=INK)
S_PEN = ParagraphStyle("pen", fontName="Helvetica", fontSize=7.5, leading=9.4,
                       textColor=RED, spaceBefore=2.2)
S_KIT = ParagraphStyle("kit", fontName="Helvetica", fontSize=7.5, leading=9.4,
                       textColor=GREEN, spaceBefore=1.4)
S_HDR = ParagraphStyle("hdr", fontName="Helvetica-Bold", fontSize=7.4, leading=9,
                       textColor=colors.white, alignment=1)
S_TITLE = ParagraphStyle("title", fontName="Helvetica", fontSize=19, leading=23)
S_SUB = ParagraphStyle("sub", fontName="Helvetica", fontSize=9, leading=12.5, textColor=INK2)
S_INTRO = ParagraphStyle("intro", fontName="Helvetica", fontSize=8.6, leading=12.2, textColor=INK)
S_LEGEND = ParagraphStyle("leg", fontName="Helvetica", fontSize=6.9, leading=9.2, textColor=INK3)
S_BAR = ParagraphStyle("bar", fontName="Helvetica-Bold", fontSize=10, leading=13,
                       textColor=colors.white)
S_SCORE = ParagraphStyle("score", fontName="Helvetica", fontSize=8.8, leading=13, textColor=INK)
S_CTA = ParagraphStyle("cta", fontName="Helvetica", fontSize=8.9, leading=13.4,
                       textColor=colors.white)
S_CTA_B = ParagraphStyle("ctab", fontName="Helvetica-Bold", fontSize=8.9, leading=13.4,
                         textColor=colors.white)

# Compact so the line stays scannable; the full basis is spelled out once in the
# legend under the intro box on page 1.
TMB = "up to $5,000 per violation, each day separate (TMB)"
OSHA = "up to $16,550 per serious violation (OSHA)"
OSHA_W = "up to $16,550 per serious violation, $165,514 if willful or repeated (OSHA)"
HIPAA = "$145–$73,011 per violation (HIPAA)"
TSBDE = "up to $5,000 per violation, each day separate (TSBDE)"
DSHS = "up to $5,000 per violation, each day separate (DSHS)"
TDLR = "up to $5,000 per violation, each day separate (TDLR)"

LEGEND = ("<b>Penalty basis:</b> TMB, TSBDE, TDLR, and DSHS may each assess up to $5,000 per "
          "violation under Occ. Code §165.001, §264.002, §51.302 and Health &amp; Safety Code "
          "§146.019, and each day a violation continues can be treated separately. OSHA serious "
          "violations reach $16,550 and willful or repeated ones $165,514. HIPAA civil penalties "
          "run $145–$73,011 per violation with a $2,190,294 annual cap for repeat violations of "
          "the same provision. OSHA and HIPAA amounts are the 2026 figures and adjust for "
          "inflation each January. Amounts shown are maximums, not predictions.")


# ---- the four sheets --------------------------------------------------------
# (question, penalty, what the Kit provides)
SHEETS = {
"medspa": {
  "file": "medspa-gap-assessment",
  "label": "MED SPA",
  "title": "Med Spa Documentation Gap Assessment",
  "sub": "Every item below maps to documentation, training, or templates included in the Compliance Ghost Kit.",
  "accent": colors.HexColor("#6d28d9"),
  "intro": "<b>How to use:</b> check YES, NO, or N/A for each item. Every “NO” is a documentation gap the $997 Compliance Kit fills with ready-to-use manuals, training guides, quizzes, certificates, forms, and templates. The green line shows exactly what the Kit provides for that item.",
  "sections": [
    ("WRITTEN PROTOCOLS & DELEGATION", [
      ("Do you have written delegation protocols (standing delegation orders) signed and dated by your delegating physician, and reviewed and re-signed within the last 12 months?",
       TMB + " — required under 22 TAC Chapter 169",
       "Physician Delegation Protocol templates + Annual Review Log"),
      ("Do your delegation documents cite the current rule, 22 TAC Chapter 169, rather than the repealed 22 TAC §193.17?",
       "Protocols citing a repealed rule are treated as out of date on inspection (Chapter 169 replaced §193.17 in January 2025)",
       "Updated Chapter 169 protocol set"),
      ("Before each new treatment, is every patient evaluated by a physician, PA, or APRN who issues an individualized treatment order documented in the chart?",
       TMB,
       "Patient Evaluation & Treatment Order forms"),
      ("For IV therapy and hydration: since September 1, 2025, are IVs administered only by an RN or above, with ordering delegated only to a PA or APRN?",
       "HB 3749 (“Jenifer’s Law”), effective September 1, 2025 — medical assistants, LVNs, and unlicensed staff may no longer administer elective IV therapy",
       "IV Therapy Protocol addendum + staff scope verification"),
      ("Is at least one BLS-trained person present whenever patients are treated, with the physician, PA, or APRN reachable per your protocol?",
       TMB,
       "Emergency Response Protocol + BLS Training Log"),
      ("Do you have a written OSHA Exposure Control Plan covering needle and cannula procedures, reviewed within the last 12 months?",
       OSHA + " — the plan must be reviewed annually (29 CFR 1910.1030(c))",
       "Exposure Control Plan template + annual update checklist"),
      ("Do you have a written Hazard Communication program with a chemical inventory for peels and disinfectants?",
       OSHA + " (29 CFR 1910.1200)",
       "HazCom program template + chemical inventory spreadsheet"),
      ("Do you have a written Emergency Action Plan with posted evacuation procedures?",
       OSHA,
       "Emergency Action Plan template + evacuation route posting"),
      ("Do you have a written PPE hazard assessment documenting the protective equipment each role requires?",
       OSHA,
       "PPE Hazard Assessment form + equipment selection guide"),
      ("Do you have a written breach notification plan with defined response procedures?",
       HIPAA + " — 60-day notification deadline",
       "Breach response plan + notification letter templates"),
      ("Do you have a written social media and online-review response policy that prevents PHI disclosure?",
       "A Dallas dental practice paid $10,000 to OCR after replying to a Yelp review with patient details (Elite Dental Associates, 2019)",
       "Social media policy template + staff training on PHI boundaries"),
    ]),
    ("RISK ANALYSIS & RECORDS", [
      ("Have you completed a HIPAA Security Risk Analysis within the last 12 months?",
       HIPAA + " — OCR reports risk analysis as its most frequently cited deficiency",
       "Step-by-step Security Risk Analysis workbook + documentation templates"),
      ("Do you have a documented risk management plan showing the corrective actions taken from that analysis?",
       "OCR’s Risk Analysis Initiative had completed 13 enforcement actions as of April 2026, with settlements starting at $10,000",
       "Risk management plan template with corrective action tracking"),
      ("Are complete treatment records — evaluation, consent, product lot numbers, photos — retained at least 7 years (for minors, until age 21 or 7 years, whichever is longer)?",
       "22 TAC Chapter 165 · " + TMB,
       "Records Retention Policy + chart completeness checklist"),
      ("Can you reconcile product purchased against product administered, with lot numbers and labeling retained for every vial?",
       "The FDA issued a warning letter to a Texas med spa on April 1, 2026 over exactly this gap — purchase-to-administration discrepancies and an unlabeled vial (fda.gov, letter #723267)",
       "Product Log + lot tracking sheets"),
    ]),
    ("TRAINING DOCUMENTATION", [
      ("Have all employees with blood or OPIM exposure completed bloodborne pathogen training within the past year?",
       OSHA + " — training records kept 3 years",
       "BBP training guide + quiz + completion certificates + training log"),
      ("Has every employee completed documented Texas privacy training within 90 days of hire, with signed and dated records?",
       "Health & Safety Code Chapter 181 (HB 300) — " + HIPAA,
       "HB 300 privacy training + signed acknowledgment log"),
      ("Has the supervising physician documented individual training verification for each provider and each delegated procedure?",
       TMB,
       "Provider training verification form for each delegated procedure"),
      ("Do you document that hepatitis B vaccination was offered to at-risk staff within 10 days of hire, with signed declinations on file?",
       OSHA + " (29 CFR 1910.1030(f))",
       "Hep B offer and declination forms + vaccination tracking log"),
    ]),
    ("POSTED NOTICES, CONSENT & STRUCTURE", [
      ("Is the TMB complaint notice posted in all public-facing areas?",
       TMB + " — posting requirement added January 2025",
       "Print-ready TMB complaint notice template"),
      ("Are the delegating physician’s name and Texas license number posted in every treatment room, with staff wearing name and credential badges?",
       TMB + " — posting and badge requirements added January 2025",
       "Treatment room posting template + badge specification"),
      ("Is a Notice of Privacy Practices provided to every patient and posted visibly?",
       HIPAA,
       "Notice of Privacy Practices template + acknowledgment form"),
      ("Are signed business associate agreements in place with every vendor that touches patient data (EMR, booking, photo storage)?",
       HIPAA,
       "BAA template customizable for all vendor types"),
      ("Do you maintain a sharps injury log?",
       OSHA,
       "Sharps Injury Log template"),
      ("Do you have complete informed consent forms for every medical procedure you offer?",
       TMB + ", plus malpractice exposure",
       "Informed consent templates for common med spa procedures"),
      ("If the business is not physician-owned, is your management services (MSO) arrangement documented consistently with the Texas prohibition on the corporate practice of medicine?",
       "Texas bars unlicensed entities from controlling medical decision-making; arrangements that cross the line have been unwound and litigated",
       "MSO agreement framework + compliance checklist"),
      ("If you offer laser hair removal: is the facility registered with TDLR, with a written consulting-physician contract and properly certified technicians?",
       TDLR + " (Health & Safety Code Chapter 401 Subchapter M; 16 TAC Chapter 118)",
       "LHR facility checklist + consulting physician contract"),
    ]),
  ]},

"dental": {
  "file": "dental-gap-assessment",
  "label": "DENTAL OFFICE",
  "title": "Dental Office Documentation Gap Assessment",
  "sub": "Every item below maps to documentation, training, or templates included in the Compliance Ghost Kit.",
  "accent": colors.HexColor("#1d4ed8"),
  "intro": "<b>How to use:</b> check YES, NO, or N/A for each item. A Texas dental office answers to TSBDE, federal OSHA, HIPAA and Texas HB 300, and the DSHS radiation control program at the same time. Every “NO” below is a documentation gap the $997 Compliance Kit fills.",
  "sections": [
    ("WRITTEN COMPLIANCE PLANS & PROTOCOLS", [
      ("Do you have a written infection control program with a designated infection control coordinator?",
       TSBDE + " — enforced through 22 TAC §108.24 and CDC guidance",
       "Infection control manual aligned with TSBDE and CDC"),
      ("Do you have a written OSHA Exposure Control Plan updated within the past 12 months?",
       OSHA + " — the plan must be reviewed annually (29 CFR 1910.1030(c))",
       "Exposure Control Plan template + annual update checklist"),
      ("Do you have a written Hazard Communication program with a chemical inventory?",
       OSHA + " (29 CFR 1910.1200)",
       "HazCom program template + chemical inventory spreadsheet"),
      ("Do you have a written Emergency Action Plan with evacuation procedures?",
       OSHA,
       "Emergency Action Plan template + evacuation posting template"),
      ("Do you have a written PPE hazard assessment?",
       OSHA,
       "PPE Hazard Assessment form + equipment selection guide"),
      ("Do you have a written breach notification plan with response procedures?",
       HIPAA + " — 60-day notification deadline",
       "Breach response plan + notification letter templates"),
      ("Do you have a written social media and online-review policy preventing PHI disclosure?",
       "Elite Dental Associates of Dallas paid $10,000 to OCR in 2019 after replying to a Yelp review with a patient’s name and treatment details",
       "Social media policy template + staff acknowledgment form"),
    ]),
    ("RISK ANALYSIS & AUDITS", [
      ("Have you completed a HIPAA Security Risk Analysis within the past 12 months?",
       HIPAA + " — OCR reports risk analysis as its most frequently cited deficiency",
       "Step-by-step Security Risk Analysis workbook"),
      ("Do you have a documented risk management plan with the corrective actions taken from that assessment?",
       "OCR’s Risk Analysis Initiative had completed 13 enforcement actions as of April 2026, with settlements starting at $10,000",
       "Risk management plan template with corrective action tracker"),
    ]),
    ("STERILIZATION & RADIATION SAFETY", [
      ("Is every sterilizer monitored with biological (spore) testing on a documented schedule — CDC guidance is at least weekly — with results retained?",
       TSBDE + " (22 TAC §108.24), plus infection control liability",
       "Sterilization monitoring log + spore test tracking form"),
      ("Do your sterilization logs record the date, time, and operator for every autoclave cycle?",
       TSBDE,
       "Sterilization log template (print-ready daily sheets)"),
      ("Is every dental x-ray machine — intraoral, panoramic, and cone-beam — registered with the DSHS radiation control program, with written operating and safety procedures available at the unit?",
       "25 TAC §§289.226 and 289.232 — DSHS administrative penalties apply",
       "Radiation registration tracker + written operating procedures"),
      ("Does every dental assistant who positions or exposes x-rays hold a current TSBDE dental assistant radiology certificate?",
       TSBDE,
       "Staff credential log covering licenses, certificates, and CE"),
    ]),
    ("TRAINING DOCUMENTATION", [
      ("Have all employees with blood or OPIM exposure completed annual bloodborne pathogen training?",
       OSHA + " — training records kept 3 years",
       "BBP training guide + quiz + completion certificates + training log"),
      ("Have all staff — front desk, billing, and clinical — completed documented privacy training within 90 days of hire?",
       "Health & Safety Code Chapter 181 (HB 300) — " + HIPAA,
       "HIPAA and HB 300 training guide + quiz + signed acknowledgment forms"),
      ("Do you document that hepatitis B vaccination was offered within 10 days of hire, with signed declinations on file?",
       OSHA,
       "Hep B declination form + vaccination tracking log"),
      ("Do you have documented employee training on chemical hazards (HazCom)?",
       OSHA,
       "HazCom training materials + completion log"),
    ]),
    ("FORMS, TEMPLATES & LOGS", [
      ("Is a Notice of Privacy Practices provided to every new patient and posted visibly?",
       HIPAA,
       "Notice of Privacy Practices template + patient acknowledgment form"),
      ("Are signed business associate agreements in place with every vendor that accesses PHI?",
       HIPAA,
       "BAA template customizable for any vendor type"),
      ("Do you maintain a sharps injury log recording all needlestick injuries?",
       OSHA,
       "Sharps Injury Log template"),
      ("Do you keep Safety Data Sheets in an organized, accessible binder or system?",
       OSHA,
       "SDS organization guide + employee access documentation"),
      ("Are patient records retained at least 5 years from the date of last treatment (for a minor, until age 21 or 5 years, whichever is longer)?",
       "22 TAC §108.8 · " + TSBDE,
       "Records retention schedule including the minors calculation"),
    ]),
  ]},

"tattoo": {
  "file": "tattoo-gap-assessment",
  "label": "TATTOO STUDIO",
  "title": "Tattoo Studio Documentation Gap Assessment",
  "sub": "Every item below maps to documentation, training, or templates included in the Compliance Ghost Kit.",
  "accent": colors.HexColor("#b91c1c"),
  "intro": "<b>How to use:</b> check YES, NO, or N/A for each item. DSHS inspects studios without notice, and inspectors start with your paperwork. A studio license runs about $927 for two years — the $997 Compliance Kit is what protects it.",
  "sections": [
    ("DSHS LICENSING & REQUIRED TRAINING", [
      ("Does the studio hold a current DSHS license for this location, covering the services you actually perform?",
       DSHS + " — operating unlicensed is its own violation",
       "License & Renewal Tracker"),
      ("Has every employee completed an approved human trafficking prevention training course, with proof kept on file?",
       "Health & Safety Code §146.0075, added by HB 1778 (2025) — no employee could be required to complete it before January 1, 2026. HHSC approves the courses and at least one is free; the approved list is posted by the department",
       "Human Trafficking Training Log + course links + completion certificates"),
      ("Are the human trafficking signs required by Government Code §402.0351 posted in the studio?",
       "Health & Safety Code §146.0075(c) · " + DSHS,
       "Required Postings Pack (print-ready)"),
      ("Do all artists have current bloodborne pathogen training certificates on file?",
       DSHS + " — expired certificates are a documentation finding on inspection",
       "BBP training guide + quiz + printable completion certificates"),
    ]),
    ("STERILIZATION & SANITATION", [
      ("Is every sterilization unit spore-tested every calendar month by a laboratory, with results retained?",
       "25 TAC §229.407 · " + DSHS,
       "Monthly Spore Test Log + laboratory submission guide"),
      ("Do your sterilization records show the date, instruments, and operator initials for every cycle?",
       "25 TAC §229.407 · " + DSHS + ". This is the most common inspection finding",
       "Sterilization Log template (print-ready daily sheets)"),
      ("Does every sterilized package carry a chemical or heat indicator confirming it went through a cycle?",
       "25 TAC §229.407 · " + DSHS,
       "Sterilization SOP + packaging checklist"),
      ("Are single-use items — needles, razors, ink caps, ointment portions — never reused between clients?",
       "25 TAC §229.407 · " + DSHS,
       "Station Setup & Teardown Checklist"),
    ]),
    ("CLIENT RECORDS & CONSENT", [
      ("Do you verify every client’s government-issued photo ID with date of birth before work begins?",
       "25 TAC §229.406 · " + DSHS,
       "Client Record & Consent form"),
      ("Does every client record capture the service, body location, ink colors with manufacturer and lot, and the artist — retained at least 2 years from the last entry?",
       "25 TAC §229.406 — records kept at the studio at least two years. " + DSHS,
       "Client Record & Consent form + retention policy guide"),
      ("For anyone under 18: do you decline all tattoos except the narrow cover-up exception — covering an existing tattoo — and only with a signed parental affidavit, proof of the parent’s identity and relationship, and a photo or written description kept in your permanent records?",
       "Health & Safety Code §146.012; 25 TAC §229.406. Tattooing a minor outside this exception is a criminal offense — a notarized consent form does NOT make it lawful",
       "Minor Cover-Up Affidavit + identity verification checklist"),
      ("If you also pierce: for a minor, do you obtain written notarized parental consent containing the required details, or have the parent present and verified at the studio?",
       "25 TAC §229.406 — the notarized-consent route applies to body piercing, not tattooing. " + DSHS,
       "Notarized Piercing Consent form (adult + minor versions)"),
      ("Does every client receive written aftercare instructions, with receipt documented?",
       "25 TAC §229.406 · " + DSHS + ". Verbal-only aftercare is not sufficient",
       "Print-ready aftercare instruction sheets"),
      ("Do you have a written procedure for reporting any infection or allergic reaction to DSHS in writing within five working days of learning of it?",
       "25 TAC §229.406 · " + DSHS,
       "Infection reporting procedure + DSHS notification form"),
    ]),
    ("OSHA, SHARPS & WASTE", [
      ("Are sharps collected in rigid, biohazard-labeled containers and removed by a registered medical waste transporter, with manifests retained?",
       "25 TAC §229.411; 30 TAC Chapter 326 · " + DSHS,
       "Sharps & Waste SOP + transporter manifest log"),
      ("Do you have a written OSHA Exposure Control Plan reviewed within the last 12 months?",
       OSHA + " — the plan must be reviewed annually (29 CFR 1910.1030(c))",
       "Exposure Control Plan template + annual update checklist"),
      ("Is annual bloodborne pathogens training documented with records kept 3 years, and hepatitis B vaccination offered to at-risk staff within 10 days of hire?",
       OSHA + " (29 CFR 1910.1030(f)–(h))",
       "Training Log + Hep B offer and declination forms"),
      ("Do you have a written Hazard Communication program with Safety Data Sheets for inks, soaps, and disinfectants in an accessible location?",
       OSHA + " (29 CFR 1910.1200)",
       "HazCom program + SDS binder + employee access log"),
      ("Do you have a documented new-employee orientation covering hygiene and safety procedures?",
       DSHS + ", plus " + OSHA,
       "New hire orientation checklist + safety training materials"),
    ]),
  ]},

"esthetician": {
  "file": "aesthetic-gap-assessment",
  "label": "ESTHETICIAN STUDIO",
  "title": "Esthetician Studio Documentation Gap Assessment",
  "sub": "Every item below maps to documentation, training, or templates included in the Compliance Ghost Kit.",
  "accent": colors.HexColor("#0d6b52"),
  "intro": "<b>How to use:</b> check YES, NO, or N/A for each item. TDLR inspects salons and studios without notice, and inspectors begin with your records and postings. Every “NO” below is a documentation gap the $997 Compliance Kit fills.",
  "sections": [
    ("TDLR LICENSING & POSTINGS", [
      ("Is every practitioner’s esthetician (or master esthetician) license current and displayed at their station?",
       TDLR + " (Occupations Code Chapters 1602 and 1603; 16 TAC Chapter 83)",
       "License & Renewal Tracker"),
      ("Is the establishment license itself — standard, specialty, or mini — current and displayed?",
       TDLR + " — operating without a current establishment license is a separate violation",
       "License & Renewal Tracker + renewal calendar"),
      ("If you rent booths, do you maintain a current renter list with names and license numbers, producible to TDLR on request?",
       "16 TAC §83.71 · " + TDLR,
       "Booth Renter Log"),
      ("Are the Chapter 83 health and safety rules and the human trafficking awareness sign posted where clients can see them?",
       "Occupations Code §1603.357; 16 TAC Chapter 83 — " + TDLR,
       "Required Postings Pack (print-ready)"),
      ("Is every licensee current on TDLR continuing education for the 2-year cycle, with certificates retained?",
       TDLR + " — CE shortfalls surface at renewal and on inspection",
       "CE Tracker + certificate file"),
    ]),
    ("SANITATION & DISINFECTION", [
      ("Do you use only EPA-registered bactericidal, fungicidal, and virucidal disinfectants, used strictly per the product label?",
       "16 TAC §§83.100–83.101 · " + TDLR,
       "Disinfection SOP + product selection guide"),
      ("Are immersion solutions, including bleach, mixed fresh daily and logged?",
       "16 TAC §§83.100–83.101 · " + TDLR,
       "Daily Solution Log"),
      ("Are multi-use implements cleaned and then disinfected before every client, with single-use items discarded and clean items stored correctly?",
       "16 TAC §§83.101–83.102 · " + TDLR,
       "Sanitation Checklist + storage guide"),
      ("Are foot spa cleaning and disinfection records kept on the TDLR-approved form and retained for 60 days?",
       "16 TAC §83.108 · " + TDLR,
       "Foot Spa Cleaning Log in the TDLR format"),
      ("For waxing: single-use applicators only, no double-dipping, and wax pots cleaned per the manufacturer’s instructions?",
       "16 TAC §83.105 · " + TDLR,
       "Waxing Service SOP"),
      ("Do you have a written blood and body-fluid response protocol, with the supplies on hand to match it?",
       "16 TAC §83.111 · " + TDLR,
       "Blood Exposure SOP card + supply list"),
    ]),
    ("SCOPE OF PRACTICE", [
      ("Do all services stay above the dermis — no injections, no medical needling, no deep peels, and nothing else that is a delegated medical act?",
       "16 TAC §83.112(c); 22 TAC Chapter 169. Crossing into medical procedures without physician delegation exposes you to " + TDLR + " and Texas Medical Board action",
       "Scope-of-Practice Guide with a depth and technique decision matrix"),
      ("Do you have a written referral procedure for clients who ask for services beyond an esthetician’s scope?",
       "16 TAC §83.112(c) · " + TDLR,
       "Medical Referral SOP + client-facing explanation script"),
      ("If a physician delegates any medical procedure performed on site, is that delegation documented in writing and reviewed annually?",
       "22 TAC Chapter 169 · " + TMB,
       "Delegation Protocol templates + Annual Review Log"),
    ]),
    ("OSHA & CHEMICAL SAFETY", [
      ("Do you have a written OSHA Exposure Control Plan, hepatitis B vaccination offers, and documented annual bloodborne pathogens training?",
       OSHA + " (29 CFR 1910.1030)",
       "Exposure Control Plan (salon edition) + training log + Hep B forms"),
      ("Is there a Safety Data Sheet for every chemical product, with all containers labeled — including anything decanted into a secondary container?",
       OSHA + " (29 CFR 1910.1200); 16 TAC §§83.102(n) and 83.114 — " + TDLR,
       "SDS Binder + labeling kit + storage checklist"),
      ("Are flammable and hazardous products stored per label directions, away from heat sources and client areas?",
       OSHA + "; 16 TAC §83.114 — " + TDLR,
       "Chemical Storage Checklist"),
    ]),
  ]},
}


def build(key, spec, outdir):
    accent = spec["accent"]
    path = os.path.join(outdir, spec["file"] + ".pdf")
    W, H = letter
    LM = RM = 0.62 * inch
    header_h = 74
    footer_h = 46

    def page_furniture(canv, doc):
        canv.saveState()
        # header band
        canv.setFillColor(NAVY)
        canv.rect(0, H - header_h, W, header_h, stroke=0, fill=1)
        canv.setFillColor(accent)
        canv.rect(0, H - header_h - 3.2, W, 3.2, stroke=0, fill=1)
        try:
            canv.drawImage(MARK, LM, H - header_h + 19, width=36, height=36,
                           mask="auto", preserveAspectRatio=True)
        except Exception:
            pass
        canv.setFillColor(colors.white)
        canv.setFont("Helvetica-Bold", 15.5)
        canv.drawString(LM + 46, H - header_h + 40, "COMPLIANCE GHOST")
        canv.setFont("Helvetica", 8.2)
        canv.setFillColor(colors.HexColor("#aab6cc"))
        canv.drawString(LM + 46, H - header_h + 26, "Texas Regulatory Compliance Documentation")
        # right pill
        txt = "%s  |  DOCUMENTATION GAP ASSESSMENT" % spec["label"]
        canv.setFont("Helvetica-Bold", 7.4)
        tw = canv.stringWidth(txt, "Helvetica-Bold", 7.4)
        pw, ph = tw + 20, 16
        px, py = W - RM - pw, H - header_h + 30
        canv.setFillColor(accent)
        canv.roundRect(px, py, pw, ph, 3, stroke=0, fill=1)
        canv.setFillColor(colors.white)
        canv.drawString(px + 10, py + 5, txt)
        # footer
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.7)
        canv.line(LM, footer_h + 8, W - RM, footer_h + 8)
        canv.setFont("Helvetica", 7)
        canv.setFillColor(INK3)
        canv.drawString(LM, footer_h - 6,
                        "COMPLIANCE GHOST  |  complianceghost.com  |  For assessment purposes only — "
                        "does not constitute legal advice.")
        canv.setFillColor(accent)
        canv.setFont("Helvetica-Bold", 7)
        canv.drawRightString(W - RM, footer_h - 6, "Page %d" % doc.page)
        canv.restoreState()

    doc = BaseDocTemplate(path, pagesize=letter,
                          leftMargin=LM, rightMargin=RM,
                          topMargin=header_h + 22, bottomMargin=footer_h + 18,
                          title="%s — Compliance Ghost" % spec["title"],
                          author="Compliance Ghost",
                          subject="Texas compliance documentation gap assessment")
    frame = Frame(LM, footer_h + 18, W - LM - RM,
                  H - (header_h + 22) - (footer_h + 18), id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=page_furniture)])

    avail = W - LM - RM
    ck = 52.0
    qw = avail - 3 * ck

    flow = []
    t = Paragraph('<font color="#%s">%s</font>' % (accent.hexval()[2:], spec["title"]), S_TITLE)
    flow += [t, Spacer(1, 3), Paragraph(spec["sub"], S_SUB), Spacer(1, 11)]

    intro = Table([[Paragraph(spec["intro"], S_INTRO)]], colWidths=[avail])
    intro.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), tint(accent, 0.10)),
        ("BOX", (0, 0), (-1, -1), 0.7, tint(accent, 0.35)),
        ("LEFTPADDING", (0, 0), (-1, -1), 13), ("RIGHTPADDING", (0, 0), (-1, -1), 13),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    legend = Table([[Paragraph(LEGEND, S_LEGEND)]], colWidths=[avail])
    legend.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 13), ("RIGHTPADDING", (0, 0), (-1, -1), 13),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    flow += [intro, legend, Spacer(1, 13)]

    for sec_title, rows in spec["sections"]:
        bar = Table([[Paragraph(sec_title, S_BAR)]], colWidths=[avail])
        bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), accent),
            ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))

        data = [["", Paragraph("YES", S_HDR), Paragraph("NO", S_HDR), Paragraph("N/A", S_HDR)]]
        for q, pen, kit in rows:
            cell = [Paragraph(q, S_Q),
                    Paragraph("<b>Rule &amp; penalty:</b> " + pen, S_PEN),
                    Paragraph("<b>KIT INCLUDES:</b> " + kit, S_KIT)]
            data.append([cell, CheckBox(), CheckBox(), CheckBox()])

        tbl = Table(data, colWidths=[qw, ck, ck, ck], repeatRows=1)
        st = [
            ("BACKGROUND", (0, 0), (-1, 0), tint(accent, 0.88)),
            ("GRID", (0, 0), (-1, -1), 0.6, LINE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (0, -1), 10), ("RIGHTPADDING", (0, 0), (0, -1), 10),
            ("TOPPADDING", (0, 1), (-1, -1), 8), ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
            ("TOPPADDING", (1, 1), (-1, -1), 11),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), tint(accent, 0.055)))
        tbl.setStyle(TableStyle(st))
        flow += [KeepTogether([bar, Spacer(1, 5)]), tbl, Spacer(1, 16)]

    score = Table([[Paragraph(
        "<b>YOUR SCORE:</b> ______ YES &nbsp;/&nbsp; ______ NO &nbsp;/&nbsp; ______ N/A"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>“NO” COUNT:</b> "
        '<font color="#0f6b47">0–2 low</font> &nbsp;·&nbsp; '
        '<font color="#9a6b00">3–5 medium</font> &nbsp;·&nbsp; '
        '<font color="#b3261e">6+ high</font>', S_SCORE)]], colWidths=[avail])
    score.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER_BG),
        ("BOX", (0, 0), (-1, -1), 1.0, AMBER_LN),
        ("LEFTPADDING", (0, 0), (-1, -1), 14), ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 11), ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    flow += [score, Spacer(1, 14)]

    cta_lines = [
        Paragraph("Every “NO” above is a documentation gap the Compliance Kit fills.", S_CTA_B),
        Spacer(1, 7),
        Paragraph("The Compliance Ghost Compliance Kit ($997) includes ready-to-use compliance "
                  "manuals, training guides with quizzes, completion certificates, the required forms "
                  "and templates, and a step-by-step implementation guide — covering every item on "
                  "this checklist, written for your business and delivered within 48 hours.", S_CTA),
        Spacer(1, 7),
        Paragraph("One-time purchase. Payment plans available: 3 × $349/mo. Compliance Shield is "
                  "optional and keeps these documents current as Texas rules change — $89/month or "
                  "$890/year, cancel anytime.", S_CTA),
        Spacer(1, 7),
        Paragraph("<b>complianceghost.com</b>", S_CTA),
    ]
    cta = Table([[cta_lines]], colWidths=[avail])
    cta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 18), ("RIGHTPADDING", (0, 0), (-1, -1), 18),
        ("TOPPADDING", (0, 0), (-1, -1), 15), ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
    ]))
    flow.append(KeepTogether(cta))

    doc.build(flow)
    return path


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(outdir, exist_ok=True)
    for key, spec in SHEETS.items():
        p = build(key, spec, outdir)
        n = sum(len(r) for _, r in spec["sections"])
        print("  %-12s %-34s %2d items  %6d bytes" % (key, os.path.basename(p), n,
                                                      os.path.getsize(p)))
