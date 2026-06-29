/* ============================================================
   Punctum — living cosmos background.
   Decorative twinkling stars + a periodic shooting star, drawn
   on a canvas behind the page. These are the DECORATIVE stars of
   the night sky — distinct from the single gold protagonist star
   ("the now") that lives inside the app itself.
   Honours prefers-reduced-motion with a single static frame.
   ============================================================ */
(function () {
  var canvas = document.getElementById('starfield');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
  var stars = [], shoot = null, nextShoot = 0;

  function rand(a, b) { return a + Math.random() * (b - a); }

  function build() {
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = Math.floor(W * dpr); canvas.height = Math.floor(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var area = W * H;
    var far = Math.round(area / 14000);   // distant, faint
    var near = Math.round(area / 9000);   // nearer, brighter
    stars = [];
    seed(far, 0.6, 1.1, 0.20, 0.40, 20000, 38000);
    seed(near, 1.0, 1.7, 0.40, 0.75, 14000, 30000);
  }

  function seed(n, rMin, rMax, aMin, aMax, lifeMin, lifeMax) {
    for (var i = 0; i < n; i++) {
      stars.push({
        x: Math.random() * W, y: Math.random() * H,
        r: rand(rMin, rMax),
        base: rand(aMin, aMax), amp: rand(0.12, 0.34),
        freq: rand(0.0005, 0.0016), phase: rand(0, Math.PI * 2),
        born: performance.now() - Math.random() * lifeMax,
        life: rand(lifeMin, lifeMax)
      });
    }
  }

  function respawn(s, t) {
    s.x = Math.random() * W; s.y = Math.random() * H;
    s.r = rand(0.6, 1.7); s.base = rand(0.2, 0.75);
    s.born = t; s.life = rand(16000, 34000);
  }

  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < stars.length; i++) {
      var s = stars[i];
      var age = t - s.born;
      if (age > s.life) { respawn(s, t); age = 0; }
      var u = age / s.life;                       // 0..1 life
      var fade = u < 0.12 ? u / 0.12 : (u > 0.7 ? (1 - u) / 0.3 : 1);
      var tw = s.base + Math.sin(t * s.freq + s.phase) * s.amp;
      var a = Math.max(0, Math.min(1, tw)) * Math.max(0, fade);
      if (a <= 0) continue;
      ctx.globalAlpha = a;
      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalAlpha = 1;
    drawShoot(t);
  }

  function drawShoot(t) {
    if (!shoot && t > nextShoot) {
      if (Math.random() < 0.5) {
        shoot = { t0: t, dur: 2200, x: rand(W * 0.1, W * 0.7), y: rand(-10, H * 0.3),
                  ang: rand(0.32, 0.6), len: rand(90, 150), speed: rand(0.5, 0.85) };
      }
      nextShoot = t + rand(8000, 16000);
    }
    if (!shoot) return;
    var p = (t - shoot.t0) / shoot.dur;
    if (p >= 1) { shoot = null; return; }
    var ease = p * p;                              // accelerate
    var dist = ease * Math.max(W, H) * shoot.speed;
    var cx = shoot.x + Math.cos(shoot.ang) * dist;
    var cy = shoot.y + Math.sin(shoot.ang) * dist;
    var tx = cx - Math.cos(shoot.ang) * shoot.len;
    var ty = cy - Math.sin(shoot.ang) * shoot.len;
    var alpha = (p < 0.15 ? p / 0.15 : (1 - p) / 0.85);
    var g = ctx.createLinearGradient(tx, ty, cx, cy);
    g.addColorStop(0, 'rgba(255,255,255,0)');
    g.addColorStop(1, 'rgba(255,244,214,' + Math.max(0, alpha) + ')');
    ctx.strokeStyle = g; ctx.lineWidth = 1.6; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(tx, ty); ctx.lineTo(cx, cy); ctx.stroke();
    ctx.globalAlpha = Math.max(0, alpha); ctx.fillStyle = '#FFFDF2';
    ctx.beginPath(); ctx.arc(cx, cy, 1.5, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;
  }

  var raf = 0;
  function loop(t) { draw(t); raf = requestAnimationFrame(loop); }

  function start() {
    build();
    if (reduce) { draw(performance.now()); return; }
    cancelAnimationFrame(raf); raf = requestAnimationFrame(loop);
  }

  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer); resizeTimer = setTimeout(start, 180);
  });
  start();
})();
