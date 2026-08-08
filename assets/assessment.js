/* Texas Compliance Gap Assessment — static, no backend.
 *
 * Wording rules baked in on purpose (see quiz/QUIZ-SPEC.md §4): this tool never
 * renders a verdict. No "compliant/non-compliant", no "pass/fail", no invented
 * penalty figures. It reports documentation gaps from the user's own answers and
 * attaches each one to the rule that asks for the document.
 */
(function () {
    'use strict';

    var VERSION = '2026-08-a';
    var FORMSPREE = 'https://formspree.io/f/mbdavkdw';

    var ICON = {
        syringe: '<path d="m18 2 4 4"/><path d="m17 7 3-3"/><path d="M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5"/><path d="m9 11 4 4"/><path d="m5 19-3 3"/><path d="m14 4 6 6"/>',
        tooth: '<path d="M12 5.5c-1.5-1.2-3-1.8-4.5-1.5C5.5 4.4 4 6 4 8.5c0 2 .6 3.4 1 5 .5 2 .7 5.5 2.2 5.5 1.3 0 1.4-2.5 1.9-4 .4-1.2.7-2 2.9-2s2.5.8 2.9 2c.5 1.5.6 4 1.9 4 1.5 0 1.7-3.5 2.2-5.5.4-1.6 1-3 1-5 0-2.5-1.5-4.1-3.5-4.5-1.5-.3-3 .3-4.5 1.5z"/>',
        palette: '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>',
        sparkles: '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .962 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.962 0z"/>'
    };

    function svg(name, cls) {
        return '<svg class="' + (cls || 'ico') + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + ICON[name] + '</svg>';
    }

    /* ---- Question banks -------------------------------------------------
       q: question · c: citation · k: category · w: weight (3 licence/practice,
       2 agency-fine, 1 supporting) · d: Kit document · g: service gate · r: recurring */
    var BANKS = {
        medspa: {
            label: 'Med Spa', icon: 'syringe',
            cats: { DEL: 'Delegation & medical oversight', LIC: 'Licensing & postings', PRIV: 'Privacy & patient records', OSHA: 'OSHA & workplace safety' },
            gates: [
                { id: 'injectables', label: 'Injectables (Botox, dermal filler)' },
                { id: 'iv', label: 'IV therapy or hydration' },
                { id: 'lhr', label: 'Laser hair removal' }
            ],
            qs: [
                { id: 'ms01', w: 3, k: 'DEL', r: true, q: 'Do you have written delegation protocols (standing delegation orders) signed and dated by your delegating physician, reviewed and re-signed within the last 12 months?', c: '22 TAC Chapter 169; Texas Occupations Code Chapter 157', d: 'Physician Delegation Protocol + Annual Review Log' },
                { id: 'ms02', w: 2, k: 'DEL', q: 'Do your delegation documents cite the current rule, 22 TAC Chapter 169, rather than the repealed 22 TAC §193.17?', c: '22 TAC Chapter 169 (replaced §193.17, January 2025)', d: 'Updated Chapter 169 protocol set' },
                { id: 'ms03', w: 3, k: 'DEL', q: 'Before each new treatment, is every patient evaluated by a physician, PA, or APRN who issues an individualized treatment order documented in the chart?', c: '22 TAC Chapter 169', d: 'Patient Evaluation & Treatment Order forms' },
                { id: 'ms04', w: 3, k: 'DEL', g: 'injectables', q: 'Are injectables performed only by a physician, PA, APRN, or RN under written delegation — never an LVN, esthetician, or unlicensed staff?', c: '22 TAC Chapter 169; Occupations Code Chapter 301', d: 'Staff Credential & Scope Verification Log' },
                { id: 'ms05', w: 3, k: 'DEL', g: 'iv', q: 'For IV drips and hydration: since September 1, 2025, are IVs administered only by an RN or above, with ordering delegated only to a PA or APRN?', c: 'HB 3749 ("Jenifer’s Law"); 22 TAC Chapter 169', d: 'IV Therapy Protocol addendum' },
                { id: 'ms06', w: 2, k: 'DEL', r: true, q: 'Is at least one BLS-trained person present whenever patients are treated, with the physician, PA, or APRN on site or immediately reachable per your protocol?', c: '22 TAC Chapter 169', d: 'Emergency Response Protocol + BLS Training Log' },
                { id: 'ms07', w: 1, k: 'LIC', q: 'Are the delegating physician’s name and Texas license number posted in treatment and public areas with the TMB complaint notice, and do staff wear name and credential badges?', c: 'HB 3749; 22 TAC Chapter 169', d: 'Required Postings & Signage Pack' },
                { id: 'ms08', w: 3, k: 'LIC', g: 'lhr', q: 'For laser hair removal: is the facility registered with TDLR, with a written consulting-physician contract and each technician holding the proper TDLR certificate?', c: 'Health & Safety Code Chapter 401 Subchapter M; 16 TAC Chapter 118', d: 'LHR Facility Checklist + Consulting Physician Contract' },
                { id: 'ms09', w: 2, k: 'PRIV', r: true, q: 'Has every employee completed documented Texas privacy training within 90 days of hire, with signed and dated records?', c: 'Health & Safety Code Chapter 181 (HB 300)', d: 'HB 300 Privacy Training + Acknowledgment Log' },
                { id: 'ms10', w: 2, k: 'PRIV', q: 'Do you have a written privacy notice and signed business associate agreements with vendors that touch patient data (EMR, booking, photo storage)?', c: '45 CFR Parts 160/164; Health & Safety Code Chapter 181', d: 'Privacy Notice + BAA templates' },
                { id: 'ms11', w: 2, k: 'PRIV', q: 'Are complete treatment records — evaluation, consent, product lot numbers, photos — retained at least 7 years (for minors, until age 21 or 7 years, whichever is longer)?', c: '22 TAC Chapter 165', d: 'Records Retention Policy + Chart Checklist' },
                { id: 'ms12', w: 3, k: 'OSHA', r: true, q: 'Do you have a written OSHA Exposure Control Plan covering needle and cannula procedures, reviewed within the last 12 months?', c: '29 CFR 1910.1030(c)', d: 'Exposure Control Plan template' },
                { id: 'ms13', w: 2, k: 'OSHA', r: true, q: 'Have exposed staff been offered hepatitis B vaccination (with signed declinations on file) and completed documented bloodborne pathogens training in the last 12 months?', c: '29 CFR 1910.1030(f), (g)', d: 'HepB Offer/Declination forms + Annual Training Log' },
                { id: 'ms14', w: 1, k: 'OSHA', q: 'Do you keep Safety Data Sheets and labeled containers for peels and disinfectants, with hazard communication training documented?', c: '29 CFR 1910.1200', d: 'HazCom Program + SDS binder' }
            ]
        },
        dental: {
            label: 'Dental Office', icon: 'tooth',
            cats: { TSBDE: 'TSBDE clinical standards', RAD: 'Radiation safety', PRIV: 'Privacy & records', OSHA: 'OSHA & workplace safety' },
            gates: [
                { id: 'sedation', label: 'Sedation or general anesthesia' },
                { id: 'amalgam', label: 'Placing or removing amalgam' }
            ],
            qs: [
                { id: 'dn01', w: 2, k: 'TSBDE', q: 'Do you have a written infection control program with a designated infection control coordinator?', c: 'CDC guidelines, enforced via 22 TAC §108.24', d: 'Infection Control Program template' },
                { id: 'dn02', w: 3, k: 'TSBDE', r: true, q: 'Is every sterilizer monitored with biological (spore) testing on a documented schedule — CDC guidance is at least weekly — with results retained?', c: '22 TAC §108.24; CDC guidelines', d: 'Sterilization Monitoring Log' },
                { id: 'dn03', w: 3, k: 'TSBDE', g: 'sedation', q: 'Do you hold the correct TSBDE sedation or anesthesia permit for the level of sedation you provide?', c: '22 TAC Chapter 110', d: 'Sedation Permit Compliance Checklist' },
                { id: 'dn04', w: 1, k: 'TSBDE', r: true, q: 'Are all licensed staff current on TSBDE continuing education, CPR/BLS certification, and the required human trafficking prevention course?', c: '22 TAC Chapter 104', d: 'CE & Certification Tracker' },
                { id: 'dn05', w: 2, k: 'RAD', q: 'Does every dental assistant who positions or exposes x-rays hold a TSBDE radiology certificate?', c: 'TSBDE registered dental assistant x-ray certification rules', d: 'Staff Credential Log' },
                { id: 'dn06', w: 2, k: 'RAD', q: 'Is every x-ray machine — including panoramic and CBCT — registered with DSHS with fees current, and are written operating and safety procedures available at each unit?', c: '25 TAC §289.226; §289.232', d: 'Radiation Registration Tracker + Safety Procedures' },
                { id: 'dn07', w: 2, k: 'PRIV', q: 'Are patient records retained at least 5 years from last treatment (for minors, until age 21 or 5 years, whichever is longer)?', c: '22 TAC §108.8', d: 'Records Retention Policy' },
                { id: 'dn08', w: 3, k: 'PRIV', q: 'Have you completed and documented a HIPAA Security Risk Analysis of your electronic patient data, updated periodically?', c: '45 CFR Part 164 Subpart C', d: 'Security Risk Analysis workbook' },
                { id: 'dn09', w: 2, k: 'PRIV', q: 'Do you have a designated privacy officer, a Notice of Privacy Practices given to patients, and signed BAAs with billing, IT, imaging, and shredding vendors?', c: '45 CFR Parts 160/164', d: 'NPP + BAA templates + Officer Designation form' },
                { id: 'dn10', w: 2, k: 'PRIV', r: true, q: 'Has every employee completed documented HB 300 privacy training within 90 days of hire, and can you produce electronic records within Texas’s 15-business-day window?', c: 'Health & Safety Code Chapter 181; §181.102', d: 'HB 300 Training Log + Records-Request SOP' },
                { id: 'dn11', w: 3, k: 'OSHA', r: true, q: 'Do you have a written OSHA Exposure Control Plan reviewed within the last 12 months that documents your safer-sharps evaluation?', c: '29 CFR 1910.1030(c)', d: 'Exposure Control Plan template' },
                { id: 'dn12', w: 2, k: 'OSHA', q: 'Was hepatitis B vaccination offered to exposed staff within 10 working days of assignment, with signed declinations retained?', c: '29 CFR 1910.1030(f)', d: 'HepB Offer/Declination forms' },
                { id: 'dn13', w: 2, k: 'OSHA', r: true, q: 'Has every exposed employee completed bloodborne pathogens training in the last 12 months, with records kept 3 years?', c: '29 CFR 1910.1030(g), (h)', d: 'Annual Training Log' },
                { id: 'dn14', w: 1, k: 'OSHA', q: 'Do you maintain a written hazard communication program with a current Safety Data Sheet for every chemical, labeled containers, and documented training?', c: '29 CFR 1910.1200', d: 'HazCom Program + SDS binder' },
                { id: 'dn15', w: 1, k: 'TSBDE', g: 'amalgam', q: 'Is an amalgam separator installed with the one-time EPA compliance report submitted?', c: '40 CFR Part 441', d: 'Amalgam Compliance Report template' }
            ]
        },
        tattoo: {
            label: 'Tattoo Studio', icon: 'palette',
            cats: { LIC: 'DSHS licensing', STER: 'Sterilization & sanitation', REC: 'Client records & consent', OSHA: 'OSHA & waste handling' },
            gates: [{ id: 'employees', label: 'I have employees (not solo)' }],
            qs: [
                { id: 'tt01', w: 3, k: 'LIC', q: 'Does the studio hold a current DSHS license for this location, covering the services you actually offer, available for inspection?', c: 'Health & Safety Code Chapter 146; 25 TAC §229.403', d: 'License & Renewal Tracker' },
                { id: 'tt13', w: 2, k: 'LIC', r: true, q: 'Has every employee completed an approved human trafficking prevention training course, with proof of completion kept on file?', c: 'Health & Safety Code \u00a7146.0075 (HB 1778, 2025) \u2014 required of each employee; no employee could be required to complete it before January 1, 2026', d: 'Human Trafficking Training Log + approved course list' },
                { id: 'tt02', w: 3, k: 'STER', r: true, q: 'Is every sterilization unit spore-tested every calendar month by a laboratory, with results retained for inspection?', c: '25 TAC §229.407', d: 'Monthly Spore Test Log' },
                { id: 'tt03', w: 2, k: 'STER', q: 'Do your sterilization records show the date, instruments, and operator initials, retained at least 2 years?', c: '25 TAC §229.407', d: 'Sterilization Log template' },
                { id: 'tt04', w: 1, k: 'STER', q: 'Does every sterilized package carry a chemical or heat indicator confirming it went through the cycle?', c: '25 TAC §229.407', d: 'Sterilization SOP' },
                { id: 'tt05', w: 2, k: 'STER', q: 'Are single-use items — needles, razors, ink caps, ointment portions — never reused between clients?', c: '25 TAC §229.407', d: 'Station Setup & Teardown Checklist' },
                { id: 'tt06', w: 2, k: 'REC', q: 'Do you verify every client’s government-issued photo ID with date of birth before work begins, and record it?', c: '25 TAC §229.406', d: 'Client Record & Consent form' },
                { id: 'tt07', w: 3, k: 'REC', q: 'Does every client record capture the service and body location, ink colors with manufacturer and lot detail, artist, aftercare acknowledgment, and client signature, kept at least 2 years?', c: '25 TAC §229.406', d: 'Client Record & Consent form' },
                { id: 'tt08', w: 3, k: 'REC', q: 'For minors: do you decline all tattoos under 18 except the narrow cover-up exception with parental consent, and for piercings require written, notarized parental consent with presence or affidavit?', c: 'Health & Safety Code §146.012; 25 TAC §229.406', d: 'Minor Consent + Affidavit forms' },
                { id: 'tt09', w: 2, k: 'REC', q: 'Does every client receive written aftercare instructions, with receipt documented?', c: '25 TAC §229.406', d: 'Aftercare Instructions handout' },
                { id: 'tt10', w: 3, k: 'OSHA', q: 'Are sharps collected in rigid, biohazard-labeled containers and removed by a registered medical waste transporter, with manifests or receipts kept?', c: '25 TAC §229.411; 30 TAC Chapter 326', d: 'Sharps & Waste SOP + Manifest Log' },
                { id: 'tt11', w: 3, k: 'OSHA', g: 'employees', r: true, q: 'Do you have a written OSHA Exposure Control Plan reviewed within the last 12 months?', c: '29 CFR 1910.1030(c); 25 TAC Chapter 229 Subchapter V', d: 'Exposure Control Plan template' },
                { id: 'tt12', w: 2, k: 'OSHA', g: 'employees', r: true, q: 'Is annual bloodborne pathogens training documented (records kept 3 years) and hepatitis B vaccination offered within 10 working days, with signed declinations?', c: '29 CFR 1910.1030(f)–(h)', d: 'Training Log + HepB Declination forms' }
            ]
        },
        esthetician: {
            label: 'Esthetician Studio', icon: 'sparkles',
            cats: { LIC: 'TDLR licensing & postings', SAN: 'Sanitation & disinfection', SCOPE: 'Scope of practice', OSHA: 'OSHA & chemical safety' },
            gates: [
                { id: 'booth', label: 'I rent booths to other practitioners' },
                { id: 'footspa', label: 'I operate foot spas or basins' },
                { id: 'employees', label: 'I have employees' }
            ],
            qs: [
                { id: 'es01', w: 3, k: 'LIC', q: 'Is every practitioner’s esthetician (or master esthetician) license current and displayed at the establishment?', c: 'Occupations Code Chapters 1602/1603; §1603.357; 16 TAC Chapter 83', d: 'License & Renewal Tracker' },
                { id: 'es02', w: 3, k: 'LIC', q: 'Is the establishment license itself (standard, specialty, or mini) current and displayed?', c: '16 TAC Chapter 83; Occupations Code Chapters 1602/1603', d: 'License & Renewal Tracker' },
                { id: 'es03', w: 1, k: 'LIC', g: 'booth', q: 'Do you maintain a current renter list with names and license numbers, producible to TDLR on request?', c: '16 TAC §83.71', d: 'Booth Renter Log' },
                { id: 'es04', w: 1, k: 'LIC', q: 'Are the Chapter 83 health and safety rules and the human trafficking awareness sign posted where required?', c: 'Occupations Code §1603.357; 16 TAC Chapter 83', d: 'Required Postings Pack' },
                { id: 'es05', w: 2, k: 'SAN', q: 'Do you use only EPA-registered bactericidal, fungicidal, and virucidal disinfectants per label, with immersion solutions (including bleach) mixed fresh daily?', c: '16 TAC §§83.100–83.101', d: 'Disinfection SOP + Daily Solution Log' },
                { id: 'es06', w: 2, k: 'SAN', q: 'Are multi-use implements cleaned then disinfected before every client, single-use items discarded after one use, and clean items stored dry, covered, and separate from soiled?', c: '16 TAC §§83.101–83.102', d: 'Sanitation Checklist' },
                { id: 'es07', w: 1, k: 'SAN', g: 'footspa', q: 'Are foot spa cleaning and disinfection logs kept on the TDLR-approved form for 60 days?', c: '16 TAC §83.108', d: 'Foot Spa Cleaning Log (TDLR format)' },
                { id: 'es08', w: 1, k: 'SAN', q: 'For waxing: single-use applicators only, no double-dipping, and wax pots cleaned per manufacturer instructions?', c: '16 TAC §83.105', d: 'Waxing Service SOP' },
                { id: 'es09', w: 2, k: 'SAN', q: 'Do you have a blood and body-fluid response protocol — hospital-grade or 10% bleach disinfection, 5-minute immersion for non-porous items, double-bag and discard porous items — with supplies on hand?', c: '16 TAC §83.111', d: 'Blood Exposure SOP card' },
                { id: 'es10', w: 3, k: 'SCOPE', q: 'Do all services stay above the dermis — no injections, medical needling, deep peels, or laser/IPL — unless performed under proper physician delegation with written protocols?', c: '16 TAC §83.112(c); 22 TAC Chapter 169', d: 'Scope-of-Practice Guide + Medical Referral SOP' },
                { id: 'es11', w: 1, k: 'LIC', r: true, q: 'Is every licensee current on TDLR continuing education for the 2-year cycle, including the required sanitation and human trafficking topics?', c: '16 TAC Chapter 83 (CE provisions)', d: 'CE Tracker' },
                { id: 'es12', w: 2, k: 'OSHA', g: 'employees', r: true, q: 'Do you have a written OSHA Exposure Control Plan, hepatitis B vaccination offers, and documented training in place?', c: '29 CFR 1910.1030', d: 'Exposure Control Plan (salon edition)' },
                { id: 'es13', w: 2, k: 'OSHA', q: 'Is there a Safety Data Sheet for every chemical product, with containers labeled (including secondary containers), and chemicals stored away from heat and never in the restroom?', c: '29 CFR 1910.1200; 16 TAC §83.102(n); §83.114', d: 'SDS Binder + Labeling Kit + Storage Checklist' }
            ]
        }
    };

    var ANSWERS = [
        { v: 'yes', label: 'Yes' },
        { v: 'no', label: 'No' },
        { v: 'notsure', label: 'Not sure / can’t find it' }
    ];

    var root = document.getElementById('quiz-root');
    if (!root) { return; }

    var S = { screen: 'intro', vertical: null, gates: {}, qs: [], i: 0, answers: {}, started: 0, result: null };

    function track(name, params) {
        if (typeof gtag === 'function') { gtag('event', name, params || {}); }
    }
    function esc(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }
    function save() {
        try { sessionStorage.setItem('cg-quiz', JSON.stringify({ s: S, v: VERSION, t: Date.now() })); } catch (e) {}
    }
    function arrivedByReload() {
        try {
            var nav = performance.getEntriesByType('navigation')[0];
            if (nav) { return nav.type === 'reload' || nav.type === 'back_forward'; }
            // Safari <15 and friends
            return performance.navigation && performance.navigation.type === 1;
        } catch (e) { return false; }
    }

    function restore() {
        // Only ever resume a refresh or a back-button return. Following a link
        // to /assessment/ means "start", so the chooser must come up.
        if (!arrivedByReload()) {
            try { sessionStorage.removeItem('cg-quiz'); } catch (e) {}
            return;
        }
        try {
            var raw = sessionStorage.getItem('cg-quiz');
            if (!raw) { return; }
            var d = JSON.parse(raw);
            if (d.v === VERSION && Date.now() - d.t < 30 * 60 * 1000 && d.s.screen === 'q') { S = d.s; }
        } catch (e) {}
    }

    /* ---- Screens -------------------------------------------------------- */
    function viewIntro() {
        var cards = Object.keys(BANKS).map(function (key) {
            var b = BANKS[key];
            return '<button type="button" class="vcard" data-v="' + key + '">' +
                   '<span class="tile">' + svg(b.icon) + '</span>' +
                   '<span class="name">' + esc(b.label) + '</span>' +
                   '<span class="sub">' + b.qs.filter(function (q) { return !q.g; }).length +
                   '+ questions &middot; about 2 minutes</span></button>';
        }).join('');
        return '<div class="section-header" style="margin-bottom:32px">' +
               '<div class="section-label">Free Self-Assessment</div>' +
               '<h1>Which documents is your business missing?</h1>' +
               '<p class="section-desc">Answer a few plain-English questions about your paperwork. You’ll get a readiness score and a breakdown by category &mdash; free, no email needed to see your results.</p>' +
               '</div><div class="vgrid">' + cards + '</div>';
    }

    function viewGates() {
        var b = BANKS[S.vertical];
        var boxes = b.gates.map(function (g) {
            return '<label class="answers-gate"><input type="checkbox" data-gate="' + g.id + '"' +
                   (S.gates[g.id] ? ' checked' : '') + '> <span>' + esc(g.label) + '</span></label>';
        }).join('');
        return '<div class="quiz-card">' +
               '<h1 style="font-size:var(--t-h3);margin-bottom:8px">Which of these apply to your ' + esc(b.label.toLowerCase()) + '?</h1>' +
               '<p style="font-size:var(--t-sm);color:var(--ink-3);margin-bottom:24px">This adds only the questions that are relevant to you. Leave them all unchecked if none apply.</p>' +
               '<div class="answers">' + boxes + '</div>' +
               '<div class="qnav"><button type="button" class="link-btn" data-act="back">&larr; Back</button>' +
               '<button type="button" class="btn btn-primary" data-act="startqs">Start the assessment &rarr;</button></div></div>';
    }

    function viewQuestion() {
        var q = S.qs[S.i];
        var pct = Math.round((S.i / S.qs.length) * 100);
        var opts = ANSWERS.map(function (a) {
            var checked = S.answers[q.id] === a.v ? ' checked' : '';
            return '<label><input type="radio" name="a" value="' + a.v + '"' + checked + '><span>' + esc(a.label) + '</span></label>';
        }).join('');
        return '<div class="quiz-card">' +
               '<div class="progress-row"><span>Question ' + (S.i + 1) + ' of ' + S.qs.length + '</span>' +
               '<span>' + esc(BANKS[S.vertical].label) + '</span></div>' +
               '<div class="bar" aria-hidden="true"><i style="width:' + pct + '%"></i></div>' +
               '<fieldset><legend tabindex="-1" id="qlegend">' + esc(q.q) + '</legend>' +
               '<p class="qcite">' + esc(q.c) + '</p>' +
               '<div class="answers">' + opts + '</div></fieldset>' +
               '<div class="qnav">' +
               '<button type="button" class="link-btn" data-act="back">&larr; Back</button>' +
               '<button type="button" class="link-btn" data-act="restart">Change industry</button>' +
               '<button type="button" class="btn btn-primary" data-act="next"' +
               (S.answers[q.id] ? '' : ' disabled') + '>' +
               (S.i === S.qs.length - 1 ? 'See my results' : 'Continue') + ' &rarr;</button></div></div>';
    }

    function score() {
        var b = BANKS[S.vertical];
        var earned = 0, possible = 0, catTot = {}, catEarn = {}, gaps = [];
        S.qs.forEach(function (q) {
            var a = S.answers[q.id];
            if (!a) { return; }
            possible += q.w;
            catTot[q.k] = (catTot[q.k] || 0) + q.w;
            var got = a === 'yes' ? q.w : (a === 'notsure' ? q.w * 0.25 : 0);
            earned += got;
            catEarn[q.k] = (catEarn[q.k] || 0) + got;
            if (a !== 'yes') { gaps.push({ q: q, answer: a }); }
        });
        var pct = possible ? Math.round((earned / possible) * 100) : 0;
        var cats = Object.keys(b.cats).map(function (k) {
            return { key: k, label: b.cats[k], pct: catTot[k] ? Math.round((catEarn[k] / catTot[k]) * 100) : null };
        }).filter(function (c) { return c.pct !== null; });
        gaps.sort(function (x, y) { return y.q.w - x.q.w; });
        return {
            pct: pct, gaps: gaps, cats: cats,
            bucket: pct >= 85 ? 'low_gaps' : (pct >= 60 ? 'moderate_gaps' : 'high_gaps'),
            recurring: gaps.filter(function (g) { return g.q.r; }).length
        };
    }

    function viewResults() {
        var r = S.result, b = BANKS[S.vertical];
        var C = 2 * Math.PI * 64;
        var dash = (r.pct / 100) * C;
        var ring = r.pct >= 85 ? '#2ecc71' : (r.pct >= 60 ? '#f59e0b' : '#ef4444');

        var headline = r.gaps.length === 0
            ? 'Your answers didn’t flag any gaps in this checklist.'
            : 'Your answers flag <strong>' + r.gaps.length + (r.gaps.length === 1 ? ' area</strong>' : ' areas</strong>') +
              ' where documents commonly required for Texas ' + esc(b.label.toLowerCase()) + 's may be missing or unverified.';

        var catRows = r.cats.map(function (c) {
            var col = c.pct >= 85 ? '#2ecc71' : (c.pct >= 60 ? '#f59e0b' : '#ef4444');
            return '<div class="cat"><span class="cname">' + esc(c.label) + '</span>' +
                   '<span class="cval">' + c.pct + '%</span>' +
                   '<span class="cbar"><i style="width:' + c.pct + '%;background:' + col + '"></i></span></div>';
        }).join('');

        var teasers = r.gaps.slice(0, 3).map(function (g) {
            return '<div class="gap"><h3>' + esc(g.q.c) + '</h3>' +
                   '<p>You answered &ldquo;' + (g.answer === 'no' ? 'No' : 'Not sure') + '&rdquo; to: ' +
                   esc(g.q.q.slice(0, 110)) + (g.q.q.length > 110 ? '&hellip;' : '') + '</p></div>';
        }).join('');

        var more = r.gaps.length > 3
            ? '<p style="font-size:var(--t-sm);color:var(--ink-3);margin-top:16px">Plus ' + (r.gaps.length - 3) +
              ' more in your full action plan below.</p>' : '';

        return '<div class="quiz-card">' +
            '<div class="score-wrap">' +
              '<div class="dial"><svg width="150" height="150" aria-hidden="true">' +
                '<circle cx="75" cy="75" r="64" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="11"/>' +
                '<circle cx="75" cy="75" r="64" fill="none" stroke="' + ring + '" stroke-width="11" stroke-linecap="round" ' +
                'stroke-dasharray="' + dash.toFixed(1) + ' ' + C.toFixed(1) + '"/></svg>' +
                '<div class="val"><span class="num">' + r.pct + '</span><span class="of">out of 100</span></div></div>' +
              '<div class="score-note"><h2 tabindex="-1" id="resh">Documentation readiness</h2>' +
              '<p style="font-size:var(--t-sm)">' + headline + '</p></div>' +
            '</div>' +
            '<div class="cats">' + catRows + '</div>' +
            (r.gaps.length ? '<h2 style="font-size:var(--t-base);margin-bottom:4px">Top areas to look at</h2>' +
              '<div class="gap-list">' + teasers + '</div>' + more : '') +
            (r.recurring ? '<p style="font-size:var(--t-sm);color:var(--ink-3);margin-top:20px">' + r.recurring +
              ' of these renew or need re-signing every year &mdash; that’s what <a href="/compliance-shield/">Compliance Shield</a> keeps current.</p>' : '') +
            '</div>' +
            gateBlock() +
            '<p style="text-align:center;margin-top:24px"><button type="button" class="link-btn" data-act="restart">Start over with a different business type</button></p>';
    }

    function gateBlock() {
        return '<div class="gate" id="gate">' +
            '<h2>Get your full action plan</h2>' +
            '<p class="sub">Every gap above, what the rule asks for, and which document closes it &mdash; emailed to you, plus your industry’s gap assessment PDF.</p>' +
            '<form id="planForm" action="' + FORMSPREE + '" method="POST">' +
            '<input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">' +
            '<label class="f" for="qemail">Email address</label>' +
            '<input type="email" id="qemail" name="email" placeholder="you@yourbusiness.com" autocomplete="email" required>' +
            '<label class="f" for="qbiz">Business name <span style="color:var(--ink-3);font-weight:400">(optional)</span></label>' +
            '<input type="text" id="qbiz" name="businessName" placeholder="e.g. Glow Aesthetics" autocomplete="organization">' +
            '<label class="consent"><input type="checkbox" name="consent_marketing" value="yes">' +
            '<span>Send me occasional Texas compliance updates. (Your action plan is sent either way.)</span></label>' +
            '<button type="submit" class="btn btn-primary btn-block" id="planBtn">Send my action plan &rarr;</button>' +
            '<p class="msg msg-error" id="qerr" role="alert" hidden>We couldn’t send that just now. Please try again, or email <a href="mailto:info@complianceghost.com">info@complianceghost.com</a> and we’ll send your plan over.</p>' +
            '<p style="font-size:var(--t-xs);color:var(--ink-3);margin-top:12px;text-align:center">No spam, ever. See our <a href="/privacy.html">Privacy Policy</a>.</p>' +
            '</form></div>';
    }

    function viewPlan() {
        var r = S.result, b = BANKS[S.vertical];
        var rows = r.gaps.map(function (g) {
            return '<div class="gap"><h3>' + esc(g.q.c) + '</h3>' +
                '<p><strong style="color:var(--ink-2)">The question:</strong> ' + esc(g.q.q) + '<br>' +
                '<strong style="color:var(--ink-2)">You answered:</strong> ' + (g.answer === 'no' ? 'No' : 'Not sure') + '<br>' +
                '<strong style="color:var(--ink-2)">Document that covers it:</strong> <span class="doc">' + esc(g.q.d) + '</span></p></div>';
        }).join('');
        return '<div class="quiz-card">' +
            '<h1 style="font-size:var(--t-h3);margin-bottom:6px">Your ' + esc(b.label) + ' action plan</h1>' +
            '<p style="font-size:var(--t-sm);color:var(--ink-3);margin-bottom:20px">Readiness score ' + r.pct +
            '/100 &middot; ' + r.gaps.length + ' area' + (r.gaps.length === 1 ? '' : 's') + ' to review. ' +
            'Check it against your own records &mdash; and confirm anything uncertain with the relevant Texas agency.</p>' +
            (rows ? '<div class="gap-list">' + rows + '</div>'
                  : '<p>Your answers didn’t flag any gaps in this checklist. Keep the documents current and re-check anything you marked &ldquo;not sure&rdquo;.</p>') +
            '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px">' +
            '<a class="btn btn-primary" href="/#pricing">See the Compliance Kit &rarr;</a>' +
            '<button type="button" class="btn btn-secondary" data-act="print">Save as PDF</button>' +
            '<a class="btn btn-ghost" href="' + pdfFor(S.vertical) + '" download>Download the gap assessment</a>' +
            '</div></div>';
    }

    function pdfFor(v) {
        return {
            medspa: '/checklist/pdfs/medspa-gap-assessment-2026-08.pdf',
            dental: '/checklist/pdfs/dental-gap-assessment-2026-08.pdf',
            tattoo: '/checklist/pdfs/tattoo-gap-assessment-2026-08.pdf',
            esthetician: '/checklist/pdfs/aesthetic-gap-assessment-2026-08.pdf'
        }[v];
    }

    /* ---- Render + events ------------------------------------------------ */
    function render(focus) {
        var html = S.screen === 'intro' ? viewIntro()
                 : S.screen === 'gates' ? viewGates()
                 : S.screen === 'q' ? viewQuestion()
                 : S.screen === 'results' ? viewResults()
                 : viewPlan();
        root.innerHTML = html;
        if (focus) {
            var el = document.getElementById(focus);
            if (el) { el.focus(); }
        }
        save();
    }

    function buildQuestions() {
        var b = BANKS[S.vertical];
        S.qs = b.qs.filter(function (q) { return !q.g || S.gates[q.g]; });
    }

    root.addEventListener('click', function (e) {
        var vcard = e.target.closest('.vcard');
        if (vcard) {
            S.vertical = vcard.dataset.v;
            S.gates = {}; S.answers = {}; S.i = 0; S.started = Date.now();
            track('quiz_start', { vertical: S.vertical });
            S.screen = BANKS[S.vertical].gates.length ? 'gates' : 'q';
            if (S.screen === 'q') { buildQuestions(); }
            render();
            return;
        }
        var act = e.target.closest('[data-act]');
        if (!act) { return; }
        var a = act.dataset.act;

        if (a === 'startqs') { buildQuestions(); S.screen = 'q'; S.i = 0; render('qlegend'); }
        else if (a === 'next') {
            if (S.i < S.qs.length - 1) { S.i++; render('qlegend'); }
            else {
                S.result = score();
                S.screen = 'results';
                track('quiz_complete', {
                    vertical: S.vertical, score: S.result.pct, gap_count: S.result.gaps.length,
                    score_bucket: S.result.bucket,
                    duration_seconds: Math.round((Date.now() - S.started) / 1000)
                });
                track('results_viewed', { vertical: S.vertical, score_bucket: S.result.bucket });
                render('resh');
            }
        } else if (a === 'back') {
            if (S.screen === 'q' && S.i > 0) { S.i--; render('qlegend'); }
            else if (S.screen === 'q') { S.screen = BANKS[S.vertical].gates.length ? 'gates' : 'intro'; render(); }
            else { S.screen = 'intro'; render(); }
        } else if (a === 'restart') {
            try { sessionStorage.removeItem('cg-quiz'); } catch (err) {}
            S = { screen: 'intro', vertical: null, gates: {}, qs: [], i: 0, answers: {}, started: 0, result: null };
            render();
        } else if (a === 'print') {
            track('plan_printed', { vertical: S.vertical });
            window.print();
        }
    });

    root.addEventListener('change', function (e) {
        var t = e.target;
        if (t.name === 'a') {
            var q = S.qs[S.i];
            S.answers[q.id] = t.value;
            track('question_answered', {
                vertical: S.vertical, question_index: S.i + 1, question_id: q.id, answer: t.value
            });
            var btn = root.querySelector('[data-act="next"]');
            if (btn) { btn.disabled = false; }
            save();
        } else if (t.dataset && t.dataset.gate) {
            S.gates[t.dataset.gate] = t.checked;
            save();
        }
    });

    root.addEventListener('submit', function (e) {
        if (e.target.id !== 'planForm') { return; }
        e.preventDefault();
        var form = e.target;
        var btn = document.getElementById('planBtn');
        var err = document.getElementById('qerr');
        err.hidden = true;
        btn.disabled = true;
        btn.textContent = 'Sending…';

        var r = S.result;
        var fd = new FormData(form);
        fd.append('vertical', S.vertical);
        fd.append('score', r.pct);
        fd.append('gap_count', r.gaps.length);
        fd.append('score_bucket', r.bucket);
        r.cats.forEach(function (c) { fd.append('cat_' + c.key.toLowerCase(), c.pct); });
        fd.append('answers', S.qs.map(function (q) { return q.id + ':' + (S.answers[q.id] || 'skip'); }).join('|'));
        fd.append('quiz_version', VERSION);
        fd.append('page', '/assessment/');
        fd.append('_subject', 'Gap Assessment lead — ' + S.vertical + ' — ' + r.gaps.length + ' gaps');

        var ctrl = new AbortController();
        var timer = setTimeout(function () { ctrl.abort(); }, 15000);

        fetch(form.action, { method: 'POST', body: fd, headers: { Accept: 'application/json' }, signal: ctrl.signal })
            .then(function (res) {
                if (!res.ok) { throw new Error('bad status'); }
                track('email_submitted', { vertical: S.vertical, score_bucket: r.bucket, gap_count: r.gaps.length });
                track('generate_lead', { currency: 'USD', value: 25, vertical: S.vertical });
                S.screen = 'plan';
                render('resh');
                track('plan_viewed', { vertical: S.vertical });
            })
            .catch(function () { err.hidden = false; })
            .then(function () {
                clearTimeout(timer);
                btn.disabled = false;
                btn.innerHTML = 'Send my action plan &rarr;';
            });
    });

    restore();
    if (S.screen === 'q') { buildQuestions(); }
    render();
})();
