# Org Chart Application — UX Design Spec

## User Story
As a corporate user, I want a visual org chart application that displays my organization's hierarchy as an interactive tree, so that I can navigate reporting relationships, understand the structure at a glance, and add new employees to the chart.

---

## User Flow

```
App Load
  └─→ Header renders (title + zoom controls)
  └─→ Tree renders from seed data (CEO at root)
  └─→ All nodes visible, connectors drawn

User clicks node card
  └─→ Card highlights (selected state)
  └─→ Previously selected card deselects

User clicks [+ Add] button on a card
  └─→ Modal opens (parent pre-identified)
  └─→ User fills Name + Title fields
        ↓ (missing required field)
      Inline validation error shown
      Submit button remains disabled
        ↓ (valid)
      [Submit] → Modal closes → New card animates in as child
      [Cancel] → Modal closes, no change

User clicks expand/collapse toggle on card
  └─→ Children subtree collapses/expands
  └─→ Toggle icon changes (▶ collapsed / ▼ expanded)
  └─→ Connector lines update

User clicks zoom [+] / [−] buttons
  └─→ Tree scales up/down (50%–150%, step 10%)
  └─→ Current zoom % shown in header

User scrolls
  └─→ Both axes scroll (overflow: auto on tree container)
```

---

## Screens & Wireframes

### Screen: Main App View

```
┌──────────────────────────────────────────────────────────────────────┐
│  🏢  Org Chart                              [−]  100%  [+]           │
│      #1565C0 bg, white text, 56px tall                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                    ┌───────────────────┐                             │
│                    │ ▐ Sarah Chen       │  ← selected (blue border)  │
│                    │   CEO             │                             │
│                    │              [+] ▼│                             │
│                    └─────────┬─────────┘                             │
│                 ┌────────────┴────────────┐                          │
│      ┌──────────┴──────┐       ┌──────────┴──────┐                  │
│      │   James Park    │       │  Aisha Okonkwo  │                  │
│      │   VP Engineering│       │  VP Marketing   │                  │
│      │            [+] ▼│       │            [+] ▼│                  │
│      └──────┬──────────┘       └─────────────────┘                  │
│      ┌──────┴──────┐                                                 │
│      │  Wei Zhang  │                                                 │
│      │  Sr. Eng.   │                                                 │
│      │        [+] ▼│                                                 │
│      └─────────────┘                                                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Screen: Collapsed Subtree

```
      ┌───────────────────┐
      │   James Park      │
      │   VP Engineering  │
      │              [+] ▶│  ← ▶ = collapsed, children hidden
      └───────────────────┘
```

### Screen: Add Employee Modal

```
┌──────────────────────────────────────────────────────────────────────┐
│  ░░░░░░░░░░░░░ BACKDROP (rgba 0,0,0,0.45) ░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░░░░  ┌──────────────────────────────────────┐  ░░░░░░░░░░░░░░  │
│  ░░░░░░░  │  Add Employee                    [✕]  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  Reporting to: James Park             │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  ─────────────────────────────────    │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  Full Name *                          │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  ┌─────────────────────────────────┐  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  │                                 │  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  └─────────────────────────────────┘  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  ⚠ Name is required                    │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │                                        │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  Job Title *                           │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  ┌─────────────────────────────────┐  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  │                                 │  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │  └─────────────────────────────────┘  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │                                        │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  │          [Cancel]      [Add Employee]  │  ░░░░░░░░░░░░░  │
│  ░░░░░░░  └────────────────────────────────────────┘  ░░░░░░░░░░░░░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Color Palette — CSS Custom Properties

