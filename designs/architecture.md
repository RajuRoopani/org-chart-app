# Org Chart Application — Architecture Design

**Author:** Software Architect  
**Thread:** ac28835e-1ebc-4124-b872-15bdd4cead51  
**Status:** Approved for Implementation  
**Deliverable:** `org_chart_app/index.html` (single-file, no external dependencies)

---

## Overview

A pure-frontend org chart application delivered as a single `index.html` with all styles and logic inline. The app renders a top-down organizational hierarchy as an interactive tree of cards connected by right-angle SVG lines. State is held entirely in JavaScript module-scope variables. The rendering pipeline is a pure function: `data + state → DOM`. No frameworks, no CDNs, no build step.

---

## 1. Data Model

### Node Schema

Each employee node is a plain JavaScript object:

```js
{
  id:         String,   // unique, e.g. "ceo", "vp-eng"
  name:       String,   // full name, e.g. "Sarah Chen"
  title:      String,   // job title, e.g. "Chief Executive Officer"
  department: String,   // e.g. "Executive", "Engineering", "Product"
  parentId:   String|null  // null for root node only
}
```

### In-Memory Index Structures

Two index structures are built once at startup from the flat array:

```js
const nodeMap   = {};  // id → node object   (O(1) lookup)
const childMap  = {};  // id → [child nodes] (O(1) children lookup)
```

### Sample Data (10 nodes, 4 levels)

```js
const ORG_DATA = [
  // Level 0 — CEO
  { id: "ceo",       name: "Sarah Chen",      title: "Chief Executive Officer",      department: "Executive",   parentId: null },

  // Level 1 — VPs
  { id: "vp-eng",    name: "Marcus Rivera",   title: "VP of Engineering",            department: "Engineering", parentId: "ceo" },
  { id: "vp-prod",   name: "Priya Patel",     title: "VP of Product",               department: "Product",     parentId: "ceo" },
  { id: "vp-mktg",   name: "James O'Brien",   title: "VP of Marketing",             department: "Marketing",   parentId: "ceo" },

  // Level 2 — Directors
  { id: "dir-fe",    name: "Aiko Tanaka",     title: "Director of Frontend Eng",    department: "Engineering", parentId: "vp-eng" },
  { id: "dir-be",    name: "Leon Fischer",    title: "Director of Backend Eng",     department: "Engineering", parentId: "vp-eng" },
  { id: "dir-pm",    name: "Chioma Obi",      title: "Director of Product Mgmt",   department: "Product",     parentId: "vp-prod" },
  { id: "dir-brand", name: "Tom Nakamura",    title: "Director of Brand",           department: "Marketing",   parentId: "vp-mktg" },

  // Level 3 — Managers / ICs
  { id: "mgr-ui",    name: "Elena Vasquez",   title: "UI Engineering Manager",      department: "Engineering", parentId: "dir-fe" },
  { id: "mgr-api",   name: "Kwame Asante",    title: "API Engineering Manager",     department: "Engineering", parentId: "dir-be" },
  { id: "pm-growth", name: "Rania Saleh",     title: "Senior Product Manager",      department: "Product",     parentId: "dir-pm" },
  { id: "ic-design", name: "Luca Ferrari",    title: "Senior Brand Designer",       department: "Marketing",   parentId: "dir-brand" }
];
```

> **12 nodes, 4 levels** — satisfies the 10-node / 4-level requirement with room for the user to add more.

---

## 2. Tree Layout Algorithm

### Approach: CSS Flexbox (Recursive)

**Decision: CSS Flexbox layout** (not absolute positioning, not SVG-based layout).

**Rationale:**
- Flexbox naturally prevents horizontal overlap: children of the same parent are distributed evenly in a row.
- No position math needed — the browser's layout engine handles width allocation.
- SVG absolute positioning requires computing subtree widths recursively in JS, which is error-prone and harder to maintain in a single file.
- Flexbox degrades gracefully when nodes are added (new children just join the flex row).

### DOM Tree Structure

The rendered HTML mirrors the logical tree:

```
<div class="tree">                          ← Root flex container (column)
  <div class="tree-node">                   ← Per-node wrapper
    <div class="card">…</div>               ← Visual card
    <div class="connector-down"></div>      ← Vertical stub (CSS)
    <div class="children-row">             ← Horizontal flex row of children
      <div class="tree-node">…</div>        ← Recursive
      <div class="tree-node">…</div>
    </div>
  </div>
</div>
```

