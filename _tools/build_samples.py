#!/usr/bin/env python3
"""Generate the dental / tattoo / esthetician sample-manual pages.

The homepage advertises "Preview first — free samples" as a core trust plank,
but only med spa had one. Three of four industries could not see what $997 buys.

These reuse /sample-manual/ as the template so the design stays identical and
there is one place to change it. Content is sourced from the material already
published and verified on the money pages, the guides, and the assessment
question bank — nothing new is asserted here.

NOTE: each table of contents becomes the build spec for that vertical's Kit,
exactly as the med spa TOC did. If you change a chapter here, change it there.

Run: python3 _tools/build_samples.py
"""
import os
import re
import sys

REPO = os.path.expanduser("~/Sites/complianceghost")
TEMPLATE = "sample-manual/index.html"

V = {}

V["dental"] = dict(
    slug="dental", pages=46, money="/dental/", label="Dental Office",
    title="Sample Compliance Manual — Texas Dental Office | Compliance Ghost",
    desc=("Sample Texas Dental Office Compliance Manual covering TSBDE, DSHS radiation "
          "control, OSHA, and HIPAA/HB 300. Preview of the full 46-page manual included "
          "in the Compliance Kit."),
    h1="Texas Dental Office<br>Compliance Manual",
    subtitle="Complete Regulatory Guide &amp; Operations Handbook",
    badges=["TSBDE", "DSHS", "OSHA", "HIPAA", "HB 300"],
    toc=[
        ("Regulatory Overview &amp; Agency Guide", [
            ("Texas State Board of Dental Examiners (TSBDE)", 3),
            ("DSHS Radiation Control Program", 6),
            ("Federal OSHA Standards for Dental Offices", 9),
            ("HIPAA and Texas HB 300", 12)]),
        ("Infection Control &amp; Sterilization", [
            ("Written Infection Control Program", 15),
            ("Sterilization Monitoring &amp; Spore Testing", 17),
            ("Instrument Processing Workflow", 19),
            ("Surface Disinfection &amp; Water Quality", 21)]),
        ("Radiation Safety &amp; X-Ray Registration", [
            ("Machine Registration with DSHS", 23),
            ("Operator Credentials &amp; Radiology Certificates", 25),
            ("ALARA, Shielding &amp; Patient Protection", 27)]),
        ("OSHA Safety &amp; Workplace Standards", [
            ("Bloodborne Pathogens Standard", 29),
            ("Hazard Communication &amp; SDS Management", 31),
            ("Sharps Handling &amp; Medical Waste", 33),
            ("Emergency Action Plan", 35)]),
        ("HIPAA, HB 300 &amp; Patient Records", [
            ("Privacy Rule &amp; Notice Requirements", 37),
            ("Security Risk Analysis", 39),
            ("Breach Notification Procedures", 41),
            ("Records Retention (22 TAC &sect;108.8)", 42)]),
        ("Appendix: Forms, Templates &amp; Checklists", [
            ("Consent &amp; Treatment Forms", 43),
            ("Incident &amp; Exposure Reports", 45),
            ("Monthly Compliance Audit Checklist", 46)]),
    ],
    ch1_intro=[
        "A Texas dental office answers to four separate authorities at the same time, and "
        "each one asks for different paperwork. The state board sets professional and "
        "recordkeeping standards, a separate state program registers every x-ray machine "
        "in the building, federal OSHA governs staff safety, and federal and Texas privacy "
        "law both apply to the same patient record.",
        "None of them coordinate with each other. An office can be entirely current with "
        "the dental board and still be cited for an unregistered panoramic unit or an "
        "Exposure Control Plan that was never reviewed. This chapter sets out who asks for "
        "what, so nothing falls between the agencies.",
    ],
    agencies=[
        ("Texas State Board of Dental Examiners (TSBDE)",
         "Professional conduct, recordkeeping, infection control",
         "Dental Practice Act (Occupations Code Ch. 251&ndash;267), 22 TAC Part 5, sterilization monitoring, records retention"),
        ("DSHS Radiation Control Program",
         "Every radiation-emitting machine",
         "Registration of intraoral, panoramic and cone-beam units, written operating and safety procedures, ALARA"),
        ("Federal OSHA",
         "Employee safety",
         "Bloodborne Pathogens (29 CFR 1910.1030), Hazard Communication (29 CFR 1910.1200), sharps injury log"),
        ("HHS Office for Civil Rights &amp; Texas AG",
         "Patient privacy and data security",
         "HIPAA Privacy and Security Rules, Texas HB 300 (Health &amp; Safety Code Ch. 181)"),
    ],
    callouts=[
        ("info", "Regulatory Reference",
         "<strong>22 TAC &sect;108.8 &mdash; Records of the Dentist.</strong> Dental records must be kept for at "
         "least five years from the date of last treatment. Where the patient was a minor at the time of last "
         "treatment, records are kept until the patient turns 21 or for five years, whichever is longer. Other "
         "rules &mdash; Medicaid, billing, malpractice &mdash; can require longer, so keep records at least as "
         "long as the strictest requirement that applies to you."),
        ("warning", "Where Penalties Come From",
         "TSBDE may assess administrative penalties of up to <strong>$5,000 per violation</strong>, with each day "
         "a violation continues treated as a separate violation (Tex. Occupations Code &sect;264.002). Federal OSHA "
         "penalties reach <strong>$16,550</strong> for a serious violation and <strong>$165,514</strong> for willful "
         "or repeated ones. HIPAA civil penalties run <strong>$145&ndash;$73,011</strong> per violation with an annual "
         "cap of <strong>$2,190,294</strong> for repeat violations of the same provision. These are statutory maximums, "
         "not predictions &mdash; and OSHA and HIPAA amounts adjust for inflation every January."),
        ("tip", "The Practical Point",
         "Almost every requirement in this manual is satisfied by a document that already exists or a log that gets "
         "filled in. Regulators look for evidence a program is running &mdash; dated logs, signed acknowledgments, "
         "current plans &mdash; not for a binder of policies nobody follows."),
    ])