```css
:root {
  /* === Primary Brand === */
  --color-primary:          #1565C0;   /* Header bg, selected border, primary CTA */
  --color-primary-dark:     #0D47A1;   /* CTA hover, focus ring */
  --color-primary-light:    #1976D2;   /* Link color, secondary accents */
  --color-primary-faint:    #E3F2FD;   /* Selected card bg tint */

  /* === App Chrome === */
  --color-header-bg:        #1565C0;
  --color-header-text:      #FFFFFF;
  --color-app-bg:           #F0F4F8;   /* Page background — cool off-white */

  /* === Card === */
  --color-card-bg:          #FFFFFF;
  --color-card-border:      #DDE3EA;   /* Resting border */
  --color-card-border-hover:#90CAF9;   /* Hover border */
  --color-card-border-selected: #1565C0; /* Selected border */
  --color-card-shadow:      rgba(0, 0, 0, 0.08);
  --color-card-shadow-hover:rgba(0, 0, 0, 0.15);

  /* === Text === */
  --color-text-heading:     #0D1B2A;   /* Employee name */
  --color-text-body:        #37474F;   /* Job title */
  --color-text-muted:       #78909C;   /* Secondary labels, "Reporting to:" */
  --color-text-on-primary:  #FFFFFF;

  /* === Connectors === */
  --color-connector:        #90A4AE;   /* SVG/border lines between nodes */

  /* === Form & Modal === */
  --color-input-border:     #B0BEC5;
  --color-input-border-focus: #1565C0;
  --color-input-bg:         #FFFFFF;
  --color-error:            #C62828;   /* Inline validation errors */
  --color-error-bg:         #FFEBEE;
  --color-modal-backdrop:   rgba(0, 0, 0, 0.45);
  --color-modal-bg:         #FFFFFF;

  /* === Interactive States === */
  --color-btn-primary-bg:       #1565C0;
  --color-btn-primary-hover:    #0D47A1;
  --color-btn-primary-text:     #FFFFFF;
  --color-btn-secondary-bg:     #FFFFFF;
  --color-btn-secondary-border: #B0BEC5;
  --color-btn-secondary-hover:  #ECEFF1;
  --color-btn-secondary-text:   #37474F;
  --color-btn-disabled-bg:      #CFD8DC;
  --color-btn-disabled-text:    #90A4AE;

  /* === Department Accent Bar (left border on card) === */
  --dept-engineering:   #1565C0;   /* Blue */
  --dept-marketing:     #7B1FA2;   /* Purple */
  --dept-sales:         #2E7D32;   /* Green */
  --dept-hr:            #E65100;   /* Orange */
  --dept-finance:       #00695C;   /* Teal */
  --dept-default:       #455A64;   /* Slate (root/unassigned) */
}
```

---

## Card Design

### Dimensions & Structure

```
┌─────────────────────────────────────┐
│▐ ← 4px dept accent bar              │
│   Employee Name (bold, 14px)         │
│   Job Title (regular, 12px, muted)   │
│                         [+]  [▼/▶]  │
└─────────────────────────────────────┘
```

### Exact CSS Values

```css
.org-card {
  min-width: 180px;
  max-width: 220px;
  padding: 12px 14px 12px 18px;  /* extra-left for accent bar space */
  background: var(--color-card-bg);
  border: 1.5px solid var(--color-card-border);
  border-radius: 8px;
  box-shadow: 0 2px 6px var(--color-card-shadow);
  position: relative;
  cursor: pointer;
  transition: box-shadow 150ms ease, border-color 150ms ease, transform 150ms ease;
}

/* Department accent bar */
.org-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  border-radius: 8px 0 0 8px;
  background: var(--dept-default);  /* JS sets inline --dept-color override */
}

/* Hover state */
.org-card:hover {
  border-color: var(--color-card-border-hover);
  box-shadow: 0 4px 12px var(--color-card-shadow-hover);
  transform: translateY(-2px);
}

/* Selected state */
.org-card.is-selected {
  border-color: var(--color-card-border-selected);
  border-width: 2px;
  background: var(--color-primary-faint);
  box-shadow: 0 4px 12px rgba(21, 101, 192, 0.20);
}

/* Name typography */
.org-card__name {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-heading);
  line-height: 1.3;
  margin-bottom: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}

/* Title typography */
.org-card__title {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  font-size: 12px;
  font-weight: 400;
  color: var(--color-text-body);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}

/* Card actions row */
.org-card__actions {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  justify-content: flex-end;
}
```

