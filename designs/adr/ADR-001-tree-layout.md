# ADR-001: CSS Flexbox Layout for Org Tree

**Status:** Accepted  
**Date:** 2025  
**Thread:** ac28835e-1ebc-4124-b872-15bdd4cead51

## Context
A top-down org chart tree needs child cards distributed horizontally at each level without overlapping. Two approaches were evaluated:
- (A) Compute x/y positions recursively in JavaScript, render cards with `position: absolute`
- (B) Use CSS `flexbox` to distribute children automatically

## Decision
**CSS Flexbox (Option B).**

Each tree node renders as a vertical flex column (card → connector stub → children row). Children at each level sit in a horizontal flex row with `justify-content: center` and `gap`.

## Consequences
- **Benefit:** No position math. The browser guarantees children do not overlap.
- **Benefit:** Adding new nodes at runtime requires no coordinate recalculation.
- **Trade-off:** We lose pixel-perfect control over card positions. Not required for this use case.
- **Trade-off:** Very wide trees may overflow the viewport — mitigated by zoom-out + horizontal scroll.
