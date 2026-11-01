'use strict';

/* 키오스크 데모: 탭 전환, 화면에 가까워지면 iframe 불러오기, 처음 상태로 되돌리기 */
(() => {
  const demo = document.querySelector('[data-demo]');
  if (!demo) return;

  const tabs = [...demo.querySelectorAll('[role="tab"]')];
  const panes = [...demo.querySelectorAll('.pane')];
  const wide = window.matchMedia('(min-width: 860px)');
  let loaded = false;
  let current = 'order';

  function load(pane) {
    const frame = pane.querySelector('iframe');
    if (loaded && !frame.src && frame.dataset.src) frame.src = frame.dataset.src;
  }

  // 칸이 이 폭보다 좁으면 이 폭으로 그린 뒤 줄인다 (키오스크 화면은 태블릿 기준이라 좁으면 잘린다).
  const BASE_WIDTH = 520;
  function fit(pane) {
    const w = pane.clientWidth;
    const h = pane.clientHeight;
    if (!w) return;
    const frame = pane.querySelector('iframe');
    const s = Math.min(1, w / BASE_WIDTH);
    frame.style.width = s < 1 ? `${w / s}px` : '';
    frame.style.height = s < 1 ? `${h / s}px` : '';
    frame.style.transform = s < 1 ? `scale(${s})` : '';
  }
  const fitAll = () => panes.forEach(fit);
  if ('ResizeObserver' in window) new ResizeObserver(fitAll).observe(demo);
  else window.addEventListener('resize', fitAll);

  function show(view) {
    // 넓은 화면에서는 주문 화면이 늘 왼쪽에 있으므로, 오른쪽에 보일 화면만 고른다.
    if (wide.matches && view === 'order') view = 'station1';
    current = view;
    for (const t of tabs) t.setAttribute('aria-selected', String(t.dataset.view === view));
    for (const p of panes) {
      const visible = p.dataset.view === view || (wide.matches && p.dataset.view === 'order');
      p.hidden = !visible;
      if (visible) { load(p); fit(p); }
    }
  }

  tabs.forEach((t) => t.addEventListener('click', () => show(t.dataset.view)));
  demo.querySelector('[role="tablist"]').addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const visibleTabs = tabs.filter((t) => getComputedStyle(t).display !== 'none');
    const i = visibleTabs.findIndex((t) => t.dataset.view === current);
    const next = visibleTabs[(i + (e.key === 'ArrowRight' ? 1 : -1) + visibleTabs.length) % visibleTabs.length];
    show(next.dataset.view);
    next.focus();
  });
  wide.addEventListener('change', () => show(current));

  function start() {
    if (loaded) return;
    loaded = true;
    show(current);
  }
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { io.disconnect(); start(); }
    }, { rootMargin: '400px 0px' });
    io.observe(demo);
  } else {
    start();
  }

  demo.querySelector('[data-reset]').addEventListener('click', () => {
    start();
    const frame = panes.map((p) => p.querySelector('iframe')).find((f) => f.src && f.contentWindow && f.contentWindow.KioskDemo);
    if (frame) {
      frame.contentWindow.KioskDemo.reset();
    } else {
      try { localStorage.removeItem('kiosk-demo-state-v1'); } catch { /* 저장 불가 */ }
    }
    // 주방 화면의 "시작하기" 안내와 화면 상태도 처음으로 돌린다.
    for (const p of panes) {
      const f = p.querySelector('iframe');
      if (f.src) f.contentWindow.location.reload();
    }
  });

  show(current);
})();