### Card Action Buttons

```css
/* Add Employee button */
.org-card__btn-add {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 1.5px solid var(--color-card-border);
  background: var(--color-card-bg);
  color: var(--color-primary-light);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: background 120ms ease, border-color 120ms ease;
}
.org-card__btn-add:hover {
  background: var(--color-primary-faint);
  border-color: var(--color-primary-light);
}

/* Expand/Collapse toggle — only shown when node has children */
.org-card__btn-toggle {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 1.5px solid var(--color-card-border);
  background: var(--color-card-bg);
  color: var(--color-text-muted);
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 120ms ease;
}
.org-card__btn-toggle:hover {
  background: #ECEFF1;
}
/* Icon: ▼ when expanded, ▶ when collapsed */
```

---

## Header Bar

```css
.app-header {
  height: 56px;
  background: var(--color-header-bg);
  color: var(--color-header-text);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.20);
  position: sticky;
  top: 0;
  z-index: 100;
  flex-shrink: 0;
}

/* App title */
.app-header__title {
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Zoom controls cluster */
.zoom-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.zoom-controls__btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1.5px solid rgba(255,255,255,0.35);
  background: rgba(255,255,255,0.12);
  color: #FFFFFF;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 120ms ease;
}
.zoom-controls__btn:hover:not(:disabled) {
  background: rgba(255,255,255,0.25);
}
.zoom-controls__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.zoom-controls__label {
  font-size: 13px;
  font-weight: 600;
  min-width: 44px;
  text-align: center;
  color: rgba(255,255,255,0.90);
  font-family: 'Segoe UI', system-ui, sans-serif;
}
```

---

## Connector Lines

```css
/* Tree layout uses a CSS-based or inline-SVG connector approach.
   Connectors are drawn as right-angle lines (elbow connectors):
   vertical drop from parent, horizontal across to child. */

--connector-color: #90A4AE;
--connector-width: 2px;

/* Vertical stem from parent card bottom to horizontal bar */
/* Horizontal bar from stem to each child card top */

/* Spacing values */
--level-gap: 48px;      /* Vertical space between parent bottom and child top */
--sibling-gap: 24px;    /* Horizontal space between sibling cards */
```

**Connector rendering spec:**
- Draw a vertical line from the bottom-center of the parent card downward `24px`
- Then a horizontal line spanning to align with each child's top-center
- Then a vertical line dropping `24px` to each child card's top
- Line style: `2px solid #90A4AE` (no dashes, no arrows)
- Corners are hard right-angles (not curved)
- Connectors disappear instantly when a subtree collapses (no animation needed on lines)

---

## Zoom Controls — Behavior

| Property | Value |
|---|---|
| Minimum zoom | 50% |
| Maximum zoom | 150% |
| Step size | 10% |
| Default | 100% |
| Mechanism | `transform: scale(N)` on tree wrapper element |
| Transform origin | `top center` |
| Label format | `"100%"` (integer, no decimal) |
| [−] disabled at | 50% |
| [+] disabled at | 150% |

```css
.tree-viewport {
  overflow: auto;          /* scroll both axes */
  flex: 1;
  padding: 40px;
}

.tree-wrapper {
  display: inline-block;   /* shrink-wraps tree content */
  transform-origin: top center;
  transition: transform 200ms ease;
}
```

---

## Modal / Form Design

### Structure & CSS

```css
/* Backdrop */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: var(--color-modal-backdrop);   /* rgba(0,0,0,0.45) */
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Open: opacity 1, visible — animation spec below */
}

/* Modal panel */
.modal {
  background: var(--color-modal-bg);
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.22);
  padding: 28px;
  width: 420px;
  max-width: calc(100vw - 32px);
  position: relative;
}

/* Modal header row */
.modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}
.modal__title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-heading);
  font-family: 'Segoe UI', system-ui, sans-serif;
}
.modal__close {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal__close:hover {
  background: #ECEFF1;
}

/* "Reporting to" subtitle */
.modal__subtitle {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 20px;
  font-family: 'Segoe UI', system-ui, sans-serif;
}
.modal__subtitle strong {
  color: var(--color-text-body);
  font-weight: 600;
}

/* Divider */
.modal__divider {
  height: 1px;
  background: #ECEFF1;
  margin-bottom: 20px;
}
```

