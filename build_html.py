#!/usr/bin/env python3
"""Writes the complete org_chart_app/index.html in one atomic operation."""

HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Org Chart</title>
  <style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif}
    button{font-family:inherit;cursor:pointer}

    :root{
      --color-primary:#1565C0;
      --color-primary-dark:#0D47A1;
      --color-primary-light:#1976D2;
      --color-primary-faint:#E3F2FD;
      --color-header-bg:#1565C0;
      --color-header-text:#FFFFFF;
      --color-app-bg:#F0F4F8;
      --color-card-bg:#FFFFFF;
      --color-card-border:#DDE3EA;
      --color-card-border-hover:#90CAF9;
      --color-card-border-selected:#1565C0;
      --color-card-shadow:rgba(0,0,0,0.08);
      --color-card-shadow-hover:rgba(0,0,0,0.15);
      --color-text-heading:#0D1B2A;
      --color-text-body:#37474F;
      --color-text-muted:#78909C;
      --color-text-on-primary:#FFFFFF;
      --color-connector:#90A4AE;
      --color-input-border:#B0BEC5;
      --color-input-border-focus:#1565C0;
      --color-input-bg:#FFFFFF;
      --color-error:#C62828;
      --color-error-bg:#FFEBEE;
      --color-modal-backdrop:rgba(0,0,0,0.45);
      --color-modal-bg:#FFFFFF;
      --color-btn-primary-bg:#1565C0;
      --color-btn-primary-hover:#0D47A1;
      --color-btn-primary-text:#FFFFFF;
      --color-btn-secondary-bg:#FFFFFF;
      --color-btn-secondary-border:#B0BEC5;
      --color-btn-secondary-hover:#ECEFF1;
      --color-btn-secondary-text:#37474F;
      --color-btn-disabled-bg:#CFD8DC;
      --color-btn-disabled-text:#90A4AE;
      --dept-engineering:#1565C0;
      --dept-product:#1976D2;
      --dept-marketing:#7B1FA2;
      --dept-sales:#2E7D32;
      --dept-hr:#E65100;
      --dept-finance:#00695C;
      --dept-design:#AD1457;
      --dept-executive:#4E342E;
      --dept-other:#455A64;
      --dept-default:#455A64;
      --level-gap:48px;
      --sibling-gap:24px;
    }

    html,body{height:100%}
    body{display:flex;flex-direction:column;background:var(--color-app-bg);overflow:hidden}

    /* Header */
    .app-header{
      height:56px;background:var(--color-header-bg);color:var(--color-header-text);
      display:flex;align-items:center;justify-content:space-between;
      padding:0 24px;box-shadow:0 2px 8px rgba(0,0,0,.2);
      position:sticky;top:0;z-index:100;flex-shrink:0;gap:16px;
    }
    .app-header__title{
      font-size:20px;font-weight:600;letter-spacing:-.01em;
      display:flex;align-items:center;gap:10px;white-space:nowrap;
    }
    .app-header__right{display:flex;align-items:center;gap:16px}

    /* Search */
    .search-wrap{position:relative;display:flex;align-items:center}
    .search-icon{position:absolute;left:9px;color:rgba(255,255,255,.6);font-size:14px;pointer-events:none}
    #search-input{
      background:rgba(255,255,255,.15);border:1.5px solid rgba(255,255,255,.3);
      border-radius:6px;color:#fff;font-size:13px;height:32px;
      padding:0 10px 0 28px;width:200px;outline:none;
      transition:background 120ms,border-color 120ms;
    }
    #search-input::placeholder{color:rgba(255,255,255,.55)}
    #search-input:focus{background:rgba(255,255,255,.22);border-color:rgba(255,255,255,.7)}

    /* Zoom */
    .zoom-controls{display:flex;align-items:center;gap:6px}
    .zoom-controls__btn{
      width:32px;height:32px;border-radius:6px;
      border:1.5px solid rgba(255,255,255,.35);background:rgba(255,255,255,.12);
      color:#fff;font-size:18px;font-weight:700;cursor:pointer;
      display:flex;align-items:center;justify-content:center;
      transition:background 120ms;line-height:1;
    }
    .zoom-controls__btn:hover:not(:disabled){background:rgba(255,255,255,.25)}
    .zoom-controls__btn:disabled{opacity:.4;cursor:not-allowed}
    .zoom-controls__label{font-size:13px;font-weight:600;min-width:44px;text-align:center;color:rgba(255,255,255,.9)}
    .zoom-controls__reset{font-size:12px;padding:0 10px;width:auto}

    /* Viewport */
    .tree-viewport{overflow:auto;flex:1;padding:40px;min-height:0}
    #tree-wrapper{display:inline-block;transform-origin:top center;transition:transform 200ms ease;position:relative;min-width:100%}

    /* Tree */
    .tree{display:flex;flex-direction:column;align-items:center;padding-bottom:60px}
    .tree-node{display:flex;flex-direction:column;align-items:center;position:relative}
    .children-row{display:flex;flex-direction:row;justify-content:center;gap:var(--sibling-gap);animation:fadeIn 200ms ease-out}
    @keyframes fadeIn{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}

    /* SVG connector overlay */
    #connector-svg{position:absolute;top:0;left:0;pointer-events:none;overflow:visible}

    /* Card */
    .org-card{
      min-width:180px;max-width:220px;padding:12px 14px 10px 18px;
      background:var(--color-card-bg);border:1.5px solid var(--color-card-border);
      border-radius:8px;box-shadow:0 2px 6px var(--color-card-shadow);
      position:relative;cursor:pointer;user-select:none;
      transition:box-shadow 150ms,border-color 150ms,transform 150ms;
      margin-bottom:var(--level-gap);
    }
    .org-card::before{
      content:'';position:absolute;left:0;top:0;bottom:0;width:4px;
      border-radius:8px 0 0 8px;background:var(--card-accent,var(--dept-default));
    }
    .org-card:hover{border-color:var(--color-card-border-hover);box-shadow:0 4px 12px var(--color-card-shadow-hover);transform:translateY(-2px)}
    .org-card.is-selected{border-color:var(--color-card-border-selected);border-width:2px;background:var(--color-primary-faint);box-shadow:0 4px 12px rgba(21,101,192,.2)}
    .org-card.is-dimmed{opacity:.25}
    .org-card:focus-visible{outline:2px dashed var(--color-primary);outline-offset:3px}
    .org-card__name{font-size:14px;font-weight:600;color:var(--color-text-heading);line-height:1.3;margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:160px}
    .org-card__title{font-size:12px;font-weight:400;color:var(--color-text-body);line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:160px}
    .org-card__dept{font-size:11px;color:var(--color-text-muted);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:160px}
    .org-card__actions{display:flex;align-items:center;gap:4px;margin-top:8px;justify-content:flex-end}
    .org-card__btn-add,.org-card__btn-toggle{
      width:24px;height:24px;border-radius:4px;
      border:1.5px solid var(--color-card-border);background:var(--color-card-bg);
      cursor:pointer;display:flex;align-items:center;justify-content:center;
      line-height:1;transition:background 120ms,border-color 120ms;flex-shrink:0;
    }
    .org-card__btn-add{color:var(--color-primary-light);font-size:16px;font-weight:700}
    .org-card__btn-add:hover{background:var(--color-primary-faint);border-color:var(--color-primary-light)}
    .org-card__btn-toggle{color:var(--color-text-muted);font-size:11px}
    .org-card__btn-toggle:hover{background:#ECEFF1}
    mark{background:#FFF176;color:inherit;border-radius:2px;padding:0 1px}
"""

    /* Modal */
    #modal-overlay{position:fixed;inset:0;background:var(--color-modal-backdrop);z-index:500;display:flex;align-items:center;justify-content:center}
    #modal-overlay.hidden{display:none}
    #modal-panel{background:var(--color-modal-bg);border-radius:10px;box-shadow:0 8px 32px rgba(0,0,0,.22);width:420px;max-width:calc(100vw - 32px);overflow:hidden}
    .modal-header{background:var(--color-primary);color:#fff;padding:16px 20px;display:flex;align-items:center;justify-content:space-between}
    .modal-header h2{font-size:16px;font-weight:600}
    .modal-header__close{background:none;border:none;color:rgba(255,255,255,.8);font-size:20px;line-height:1;cursor:pointer;padding:2px 4px;border-radius:4px;transition:color 120ms}
    .modal-header__close:hover{color:#fff}
    .modal-reports-to{font-size:13px;color:var(--color-text-muted);padding:10px 20px;background:#FAFAFA;border-bottom:1px solid #ECEFF1}
    .modal-reports-to strong{color:var(--color-text-body)}
    #add-member-form{padding:20px;display:flex;flex-direction:column;gap:14px}
    .form-field{display:flex;flex-direction:column;gap:5px}
    .form-field label{font-size:13px;font-weight:600;color:var(--color-text-body)}
    .form-field .req{color:var(--color-error);margin-left:2px}
    .form-field input,.form-field select{
      border:1.5px solid var(--color-input-border);border-radius:6px;background:var(--color-input-bg);
      font-size:14px;color:var(--color-text-heading);padding:8px 11px;outline:none;
      transition:border-color 120ms,box-shadow 120ms;width:100%;font-family:inherit;
    }
    .form-field input:focus,.form-field select:focus{border-color:var(--color-input-border-focus);box-shadow:0 0 0 3px rgba(21,101,192,.12)}
    .form-field input.error,.form-field select.error{border-color:var(--color-error)}
    .field-error{font-size:12px;color:var(--color-error);min-height:16px}
    .modal-actions{display:flex;justify-content:flex-end;gap:10px;padding:0 20px 20px}
    .btn-secondary{padding:8px 18px;border-radius:6px;border:1.5px solid var(--color-btn-secondary-border);background:var(--color-btn-secondary-bg);color:var(--color-btn-secondary-text);font-size:14px;font-weight:500;cursor:pointer;transition:background 120ms}
    .btn-secondary:hover{background:var(--color-btn-secondary-hover)}
    .btn-primary{padding:8px 18px;border-radius:6px;border:none;background:var(--color-btn-primary-bg);color:var(--color-btn-primary-text);font-size:14px;font-weight:600;cursor:pointer;transition:background 120ms}
    .btn-primary:hover{background:var(--color-btn-primary-hover)}
    .btn-primary:disabled{background:var(--color-btn-disabled-bg);color:var(--color-btn-disabled-text);cursor:not-allowed}
    .empty-state{text-align:center;padding:80px 24px;color:var(--color-text-muted);font-size:15px}
  </style>
</head>
<body>

  <header class="app-header" role="banner">
    <div class="app-header__title"><span aria-hidden="true">🏢</span> Org Chart</div>
    <div class="app-header__right">
      <div class="search-wrap">
        <span class="search-icon" aria-hidden="true">🔍</span>
        <input type="search" id="search-input" placeholder="Search people\u2026" aria-label="Search employees" autocomplete="off"/>
      </div>
      <div class="zoom-controls" role="group" aria-label="Zoom controls">
        <button class="zoom-controls__btn" id="btn-zoom-out" aria-label="Zoom out" title="Zoom out">\u2212</button>
        <span class="zoom-controls__label" id="zoom-display" aria-live="polite" aria-atomic="true">100%</span>
        <button class="zoom-controls__btn" id="btn-zoom-in" aria-label="Zoom in" title="Zoom in">+</button>
        <button class="zoom-controls__btn zoom-controls__reset" id="btn-zoom-reset" aria-label="Reset zoom">Reset</button>
      </div>
    </div>
  </header>

  <div class="tree-viewport" id="chart-container" role="main" aria-label="Organization chart">
    <div id="tree-wrapper">
      <div id="tree" class="tree"></div>
      <svg id="connector-svg" aria-hidden="true"></svg>
    </div>
  </div>

  <div id="modal-overlay" class="hidden" role="dialog" aria-modal="true" aria-labelledby="modal-title" aria-hidden="true">
    <div id="modal-panel">
      <div class="modal-header">
        <h2 id="modal-title">Add Team Member</h2>
        <button class="modal-header__close" id="modal-close-btn" aria-label="Close modal">\u2715</button>
      </div>
      <div class="modal-reports-to">Reporting to: <strong id="modal-parent-name">\u2014</strong></div>
      <form id="add-member-form" novalidate>
        <div class="form-field">
          <label for="input-name">Full Name<span class="req" aria-hidden="true">*</span></label>
          <input type="text" id="input-name" placeholder="e.g. Jane Smith" autocomplete="off"/>
          <div class="field-error" id="error-name" role="alert" aria-live="polite"></div>
        </div>
        <div class="form-field">
          <label for="input-title">Job Title<span class="req" aria-hidden="true">*</span></label>
          <input type="text" id="input-title" placeholder="e.g. Senior Engineer" autocomplete="off"/>
          <div class="field-error" id="error-title" role="alert" aria-live="polite"></div>
        </div>
        <div class="form-field">
          <label for="input-dept">Department<span class="req" aria-hidden="true">*</span></label>
          <select id="input-dept">
            <option value="">\u2014 Select department \u2014</option>
            <option value="Engineering">Engineering</option>
            <option value="Product">Product</option>
            <option value="Marketing">Marketing</option>
            <option value="Sales">Sales</option>
            <option value="HR">HR</option>
            <option value="Finance">Finance</option>
            <option value="Design">Design</option>
            <option value="Executive">Executive</option>
            <option value="Other">Other</option>
          </select>
          <div class="field-error" id="error-dept" role="alert" aria-live="polite"></div>
        </div>
      </form>
      <div class="modal-actions">
        <button class="btn-secondary" id="modal-cancel-btn">Cancel</button>
        <button class="btn-primary" id="modal-save-btn">Add Employee</button>
      </div>
    </div>
  </div>

  <script>
  'use strict';
"""

HTML += """\
  // 1. DATA
  const ORG_DATA = [
    {id:'ceo',       name:'Sarah Chen',    title:'Chief Executive Officer',   department:'Executive',   parentId:null},
    {id:'vp-eng',    name:'Marcus Rivera', title:'VP of Engineering',          department:'Engineering', parentId:'ceo'},
    {id:'vp-prod',   name:'Priya Patel',   title:'VP of Product',             department:'Product',     parentId:'ceo'},
    {id:'vp-mktg',   name:"James O'Brien", title:'VP of Marketing',           department:'Marketing',   parentId:'ceo'},
    {id:'dir-fe',    name:'Aiko Tanaka',   title:'Director of Frontend Eng',  department:'Engineering', parentId:'vp-eng'},
    {id:'dir-be',    name:'Leon Fischer',  title:'Director of Backend Eng',   department:'Engineering', parentId:'vp-eng'},
    {id:'dir-pm',    name:'Chioma Obi',    title:'Director of Product Mgmt',  department:'Product',     parentId:'vp-prod'},
    {id:'dir-brand', name:'Tom Nakamura',  title:'Director of Brand',         department:'Marketing',   parentId:'vp-mktg'},
    {id:'mgr-ui',    name:'Elena Vasquez', title:'UI Engineering Manager',    department:'Engineering', parentId:'dir-fe'},
    {id:'mgr-api',   name:'Kwame Asante',  title:'API Engineering Manager',   department:'Engineering', parentId:'dir-be'},
    {id:'pm-growth', name:'Rania Saleh',   title:'Senior Product Manager',    department:'Product',     parentId:'dir-pm'},
    {id:'ic-design', name:'Luca Ferrari',  title:'Senior Brand Designer',     department:'Marketing',   parentId:'dir-brand'},
  ];
  let nodeMap = {}, childMap = {};
  function buildIndexes() {
    nodeMap = {}; childMap = {};
    for (const n of ORG_DATA) { nodeMap[n.id] = n; childMap[n.id] = []; }
    for (const n of ORG_DATA) { if (n.parentId && nodeMap[n.parentId]) childMap[n.parentId].push(n); }
  }

  // 2. STATE
  const state = {
    collapsed: new Set(), selected: null, zoomLevel: 1.0,
    searchQuery: '', modalMode: null, modalParentId: null,
  };
  const ZOOM_MIN = 0.5, ZOOM_MAX = 1.5, ZOOM_STEP = 0.10;

  // 3. UTILITIES
  function escapeHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }
  function deptColor(d) {
    const m = {Engineering:'var(--dept-engineering)',Product:'var(--dept-product)',
      Marketing:'var(--dept-marketing)',Sales:'var(--dept-sales)',HR:'var(--dept-hr)',
      Finance:'var(--dept-finance)',Design:'var(--dept-design)',Executive:'var(--dept-executive)',Other:'var(--dept-other)'};
    return m[d] || 'var(--dept-default)';
  }
  function highlightMatch(esc, q) {
    if (!q) return esc;
    const i = esc.toLowerCase().indexOf(q.toLowerCase());
    if (i === -1) return esc;
    return esc.slice(0,i) + '<mark>' + esc.slice(i, i+q.length) + '</mark>' + esc.slice(i+q.length);
  }
  function getAncestorIds(id) {
    const s = new Set(); let c = nodeMap[id] ? nodeMap[id].parentId : null;
    while (c) { s.add(c); c = nodeMap[c] ? nodeMap[c].parentId : null; }
    return s;
  }
  function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(()=>fn(...a), ms); }; }

  // 4. SEARCH
  function computeSearchSets() {
    const q = state.searchQuery;
    if (!q) return {matchIds:null, visibleIds:null};
    const matchIds = new Set(), visibleIds = new Set();
    for (const n of ORG_DATA) {
      if ((n.name+' '+n.title+' '+n.department).toLowerCase().includes(q)) {
        matchIds.add(n.id); visibleIds.add(n.id);
        getAncestorIds(n.id).forEach(id => visibleIds.add(id));
      }
    }
    return {matchIds, visibleIds};
  }

  // 5. RENDERER
  function buildCardHTML(node, isDimmed) {
    const children = childMap[node.id] || [];
    const hasCh = children.length > 0;
    const collapsed = state.collapsed.has(node.id);
    const selected  = state.selected === node.id;
    const q = state.searchQuery;
    const sn = escapeHtml(node.name), st = escapeHtml(node.title),
          sd = escapeHtml(node.department), si = escapeHtml(node.id);
    const cls = ['org-card', selected?'is-selected':'', isDimmed?'is-dimmed':''].filter(Boolean).join(' ');
    const toggleBtn = hasCh
      ? \`<button class="org-card__btn-toggle" data-action="toggle" data-node-id="\${si}"
           aria-label="\${collapsed?'Expand':'Collapse'} \${sn} reports"
           aria-expanded="\${!collapsed}" title="\${collapsed?'Expand':'Collapse'}">\${collapsed?'&#9658;':'&#9660;'}</button>\`
      : '';
    return \`<div class="\${cls}" data-node-id="\${si}" role="button" tabindex="0"
        aria-label="\${sn}, \${st}" aria-pressed="\${selected}"
        style="--card-accent:\${deptColor(node.department)}">
      <div class="org-card__name">\${highlightMatch(sn,q)}</div>
      <div class="org-card__title">\${highlightMatch(st,q)}</div>
      <div class="org-card__dept">\${highlightMatch(sd,q)}</div>
      <div class="org-card__actions">
        <button class="org-card__btn-add" data-action="add-child" data-node-id="\${si}"
          aria-label="Add report to \${sn}" title="Add direct report">+</button>
        \${toggleBtn}
      </div>
    </div>\`;
  }
  function renderNode(node, container, ss) {
    const isDimmed = ss.visibleIds !== null && !ss.visibleIds.has(node.id);
    const el = document.createElement('div');
    el.className = 'tree-node';
    el.innerHTML = buildCardHTML(node, isDimmed);
    container.appendChild(el);
    if (!state.collapsed.has(node.id) && (childMap[node.id]||[]).length) {
      const row = document.createElement('div');
      row.className = 'children-row';
      el.appendChild(row);
      for (const ch of childMap[node.id]) renderNode(ch, row, ss);
    }
  }
  function renderTree() {
    const tree = document.getElementById('tree');
    tree.innerHTML = '';
    const root = ORG_DATA.find(n => n.parentId === null);
    if (!root) { tree.innerHTML = '<div class="empty-state">No data.</div>'; return; }
    renderNode(root, tree, computeSearchSets());
    requestAnimationFrame(() => requestAnimationFrame(drawConnectors));
  }
  function render() { renderTree(); applyZoom(); }
"""

HTML += """\
  // 6. CONNECTORS
  function drawConnectors() {
    const svg = document.getElementById('connector-svg');
    const wrapper = document.getElementById('tree-wrapper');
    const tree = document.getElementById('tree');
    if (!svg||!wrapper||!tree) return;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const wr = wrapper.getBoundingClientRect();
    for (const node of ORG_DATA) {
      if (state.collapsed.has(node.id)) continue;
      const children = childMap[node.id];
      if (!children||!children.length) continue;
      const pEl = wrapper.querySelector('.org-card[data-node-id="'+CSS.escape(node.id)+'"]');
      if (!pEl) continue;
      const pr = pEl.getBoundingClientRect();
      const px = pr.left + pr.width/2 - wr.left;
      const py = pr.bottom - wr.top;
      for (const ch of children) {
        const cEl = wrapper.querySelector('.org-card[data-node-id="'+CSS.escape(ch.id)+'"]');
        if (!cEl) continue;
        const cr = cEl.getBoundingClientRect();
        const cx = cr.left + cr.width/2 - wr.left;
        const cy = cr.top - wr.top;
        const my = py + (cy - py) / 2;
        const p = document.createElementNS('http://www.w3.org/2000/svg','path');
        p.setAttribute('d',\`M\${px} \${py} L\${px} \${my} L\${cx} \${my} L\${cx} \${cy}\`);
        p.setAttribute('stroke','var(--color-connector)');
        p.setAttribute('stroke-width','2');
        p.setAttribute('fill','none');
        p.setAttribute('stroke-linecap','round');
        svg.appendChild(p);
      }
    }
    svg.setAttribute('width', tree.scrollWidth);
    svg.setAttribute('height', tree.scrollHeight + 80);
  }

  // 7. ZOOM
  function applyZoom() {
    const w = document.getElementById('tree-wrapper');
    const d = document.getElementById('zoom-display');
    if (!w||!d) return;
    w.style.transform = \`scale(\${state.zoomLevel})\`;
    w.style.transformOrigin = 'top center';
    d.textContent = Math.round(state.zoomLevel * 100) + '%';
    const bi = document.getElementById('btn-zoom-in');
    const bo = document.getElementById('btn-zoom-out');
    if (bi) bi.disabled = state.zoomLevel >= ZOOM_MAX;
    if (bo) bo.disabled = state.zoomLevel <= ZOOM_MIN;
  }
  function zoomIn()    { state.zoomLevel = Math.min(ZOOM_MAX, +(state.zoomLevel+ZOOM_STEP).toFixed(2)); applyZoom(); }
  function zoomOut()   { state.zoomLevel = Math.max(ZOOM_MIN, +(state.zoomLevel-ZOOM_STEP).toFixed(2)); applyZoom(); }
  function zoomReset() { state.zoomLevel = 1.0; applyZoom(); }

  // 8. MODAL
  let _trap = null, _prevFocus = null;
  function showModal(parentId) {
    state.modalMode = 'add'; state.modalParentId = parentId;
    const ov = document.getElementById('modal-overlay');
    const pn = nodeMap[parentId];
    document.getElementById('modal-parent-name').textContent = pn ? pn.name : '—';
    document.getElementById('input-name').value = '';
    document.getElementById('input-title').value = '';
    document.getElementById('input-dept').value = '';
    ['name','title','dept'].forEach(f => {
      setFieldError(f,'');
      document.getElementById('input-'+f).classList.remove('error');
    });
    _prevFocus = document.activeElement;
    ov.classList.remove('hidden');
    ov.removeAttribute('aria-hidden');
    setTimeout(() => document.getElementById('input-name').focus(), 40);
    _trap = makeFocusTrap(document.getElementById('modal-panel'));
    document.addEventListener('keydown', _trap);
  }
  function hideModal() {
    const ov = document.getElementById('modal-overlay');
    ov.classList.add('hidden');
    ov.setAttribute('aria-hidden','true');
    state.modalMode = null; state.modalParentId = null;
    if (_trap) { document.removeEventListener('keydown', _trap); _trap = null; }
    if (_prevFocus && _prevFocus.focus) { _prevFocus.focus(); _prevFocus = null; }
  }
  function makeFocusTrap(panel) {
    const SEL = 'button:not([disabled]),input:not([disabled]),select:not([disabled]),[tabindex]:not([tabindex="-1"])';
    return function(e) {
      if (e.key === 'Escape') { hideModal(); return; }
      if (e.key !== 'Tab') return;
      const els = Array.from(panel.querySelectorAll(SEL)).filter(el => el.offsetParent !== null);
      if (!els.length) return;
      const first = els[0], last = els[els.length-1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };
  }
  function setFieldError(field, msg) {
    const e = document.getElementById('error-'+field);
    const i = document.getElementById('input-'+field);
    if (e) e.textContent = msg ? '\\u26a0 '+msg : '';
    if (i) i.classList.toggle('error', Boolean(msg));
  }
  function handleSaveModal() {
    const name  = document.getElementById('input-name').value.trim();
    const title = document.getElementById('input-title').value.trim();
    const dept  = document.getElementById('input-dept').value;
    let ok = true;
    if (!name)  { setFieldError('name',  'Full name is required');      ok=false; } else setFieldError('name','');
    if (!title) { setFieldError('title', 'Job title is required');      ok=false; } else setFieldError('title','');
    if (!dept)  { setFieldError('dept',  'Please select a department'); ok=false; } else setFieldError('dept','');
    if (!ok) return;
    // escapeHtml applied at render time — raw strings stored in data
    ORG_DATA.push({ id:'node-'+Date.now(), name, title, department:dept, parentId:state.modalParentId });
    buildIndexes(); hideModal(); render();
  }

  // 9. EVENTS
  function handleToggle(id) {
    if (state.collapsed.has(id)) state.collapsed.delete(id); else state.collapsed.add(id);
    render();
  }
  function handleSelect(id) {
    state.selected = state.selected === id ? null : id;
    document.querySelectorAll('.org-card').forEach(el => {
      const sel = el.dataset.nodeId === state.selected;
      el.classList.toggle('is-selected', sel);
      el.setAttribute('aria-pressed', String(sel));
    });
  }
  document.getElementById('chart-container').addEventListener('click', e => {
    const tog = e.target.closest('[data-action="toggle"]');
    const add = e.target.closest('[data-action="add-child"]');
    const card = e.target.closest('[data-node-id]');
    if (tog)  { handleToggle(tog.dataset.nodeId); return; }
    if (add)  { showModal(add.dataset.nodeId);    return; }
    if (card) { handleSelect(card.dataset.nodeId); }
  });
  document.getElementById('chart-container').addEventListener('keydown', e => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const card = e.target.closest('[data-node-id]');
    if (card) { e.preventDefault(); handleSelect(card.dataset.nodeId); }
  });
  document.getElementById('modal-close-btn').addEventListener('click', hideModal);
  document.getElementById('modal-cancel-btn').addEventListener('click', hideModal);
  document.getElementById('modal-save-btn').addEventListener('click', handleSaveModal);
  document.getElementById('add-member-form').addEventListener('submit', e => { e.preventDefault(); handleSaveModal(); });
  document.getElementById('modal-overlay').addEventListener('click', e => {
    if (e.target === document.getElementById('modal-overlay')) hideModal();
  });
  document.getElementById('btn-zoom-in').addEventListener('click', zoomIn);
  document.getElementById('btn-zoom-out').addEventListener('click', zoomOut);
  document.getElementById('btn-zoom-reset').addEventListener('click', zoomReset);
  document.getElementById('search-input').addEventListener('input', debounce(e => {
    state.searchQuery = e.target.value.toLowerCase().trim();
    renderTree();
  }, 120));
  window.addEventListener('resize', debounce(drawConnectors, 100));

  // 10. BOOTSTRAP
  document.addEventListener('DOMContentLoaded', () => { buildIndexes(); render(); });
  </script>
</body>
</html>
"""

import os
out = os.path.join(os.path.dirname(__file__), 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"Written {len(HTML)} chars to {out}")