V["tattoo"] = dict(
    slug="tattoo", pages=38, money="/tattoo/", label="Tattoo Studio",
    title="Sample Compliance Manual — Texas Tattoo Studio | Compliance Ghost",
    desc=("Sample Texas Tattoo Studio Compliance Manual covering DSHS licensing, "
          "sterilization records, client consent, and OSHA. Preview of the full 38-page "
          "manual included in the Compliance Kit."),
    h1="Texas Tattoo Studio<br>Compliance Manual",
    subtitle="Complete Regulatory Guide &amp; Operations Handbook",
    badges=["DSHS", "TCEQ", "OSHA", "HSC Ch. 146"],
    toc=[
        ("Regulatory Overview &amp; Agency Guide", [
            ("Texas DSHS &mdash; Studio Licensing", 3),
            ("TCEQ &mdash; Medical Waste Rules", 6),
            ("Federal OSHA Standards", 8)]),
        ("Licensing &amp; Required Training", [
            ("Studio License &amp; Renewal", 11),
            ("Bloodborne Pathogen Certificates", 13),
            ("Human Trafficking Prevention Training (&sect;146.0075)", 15),
            ("Required Postings &amp; Signage", 16)]),
        ("Sterilization &amp; Sanitation", [
            ("Monthly Spore Testing (25 TAC &sect;229.407)", 17),
            ("Sterilization Records &amp; Package Indicators", 19),
            ("Single-Use Items &amp; Station Setup", 21)]),
        ("Client Records, Consent &amp; Minors", [
            ("Identity Verification &amp; Client Records", 23),
            ("Two-Year Retention Requirements", 25),
            ("Minors: the Narrow Cover-Up Exception", 26),
            ("Aftercare &amp; Infection Reporting", 28)]),
        ("OSHA, Sharps &amp; Waste Handling", [
            ("Exposure Control Plan", 30),
            ("Training, Hepatitis B &amp; Records", 32),
            ("Sharps Containers &amp; Waste Manifests", 34)]),
        ("Appendix: Forms, Logs &amp; Checklists", [
            ("Client Record &amp; Consent Forms", 35),
            ("Sterilization &amp; Spore Test Logs", 37),
            ("Monthly Compliance Audit Checklist", 38)]),
    ],
    ch1_intro=[
        "There is no single Texas license that covers everything a tattoo studio does. The "
        "health department licenses the studio and inspects it without notice, a separate "
        "environmental agency governs what happens to your sharps after they leave the "
        "station, and federal OSHA applies from the moment you have one employee.",
        "Inspections here are records-first. An inspector who walks in will ask for your "
        "license, your spore test results, your client records, and your waste manifests "
        "before looking at anything else. This chapter sets out which agency asks for what.",
    ],
    agencies=[
        ("Texas DSHS",
         "Studio licensing and operating standards",
         "Health &amp; Safety Code Ch. 146 and 25 TAC Ch. 229 Subchapter V &mdash; licensing, sterilization, client records, "
         "and the employee human trafficking prevention training added by &sect;146.0075"),
        ("TCEQ",
         "Medical waste handling and transport",
         "30 TAC Ch. 326 &mdash; sharps containers, storage limits, transporters and manifests"),
        ("Federal OSHA",
         "Employee safety",
         "Bloodborne Pathogens (29 CFR 1910.1030) applies once you have employees; universal precautions apply to everyone"),
    ],
    callouts=[
        ("warning", "New Since January 2026",
         "<strong>Health &amp; Safety Code &sect;146.0075</strong>, added by HB 1778 in 2025, requires <strong>every "
         "employee</strong> of a tattoo or body piercing studio to complete a human trafficking prevention training "
         "course approved by the state. No employee could be required to complete one before <strong>January 1, "
         "2026</strong> &mdash; a date that has now passed. At least one approved course is free, and the department "
         "publishes the approved list. Studios must separately post the human trafficking signs required by Government "
         "Code &sect;402.0351. Signage and training are different duties; doing one does not satisfy the other."),
        ("info", "Regulatory Reference",
         "<strong>25 TAC &sect;229.406 and &sect;229.407.</strong> Client records are kept at the studio for at least "
         "<strong>two years</strong> from the date of last entry. Every sterilization unit is spore-tested "
         "<strong>every calendar month</strong> by a laboratory with results retained. Any infection or allergic "
         "reaction is reported to the department in writing <strong>within five working days</strong> of learning of it."),
        ("tip", "The Minor Rule People Get Wrong",
         "Notarized parental consent is the <strong>body piercing</strong> rule. Tattooing anyone under 18 is prohibited "
         "<strong>except</strong> to cover an existing tattoo, and then only with a parental affidavit, proof of the "
         "parent&rsquo;s identity and relationship, and a photo or written description kept in your permanent records "
         "(Health &amp; Safety Code &sect;146.012; 25 TAC &sect;229.406). Getting this backwards is a criminal exposure, "
         "not a paperwork one."),
    ])

