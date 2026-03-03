# ADR-002: SVG Overlay for Tree Connectors

**Status:** Accepted  
**Date:** 2025  
**Thread:** ac28835e-1ebc-4124-b872-15bdd4cead51

## Context
Right-angle elbow connectors must be drawn between parent and child cards at arbitrary horizontal distances. Three options evaluated:

| Option | Mechanism | Right-angle elbows | Dynamic width |
|---|---|---|---|
| CSS pseudo-elements | `::before`/`::after` on cards | ❌ Vertical stubs only | ❌ |
| SVG overlay | `<path>` elements, absolute positioned | ✅ | ✅ |
| Canvas | `ctx.lineTo()` | ✅ | ✅ |

## Decision
**SVG overlay positioned `absolute` inside `#tree-wrapper`.**

After each render, `drawConnectors()` walks all visible parent-child pairs, reads card positions via `getBoundingClientRect()`, converts to wrapper-relative coordinates, and emits `<path>` elements with right-angle elbows (vertical → horizontal → vertical).

## Consequences
- **Benefit:** Pixel-accurate connectors at any tree width/depth.
- **Benefit:** SVG is inside the same CSS-scaled wrapper as the cards, so zoom does NOT require connector redraw.
- **Cost:** Must redraw after every render and on window resize (debounced).
- **Cost:** `getBoundingClientRect()` forces a layout — acceptable at <200 nodes.
