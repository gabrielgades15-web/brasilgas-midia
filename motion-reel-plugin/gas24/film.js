// Acabou o gás? A gente leva sua recarga — Brasilgás. Pure function of time (window.seek(t)).
// Timing in beats (u) on the measured grid (128 bpm, 32 beats). Plan: docs/shotlist.md (approved 23/11/2026).
import * as M from './lib/motion.js';

const { W, H, FORMAT, E, prog, lerp, clamp, springU, springKeys, SPRING, wobble, font, layout, glyph, text, fill, rrect, crop, mix } = M;

// Brand tokens (templates/post.html of brasilgas-midia). Red is the field, yellow the one accent.
const C = { red: '#E1061A', redDeep: '#A30F1C', blue: '#1D4FA3', yellow: '#FFC72C', green: '#25D366', white: '#FFFFFF', ink: '#2B0306' };
const DISPLAY = 'Display', UI = 'UI';

const HITS = [
  [0, 'hook: ACABOU O GÁS?', 'impact'],
  [0.5, 'kicker', 'click'],
  [4, 'A GENTE LEVA', 'thud', { pitch: 140, to: 60 }],
  [5, 'SUA RECARGA', 'pop', { pitch: 'E5' }],
  [7.5, 'whip to the shop', 'whoosh', { len: 0.5 }],
  [8, 'drop: revenda autorizada', 'impact'],
  [9, 'RECARGA PARAGÁS', 'pop', { pitch: 'G5' }],
  [12, 'camera lands on the sign', 'tick'],
  [14, 'cut: Gás do Povo', 'thud', { pitch: 120, to: 55 }],
  [15, 'TEM GÁS DO POVO', 'pop', { pitch: 'B5' }],
  [20, 'cut: entrega', 'click'],
  [20.5, 'PEDIU NO ZAP', 'pop', { pitch: 'D6' }],
  [23, 'água 20L slides in', 'whoosh', { len: 0.4, from: 2400, to: 600 }],
  [25.5, 'red wipe', 'riser', { len: 0.6 }],
  [26, 'end card', 'impact'],
  [27, 'WhatsApp button', 'bell', { pitch: 'G6' }],
];

// ---------------------------------------------------------------- helpers
// Cover-fit a photo with the focal point (px, py in 0..1 of the image) as close to the frame centre as the edges allow.
function photo(ctx, img, px, py, zoom = 1, ox = 0, oy = 0) {
  const s = Math.max(W / img.width, H / img.height) * zoom;
  const dw = img.width * s, dh = img.height * s;
  const x = clamp(W / 2 - px * dw, W - dw, 0) + ox;
  const y = clamp(H / 2 - py * dh, H - dh, 0) + oy;
  ctx.drawImage(img, x, y, dw, dh);
}
// Brand veil: deep red over the top and bottom thirds so white type reads, the middle shows the photo.
function veil(ctx, a = 1) {
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, `rgba(163,15,28,${0.92 * a})`);
  g.addColorStop(0.34, `rgba(163,15,28,${0.45 * a})`);
  g.addColorStop(0.55, 'rgba(163,15,28,0)');
  g.addColorStop(0.78, `rgba(120,8,18,${0.55 * a})`);
  g.addColorStop(1, `rgba(90,6,14,${0.95 * a})`);
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
}
// Per-glyph headline line: glyphs rise into place on a spring, staggered left to right.
function headline(ctx, str, x, base, size, u, u0, color = C.white, exitU = null) {
  const f = font(size, 400, DISPLAY), L = layout(ctx, str, f, 0);
  L.glyphs.forEach((g, j) => {
    const k = springU(u, u0 + j * 0.035, SPRING.bouncy);
    if (k <= 0.001) return;
    let dy = (1 - k) * size * 0.9;
    if (exitU !== null) dy -= E.inBack(prog(u, exitU + j * 0.01, exitU + 0.35 + j * 0.01), 1.3) * (H * 0.6);
    ctx.save(); ctx.beginPath(); ctx.rect(0, base - size * 1.15, W, size * 1.4); ctx.clip();
    glyph(ctx, g.ch, x + g.cx, base + dy, f, color);
    ctx.restore();
  });
  return L.width;
}
function headlineC(ctx, str, base, size, u, u0, color = C.white) {
  const L = layout(ctx, str, font(size, 400, DISPLAY), 0);
  return headline(ctx, str, (W - L.width) / 2, base, size, u, u0, color);
}
// Pill label (kicker). Slides in from the left with a snappy spring; text in Montserrat 800 uppercase.
function pill(ctx, str, x, y, size, bg, fg, u, u0) {
  const k = springU(u, u0, SPRING.snappy);
  if (k <= 0.001) return;
  const f = font(size, 800, UI);
  ctx.font = f; const w = ctx.measureText(str).width + size * 1.3, h = size * 1.75;
  ctx.save();
  ctx.translate(lerp(-w - 80, 0, k), 0);
  rrect(ctx, x, y, w, h, h * 0.28); ctx.fillStyle = bg; ctx.fill();
  text(ctx, str, x + size * 0.65, y + h * 0.68, f, fg);
  ctx.restore();
}
// The Brasilgás wordmark card, cropped from the real profile picture (white card in the middle of the red square).
function logo(ctx, img, cx, cy, w, k = 1) {
  if (!img || k <= 0.001) return;
  const sx = img.width * 0.155, sy = img.height * 0.265, sw = img.width * 0.69, sh = img.height * 0.47;
  const h = w * sh / sw;
  ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k);
  rrect(ctx, -w / 2, -h / 2, w, h, w * 0.06); ctx.clip();
  crop(ctx, img, [sx, sy, sw, sh], -w / 2, -h / 2, w, h);
  ctx.restore();
}
const S = FORMAT.safe;           // 9x16: x 72..1008, y 250..1490
const LX = S.x + 4;

