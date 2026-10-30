/* Figura de traço em vista lateral. Uma pose é o esqueleto em ângulos (ver o _nota de conteudo/esercizi.json);
   o exercício vai e volta entre a pose A e a B. Sem imagem nem vídeo: o app fica leve e funciona offline. */
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const R = Math.PI / 180;
  const v = (a, l) => [Math.cos(a * R) * l, Math.sin(a * R) * l];
  const soma = (p, q) => [p[0] + q[0], p[1] + q[1]];
  const mistura = (a, b, f) => Array.isArray(a) ? a.map((x, i) => mistura(x, b[i], f)) : a + (b - a) * f;

  function pose(A, B, f) {
    const o = {};
    for (const k of new Set([...Object.keys(A), ...Object.keys(B)])) {
      const a = A[k] ?? B[k], b = B[k] ?? A[k];
      o[k] = typeof a === 'string' ? a : mistura(a, b, f);
    }
    return o;
  }

  function pontos(p) {
    const H = p.h, S = soma(H, v(p.t, 58)), Sa = soma(S, [0, p.sh || 0]);
    const n = [-Math.sin(p.t * R), Math.cos(p.t * R)], meio = [(H[0] + S[0]) / 2, (H[1] + S[1]) / 2];
    const C = [meio[0] + n[0] * (p.c || 0) * 2, meio[1] + n[1] * (p.c || 0) * 2];
    const cab = soma(soma(S, v(p.t + (p.k || 0), 15)), p.hd || [0, 0]);
    const braco = a => { const e = soma(Sa, v(a[0], 30)); return [Sa, e, soma(e, v(a[1], 28))]; };
    const perna = l => { const j = soma(H, v(l[0], 40)); return [H, j, soma(j, v(l[1], 40))]; };
    return { H, S, C, cab, a1: braco(p.a1), a2: braco(p.a2), l1: perna(p.l1), l2: perna(p.l2) };
  }

  const el = (n, a) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); return e; };
  const linha = q => q.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ');

  function sedia(svg) {
    const g = el('g', { class: 'adereco' });
    g.appendChild(el('path', { d: 'M88 104 H138 M92 104 V140 M134 104 V140 M90 104 V52' }));
    svg.appendChild(g);
  }

  /* Enquadra o exercício: a caixa que cobre as duas poses (e a cadeira), com folga, no formato 4:3. */
  function quadro(ex) {
    const ps = [0, 1].map(f => pontos(pose(ex.A, ex.B, f)));
    const xs = [], ys = [];
    ps.forEach(q => { [q.H, q.S, q.cab, ...q.a1, ...q.a2, ...q.l1, ...q.l2].forEach(p => { xs.push(p[0]); ys.push(p[1]); }); ys.push(q.cab[1] - 11); });
    if (ex.p === 'sedia') { xs.push(88, 138); ys.push(52); }
    ys.push(141);
    let x0 = Math.min(...xs) - 16, x1 = Math.max(...xs) + 16, y0 = Math.min(...ys) - 14, y1 = 147;
    let w = x1 - x0, h = y1 - y0;
    if (w / h > 4 / 3) { const nh = w * 3 / 4; y0 -= nh - h; h = nh; } else { const nw = h * 4 / 3; x0 -= (nw - w) / 2; w = nw; }
    return [x0, y0, w, h].map(n => n.toFixed(1)).join(' ');
  }

  /* Desenha a pose num <svg>; devolve a função que redesenha com a fração f (0 = A, 1 = B). */
  function montar(svg, ex) {
    svg.setAttribute('viewBox', quadro(ex));
    svg.innerHTML = '';
    svg.appendChild(el('line', { x1: -200, y1: 141, x2: 440, y2: 141, class: 'chao' }));
    if (ex.p === 'sedia') sedia(svg);
    const longe = el('g', { class: 'longe' }), perto = el('g', { class: 'perto' });
    const pl2 = el('path', {}), pa2 = el('path', {}), tronco = el('path', {}), pl1 = el('path', {}), pa1 = el('path', {});
    const cab = el('circle', { r: 10.5 });
    longe.append(pl2, pa2); perto.append(tronco, pl1, pa1, cab);
    svg.append(longe, perto);
    return f => {
      const q = pontos(pose(ex.A, ex.B, f));
      pl2.setAttribute('d', linha(q.l2)); pa2.setAttribute('d', linha(q.a2));
      tronco.setAttribute('d', `M${q.H[0].toFixed(1)} ${q.H[1].toFixed(1)} Q${q.C[0].toFixed(1)} ${q.C[1].toFixed(1)} ${q.S[0].toFixed(1)} ${q.S[1].toFixed(1)}`);
      pl1.setAttribute('d', linha(q.l1)); pa1.setAttribute('d', linha(q.a1));
      cab.setAttribute('cx', q.cab[0].toFixed(1)); cab.setAttribute('cy', q.cab[1].toFixed(1));
    };
  }

  /* Anima ida e volta: segura em A, vai, segura em B, volta. Devolve a função que para. */
  function animar(svg, ex) {
    const desenha = montar(svg, ex), T = (ex.v || 5) * 1000;
    let vivo = true, t0 = performance.now();
    const passo = agora => {
      if (!vivo) return;
      const x = ((agora - t0) % T) / T;
      const f = x < .15 ? 0 : x < .5 ? .5 - .5 * Math.cos(Math.PI * (x - .15) / .35) : x < .65 ? 1 : .5 + .5 * Math.cos(Math.PI * (x - .65) / .35);
      desenha(f);
      requestAnimationFrame(passo);
    };
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) desenha(1); else requestAnimationFrame(passo);
    return () => { vivo = false; };
  }

  window.Figura = { montar, animar };
})();