### Form Fields

```css
/* Field group */
.form-field {
  margin-bottom: 18px;
}

/* Label */
.form-field__label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-body);
  margin-bottom: 6px;
  font-family: 'Segoe UI', system-ui, sans-serif;
}
/* Required asterisk */
.form-field__label .required {
  color: var(--color-error);
  margin-left: 2px;
}

/* Input */
.form-field__input {
  width: 100%;
  box-sizing: border-box;
  height: 40px;
  padding: 0 12px;
  border: 1.5px solid var(--color-input-border);
  border-radius: 6px;
  background: var(--color-input-bg);
  font-size: 14px;
  color: var(--color-text-heading);
  font-family: 'Segoe UI', system-ui, sans-serif;
  transition: border-color 120ms ease, box-shadow 120ms ease;
  outline: none;
}
.form-field__input:focus {
  border-color: var(--color-input-border-focus);
  box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.18);
}
.form-field__input.has-error {
  border-color: var(--color-error);
}
.form-field__input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(198, 40, 40, 0.15);
}

/* Validation error message */
.form-field__error {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 5px;
  font-size: 12px;
  color: var(--color-error);
  font-family: 'Segoe UI', system-ui, sans-serif;
  /* ⚠ icon prefix in HTML: use Unicode U+26A0 or SVG inline */
}
```

### Modal Buttons

```css
/* Button row */
.modal__footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 24px;
}

/* Cancel button */
.btn-secondary {
  height: 38px;
  padding: 0 20px;
  border: 1.5px solid var(--color-btn-secondary-border);
  border-radius: 6px;
  background: var(--color-btn-secondary-bg);
  color: var(--color-btn-secondary-text);
  font-size: 14px;
  font-weight: 500;
  font-family: 'Segoe UI', system-ui, sans-serif;
  cursor: pointer;
  transition: background 120ms ease;
}
.btn-secondary:hover {
  background: var(--color-btn-secondary-hover);
}

/* Submit button */
.btn-primary {
  height: 38px;
  padding: 0 20px;
  border: none;
  border-radius: 6px;
  background: var(--color-btn-primary-bg);
  color: var(--color-btn-primary-text);
  font-size: 14px;
  font-weight: 600;
  font-family: 'Segoe UI', system-ui, sans-serif;
  cursor: pointer;
  transition: background 120ms ease;
}
.btn-primary:hover:not(:disabled) {
  background: var(--color-btn-primary-hover);
}
.btn-primary:disabled {
  background: var(--color-btn-disabled-bg);
  color: var(--color-btn-disabled-text);
  cursor: not-allowed;
}
```

**Submit button disabled rule:** Disabled when either required field is empty OR has a validation error. Enabled immediately when both fields contain at least 1 non-whitespace character.

---

## Component Specs

| Component | States | Behavior |
|---|---|---|
| **Org Card** | default, hover, selected, no-children | Click card body → selects (highlights); deselects previous selection. Click `[+]` → opens modal with this node as parent. Click toggle → collapses/expands children. No-children nodes: toggle button hidden, `[+]` still shown. |
| **Expand/Collapse Toggle** | expanded (▼), collapsed (▶), hidden (leaf node) | Visible only when node has ≥1 child. Click → toggles subtree visibility. Icon: `▼` = children visible; `▶` = children hidden. Button sits in card's action row, rightmost. |
| **Add Employee Button** | default, hover | `+` icon. Always visible on all cards. Click → fires modal open event with parent node ID. Stoppage: click does not also trigger card selection. |
| **Header Zoom [+]** | default, hover, disabled | Disabled (opacity 0.4, pointer-events none) when zoom = 150%. Each click increases zoom by 10%. |
| **Header Zoom [−]** | default, hover, disabled | Disabled when zoom = 50%. Each click decreases zoom by 10%. |
| **Zoom % Label** | live | Displays current zoom level as integer + `%`. Updates synchronously on button click. |
| **Modal Backdrop** | open, closed | Click on backdrop → same as Cancel (modal closes). |
| **Name Input** | empty, filled, error, focus | Required field. Error shown on first blur if empty, or on attempted submit. Clears error on next keystroke. |
| **Job Title Input** | empty, filled, error, focus | Required field. Same error behavior as Name Input. |
| **Submit Button** | enabled, disabled | Disabled until both inputs have value. Never shows loading state (in-memory, instant). |

