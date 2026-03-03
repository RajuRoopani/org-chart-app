# ADR-004: `<div>` Modal Overlay vs Native `<dialog>`

**Status:** Accepted  
**Date:** 2025  
**Thread:** ac28835e-1ebc-4124-b872-15bdd4cead51

## Context
The "Add Member" form needs a modal overlay. Two options:
- Native `<dialog>` element with `showModal()` / `::backdrop`
- A `<div id="modal-overlay">` with `position: fixed; inset: 0`

## Decision
**`<div>` overlay.** 

Safari's handling of `<dialog>` backdrop styling and `showModal()` has had inconsistencies. A hand-rolled overlay is ~20 additional lines of JS but is fully predictable across all target browsers.

## Consequences
- **Benefit:** Full control over backdrop, animation, and focus trap.
- **Cost:** Must implement Escape-key handler (`keydown` → `hideModal()`) and focus trap (cycle Tab within modal) manually.
- **Note:** Re-evaluate if browser support for `<dialog>` stabilizes further — it is the right long-term answer.