### Layout Rules

```
.tree              { display: flex; flex-direction: column; align-items: center; }
.tree-node         { display: flex; flex-direction: column; align-items: center; position: relative; }
.children-row      { display: flex; flex-direction: row; justify-content: center; gap: 24px; padding-top: 0; }
```

Each `.tree-node` stacks vertically: card → connector stub → children row. Children in `.children-row` sit side by side without overlap because flex distributes available space.

### Connector Lines

See **Section 6** for full connector design. The top-level approach: an SVG overlay drawn **after** the DOM is laid out (using `getBoundingClientRect()`). This gives pixel-accurate lines regardless of tree width.

---

## 3. Component Architecture

### Module Organization (single `<script>` block)

The script is structured in clearly separated sections, top to bottom:

```
<script>
// ─── 1. DATA ──────────────────────────────────────────────────────
//   ORG_DATA array + buildIndexes()

// ─── 2. STATE ─────────────────────────────────────────────────────
//   Module-scope state object

// ─── 3. RENDERER ──────────────────────────────────────────────────
//   renderTree(), renderNode(), buildCardHTML()

// ─── 4. CONNECTOR DRAWING ─────────────────────────────────────────
//   drawConnectors()  ← runs after renderTree() paints to DOM

// ─── 5. MODAL ─────────────────────────────────────────────────────
//   showModal(), hideModal(), handleAddMember()

// ─── 6. EVENT HANDLING ────────────────────────────────────────────
//   Single delegated listener on #chart-container

// ─── 7. SEARCH ────────────────────────────────────────────────────
//   filterNodes(), highlightMatch()

// ─── 8. ZOOM ──────────────────────────────────────────────────────
//   applyZoom()

// ─── 9. BOOTSTRAP ─────────────────────────────────────────────────
//   DOMContentLoaded → buildIndexes() → render() → drawConnectors()
</script>
```

### State Object

```js
const state = {
  collapsed:    new Set(),   // Set<nodeId> — nodes whose children are hidden
  selected:     null,        // String|null — currently selected node id
  zoomLevel:    1.0,         // Number — current CSS scale factor
  searchQuery:  "",          // String — live search text
  modalMode:    null,        // null | "add"
  modalParentId: null,       // String — parentId for new node being added
};
```

**Why a `Set` for collapsed?**  
O(1) add/delete/has. Clean semantics: if id is in the Set, node is collapsed. No boolean flags scattered across node objects (which would mutate the source data).

### Rendering Pipeline

```
state.collapsed + ORG_DATA
        │
        ▼
   renderTree()          ← clears #chart-container innerHTML, builds DOM
        │
        ├── renderNode(node, depth)   [recursive]
        │       ├── buildCardHTML(node)
        │       ├── if not collapsed: recurse children
        │       └── append to parent's .children-row
        │
        ▼
   drawConnectors()      ← reads getBoundingClientRect(), paints SVG overlay
```

**Key principle:** `renderTree()` is a full re-render on every state change. No diffing, no patching. For an org chart with <200 nodes this is imperceptible (~1ms). This eliminates an entire class of stale-state bugs.

### Event Handling — Single Delegated Listener

```js
document.getElementById('chart-container').addEventListener('click', (e) => {
  const card    = e.target.closest('[data-node-id]');
  const toggle  = e.target.closest('[data-action="toggle"]');
  const addBtn  = e.target.closest('[data-action="add-child"]');

  if (toggle)  { handleToggle(toggle.dataset.nodeId);    return; }
  if (addBtn)  { handleAddClick(addBtn.dataset.nodeId);  return; }
  if (card)    { handleSelect(card.dataset.nodeId);      return; }
});
```

**Why delegation?** The tree is fully re-rendered on each state change, destroying and recreating all DOM nodes. Attaching per-node listeners would require re-registering them after every render. A single listener on the stable container survives re-renders without cleanup.

**`data-*` attributes as the contract between HTML and JS** — no class name coupling.

---

## 4. Expand / Collapse

### Data Structure

`state.collapsed` is a `Set<nodeId>`. A node is "collapsed" if its id is in the set; its children are not rendered.

### Toggle Logic

```js
function handleToggle(nodeId) {
  if (state.collapsed.has(nodeId)) {
    state.collapsed.delete(nodeId);   // expand
  } else {
    state.collapsed.add(nodeId);      // collapse
  }
  render();   // full re-render → drawConnectors() automatically redraws lines
}
```