---

## Interaction Notes

### Loading
No async loading — data is in-memory. App renders immediately on page load. No spinner needed.

### Empty State
The root node (CEO) is always present in seed data. The tree is never empty. No empty state required.

### Error State
- **Form validation:** Inline error messages below each field (see form spec above). Red text + ⚠ icon. Shown on field blur OR on Submit click if field is empty.
- **No toast/banner errors** — all interactions are local, no network calls.

### Success Feedback
- **Add Employee:** New card appears in the tree as a child of the parent node. The new card entrance animation is: `opacity 0→1` + `transform: scale(0.85)→scale(1)` over `250ms ease-out`. Modal closes instantly (no delay).
- **No persistent success toast** — the new card appearing IS the success feedback.

### Hover / Focus
- **Card hover:** `translateY(-2px)` + deeper box shadow + blue border tint (see card CSS)
- **Button hover:** Background lightens (see button CSS)
- **Input focus:** Blue border + soft blue glow ring (see input CSS)
- **Card keyboard focus** (tabbing): 2px dashed focus ring `outline: 2px dashed var(--color-primary)` at 2px offset — ensures keyboard accessibility

### Collapse / Expand
- Collapsed state: child cards and connectors are `display: none` (instant, no animation). This avoids layout jank and keeps the tree stable during zoom.
- The toggle icon change (▶ ↔ ▼) is instant.
- *Note: No height animation on collapse — spec explicitly set to instant to avoid complexity with variable-depth subtrees.*

---

## Animation & Transitions

| Event | Property | Duration | Easing |
|---|---|---|---|
| Card hover (shadow, border, lift) | `box-shadow`, `border-color`, `transform` | `150ms` | `ease` |
| Card button hover (bg) | `background` | `120ms` | `ease` |
| Tree zoom change | `transform` on `.tree-wrapper` | `200ms` | `ease` |
| Modal open (backdrop) | `opacity: 0 → 1` | `180ms` | `ease` |
| Modal open (panel) | `opacity: 0→1` + `transform: scale(0.95)→scale(1)` | `180ms` | `ease-out` |
| Modal close | `opacity: 1→0` + `transform: scale(1)→scale(0.95)` | `140ms` | `ease-in` |
| New node entrance | `opacity: 0→1` + `transform: scale(0.85)→scale(1)` | `250ms` | `ease-out` |
| Collapse/Expand subtree | **None** — instant `display: none / block` | `0ms` | — |
| Input focus ring | `box-shadow` | `120ms` | `ease` |

**Implementation note:** All transitions are CSS-only (`transition` property). No JavaScript animation libraries. Use a `.is-open` / `.is-closing` class pattern on the modal to trigger enter/exit transitions.

---

## Typography

```css
/* Font stack — system fonts only, no web font loading */
--font-family: 'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif;

/* Scale */
--text-xs:    11px;   /* Badge labels, helper text */
--text-sm:    12px;   /* Card job title, form error messages */
--text-base:  14px;   /* Card name, form inputs, body text */
--text-md:    16px;   /* Modal section labels */
--text-lg:    18px;   /* Modal title */
--text-xl:    20px;   /* Header app title */

/* Weights */
--weight-normal:   400;
--weight-medium:   500;
--weight-semibold: 600;
--weight-bold:     700;

/* Line heights */
--leading-tight:  1.3;
--leading-normal: 1.5;
```

