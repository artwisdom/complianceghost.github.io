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
