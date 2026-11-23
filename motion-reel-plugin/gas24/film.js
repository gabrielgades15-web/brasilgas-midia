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
  [3, 'A GENTE LEVA', 'thud', { pitch: 140, to: 60 }],
  [4, 'SUA RECARGA', 'pop', { pitch: 'E5' }],
  [7.5, 'whip to the shop', 'whoosh', { len: 0.5 }],
  [8, 'drop: revenda autorizada', 'impact'],
  [8.8, 'PARAGÁS', 'pop', { pitch: 'G5' }],
  [16.5, 'whip to Gás do Povo', 'whoosh', { len: 0.5 }],
  [17, 'TEM GÁS DO POVO', 'thud', { pitch: 120, to: 55 }],
  [17.8, 'AQUI', 'pop', { pitch: 'B5' }],
  [25.5, 'whip to entrega', 'whoosh', { len: 0.5 }],
  [26, 'PEDIU NO ZAP', 'click'],
  [27, 'CHEGA', 'pop', { pitch: 'D6' }],
  [30, 'água 20L slides in', 'whoosh', { len: 0.4, from: 2400, to: 600 }],
  [35.4, 'red wipe', 'riser', { len: 0.6 }],
  [36, 'end card', 'impact'],
  [37, 'WhatsApp button', 'bell', { pitch: 'G6' }],
  [42, 'button pulse', 'bell', { pitch: 'D6' }],
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
  const z = 1.0 * (1.32 / 1.0) ** E.inOutSine(prog(u, -1, 8.2));
  photo(ctx, IMG.p13, 0.5, 0.58, z, slide, 0);
  ctx.save(); ctx.translate(slide, 0);
  veil(ctx);
  logo(ctx, IMG.logo, LX + 150, S.y + 20, 300, springU(u, -0.3, SPRING.snappy));
  pill(ctx, 'RECARGA DE GÁS EM CASTANHAL', LX, S.y + 160, 40, C.yellow, C.redDeep, u, 0.5);
  headline(ctx, 'ACABOU', LX, S.y + 430, 190, u, -0.2);
  headline(ctx, 'O GÁS?', LX, S.y + 610, 190, u, 0.6, C.yellow);
  headline(ctx, 'A GENTE LEVA', LX, H - 640, 132, u, 3);
  headline(ctx, 'SUA RECARGA', LX, H - 495, 132, u, 4, C.yellow);
  ctx.restore();
}

// ---------------------------------------------------------------- S2 revenda autorizada (u 8..17): already framed on the PARAGÁS sign, slow push
function sShop(ctx, u, IMG, slide = 0) {
  const p = E.inOutSine(prog(u, 7.5, 17));
  photo(ctx, IMG.lateral, lerp(0.21, 0.16, p), 0.36, 1.18 * (1.32 / 1.18) ** p, slide, 0);
  ctx.save(); ctx.translate(slide, 0);
  veil(ctx, 0.95);
  pill(ctx, 'REVENDA AUTORIZADA PARAGÁS', LX, S.y + 40, 40, C.blue, C.white, u, 7.6);
  headline(ctx, 'RECARGA', LX, S.y + 330, 170, u, 7.8);
  headline(ctx, 'PARAGÁS', LX, S.y + 490, 170, u, 8.6, C.yellow);
  headline(ctx, 'ORIGINAL', LX, S.y + 625, 120, u, 9.6);
  ctx.restore();
}

// ---------------------------------------------------------------- S3 Gás do Povo (u 17..26): push in to the banner
function sPovo(ctx, u, IMG, slide = 0) {
  const z = 1.05 * (1.5 / 1.05) ** E.inOutSine(prog(u, 16.5, 26));
  photo(ctx, IMG.frente, 0.44, 0.47, z, slide, 0);
  ctx.save(); ctx.translate(slide, 0);
  veil(ctx, 0.95);
  pill(ctx, 'REVENDA CREDENCIADA', LX, S.y + 40, 40, C.yellow, C.redDeep, u, 16.6);
  headline(ctx, 'TEM GÁS', LX, S.y + 330, 170, u, 16.8);
  headline(ctx, 'DO POVO', LX, S.y + 490, 170, u, 17.4, C.yellow);
  headline(ctx, 'AQUI', LX, S.y + 625, 120, u, 18.2);
  ctx.restore();
}

