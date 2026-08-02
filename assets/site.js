/* Compliance Ghost — shared behaviour. Progressive enhancement only:
   every page works without this file (nav menu is CSS-only). */
(function () {
    'use strict';
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* Close the CSS-only mobile menu after a link is tapped */
    var toggle = document.getElementById('nav-toggle');
    if (toggle) {
        var links = document.querySelector('.nav-links');
        if (links) {
            links.addEventListener('click', function (e) {
                if (e.target.closest('a')) { toggle.checked = false; }
            });
        }
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && toggle.checked) { toggle.checked = false; }
        });
    }

    /* Sticky mobile buy bar — reveals after the hero, dismissible for the session */
    var bar = document.querySelector('.buybar');
    if (bar) {
        var dismissed = false;
        try { dismissed = sessionStorage.getItem('cg-buybar') === 'off'; } catch (err) {}
        var closeBtn = bar.querySelector('.buybar-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                bar.classList.remove('is-visible');
                try { sessionStorage.setItem('cg-buybar', 'off'); } catch (err) {}
                dismissed = true;
            });
        }
        if (!dismissed) {
            var onScroll = function () {
                if (dismissed) return;
                bar.classList.toggle('is-visible', window.scrollY > 600);
            };
            window.addEventListener('scroll', onScroll, { passive: true });
            onScroll();
        }
    }

    /* Exit intent — desktop only, and never on mobile entry (that is the pattern
       Google's intrusive-interstitial rule targets). Armed after 11s, shown once
       per 14 days, and skipped where it would be redundant or unwelcome. */
    (function exitIntent() {
        var path = location.pathname;
        var SKIP = ['/assessment/', '/thanks/', '/checklist/', '/privacy.html', '/terms.html'];
        if (SKIP.indexOf(path) !== -1) { return; }
        if (!window.matchMedia('(min-width: 861px)').matches) { return; }
        if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) { return; }

        var KEY = 'cg-exit-seen';
        try {
            var last = parseInt(localStorage.getItem(KEY) || '0', 10);
            if (last && Date.now() - last < 14 * 24 * 60 * 60 * 1000) { return; }
        } catch (e) {}

        var armed = false;
        setTimeout(function () { armed = true; }, 11000);

        function show() {
            if (!armed) { return; }
            armed = false;
            document.removeEventListener('mouseout', onOut);
            try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}

            var wrap = document.createElement('div');
            wrap.className = 'exit-modal';
            wrap.innerHTML =
                '<div class="exit-card" role="dialog" aria-modal="true" aria-labelledby="exit-h">' +
                  '<button type="button" class="exit-close" aria-label="Close">' +
                    '<svg class="ico ico-sm" viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>' +
                  '</button>' +
                  '<h2 id="exit-h">Before you go — see where you stand</h2>' +
                  '<p>Answer a few questions about your paperwork and get a scored breakdown of the documents your industry is expected to keep. Free, about two minutes, and you see the results without giving us an email.</p>' +
                  '<a class="btn btn-primary" href="/assessment/">Start the free assessment &rarr;</a>' +
                  '<button type="button" class="exit-dismiss">No thanks</button>' +
                '</div>';
            document.body.appendChild(wrap);

            var card = wrap.querySelector('.exit-card');
            var closeBtn = wrap.querySelector('.exit-close');
            var prevFocus = document.activeElement;
            closeBtn.focus();

            function close() {
                wrap.remove();
                document.removeEventListener('keydown', onKey);
                if (prevFocus && prevFocus.focus) { prevFocus.focus(); }
            }
            function onKey(e) {
                if (e.key === 'Escape') { close(); return; }
                if (e.key !== 'Tab') { return; }
                var f = card.querySelectorAll('a[href], button');
                var first = f[0], lastEl = f[f.length - 1];
                if (e.shiftKey && document.activeElement === first) { e.preventDefault(); lastEl.focus(); }
                else if (!e.shiftKey && document.activeElement === lastEl) { e.preventDefault(); first.focus(); }
            }
            document.addEventListener('keydown', onKey);
            closeBtn.addEventListener('click', close);
            wrap.querySelector('.exit-dismiss').addEventListener('click', close);
            wrap.addEventListener('click', function (e) { if (e.target === wrap) { close(); } });
            if (typeof gtag === 'function') { gtag('event', 'exit_intent_shown', { page: path }); }
        }

        function onOut(e) {
            if (e.clientY <= 0 && !e.relatedTarget) { show(); }
        }
        document.addEventListener('mouseout', onOut);
    })();

    /* Scroll reveal — opt-in via .reveal, skipped entirely under reduced motion */
    var targets = document.querySelectorAll('.reveal');
    if (targets.length) {
        if (reduced || !('IntersectionObserver' in window)) {
            targets.forEach(function (el) { el.classList.add('is-in'); });
        } else {
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-in');
                        io.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '0px 0px -8% 0px', threshold: .05 });
            targets.forEach(function (el) { io.observe(el); });
        }
    }
})();