// ---------------------------------------------------------------- S1 hook (u 0..8): P13 row, camera pushes in
function sHook(ctx, u, IMG, slide = 0) {
  const z = 1.0 * (1.32 / 1.0) ** E.inOutSine(prog(u, -1, 8));          // log-space dolly
  photo(ctx, IMG.p13, 0.5, 0.58, z, slide, 0);
  ctx.save(); ctx.translate(slide, 0);
  veil(ctx);
  logo(ctx, IMG.logo, LX + 150, S.y + 20, 300, springU(u, -0.3, SPRING.snappy));
  pill(ctx, 'RECARGA DE GÁS EM CASTANHAL', LX, S.y + 160, 40, C.yellow, C.redDeep, u, 0.5);
  headline(ctx, 'ACABOU', LX, S.y + 430, 190, u, -0.2);
  headline(ctx, 'O GÁS?', LX, S.y + 610, 190, u, 0.6, C.yellow);
  // answer lands on beat 4, bottom third
  headline(ctx, 'A GENTE LEVA', LX, H - 640, 132, u, 4);
  headline(ctx, 'SUA RECARGA', LX, H - 495, 132, u, 5, C.yellow);
  ctx.restore();
}

// ---------------------------------------------------------------- S2 revenda autorizada (u 8..14): pan along the wall to the PARAGÁS sign
function sShop(ctx, u, IMG, slide = 0) {
  const p = E.inOutCubic(prog(u, 7.5, 12.2));
  const fx = lerp(0.5, 0.17, p), z = 1.0 * (1.28) ** p;
  photo(ctx, IMG.lateral, fx, 0.30, z, slide, 0);
  ctx.save(); ctx.translate(slide, 0);
  veil(ctx, 0.95);
  pill(ctx, 'REVENDA AUTORIZADA PARAGÁS', LX, S.y + 40, 40, C.blue, C.white, u, 8.3);
  headline(ctx, 'RECARGA', LX, S.y + 330, 170, u, 8.8);
  headline(ctx, 'PARAGÁS', LX, S.y + 490, 170, u, 9.4, C.yellow);
  headline(ctx, 'ORIGINAL', LX, S.y + 625, 120, u, 10.2);
  ctx.restore();
}

// ---------------------------------------------------------------- S3 Gás do Povo (u 14..20): push in to the banner
function sPovo(ctx, u, IMG) {
  const z = 1.05 * (1.6 / 1.05) ** E.outCubic(prog(u, 14, 20.5));
  photo(ctx, IMG.frente, 0.44, 0.47, z);
  veil(ctx, 0.95);
  pill(ctx, 'REVENDA CREDENCIADA', LX, S.y + 40, 40, C.yellow, C.redDeep, u, 14);
  headline(ctx, 'TEM GÁS', LX, S.y + 330, 170, u, 14.3);
  headline(ctx, 'DO POVO', LX, S.y + 490, 170, u, 14.9, C.yellow);
  headline(ctx, 'AQUI', LX, S.y + 625, 120, u, 15.7);
}