V["esthetician"] = dict(
    slug="esthetician", pages=36, money="/esthetician/", label="Esthetician Studio",
    title="Sample Compliance Manual — Texas Esthetician Studio | Compliance Ghost",
    desc=("Sample Texas Esthetician Studio Compliance Manual covering TDLR licensing, "
          "sanitation, scope of practice, and OSHA. Preview of the full 36-page manual "
          "included in the Compliance Kit."),
    h1="Texas Esthetician Studio<br>Compliance Manual",
    subtitle="Complete Regulatory Guide &amp; Operations Handbook",
    badges=["TDLR", "OSHA", "16 TAC Ch. 83"],
    toc=[
        ("Regulatory Overview &amp; Agency Guide", [
            ("TDLR &mdash; Licensing &amp; Establishment Rules", 3),
            ("Where TDLR Ends and the Medical Board Begins", 6),
            ("Federal OSHA Standards for Salons", 8)]),
        ("Licensing, Postings &amp; Renewals", [
            ("Practitioner &amp; Establishment Licenses", 10),
            ("Booth Renters &amp; the Renter List (&sect;83.71)", 12),
            ("Required Postings &amp; Trafficking Signage", 13),
            ("Continuing Education &amp; Renewal Cycle", 14)]),
        ("Sanitation &amp; Disinfection", [
            ("EPA-Registered Disinfectants (&sect;&sect;83.100&ndash;83.101)", 15),
            ("Implement Cleaning &amp; Storage", 17),
            ("Foot Spa Cleaning Logs (&sect;83.108)", 19),
            ("Waxing Services &amp; Wax Pot Hygiene (&sect;83.105)", 21),
            ("Blood Exposure Response (&sect;83.111)", 22)]),
        ("Scope of Practice", [
            ("The Dermis Line (&sect;83.112(c))", 24),
            ("Delegated Medical Procedures (22 TAC Ch. 169)", 26),
            ("Client Referral Procedures", 28)]),
        ("OSHA &amp; Chemical Safety", [
            ("Exposure Control Plan", 29),
            ("Safety Data Sheets &amp; Labeling", 31),
            ("Chemical Storage Requirements", 33)]),
        ("Appendix: Forms, Logs &amp; Checklists", [
            ("Client Intake &amp; Consent Forms", 34),
            ("Sanitation &amp; Foot Spa Logs", 35),
            ("Monthly Compliance Audit Checklist", 36)]),
    ],
    ch1_intro=[
        "An esthetician studio is regulated mostly by one agency &mdash; which sounds "
        "simpler than it is, because that agency licenses three different things at once: "
        "the practitioner, the establishment, and in some cases the specific service.",
        "The harder question is the one this chapter ends on: where esthetics stops and "
        "medicine starts. That line is not about the room you are in or the training you "
        "paid for. It is about depth, and crossing it turns a licensing question into an "
        "unlicensed-practice-of-medicine question.",
    ],
    agencies=[
        ("TDLR",
         "Practitioners, establishments, sanitation",
         "Occupations Code Ch. 1602/1603 and 16 TAC Ch. 83 &mdash; licenses, postings, disinfection, foot spas, waxing, "
         "booth renters, continuing education"),
        ("Texas Medical Board",
         "Anything below the dermis",
         "22 TAC Ch. 169 &mdash; injections, medical needling, deeper peels and laser treatments are delegated medical "
         "acts requiring physician delegation, not esthetics"),
        ("Federal OSHA",
         "Employee safety and chemicals",
         "Bloodborne Pathogens (29 CFR 1910.1030) and Hazard Communication (29 CFR 1910.1200) &mdash; peels, "
         "disinfectants and solvents all count"),
    ],
    callouts=[
        ("warning", "The Line That Matters Most",
         "<strong>16 TAC &sect;83.112(c).</strong> Services must stay <strong>above the dermis</strong> to remain "
         "esthetics. Injections, medical needling, deeper chemical peels, and laser or IPL treatments are delegated "
         "medical procedures under the Texas Medical Board. Performing one without physician delegation can constitute "
         "the unlicensed practice of medicine &mdash; exposure for the individual practitioner <em>and</em> for the "
         "establishment."),
        ("info", "Regulatory Reference",
         "<strong>16 TAC &sect;83.108 and &sect;83.71.</strong> Foot spa cleaning and disinfection records go on the "
         "TDLR-approved form and are retained for <strong>60 days</strong>. If you rent booths, the establishment must "
         "keep a current renter list with names and license numbers, producible to TDLR on request. Both are documents "
         "an inspector can ask for without notice."),
        ("tip", "Two Licenses, Not One",
         "The practitioner license and the establishment license are separate, and both must be current and displayed. "
         "Operating a studio on current practitioner licenses but a lapsed establishment license is its own violation "
         "&mdash; and it is one of the easiest to miss, because nothing about the day-to-day feels different."),
    ])