### CSS Transition Approach

Since we do a full re-render (not a show/hide of existing DOM), CSS transitions on the container itself are not straightforward. The recommended approach:

1. Apply a **CSS animation** on `.children-row` appearing:

```css
.children-row {
  animation: fadeSlideIn 200ms ease-out;
}

@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

2. The collapse direction (hiding) is instant because the DOM node is simply not rendered. This is acceptable UX — the expand animation (appearing) gives enough visual feedback.

> **Alternative:** Toggle a `.collapsed` class and use `max-height: 0` + `overflow: hidden` transitions on `.children-row` without re-rendering. This avoids full re-render for collapse/expand. **Prefer this if smooth bidirectional animation is required.** In that case, `renderNode()` always renders all children but adds `class="children-row collapsed"` if collapsed, and `handleToggle` just adds/removes the class. The SVG connectors must still be redrawn via `requestAnimationFrame` after the transition ends.

**Recommendation for implementation:** Use the class-toggle approach (option 2) to get bidirectional animation. Keep `state.collapsed` as the truth; sync it to DOM classes instead of re-rendering.

---

## 5. Zoom

### Approach: CSS `transform: scale()` on the Chart Wrapper

```js
const ZOOM_MIN  = 0.4;
const ZOOM_MAX  = 2.0;
const ZOOM_STEP = 0.15;

function zoomIn()  { state.zoomLevel = Math.min(ZOOM_MAX, state.zoomLevel + ZOOM_STEP); applyZoom(); }
function zoomOut() { state.zoomLevel = Math.max(ZOOM_MIN, state.zoomLevel - ZOOM_STEP); applyZoom(); }
function zoomReset(){ state.zoomLevel = 1.0; applyZoom(); }

function applyZoom() {
  const wrapper = document.getElementById('tree-wrapper');
  wrapper.style.transform       = `scale(${state.zoomLevel})`;
  wrapper.style.transformOrigin = 'top center';
  document.getElementById('zoom-display').textContent = Math.round(state.zoomLevel * 100) + '%';
}
```

**`#tree-wrapper`** contains the entire tree DOM + SVG connector overlay. Scaling both together keeps lines aligned with cards at any zoom level — no recalculation needed.

**Pan / scroll:** The chart area (`#chart-container`) uses `overflow: auto`. At zoom < 1.0, the wrapper shrinks, so scrollbars may disappear — this is acceptable. At zoom > 1.0, the scaled wrapper overflows its container and scrollbars appear.

> **Do NOT use SVG `viewBox` zoom** — that would require rebuilding the entire SVG from scratch on each zoom. CSS transform is instant.

**Zoom controls UI:**
```
[−]  [100%]  [+]  [Reset]
```
Buttons bind to `zoomOut()`, `zoomIn()`, `zoomReset()` directly via `onclick` attributes or a single delegated listener on `#toolbar`.

---

## 6. Connector Drawing (SVG Overlay)

### Decision: SVG Overlay (not CSS pseudo-elements)

| Approach | Pros | Cons |
|---|---|---|
| **CSS pseudo-elements** | No JS needed, purely declarative | Cannot draw horizontal segments between siblings; only vertical stubs work. Right-angle connectors across arbitrary widths are impossible without knowing sibling positions. |
| **SVG overlay** | Pixel-perfect, right-angle lines, handles any tree width | Must be redrawn after render + resize; uses `getBoundingClientRect()` |
| Canvas | Fast for many nodes | Overkill; no DOM event integration; must handle HiDPI manually |

**Decision: SVG overlay.** It is the only approach that can draw accurate right-angle elbow connectors at arbitrary tree widths.

### SVG Structure

```html
<div id="chart-container">
  <div id="tree-wrapper">
    <div id="tree">…cards…</div>
    <svg id="connector-svg" style="position:absolute;top:0;left:0;pointer-events:none;overflow:visible;"></svg>
  </div>
</div>
```

The SVG is positioned absolute at (0,0) inside `#tree-wrapper` with `overflow: visible`. It shares the same coordinate space as the cards, so `getBoundingClientRect()` offsets can be converted using the wrapper's own rect.

### Connector Drawing Algorithm

For every parent-child pair in the visible tree:

```
parentRect = parentCard.getBoundingClientRect()
childRect  = childCard.getBoundingClientRect()
wrapperRect = treeWrapper.getBoundingClientRect()

// Parent exit point: bottom-center of parent card
px = parentRect.left + parentRect.width/2  - wrapperRect.left
py = parentRect.bottom                     - wrapperRect.top

// Child entry point: top-center of child card
cx = childRect.left + childRect.width/2   - wrapperRect.left
cy = childRect.top                         - wrapperRect.top

// Midpoint Y for the horizontal elbow
my = (py + cy) / 2

// SVG path: vertical down → horizontal → vertical down
path = `M ${px} ${py}
        L ${px} ${my}
        L ${cx} ${my}
        L ${cx} ${cy}`
```

Each path is a `<path>` element with `stroke="#CBD5E1"` (or theme color), `stroke-width="2"`, `fill="none"`.

### Redraw Triggers

`drawConnectors()` must be called:
1. After `renderTree()` (initial render)
2. After every `handleToggle()` (tree shape changes)
3. After `applyZoom()` — because `getBoundingClientRect()` returns scaled values; since the SVG is inside the same scaled wrapper, the relative positions remain correct. ✅ No redraw needed for zoom.
4. On `window.resize` (debounced 100ms)

```js
window.addEventListener('resize', debounce(drawConnectors, 100));
```

### CSS Vertical Stub (Optional Optimization)

A thin vertical line below each card to the connector horizontal bar can be done in CSS using `::after` on `.card`, avoiding SVG for the "simple" part:

```css
.card::after {
  content: '';
  display: block;
  width: 2px;
  height: 20px;       /* half the gap between card bottom and children row */
  background: #CBD5E1;
  margin: 0 auto;
}
```

However, mixing CSS stubs with SVG elbows risks misalignment. **Recommendation: use SVG for all connector segments** for consistency.

---

## 7. Add Member Modal

### Form Fields

```
Name*         [text input]
Title*        [text input]
Department*   [select: Engineering | Product | Marketing | Design | Executive | HR | Finance | Other]
Reports To    [read-only, pre-filled with parent node name]
              [Save]  [Cancel]
```

### Flow

1. User clicks **"+ Add Report"** button on any card → `showModal(nodeId)` called
2. Modal appears with "Reports To" pre-filled
3. On Save: validate required fields → create new node object with `id = "node-" + Date.now()` → push to `ORG_DATA` → rebuild indexes → re-render
4. On Cancel / click-outside / Escape key → `hideModal()`

### Modal DOM

```html
<div id="modal-overlay" class="hidden" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div id="modal-panel">
    <h2 id="modal-title">Add Team Member</h2>
    <form id="add-member-form">…</form>
  </div>
</div>
```

`<dialog>` element is intentionally **not** used — native `<dialog>` has inconsistent backdrop support across browsers. A `div` overlay with `position:fixed; inset:0` is more predictable.

---

## 8. Search

### Approach: Live filter with highlight

```js
function filterNodes(query) {
  state.searchQuery = query.toLowerCase().trim();
  renderTree();   // re-render applies highlight and dims non-matching nodes
}
```

In `buildCardHTML(node)`:
- If `searchQuery` is non-empty and the node's name/title/department does **not** match → add class `card--dimmed` (reduced opacity)
- If it matches → wrap matched substring in `<mark>` tag
- Ancestors of matching nodes are **not** dimmed (show the path to the match)

Ancestor-preservation logic:
```js
function getAncestorIds(nodeId) {
  const ancestors = new Set();
  let current = nodeMap[nodeId]?.parentId;
  while (current) {
    ancestors.add(current);
    current = nodeMap[current]?.parentId;
  }
  return ancestors;
}
```
Pre-compute the set of matching node IDs + their ancestors before rendering. Any node not in this set gets `card--dimmed`.

---

## 9. Non-Functional Considerations

### Performance
- Full re-render is O(n) where n = number of nodes. At <200 nodes, this is <5ms per render — no virtual DOM or diffing needed.
- `drawConnectors()` is O(e) where e = visible edges. Same bound.
- Search filtering re-renders on every keystroke — acceptable at this scale. Debounce if >150 nodes.

### Security
- No external requests. No `eval()`. No `innerHTML` injection with user-controlled `id`/`name` without sanitization.
- **IMPORTANT for SR1:** When inserting user-provided name/title into card HTML, use `textContent` assignment or escape HTML entities — do **not** use raw `innerHTML` with unsanitized user input.
  ```js
  function escapeHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  ```