// ---------------------------------------------------------------- S4 entrega (u 26..36): alças, then the 20 L card slides in
function sEntrega(ctx, u, IMG, slide = 0) {
  const z = 1.08 * (1.3 / 1.08) ** E.inOutSine(prog(u, 25.5, 36));
  photo(ctx, IMG.alcas, 0.52, 0.55, z, slide, 0);
  ctx.save(); ctx.translate(slide, 0);
  veil(ctx);
  pill(ctx, 'ENTREGA EM CASA', LX, S.y + 40, 40, C.yellow, C.redDeep, u, 25.6);
  headline(ctx, 'PEDIU NO ZAP,', LX, S.y + 290, 140, u, 25.8);
  headline(ctx, 'SUA RECARGA', LX, S.y + 430, 140, u, 26.6, C.yellow);
  headline(ctx, 'CHEGA', LX, S.y + 570, 140, u, 27.2);
  const k = springU(u, 30, SPRING.bouncy);
  if (k > 0.001) {
    const w = 430, h = 560, cx = W - 72 - w / 2 + 10, cy = lerp(H + h, S.y + S.h - h / 2 - 20, k);
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.06 + 0.03 * wobble(u - 30, 1.6, 3));
    rrect(ctx, -w / 2 - 10, -h / 2 - 10, w + 20, h + 20, 30); ctx.fillStyle = C.white; ctx.fill();
    rrect(ctx, -w / 2, -h / 2, w, h, 22); ctx.save(); ctx.clip();
    const s = Math.max(w / IMG.agua.width, h / IMG.agua.height) * 1.15;
    ctx.drawImage(IMG.agua, -IMG.agua.width * s * 0.5, -IMG.agua.height * s * 0.62, IMG.agua.width * s, IMG.agua.height * s);
    ctx.restore(); ctx.restore();
  }
  pill(ctx, '+ ÁGUA 20L', LX, S.y + 760, 56, C.yellow, C.redDeep, u, 30.4);
  pill(ctx, 'NO MESMO PEDIDO', LX, S.y + 880, 40, C.white, C.redDeep, u, 31);
  ctx.restore();
}

// ---------------------------------------------------------------- S5 end card (u 36..48, 5.6 s on screen)
function sEnd(ctx, u, IMG) {
  fill(ctx, C.red);
  ctx.fillStyle = C.redDeep; ctx.fillRect(0, S.y + 960, W, H - S.y - 960);
  logo(ctx, IMG.logo, W / 2, S.y + 170, 600, springU(u, 36, SPRING.bouncy));
  headlineC(ctx, 'CHAME NO', S.y + 590, 150, u, 36.4);
  headlineC(ctx, 'WHATSAPP', S.y + 740, 150, u, 36.8, C.yellow);
  const kb = springU(u, 37, SPRING.bouncy);
  if (kb > 0.001) {
    const pulse = 1 + 0.06 * Math.max(0, wobble(u - 38, 1.4, 4)) + 0.06 * Math.max(0, wobble(u - 42, 1.4, 4));
    const bw = 860, bh = 190, cx = W / 2, cy = S.y + 860;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(kb * pulse, kb * pulse);
    rrect(ctx, -bw / 2, -bh / 2, bw, bh, 34); ctx.fillStyle = C.green; ctx.fill();
    text(ctx, '(91) 98222-7035', 0, 18, font(104, 400, DISPLAY), C.white, 'center');
    text(ctx, 'PEÇA SUA RECARGA', 0, 72, font(34, 800, UI), C.white, 'center', 2);
    ctx.restore();
  }
  const kf2 = E.outQuint(prog(u, 37.8, 38.8));
  if (kf2 > 0) {
    const f = font(36, 800, UI), y0 = S.y + 1070 + (1 - kf2) * 40;
    ctx.globalAlpha = kf2;
    text(ctx, 'SEG A SÁB, 7H ÀS 20H', W / 2, y0, f, C.white, 'center');
    text(ctx, 'DOMINGOS E FERIADOS, 7H ÀS 13H', W / 2, y0 + 56, f, C.white, 'center');
    text(ctx, 'ALAMEDA PADRE ROLIM, 139 · CASTANHAL', W / 2, y0 + 112, f, C.yellow, 'center');
    ctx.globalAlpha = 1;
  }
}

// whip: A slides out left while B slides in from the right, both fully drawn (veil + type), no empty frame
function whip(ctx, u, IMG, A, B, u0) {
  const p = E.inOutCubic(prog(u, u0, u0 + 0.6));
  const xa = -p * W, xb = (1 - p) * W;
  ctx.save(); ctx.beginPath(); ctx.rect(xa, 0, W, H); ctx.clip(); A(ctx, u, IMG, xa); ctx.restore();
  ctx.save(); ctx.beginPath(); ctx.rect(xb, 0, W, H); ctx.clip(); B(ctx, u, IMG, xb); ctx.restore();
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
    if (u < 8.1) return whip(ctx, u, IMG, sHook, sShop, 7.5);
    if (u < 16.5) return sShop(ctx, u, IMG);
    if (u < 17.1) return whip(ctx, u, IMG, sShop, sPovo, 16.5);
    if (u < 25.5) return sPovo(ctx, u, IMG);
    if (u < 26.1) return whip(ctx, u, IMG, sPovo, sEntrega, 25.5);
    if (u < 35.4) return sEntrega(ctx, u, IMG);
    if (u < 36) {
      sEntrega(ctx, u, IMG);
      const p = E.inCubic(prog(u, 35.4, 36));
      ctx.fillStyle = C.red; ctx.fillRect(0, H * (1 - p), W, H * p);
      return;
    }
    sEnd(ctx, u, IMG);
  },
});