// ---------------------------------------------------------------- S4 entrega (u 20..26): alças, then the 20 L card slides in
function sEntrega(ctx, u, IMG) {
  const z = 1.08 * (1.3 / 1.08) ** E.inOutSine(prog(u, 20, 26));
  photo(ctx, IMG.alcas, 0.52, 0.55, z);
  veil(ctx);
  pill(ctx, 'ENTREGA EM CASA', LX, S.y + 40, 40, C.yellow, C.redDeep, u, 20);
  headline(ctx, 'PEDIU NO ZAP,', LX, S.y + 290, 140, u, 20.2);
  headline(ctx, 'SUA RECARGA', LX, S.y + 430, 140, u, 21.2, C.yellow);
  headline(ctx, 'CHEGA', LX, S.y + 570, 140, u, 21.8);
  // water card: real photo in a tilted card, springs up from below on beat 23
  const k = springU(u, 23, SPRING.bouncy);
  if (k > 0.001) {
    const w = 430, h = 560, cx = W - 72 - w / 2 + 10, cy = lerp(H + h, S.y + S.h - h / 2 - 20, k);
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.06 + 0.03 * wobble(u - 23, 1.6, 3));
    rrect(ctx, -w / 2 - 10, -h / 2 - 10, w + 20, h + 20, 30); ctx.fillStyle = C.white; ctx.fill();
    rrect(ctx, -w / 2, -h / 2, w, h, 22); ctx.save(); ctx.clip();
    const s = Math.max(w / IMG.agua.width, h / IMG.agua.height) * 1.15;
    ctx.drawImage(IMG.agua, -IMG.agua.width * s * 0.5, -IMG.agua.height * s * 0.62, IMG.agua.width * s, IMG.agua.height * s);
    ctx.restore(); ctx.restore();
  }
  const kp = springU(u, 23.4, SPRING.snappy);
  if (kp > 0.001) pill(ctx, '+ ÁGUA 20L', LX, S.y + 760, 56, C.yellow, C.redDeep, u, 23.4);
  if (kp > 0.001) pill(ctx, 'NO MESMO PEDIDO', LX, S.y + 880, 40, C.white, C.redDeep, u, 23.7);
}

// ---------------------------------------------------------------- S5 end card (u 26..32)
function sEnd(ctx, u, IMG) {
  fill(ctx, C.red);
  // soft darker band behind the footer for structure (flat, not a gradient)
  ctx.fillStyle = C.redDeep; ctx.fillRect(0, S.y + 960, W, H - S.y - 960);
  const kl = springU(u, 26, SPRING.bouncy);
  logo(ctx, IMG.logo, W / 2, S.y + 170, 600, kl);
  // headline
  headlineC(ctx, 'CHAME NO', S.y + 590, 150, u, 26.4);
  headlineC(ctx, 'WHATSAPP', S.y + 740, 150, u, 26.8, C.yellow);
  // button: springs in on 27, one pulse on 28
  const kb = springU(u, 27, SPRING.bouncy);
  if (kb > 0.001) {
    const pulse = 1 + 0.06 * Math.max(0, wobble(u - 28, 1.4, 4));
    const bw = 860, bh = 190, cx = W / 2, cy = S.y + 860;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(kb * pulse, kb * pulse);
    rrect(ctx, -bw / 2, -bh / 2, bw, bh, 34); ctx.fillStyle = C.green; ctx.fill();
    text(ctx, '(91) 98222-7035', 0, 18, font(104, 400, DISPLAY), C.white, 'center');
    text(ctx, 'PEÇA SUA RECARGA', 0, 72, font(34, 800, UI), C.white, 'center', 2);
    ctx.restore();
  }
  const kf2 = E.outQuint(prog(u, 27.6, 28.4));
  if (kf2 > 0) {
    const f = font(36, 800, UI), y0 = S.y + 1070 + (1 - kf2) * 40;
    ctx.globalAlpha = kf2;
    text(ctx, 'SEG A SÁB, 7H ÀS 20H', W / 2, y0, f, C.white, 'center');
    text(ctx, 'DOMINGOS E FERIADOS, 7H ÀS 13H', W / 2, y0 + 56, f, C.white, 'center');
    text(ctx, 'ALAMEDA PADRE ROLIM, 139 · CASTANHAL', W / 2, y0 + 112, f, C.yellow, 'center');
    ctx.globalAlpha = 1;
  }
}

M.film({
  fonts: [font(100, 400, DISPLAY), font(40, 800, UI)],
  images: {
    p13: 'assets/estoque-p13-ceu-azul.jpg', lateral: 'assets/fachada-paragas-lateral-1.jpg',
    frente: 'assets/fachada-frente-gas-do-povo.jpg', alcas: 'assets/estoque-p13-alcas-ceu.jpg',
    agua: 'assets/porta-grade-galoes.jpg', logo: 'assets/logo-perfil.png',
  },
  hits: HITS,
  draw(ctx, u, t, IMG) {
    if (u < 7.5) return sHook(ctx, u, IMG);
    if (u < 8.15) {                     // whip: hook slides out left while the shop slides in, both on screen
      const p = E.inOutCubic(prog(u, 7.5, 8.15));
      sHook(ctx, u, IMG, -p * W);
      sShop(ctx, u, IMG, (1 - p) * W);
      return;
    }
    if (u < 14) return sShop(ctx, u, IMG);
    if (u < 20) return sPovo(ctx, u, IMG);
    if (u < 25.5) return sEntrega(ctx, u, IMG);
    if (u < 26) {                       // red wipe up from the bottom carries into the end card
      sEntrega(ctx, u, IMG);
      const p = E.inCubic(prog(u, 25.5, 26));
      ctx.fillStyle = C.red; ctx.fillRect(0, H * (1 - p), W, H * p);
      return;
    }
    sEnd(ctx, u, IMG);
  },
});