---

## Spacing System

```css
/* Base unit: 4px */
--space-1:   4px;
--space-2:   8px;
--space-3:   12px;
--space-4:   16px;
--space-5:   20px;
--space-6:   24px;
--space-7:   28px;
--space-8:   32px;
--space-10:  40px;
--space-12:  48px;
--space-14:  56px;

/* Tree-specific */
--tree-level-gap:   48px;   /* Vertical distance between levels */
--tree-sibling-gap: 24px;   /* Horizontal distance between siblings */
--tree-padding:     40px;   /* Padding inside the scrollable viewport */
```

---

## Responsive Behavior

### Breakpoints

| Breakpoint | Width | Behavior |
|---|---|---|
| Mobile | 375px – 767px | Tree scrolls both axes; cards scale to min-width 160px; header zoom controls visible but smaller; touch targets ≥ 44px |
| Tablet | 768px – 1279px | Default layout, zoom at 90% initial |
| Desktop | 1280px+ | Default layout, zoom at 100% initial |

### Mobile Specifics

```css
@media (max-width: 767px) {
  /* Header */
  .app-header {
    padding: 0 16px;
  }
  .app-header__title {
    font-size: 16px;
  }
  .zoom-controls__btn {
    width: 40px;    /* enlarged for touch — 40px min touch target */
    height: 40px;
  }

  /* Cards */
  .org-card {
    min-width: 160px;
    max-width: 190px;
    padding: 10px 12px 10px 16px;
  }
  .org-card__name  { font-size: 13px; }
  .org-card__title { font-size: 11px; }

  /* Card action buttons — bigger touch target */
  .org-card__btn-add,
  .org-card__btn-toggle {
    width: 32px;
    height: 32px;
  }

  /* Modal */
  .modal {
    width: calc(100vw - 32px);
    padding: 20px 16px;
  }

  /* Zoom initial value set via JS */
  /* initialZoom = window.innerWidth < 768 ? 0.75 : 1.0 */
}
```

### Touch Behavior
- **Tap on card:** same as click — selects card
- **Tap on [+]:** opens add modal
- **Tap on toggle:** expand/collapse
- **Pinch-to-zoom:** native browser zoom allowed (do NOT block with `user-scalable=no`)
- **Scroll:** `overflow: auto` on the tree viewport handles both-axis scroll on touch

### Scroll Behavior
- The entire tree is wrapped in a `div.tree-viewport` with `overflow: auto`
- When zoomed > 100%, the tree expands beyond the viewport and becomes scrollable naturally
- Header is `position: sticky; top: 0` — stays visible while tree scrolls
- No custom scroll logic required

---

## Data Model Reference (for JS implementation)

The following is the minimum shape of a node object needed by the renderer:

```js
{
  id: "unique-string",
  name: "Sarah Chen",
  title: "CEO",
  department: "default",       // maps to --dept-{department} CSS var
  parentId: null,              // null for root
  children: [],                // array of child node objects (tree, not flat)
  isExpanded: true             // default true
}
```

**Seed data:** At least 10 nodes across 3+ levels. Suggested structure:
- Level 0: CEO (1 node)
- Level 1: VP Engineering, VP Marketing, VP Sales (3 nodes)
- Level 2: Sr. Engineers ×2, Marketing Manager, Sales Lead, HR Director (5 nodes)
- Level 3: Junior Engineer ×1 (1 node)

---

## Delete Employee — Interaction Spec

### Resolved: Both open questions closed by EM (confirmed in-scope)

**Department field:** No dropdown in Add form. New node inherits parent's `department` value directly. Accent bar color is set automatically.

**Node deletion:** In scope. Delete must handle subtree reassignment.

---

### Delete Flow

```
User clicks [🗑] on a card
  └─→ Confirmation dialog appears (inline modal — same backdrop pattern as Add)
        Dialog shows:
          "Delete [Name]?"
          "Their direct reports will be reassigned to [Parent Name]."
          [Cancel]  [Delete]
        ↓ (Cancel)
      Modal closes, no change
        ↓ (Delete)
      Node removed from tree
      All direct children promoted one level up (reassigned to deleted node's parent)
      If deleted node IS the root (no parent) → deletion blocked (see below)
```

