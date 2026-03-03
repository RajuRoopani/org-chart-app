# Org Chart Application

A professional, interactive organizational hierarchy visualization tool. Display, explore, and manage your organization's structure with a beautiful top-down tree layout, all in a single, zero-dependency HTML file.

---

## Features

- 🏢 **Interactive Organizational Hierarchy** — Visualize your organization structure as a top-down tree with professional card-based employee nodes
- 🔗 **Connected Tree Layout** — Automatic right-angle SVG connector lines between parent and child nodes, no overlap guaranteed
- 📁 **Expand / Collapse Subtrees** — Click the toggle arrow to hide or show an employee's direct reports and their descendants
- ✨ **Click to Select & Highlight** — Click any employee card to select it; selected cards are highlighted with a blue border and light blue background
- ➕ **Add New Team Members** — Click the "+" button on any card to open a modal form and add a new employee to the org chart
- 🔍 **Live Search & Filter** — Search by employee name, job title, or department; matching nodes are highlighted and non-matching cards are dimmed
- 🔎 **Zoom Controls** — Zoom in (up to 150%), zoom out (down to 50%), or reset to 100% zoom; use keyboard or toolbar buttons
- 🎨 **Department Color-Coded Cards** — Each card has a colored accent bar that identifies the employee's department (Engineering, Product, Marketing, etc.)
- ⚡ **Pure HTML/CSS/JS** — No dependencies, no build step, no external CDNs, no frameworks — just open and use
- 📱 **Responsive & Accessible** — Works in modern browsers (Chrome, Firefox, Safari, Edge); supports keyboard navigation and screen readers

---

## Getting Started

### Installation

No installation required. The entire application is a single `index.html` file.

### How to Use

1. **Download or clone** this repository
2. **Open `index.html`** in your web browser (Chrome 80+, Firefox 75+, Safari 13+, Edge 80+)
3. The org chart loads instantly with 12 pre-loaded employees across 4 organizational levels

No server, no build process, no dependencies.

---

## Usage Guide

### Navigating the Org Chart

#### **Expand and Collapse Subtrees**
- Click the **down arrow (▼)** on a card to collapse an employee's subtree and hide their direct reports
- Click the **right arrow (▶)** to expand and reveal the subtree again
- The connector lines automatically update when you expand or collapse

#### **Select an Employee**
- Click anywhere on an employee card to select it
- The selected card is highlighted with a blue border and light blue background
- Only one employee can be selected at a time; clicking another card deselects the previous one

#### **Add a New Team Member**
- Click the **"+" button** on any card to open the "Add Employee" modal
- Fill in the required fields:
  - **Full Name** (required)
  - **Job Title** (required)
  - **Department** (required) — choose from Engineering, Product, Marketing, Design, HR, Finance, or Other
- The "Reports To" field is automatically pre-filled with the parent employee's name
- Click **"Add Employee"** to save the new team member, or **"Cancel"** to close without saving
- The new employee appears as a child of the selected parent, and connector lines update automatically

#### **Search and Filter Employees**
- Use the **search box** in the toolbar to search by employee name, job title, or department
- As you type, the chart filters in real-time:
  - **Matching employees** are highlighted with yellow or colored backgrounds
  - **Non-matching employees** are dimmed (reduced opacity)
  - **Ancestors of matches** remain fully visible so you can see the organizational path
- Clear the search box to show all employees again

#### **Zoom In and Out**
- Use the **zoom controls** in the header:
  - Click **[−]** to zoom out (minimum 50%)
  - Click **[+]** to zoom in (maximum 150%)
  - Click **[Reset]** to return to 100% zoom
  - The current zoom percentage is displayed between the buttons
- **Scroll** both horizontally and vertically to pan around the chart when zoomed in
- At zoom levels < 100%, you may see fewer scrollbars

---

## Sample Data

The application comes pre-loaded with **12 employees** across **4 organizational levels**:

- **Level 0 (CEO):** Sarah Chen — Chief Executive Officer
- **Level 1 (VPs):** Marcus Rivera (VP Engineering), Priya Patel (VP Product), James O'Brien (VP Marketing)
- **Level 2 (Directors):** Aiko Tanaka, Leon Fischer, Chioma Obi, Tom Nakamura
- **Level 3 (Managers/ICs):** Elena Vasquez, Kwame Asante, Rania Saleh, Luca Ferrari

You can expand each node to see its subtree, select employees, and add new team members. The sample data demonstrates the full feature set and provides a good starting point for exploring your own organizational data.

---

## Technical Details

### Architecture

- **CSS Flexbox Layout** — The tree is rendered using CSS Flexbox (not absolute positioning), which prevents horizontal overlap and allows the browser's layout engine to distribute cards evenly
- **SVG Connector Lines** — Right-angle elbow connectors are drawn using an SVG overlay that is positioned over the tree; connectors are redrawn after each state change to ensure accurate positioning
- **Single Delegated Event Listener** — All user interactions (click to select, expand/collapse, modal actions, search) are handled by a single delegated event listener on the main chart container, avoiding the need to re-register listeners after re-renders
- **Full Re-render on State Change** — The entire tree DOM is rebuilt on every state change (collapse, add member, search filter, etc.). For trees with fewer than 200 nodes, this is imperceptible (~1–5ms per render) and eliminates stale-state bugs