def sub1(s, pattern, repl, what, flags=0):
    """re.sub that fails loudly. A silent no-match here ships med spa content
    on a dental page, which is exactly the bug this guards against."""
    out, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f"ABORT: substitution '{what}' matched {n} times, expected 1")
    return out


def replace_between(s, start_marker, end_marker, new_inner, what):
    """Replace everything between two markers, chosen by index not regex."""
    i = s.find(start_marker)
    if i < 0:
        raise SystemExit(f"ABORT: start marker for '{what}' not found")
    j = s.find(end_marker, i + len(start_marker))
    if j < 0:
        raise SystemExit(f"ABORT: end marker for '{what}' not found")
    return s[:i + len(start_marker)] + new_inner + s[j:]


def toc_html(toc):
    cards = []
    for i, (title, items) in enumerate(toc, 1):
        lis = "\n".join(
            f'                        <li>{t} <span class="page-num">{p}</span></li>'
            for t, p in items)
        cards.append(
            f'                <div class="toc-card">\n'
            f'                    <div class="toc-card-number">{i}</div>\n'
            f'                    <h3>{title}</h3>\n'
            f'                    <ul class="toc-list">\n{lis}\n'
            f'                    </ul>\n'
            f'                </div>')
    return "\n".join(cards)


SUBSECTIONS = {'dental': [('1.2 &nbsp;Texas State Board of Dental Examiners', ['TSBDE licenses dentists, hygienists and registered assistants, and sets the professional-conduct and recordkeeping rules in the Dental Practice Act (Occupations Code Ch. 251&ndash;267) and 22 TAC Part 5.', "For documentation purposes the board's reach is broader than most offices expect. It covers your infection control program and the designated coordinator who owns it, sterilization monitoring and the records proving it happened, the credentials of every clinical role including which assistants may expose radiographs, and how long you keep patient records and what those records must contain.", 'The board can assess administrative penalties of up to <strong>$5,000 per violation</strong>, with each day a violation continues treated as a separate violation (Occupations Code &sect;264.002). A separate informal track caps at $1,000 per violation and $3,000 per calendar year.']), ('1.3 &nbsp;DSHS Radiation Control Program', ['Every radiation machine in the office &mdash; intraoral, panoramic, and cone-beam CT alike &mdash; must be registered with the DSHS Radiation Control Program under 25 TAC &sect;289.226, and operated according to the dental-specific rules in 25 TAC &sect;289.232.', 'Registration is not a one-time event. It has to be kept current, written operating and safety procedures must be available at the unit, and you need service and calibration records. ALARA principles and patient shielding practices apply to every exposure.', 'This is the requirement most likely to be quietly out of date, because a machine bought years ago keeps working perfectly whether or not its registration was renewed.']), ('1.4 &nbsp;Federal OSHA', ['Texas does not operate a state OSHA plan for private employers, so federal OSHA rules apply directly from your first employee. Two standards do most of the work in a dental setting.', 'The <strong>Bloodborne Pathogens standard</strong> (29 CFR 1910.1030) requires a written Exposure Control Plan, reviewed and updated at least annually and whenever procedures change, with the evaluation of safer sharps devices documented. It also requires hepatitis B vaccination offered within 10 days of assignment, annual training with records kept three years, and a sharps injury log.', 'The <strong>Hazard Communication standard</strong> (29 CFR 1910.1200) requires a Safety Data Sheet for every chemical on site, labels on all containers including anything decanted into a secondary bottle, and training at assignment and whenever a new hazard appears.']), ('1.5 &nbsp;HIPAA and Texas HB 300', ['Both apply to the same patient record, and Texas is stricter in three ways worth knowing.', "HB 300 (Health &amp; Safety Code Ch. 181) defines &ldquo;covered entity&rdquo; more broadly than HIPAA &mdash; broadly enough to reach practices that never bill insurance. It requires customized privacy training for employees who handle protected health information <strong>within 90 days of hire</strong>, with signed proof. And where records are held in a capable electronic system, it requires them to be provided within <strong>15 business days</strong> of a written request, against HIPAA's 30.", 'Work to the stricter number in each case and you satisfy both.']), ('1.6 &nbsp;Record Retention', ['Under 22 TAC &sect;108.8, dental records are kept for at least <strong>five years</strong> from the date of last treatment. Where the patient was a minor at the time of last treatment, records are kept until the patient turns 21 or for five years, whichever is longer.', 'Other rules can require longer &mdash; Medicaid, billing, and malpractice considerations among them &mdash; so the working rule is to keep records at least as long as the strictest requirement that applies to you. OSHA employee exposure and medical records have their own, much longer horizon: the duration of employment plus 30 years.'])], 'tattoo': [('1.2 &nbsp;DSHS Studio Licensing', ['Every studio location holds its own DSHS license covering the services actually performed there, under Health &amp; Safety Code Ch. 146 and 25 TAC Ch. 229 Subchapter V. Tattooing and body piercing are licensed separately, so a studio adding piercing needs its license to reflect it.', 'Operating without a current license is its own violation, distinct from anything found during an inspection. DSHS may assess administrative penalties of up to <strong>$5,000 per violation</strong>, with each day a violation continues treated separately (Health &amp; Safety Code &sect;146.019).', 'Renewals run on a two-year cycle. Track the date somewhere you will actually see it &mdash; a lapsed license is the most avoidable finding on this list.']), ('1.3 &nbsp;What Inspectors Actually Check', ['DSHS conducts unannounced inspections, and they are records-first. The paperwork is examined before anything else, because the paperwork is what proves the practice.', 'In practice that means your current license, spore test results for every sterilizer, sterilization logs showing date and instruments and operator, client records with consent and identification, written aftercare, and evidence that sharps left the building through a registered transporter.', 'The most common single finding is incomplete sterilization records &mdash; not because studios are not sterilizing, but because the log stops being filled in on a busy day and never restarts.']), ('1.4 &nbsp;TCEQ and Medical Waste', ['What happens to your sharps after the station is regulated separately, by the Texas Commission on Environmental Quality under 30 TAC Ch. 326.', 'Generators are classified by volume: a <strong>small quantity generator</strong> produces 50 pounds or less of medical waste per month, which covers almost every tattoo studio. Sharps go in rigid, puncture-resistant, leak-proof, closable containers labeled with the biohazard symbol and kept upright.', 'Untreated sharps waste may not be stored more than <strong>30 days</strong> at the point of generation. Keep every manifest or receipt from your transporter &mdash; those documents are the proof of proper disposal.']), ('1.5 &nbsp;Federal OSHA', ['OSHA applies from your first employee. A true sole proprietor with no employees is not an &ldquo;employer&rdquo; under the Act and so is not covered by it &mdash; though universal precautions remain the standard of care regardless, and client-safety rules under Ch. 146 apply either way.', 'Once you have staff, you need a written Exposure Control Plan reviewed at least annually, bloodborne pathogen training at assignment and annually after with records kept three years, hepatitis B vaccination offered within 10 days of assignment with signed declinations on file, and a sharps injury log recording the device type and brand.']), ('1.6 &nbsp;Client Records and Retention', ["Under 25 TAC &sect;229.406, client records are kept at the studio for at least <strong>two years</strong> following the date of the last entry. Each record captures the service and body location, the inks used with manufacturer and lot numbers, the artist, and the client's verified identification.", 'Written aftercare instructions go to every client with receipt documented &mdash; verbal-only aftercare does not satisfy the rule. Any infection or allergic reaction is reported to the department in writing <strong>within five working days</strong> of learning of it, whether or not it originated at your studio.'])], 'esthetician': [('1.2 &nbsp;TDLR Licensing', ['TDLR licenses two separate things, and both must be current and displayed: the <strong>practitioner</strong>, under Occupations Code Ch. 1602/1603, and the <strong>establishment</strong> itself, under 16 TAC Ch. 83.', 'Establishment licenses come in standard, specialty, and mini variants depending on what the location offers. Operating on current practitioner licenses but a lapsed establishment license is its own violation, and it is easy to miss because nothing about the day-to-day feels different.', 'If you rent booths, the establishment must keep a current renter list with names and license numbers, producible to TDLR on request (&sect;83.71). Continuing education runs on a two-year cycle and shortfalls surface at renewal.']), ('1.3 &nbsp;Where Esthetics Ends and Medicine Begins', ['This is the boundary that carries the most risk, and it is not about the room, the equipment, or the training certificate on the wall. It is about <strong>depth</strong>.', 'Under 16 TAC &sect;83.112(c), services must stay above the dermis to remain esthetics. Injections, medical needling, deeper chemical peels, and laser or IPL treatments are delegated medical procedures governed by the Texas Medical Board under 22 TAC Ch. 169 &mdash; not esthetics under TDLR.', 'Performing one without proper physician delegation can constitute the unlicensed practice of medicine, which is exposure for the individual practitioner <em>and</em> for the establishment that allowed it. The practical answer is a written scope-of-practice guide and a referral procedure, so the boundary is decided in advance rather than in the treatment room.']), ('1.4 &nbsp;Sanitation and Disinfection', ['Most of what TDLR inspects day to day comes down to disinfection discipline and the records proving it.', 'Only EPA-registered bactericidal, fungicidal and virucidal disinfectants may be used, strictly per the product label (&sect;&sect;83.100&ndash;83.101). Immersion solutions, including bleach, are mixed fresh daily. Multi-use implements are cleaned and then disinfected before every client; single-use items are discarded.', 'Foot spa cleaning and disinfection records go on the <strong>TDLR-approved form</strong> and are retained for <strong>60 days</strong> (&sect;83.108). Waxing requires single-use applicators with no double-dipping (&sect;83.105), and a written blood and body-fluid response protocol is required with the supplies to match (&sect;83.111).']), ('1.5 &nbsp;Federal OSHA and Chemical Safety', ['Federal OSHA applies from your first employee, and a salon has more chemical exposure than most people assume.', 'You need a written Exposure Control Plan, hepatitis B vaccination offered to at-risk staff, and documented annual bloodborne pathogens training (29 CFR 1910.1030). Under Hazard Communication (29 CFR 1910.1200), every chemical product needs a Safety Data Sheet accessible during every shift, and every container must be labeled &mdash; including anything decanted into a secondary bottle.', 'TDLR reinforces the same ground in &sect;83.102(n) and &sect;83.114, which cover labeling and safe storage. Flammable products go away from heat sources and out of client areas.']), ('1.6 &nbsp;Postings and Records', ['Current licenses must be displayed, along with the Chapter 83 health and safety rules and the human trafficking awareness sign required by Occupations Code &sect;1603.357.', 'The records an inspector can ask for without notice are the ones easiest to let slip: the daily disinfectant solution log, foot spa cleaning records on the approved form for the last 60 days, the booth renter list, and continuing education certificates for every licensee. None of them take long to keep. All of them take a long time to reconstruct.'])]}