### Root Node Deletion — Blocked State

The CEO (root node) cannot be deleted. If the card has `parentId: null`:
- The delete button `[🗑]` is hidden entirely on the root card
- No need for an error — just remove the button from the root

### Delete Button — Card Placement

```
┌─────────────────────────────────────┐
│▐ ← 4px dept accent bar              │
│   Employee Name (bold, 14px)         │
│   Job Title (regular, 12px, muted)   │
│                    [🗑]  [+]  [▼/▶]  │
└─────────────────────────────────────┘
```

- Delete button sits leftmost in the action row, before `[+]` and the toggle
- Icon: `🗑` (trash can) or Unicode `✕` — whichever renders crisply at 14px

```css
/* Delete button */
.org-card__btn-delete {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 1.5px solid var(--color-card-border);
  background: var(--color-card-bg);
  color: var(--color-text-muted);
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 120ms ease, color 120ms ease, border-color 120ms ease;
}
.org-card__btn-delete:hover {
  background: #FFEBEE;
  border-color: #EF9A9A;
  color: var(--color-error);   /* #C62828 — destructive red on hover only */
}
```

**Important:** Delete button is red-on-hover only — resting state is muted grey. This prevents visual alarm for every card in a large org.

### Confirmation Modal Spec

```
┌────────────────────────────────────────────┐
│  Delete Employee                      [✕]  │
│  ─────────────────────────────────────     │
│  Are you sure you want to remove            │
│  Wei Zhang from the org chart?             │
│                                            │
│  Their 2 direct report(s) will be          │
│  reassigned to James Park.                 │
│                                            │
│                  [Cancel]  [Delete]        │
└────────────────────────────────────────────┘
```

- **Title:** "Delete Employee"
- **Body copy (leaf node — no children):** `"Are you sure you want to remove [Name] from the org chart?"`
- **Body copy (node with children):** `"Are you sure you want to remove [Name] from the org chart? Their [N] direct report(s) will be reassigned to [ParentName]."`
- **[Delete] button:** Destructive red — `background: #C62828`, white text. Hover: `#B71C1C`.
- **[Cancel] button:** Same secondary style as Add modal cancel.
- **Modal width:** Same as Add modal — 420px, `max-width: calc(100vw - 32px)`.
- **Animation:** Same enter/exit as Add modal (`scale(0.95)` → `scale(1)`, `180ms ease-out`).
- **Backdrop click:** Same as Cancel.

```css
/* Destructive confirm button */
.btn-destructive {
  height: 38px;
  padding: 0 20px;
  border: none;
  border-radius: 6px;
  background: #C62828;
  color: #FFFFFF;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Segoe UI', system-ui, sans-serif;
  cursor: pointer;
  transition: background 120ms ease;
}
.btn-destructive:hover {
  background: #B71C1C;
}
```

### Component Spec — Delete Button

| Component | States | Behavior |
|---|---|---|
| **Delete Button** `[🗑]` | default (muted), hover (red tint), hidden (root node) | Click → opens delete confirmation modal. Does NOT trigger card selection. Hidden on root node (`parentId: null`). Click stopPropagation to prevent card select. |
| **Delete Confirm Modal** | open, closed | [Delete] → removes node, reassigns children to grandparent, re-renders tree. [Cancel] / [✕] / backdrop click → closes with no change. |

---

## Open Questions

- [x] **Department field in Add form:** ~~Confirm with PO~~ — **Resolved: No dropdown. New node inherits parent's department automatically.**
- [x] **Node deletion:** ~~Confirm before SR1 implements~~ — **Resolved: In scope. Delete with subtree reassignment to parent. Spec above.**

---

*Design spec authored by UX Engineer. Implementation deliverable: `/workspace/org_chart_app/index.html`. Reference: Microsoft org chart visual style — corporate blue, clean white cards, professional shadows.*
