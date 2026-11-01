'use strict';

/*
 * 키오스크 데모용 가짜 서버.
 * 진짜 키오스크(github.com/killerwhalee/kiosk)는 Node.js 서버가 SSE로 상태를 나눠 주지만,
 * 이 데모는 서버 없이 정적 페이지로 돌아야 하므로 fetch('/api/…')와 EventSource('/api/events')를
 * 이 파일이 가로채 브라우저 안에서 처리한다. 상태는 localStorage에 두고, 같은 브라우저의 다른 화면
 * (iframe, 새 탭)과는 BroadcastChannel로 맞춘다. 주문 로직은 lib/store.js를 그대로 옮겼다.
 */
(() => {
  const CONFIG = {
    title: '데모 카페',
    tables: 8,
    stations: [
      { id: 1, name: '음료' },
      { id: 2, name: '주방' },
    ],
    menus: [
      { id: 'americano', name: '아메리카노', price: 3000, station: 1 },
      { id: 'latte', name: '카페라테', price: 3500, station: 1 },
      { id: 'lemonade', name: '레몬에이드', price: 4000, station: 1 },
      { id: 'sandwich', name: '샌드위치', price: 5500, station: 2 },
      { id: 'cheesecake', name: '치즈케이크', price: 5000, station: 2 },
    ],
  };
  const KEY = 'kiosk-demo-state-v1';
  const STATUSES = ['pending', 'requested', 'served'];

  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* 저장 불가: 메모리로만 동작 */ } },
  };

  // 데모에서는 알림음을 기본으로 끈다 (화면의 "알림음" 버튼으로 켤 수 있다).
  if (store.get('kiosk-sound') === null) store.set('kiosk-sound', 'off');

  class HttpError extends Error {
    constructor(status, message) { super(message); this.status = status; }
  }

  const emptyState = () => ({ nextOrderId: 1, orders: [], soldOut: {} });

  function seedState() {
    const ago = (min) => new Date(Date.now() - min * 60000).toISOString();
    const line = (id, qty) => {
      const m = CONFIG.menus.find((x) => x.id === id);
      return { menuId: m.id, name: m.name, price: m.price, qty };
    };
    const order = (id, tableNo, min, note, tickets) => ({
      id, tableNo, note, requestId: null, createdAt: ago(min), cancelled: false,
      total: tickets.flatMap((t) => t.items).reduce((s, l) => s + l.price * l.qty, 0),
      tickets,
    });
    const ticket = (stationId, status, items, min) => ({
      stationId, status, items,
      requestedAt: status === 'pending' ? null : ago(min),
      servedAt: status === 'served' ? ago(min) : null,
    });
    return {
      nextOrderId: 4,
      soldOut: {},
      orders: [
        order(1, 2, 14, '', [ticket(1, 'served', [line('americano', 2)], 11), ticket(2, 'served', [line('cheesecake', 1)], 9)]),
        order(2, 5, 6, '샌드위치 하나는 반으로 잘라 주세요', [ticket(1, 'requested', [line('latte', 1)], 4), ticket(2, 'requested', [line('sandwich', 2)], 4)]),
        order(3, 3, 1, '', [ticket(1, 'pending', [line('lemonade', 2)], 0)]),
      ],
    };
  }

  function load() {
    const raw = store.get(KEY);
    if (!raw) return seedState();
    try { return { ...emptyState(), ...JSON.parse(raw) }; } catch { return seedState(); }
  }

  let state = load();
  let version = 0;
  const listeners = new Set();
  const channel = 'BroadcastChannel' in window ? new BroadcastChannel('kiosk-demo') : null;

  function snapshot() {
    return {
      version,
      title: CONFIG.title,
      tables: CONFIG.tables,
      stations: CONFIG.stations,
      menus: CONFIG.menus.map((m) => ({ ...m, soldOut: !!state.soldOut[m.id] })),
      orders: state.orders,
    };
  }

  function emit() {
    version += 1;
    const snap = JSON.stringify(snapshot());
    for (const fn of listeners) fn(snap);
  }

  function commit() {
    store.set(KEY, JSON.stringify(state));
    if (channel) channel.postMessage({ type: 'state', state });
    emit();
  }

  if (channel) {
    channel.onmessage = (e) => {
      if (e.data && e.data.type === 'state') {
        state = e.data.state;
        emit();
      }
    };
  }
  // BroadcastChannel이 없는 브라우저: 다른 탭의 저장을 storage 이벤트로 받는다.
  window.addEventListener('storage', (e) => {
    if (e.key === KEY && !channel) { state = load(); emit(); }
  });

  // ---- lib/store.js 와 같은 규칙 ----
  const menu = (id) => CONFIG.menus.find((m) => m.id === id);

  function findOrder(orderId) {
    const order = state.orders.find((o) => o.id === Number(orderId));
    if (!order) throw new HttpError(404, '주문을 찾을 수 없습니다.');
    return order;
  }

  function applyStatus(ticket, status) {
    const now = new Date().toISOString();
    ticket.status = status;
    if (status === 'pending') { ticket.requestedAt = null; ticket.servedAt = null; }
    else if (status === 'requested') { ticket.requestedAt = ticket.requestedAt || now; ticket.servedAt = null; }
    else { ticket.requestedAt = ticket.requestedAt || now; ticket.servedAt = now; }
  }

  function createOrder({ tableNo, items, note, requestId }) {
    if (requestId) {
      const dup = state.orders.find((o) => o.requestId === requestId);
      if (dup) return dup;
    }
    tableNo = Number(tableNo);
    if (!Number.isInteger(tableNo) || tableNo < 1 || tableNo > CONFIG.tables) throw new HttpError(400, '테이블 번호가 올바르지 않습니다.');
    if (!Array.isArray(items)) throw new HttpError(400, '메뉴를 선택해 주세요.');
    const lines = [];
    for (const item of items) {
      const qty = Number(item.qty);
      if (!qty) continue;
      if (!Number.isInteger(qty) || qty < 0 || qty > 99) throw new HttpError(400, '수량이 올바르지 않습니다.');
      const m = menu(item.menuId);
      if (!m) throw new HttpError(400, '없는 메뉴입니다.');
      if (state.soldOut[m.id]) throw new HttpError(409, `${m.name}은(는) 품절입니다.`);
      const existing = lines.find((l) => l.menuId === m.id);
      if (existing) existing.qty += qty;
      else lines.push({ menuId: m.id, name: m.name, price: m.price, station: m.station, qty });
    }
    if (lines.length === 0) throw new HttpError(400, '메뉴를 선택해 주세요.');
    const tickets = CONFIG.stations
      .map((s) => ({
        stationId: s.id, status: 'pending', requestedAt: null, servedAt: null,
        items: lines.filter((l) => l.station === s.id).map(({ station, ...rest }) => rest),
      }))
      .filter((t) => t.items.length > 0);
    const order = {
      id: state.nextOrderId++,
      tableNo,
      note: typeof note === 'string' ? note.trim().slice(0, 100) : '',
      requestId: requestId || null,
      createdAt: new Date().toISOString(),
      cancelled: false,
      total: lines.reduce((sum, l) => sum + l.price * l.qty, 0),
      tickets,
    };
    state.orders.push(order);
    commit();
    return order;
  }

  function route(method, pathname, body) {
    let m;
    if (method === 'GET' && pathname === '/api/ping') return [204, null];
    if (method === 'GET' && pathname === '/api/state') return [200, snapshot()];
    if (method !== 'POST') throw new HttpError(404, '없는 API입니다.');

    if (pathname === '/api/orders') return [201, createOrder(body)];
    if ((m = pathname.match(/^\/api\/orders\/(\d+)\/tickets\/(\d+)\/status$/))) {
      if (!STATUSES.includes(body.status)) throw new HttpError(400, '상태 값이 올바르지 않습니다.');
      const order = findOrder(m[1]);
      if (order.cancelled) throw new HttpError(409, '취소된 주문입니다.');
      const ticket = order.tickets.find((t) => t.stationId === Number(m[2]));
      if (!ticket) throw new HttpError(404, '해당 주방의 주문이 없습니다.');
      applyStatus(ticket, body.status);
      commit();
      return [200, order];
    }
    if ((m = pathname.match(/^\/api\/stations\/(\d+)\/request-all$/))) {
      const stationId = Number(m[1]);
      let count = 0;
      for (const order of state.orders) {
        if (order.cancelled) continue;
        for (const t of order.tickets) {
          if (t.stationId === stationId && t.status === 'pending') { applyStatus(t, 'requested'); count += 1; }
        }
      }
      if (count > 0) commit();
      return [200, { count }];
    }
    if (pathname === '/api/admin/check') return [200, { ok: true }];
    if ((m = pathname.match(/^\/api\/orders\/(\d+)\/cancel$/))) {
      const order = findOrder(m[1]);
      order.cancelled = body.cancelled !== false;
      commit();
      return [200, order];
    }
    if ((m = pathname.match(/^\/api\/menus\/([\w-]+)\/sold-out$/))) {
      if (!menu(m[1])) throw new HttpError(404, '없는 메뉴입니다.');
      if (body.soldOut) state.soldOut[m[1]] = true;
      else delete state.soldOut[m[1]];
      commit();
      return [200, { ok: true }];
    }
    if (pathname === '/api/reset') {
      state = emptyState();
      commit();
      return [200, { ok: true }];
    }
    throw new HttpError(404, '없는 API입니다.');
  }

  // ---- fetch / EventSource 가로채기 ----
  const realFetch = window.fetch.bind(window);
  window.fetch = async (input, init = {}) => {
    const url = new URL(typeof input === 'string' ? input : input.url, location.href);
    const isApi = typeof input === 'string' && input.startsWith('/api/');
    if (!isApi) return realFetch(input, init);
    const method = (init.method || 'GET').toUpperCase();
    let body = {};
    try { body = init.body ? JSON.parse(init.body) : {}; } catch { body = {}; }
    try {
      const [status, data] = route(method, url.pathname, body);
      if (data === null) return new Response(null, { status });
      return new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json' } });
    } catch (err) {
      const status = err instanceof HttpError ? err.status : 500;
      return new Response(JSON.stringify({ error: status === 500 ? '오류가 발생했습니다.' : err.message }), {
        status, headers: { 'Content-Type': 'application/json' },
      });
    }
  };

  class DemoEventSource {
    constructor() {
      this.readyState = 0;
      this.onopen = null;
      this.onmessage = null;
      this.onerror = null;
      this._send = (data) => { if (this.onmessage) this.onmessage({ data }); };
      setTimeout(() => {
        if (this.readyState === 2) return;
        this.readyState = 1;
        listeners.add(this._send);
        if (this.onopen) this.onopen({});
        this._send(JSON.stringify(snapshot()));
      }, 0);
    }
    close() { this.readyState = 2; listeners.delete(this._send); }
  }
  DemoEventSource.CONNECTING = 0;
  DemoEventSource.OPEN = 1;
  DemoEventSource.CLOSED = 2;
  window.EventSource = DemoEventSource;

  /** 소개 페이지의 "처음 상태로" 버튼이 부른다. */
  window.KioskDemo = {
    reset() {
      state = seedState();
      commit();
    },
  };

  // 단독 탭으로 열었을 때만 데모 표시를 붙인다.
  if (window.top === window) {
    document.addEventListener('DOMContentLoaded', () => {
      const tag = document.createElement('a');
      tag.href = '../../#kiosk';
      tag.textContent = '데모 · 이 브라우저 안에서만 동작합니다 · killerwhalee.com';
      tag.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:9999;padding:6px 12px;border-radius:999px;'
        + 'background:#101316;color:#fff;font:600 13px/1.4 system-ui,sans-serif;text-decoration:none;opacity:.85';
      document.body.appendChild(tag);
    });
  }
})();