def chapter_html(v):
    paras = "\n".join(f"            <p>{p}</p>" for p in v["ch1_intro"])
    rows = "\n".join(
        f"                    <tr><td><strong>{a}</strong></td><td>{j}</td><td>{k}</td></tr>"
        for a, j, k in v["agencies"])
    outs = []
    for kind, title, body in v["callouts"]:
        outs.append(
            f'            <div class="callout {kind}">\n'
            f'                <div class="callout-title">{title}</div>\n'
            f'                <p>{body}</p>\n'
            f'            </div>')
    callouts = "\n\n".join(outs)
    subs = []
    for sub_title, sub_paras in SUBSECTIONS[v["slug"]]:   # not `paras` — that is the intro
        body = "\n".join(f"            <p>{t}</p>" for t in sub_paras)
        subs.append(f"            <h3>{sub_title}</h3>\n{body}")
    extra_sections = "\n\n" + "\n\n".join(subs) + "\n"
    return f'''        <div class="narrow">
            <div class="chapter-label">Chapter 1</div>
            <h2>Regulatory Overview &amp; Agency Guide</h2>
{paras}

{callouts}

            <h3>1.1 &nbsp;Who Regulates You</h3>
            <p>These are the bodies whose rules your documentation has to satisfy. Each one
            can inspect, and each one asks for different evidence.</p>
            <table class="data-table">
                <thead>
                    <tr><th>Agency</th><th>Jurisdiction</th><th>What they ask for</th></tr>
                </thead>
                <tbody>
{rows}
                </tbody>
            </table>

{extra_sections}
            <div class="sample-end">
                <p><strong>This is where the sample ends.</strong> The complete manual continues
                through {len(v["toc"])} chapters and {v["pages"]} pages, written for your business with your
                details, your services, and your staff roles filled in &mdash; plus the training
                guides, forms, logs and postings that go with it.</p>
            </div>
        </div>'''


