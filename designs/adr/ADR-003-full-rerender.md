# ADR-003: Full Re-render on Every State Change

**Status:** Accepted  
**Date:** 2025  
**Thread:** ac28835e-1ebc-4124-b872-15bdd4cead51

## Context
State changes (collapse/expand, add member, search) require the tree DOM to update. Options:
- (A) Patch the DOM in-place (find changed nodes, update their subtrees)
- (B) Clear `innerHTML` and rebuild the entire tree from data + state

## Decision
**Full re-render (Option B).** `renderTree()` clears `#tree-wrapper` and rebuilds from `ORG_DATA + state`.

## Consequences
- **Benefit:** Zero stale-state bugs. The DOM is always a pure function of the data + state.
- **Benefit:** Simpler code — no diffing logic, no partial-update bookkeeping.
- **Benefit:** Per-node event listeners cannot go stale — a single delegated listener on the stable container handles all events.
- **Trade-off:** Full re-render on every keystroke during search. Acceptable for <200 nodes (<5ms). Debounce at >150 nodes if needed.
- **Trade-off:** Bidirectional collapse animation requires toggling a CSS class rather than destroying/creating DOM — addressed by the class-toggle approach in the expand/collapse section.
