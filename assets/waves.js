/* Decorative wave field behind light sections. Extracted from index.html
   during the refresh so every page can share it; skipped entirely when the
   visitor prefers reduced motion. */
(function () {
    'use strict';
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { return; }
document.addEventListener('DOMContentLoaded', function() {
    var WAVE_COUNT = 5;
    var MOUSE_RADIUS = 220;
    var MOUSE_STRENGTH = 18;

    var systems = [];

    document.querySelectorAll('.light-bg-effects').forEach(function(section) {
        var canvas = section.querySelector('.particle-canvas');
        if (!canvas) return;
        var ctx = canvas.getContext('2d');
        var mouse = { x: -9999, y: -9999, smoothX: -9999, smoothY: -9999, active: false };
        var w = 0, h = 0;

        // Each wave has its own properties
        var waves = [];
        for (var i = 0; i < WAVE_COUNT; i++) {
            waves.push({
                baseY: 0,           // set on resize
                amplitude: 18 + i * 8,
                frequency: 0.003 + i * 0.0008,
                speed: 0.0004 + i * 0.00012,
                phase: i * 1.2,
                lineWidth: 1.8 - i * 0.15,
                // Alternate between teal and green tones
                color: i % 2 === 0
                    ? { r: 78, g: 205, b: 196 }    // teal
                    : { r: 46, g: 204, b: 113 },   // green
                alpha: 0.08 + (WAVE_COUNT - i) * 0.015
            });
        }

        function resize() {
            var rect = section.getBoundingClientRect();
            var dpr = Math.min(window.devicePixelRatio || 1, 2);
            w = rect.width;
            h = rect.height;
            canvas.width = w * dpr;
            canvas.height = h * dpr;
            canvas.style.width = w + 'px';
            canvas.style.height = h + 'px';
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            // Distribute wave baselines evenly across section height
            for (var i = 0; i < waves.length; i++) {
                waves[i].baseY = h * (0.2 + (i / (waves.length - 1)) * 0.6);
            }
        }

        resize();

        section.addEventListener('mousemove', function(e) {
            var rect = section.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
            mouse.active = true;
        });

        section.addEventListener('mouseleave', function() {
            mouse.active = false;
        });

        systems.push({ ctx: ctx, waves: waves, mouse: mouse, section: section, resize: resize, w: function() { return w; }, h: function() { return h; } });
    });

    window.addEventListener('resize', function() {
        systems.forEach(function(s) { s.resize(); });
    });

    function animate(now) {
        for (var s = 0; s < systems.length; s++) {
            var sys = systems[s];
            var ctx = sys.ctx;
            var wavesArr = sys.waves;
            var m = sys.mouse;
            var cw = sys.w();
            var ch = sys.h();

            // Smooth the mouse position for fluid interaction
            if (m.active) {
                m.smoothX += (m.x - m.smoothX) * 0.035;
                m.smoothY += (m.y - m.smoothY) * 0.035;
            } else {
                m.smoothX += (-9999 - m.smoothX) * 0.03;
                m.smoothY += (-9999 - m.smoothY) * 0.03;
            }

            ctx.clearRect(0, 0, cw, ch);

            // Draw each wave
            for (var wi = 0; wi < wavesArr.length; wi++) {
                var wave = wavesArr[wi];
                var c = wave.color;
                var step = 4; // pixel step for smoothness

                // Build points array for this wave
                var points = [];
                for (var x = -step; x <= cw + step; x += step) {
                    // Base sine wave
                    var y = wave.baseY
                        + Math.sin(x * wave.frequency + now * wave.speed + wave.phase) * wave.amplitude
                        + Math.sin(x * wave.frequency * 0.6 + now * wave.speed * 0.7 + wave.phase + 2) * wave.amplitude * 0.4;

                    // Mouse displacement — push wave away from cursor
                    var dx = x - m.smoothX;
                    var dy = y - m.smoothY;
                    var dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < MOUSE_RADIUS && dist > 1) {
                        var pushStrength = (1 - dist / MOUSE_RADIUS);
                        pushStrength = pushStrength * pushStrength; // ease-in curve
                        y += (dy / dist) * pushStrength * MOUSE_STRENGTH;
                    }

                    points.push({ x: x, y: y });
                }

                // Draw the wave line
                ctx.beginPath();
                ctx.moveTo(points[0].x, points[0].y);
                for (var p = 1; p < points.length - 1; p++) {
                    // Smooth curve through points
                    var xc = (points[p].x + points[p + 1].x) / 2;
                    var yc = (points[p].y + points[p + 1].y) / 2;
                    ctx.quadraticCurveTo(points[p].x, points[p].y, xc, yc);
                }
                ctx.strokeStyle = 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',' + wave.alpha + ')';
                ctx.lineWidth = wave.lineWidth;
                ctx.stroke();

                // Draw soft glow underneath wave (filled area to bottom)
                ctx.beginPath();
                ctx.moveTo(points[0].x, points[0].y);
                for (var p = 1; p < points.length - 1; p++) {
                    var xc = (points[p].x + points[p + 1].x) / 2;
                    var yc = (points[p].y + points[p + 1].y) / 2;
                    ctx.quadraticCurveTo(points[p].x, points[p].y, xc, yc);
                }
                ctx.lineTo(cw + step, points[points.length - 1].y);
                ctx.lineTo(cw + step, points[points.length - 1].y + 60);
                ctx.lineTo(-step, points[0].y + 60);
                ctx.closePath();
                var glow = ctx.createLinearGradient(0, wave.baseY - 10, 0, wave.baseY + 60);
                glow.addColorStop(0, 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',' + (wave.alpha * 0.4) + ')');
                glow.addColorStop(1, 'rgba(' + c.r + ',' + c.g + ',' + c.b + ',0)');
                ctx.fillStyle = glow;
                ctx.fill();
            }

            // Soft mouse glow
            if (m.active) {
                var mg = ctx.createRadialGradient(m.smoothX, m.smoothY, 0, m.smoothX, m.smoothY, 160);
                mg.addColorStop(0, 'rgba(78, 205, 196, 0.04)');
                mg.addColorStop(0.5, 'rgba(78, 205, 196, 0.015)');
                mg.addColorStop(1, 'rgba(78, 205, 196, 0)');
                ctx.beginPath();
                ctx.fillStyle = mg;
                ctx.arc(m.smoothX, m.smoothY, 160, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);
});
})();