def build(key):
    v = V[key]
    src = open(os.path.join(REPO, TEMPLATE), encoding="utf-8").read()
    s = src

    s = re.sub(r"<title>.*?</title>", f"<title>{v['title']}</title>", s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*"',
               lambda m: m.group(1) + v["desc"] + '"', s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*"',
               lambda m: m.group(1) + f"https://complianceghost.com/sample-manual/{v['slug']}/\"", s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*"',
               lambda m: m.group(1) + f"https://complianceghost.com/sample-manual/{v['slug']}/\"", s)
    for prop in ("og:title", "twitter:title"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*"',
                   lambda m: m.group(1) + v["title"] + '"', s)
    for prop in ("og:description", "twitter:description"):
        s = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*"',
                   lambda m: m.group(1) + v["desc"] + '"', s)

    # JSON-LD carries its own copy of the title/description/url — rewrite the
    # WebPage node by field rather than by matching exact prose.
    s = re.sub(r'("url": "https://complianceghost\.com)/sample-manual/"',
               lambda m: m.group(1) + f'/sample-manual/{v["slug"]}/"', s)
    s = re.sub(r'("name": ")Sample Compliance Manual[^"]*"',
               lambda m: m.group(1) + v["title"] + '"', s)
    s = re.sub(r'("description": ")Sample Texas Med Spa Compliance Manual[^"]*"',
               lambda m: m.group(1) + v["desc"] + '"', s)

    # The template carries the med spa switcher; rebuild it for this vertical so
    # the current page is the one shown in bold.
    SAMPLES = [("/sample-manual/", "Med Spa"), ("/sample-manual/dental/", "Dental Office"),
               ("/sample-manual/tattoo/", "Tattoo Studio"),
               ("/sample-manual/esthetician/", "Esthetician Studio")]
    mine = f"/sample-manual/{v['slug']}/"
    links = " &middot; ".join(
        (f"<strong>{lab}</strong>" if u == mine else f'<a href="{u}">{lab}</a>')
        for u, lab in SAMPLES)
    switcher = (
        f'<div class="sample-switch" style="background:var(--navy-2);border-bottom:1px solid '
        f'var(--line);padding:12px 0;text-align:center;font-size:.85rem;color:var(--ink-3)">'
        f'<div class="container">Viewing the <strong style="color:var(--ink)">{v["label"]}'
        f'</strong> sample &mdash; also available: {links}</div></div>')
    s = re.sub(r'<div class="sample-switch".*?</div></div>', switcher, s, count=1, flags=re.S)

    # cover
    s = re.sub(r"<h1>Texas Med Spa<br>Compliance Manual</h1>", f"<h1>{v['h1']}</h1>", s, count=1)
    badges = "\n".join(f'            <span class="cover-badge">{b}</span>' for b in v["badges"])
    s = re.sub(r'<div class="cover-badges">.*?</div>',
               f'<div class="cover-badges">\n{badges}\n        </div>', s, count=1, flags=re.S)

    # table of contents — index-based, verified below
    s = replace_between(s, '<div class="toc-grid">', '\n        </div>\n    </div>\n</section>',
                        "\n" + toc_html(v["toc"]), "toc-grid")

    # chapter 1
    s = replace_between(s, '<section class="content-section">\n    <div class="container">\n',
                        '\n    </div>\n</section>', chapter_html(v), "chapter-1")

    # closing CTA
    s = re.sub(r"<h2>Get the Complete Manual</h2>\s*<p>.*?</p>",
               f"<h2>Get the Complete Manual</h2>\n        <p>The full Texas {v['label']} "
               f"Compliance Kit includes the complete {v['pages']}-page manual, training documents "
               f"with quizzes and certificates, every required form and log, print-ready postings, "
               f"and a step-by-step implementation guide &mdash; built for your business and "
               f"delivered in 48 hours.</p>", s, count=1, flags=re.S)
    s = s.replace('<a href="/#pricing" class="btn btn-primary">Get Your Kit &middot; $997</a>',
                  f'<a href="{v["money"]}" class="btn btn-primary">See the {v["label"]} Kit &middot; $997</a>')

    # Guard: no med-spa-specific content may survive on another vertical's page.
    # The company boilerplate legitimately names all four verticals on every page;
    # strip those known-good strings before hunting for real leaks.
    BOILERPLATE = [
        "Texas regulatory compliance documentation for med spas, dental offices, "
        "tattoo studios, and esthetician studios.",
        "compliance documentation for med spas, dental offices, tattoo studios, "
        "and esthetician studios",
        "Med Spas, Dental, Tattoo",
        "med-spa",
        "/med-spa/",
        # The sample switcher deliberately links to the med spa sample by name.
        '<a href="/sample-manual/">Med Spa</a>',
    ]
    probe = s
    for b in BOILERPLATE:
        probe = probe.replace(b, "")

    LEAK = ["Med Spa", "med spa", "Botox", "delegating physician", "Good Faith Exam",
            "Medical Director Responsibilities", "TMB) Requirements", "48-page"]
    allowed = {"dental": [], "tattoo": [], "esthetician": ["22 TAC Ch. 169"]}
    for term in LEAK:
        if term in probe and term not in "".join(allowed[v["slug"]]):
            i = probe.find(term)
            ctx = probe[max(0, i - 90):i + 90].replace("\n", " ")
            raise SystemExit(f"ABORT: '{term}' leaked onto the {v['slug']} page -> ...{ctx}...")

    out_dir = os.path.join(REPO, "sample-manual", v["slug"])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(s)
    return f"sample-manual/{v['slug']}/index.html", len(s)


if __name__ == "__main__":
    for k in ("dental", "tattoo", "esthetician"):
        path, n = build(k)
        print(f"  built {path:44s} {n:6d} bytes")
    sys.exit(0)