### Accessibility
- Cards use `role="button"` + `tabindex="0"` + `aria-expanded` for expand/collapse toggles.
- Modal uses `role="dialog"` + `aria-modal="true"` + focus trap on open.
- Color is not the sole differentiator for departments — use `data-department` attribute for CSS and include the department name in the card text.

### Scalability
- This architecture handles up to ~200 nodes without modifications.
- Beyond 200 nodes: switch renderNode to document fragment batching to reduce reflow cycles. Out of scope for this build.

### Browser Compatibility
- All APIs used (`Set`, `getBoundingClientRect`, `closest`, `dataset`, CSS flex) are supported in Chrome 80+, Firefox 75+, Safari 13+, Edge 80+. No polyfills needed.

---

## 10. File Structure

```
org_chart_app/
├── index.html          ← EVERYTHING: inline <style> + <script>
├── designs/
│   ├── ux-spec.md      ← UX Engineer deliverable
│   └── architecture.md ← This document
└── README.md
```

`index.html` internal structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Org Chart</title>
  <style>
    /* ── Reset ── */
    /* ── CSS Custom Properties (design tokens) ── */
    /* ── Layout shells ── */
    /* ── Toolbar ── */
    /* ── Tree & Cards ── */
    /* ── Connectors ── */
    /* ── Modal ── */
    /* ── Search ── */
    /* ── Animations ── */
    /* ── Utility ── */
  </style>
</head>
<body>
  <!-- Toolbar -->
  <!-- Chart container -->
  <!-- Modal overlay -->
  <script>
    // 1. DATA
    // 2. STATE
    // 3. RENDERER
    // 4. CONNECTOR DRAWING
    // 5. MODAL
    // 6. EVENT HANDLING
    // 7. SEARCH
    // 8. ZOOM
    // 9. BOOTSTRAP
  </script>
</body>
</html>
```

---

## ADR-001: CSS Flexbox vs Absolute Positioning for Tree Layout

**Status:** Accepted  
**Context:** A top-down tree chart needs child cards to be distributed horizontally without overlapping. Two approaches were considered: (a) compute x/y positions in JS and use `position:absolute`, or (b) use CSS flexbox to distribute children automatically.  
**Decision:** CSS Flexbox. The browser's layout engine handles distribution, gap, and wrap. No position math required. Cards cannot overlap because flex does not allow it.  
**Consequences:** We lose fine-grained control over exact card positions, but gain correctness-by-default. Edge case: very deep/wide trees may overflow the viewport — mitigated by zoom-out and horizontal scroll.

## ADR-002: SVG Overlay for Connectors

**Status:** Accepted  
**Context:** Right-angle elbow connectors between parent and child cards must adapt to any tree width. CSS pseudo-elements can only draw simple top/bottom stubs — they cannot draw horizontal segments between arbitrary sibling positions.  
**Decision:** SVG overlay positioned absolute inside the scaled `#tree-wrapper`. After each render, `drawConnectors()` walks visible parent-child pairs, reads `getBoundingClientRect()`, and emits `<path>` elements with right-angle elbows.  
**Consequences:** Connectors must be redrawn after render and window resize. Since SVG is inside the same CSS-scaled wrapper, zoom does not require redraw.

## ADR-003: Full Re-render on State Change

**Status:** Accepted  
**Context:** State changes (collapse, add member, search) require updating the tree. Two options: (a) patch the DOM in-place, or (b) clear and re-render from scratch.  
**Decision:** Full re-render. `renderTree()` clears `innerHTML` and rebuilds from data + state. For <200 nodes this is imperceptible.  
**Consequences:** Per-node event listeners cannot survive re-render — mitigated by a single delegated listener on the stable container. The simplicity payoff is zero stale-state bugs.

## ADR-004: No `<dialog>` Element for Modal

**Status:** Accepted  
**Context:** Native `<dialog>` is now well-supported but `::backdrop` styling and `showModal()` behavior has subtle cross-browser quirks in Safari.  
**Decision:** Use a `<div id="modal-overlay">` with `position:fixed; inset:0` and manual focus trap. More predictable, zero dependency on browser modal stack.  
**Consequences:** Must implement Escape-key handler and focus trap manually. Both are ~10 lines of JS each.