### Component Structure

Inside `index.html`:

1. **HTML** — Single page with a header (title + zoom controls), search box, chart container, and modal overlay
2. **CSS** — Comprehensive inline stylesheet with design tokens, layout rules, card styles, modal styles, animations, and utility classes
3. **JavaScript** — Module-scope code organized into sections:
   - Data: Organization structure (ORG_DATA array) and index structures (nodeMap, childMap)
   - State: Application state object (collapsed nodes, selected node, zoom level, search query, modal state)
   - Renderer: Tree rendering functions (renderTree, renderNode, buildCardHTML)
   - Connector Drawing: SVG line drawing (drawConnectors)
   - Modal: Add employee modal (showModal, hideModal, handleAddMember)
   - Event Handling: Single delegated listener for all interactions
   - Search: Live filtering and highlighting (filterNodes, highlightMatch)
   - Zoom: Scale transforms (applyZoom, zoomIn, zoomOut)
   - Bootstrap: DOMContentLoaded initialization

### Data Model

Each employee is represented as a plain JavaScript object:

```javascript
{
  id:         String,        // Unique ID (e.g., "ceo", "vp-eng")
  name:       String,        // Full name
  title:      String,        // Job title
  department: String,        // Department (used for color-coding)
  parentId:   String|null    // ID of the parent (null for root)
}
```

State is maintained in a module-scope object:

```javascript
{
  collapsed:     Set<nodeId>,    // Set of collapsed node IDs
  selected:      String|null,    // Currently selected node ID
  zoomLevel:     Number,         // Current zoom factor (default 1.0)
  searchQuery:   String,         // Current search text
  modalMode:     String|null,    // null or "add"
  modalParentId: String|null     // Parent ID for new employee
}
```

### Performance

- **Rendering:** O(n) where n = number of visible nodes. At <200 nodes, full re-render takes <5ms
- **Search filtering:** O(n) to compute matching set + ancestors; O(n) to re-render
- **Connector drawing:** O(e) where e = visible edges (parent-child relationships)
- **No virtual DOM or diffing** — simplicity and correctness are prioritized over advanced optimization

### Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 80+     | ✅ Supported |
| Firefox | 75+     | ✅ Supported |
| Safari  | 13+     | ✅ Supported |
| Edge    | 80+     | ✅ Supported |

All required APIs are natively supported: CSS Flexbox, SVG, `Set`, `getBoundingClientRect()`, `closest()`, `dataset`, ES6 template literals, `const`/`let`, arrow functions, spread operator.

---

## License

MIT License — feel free to use, modify, and distribute this application.

---

## Questions & Support

For issues, feature requests, or questions about the application:

1. Check the `designs/` folder for detailed technical specifications:
   - `architecture.md` — Full system design, data model, algorithm descriptions, ADRs
   - `ux-spec.md` — Visual and interaction specifications, color palette, typography

2. Review the inline comments in `index.html` for implementation details

3. The application is intentionally simple (single file, no dependencies) to make debugging and customization straightforward

---

## Customization

### Adding Initial Employees

Edit the `ORG_DATA` array in the `<script>` section of `index.html`. Each object must have `id`, `name`, `title`, `department`, and `parentId` fields. The `id` must be unique; `parentId` should reference another employee's `id` (or `null` for the root node).

### Changing the Color Palette

Modify the CSS custom properties (variables) in the `<style>` section:
- Primary brand color: `--color-primary`
- Department accent colors: `--dept-engineering`, `--dept-marketing`, etc.
- Text colors, card styles, and more are all customizable via CSS variables

### Styling Cards

The card layout, typography, spacing, and appearance are controlled by CSS classes:
- `.card` — Main card container
- `.card__name` — Employee name
- `.card__title` — Job title
- `.card__actions` — Action buttons row

Modify these classes to customize the look and feel without touching the JavaScript logic.

---

## Known Limitations

1. **No data persistence** — Data is held in memory only. Refresh the page to reset to the initial ORG_DATA. To save data, you would need to integrate with a backend API or local storage (out of scope for this single-file version).

2. **No edit or delete** — Employees can be added but not edited or deleted. This can be added in a future version.

3. **No undo/redo** — Changes are applied immediately with no undo history.

4. **Large trees (>200 nodes)** — While the application can technically handle larger datasets, the full re-render approach becomes less performant. For >200 nodes, consider optimizations like virtual scrolling or DOM patching (advanced, out of scope).

---

## File Structure

```
org_chart_app/
├── index.html              # ← The entire application (HTML + CSS + JS)
├── README.md               # ← This file
├── designs/
│   ├── architecture.md     # Technical architecture and design decisions
│   ├── ux-spec.md          # Visual design, color palette, interaction specs
│   └── adr/                # Architecture Decision Records
│       ├── ADR-001-tree-layout.md
│       ├── ADR-002-svg-connectors.md
│       ├── ADR-003-full-rerender.md
│       └── ADR-004-modal-div-not-dialog.md
└── .git/                   # Git version control
```

---

Enjoy exploring your organization's hierarchy! 🚀
