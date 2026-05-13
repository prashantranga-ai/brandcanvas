# BrandCanvas — Product Requirements Document

**Prashant Rangarajan** · May 2026

A web app that helps small businesses generate brand-consistent campaign images from a logo, up to 5 reference images, and a text prompt. Designed to give a SMB owner two usable on-brand candidates in under a minute, with controls to iterate.

---

## 1. The problem worth solving

Small businesses generate marketing creative constantly — product shots, lifestyle photos, social posts, ad variations — and the dominant constraint is **brand consistency**, not volume. A SMB owner can produce 50 images with any off-the-shelf model in an hour. They can produce 5 *on-brand* images in the same hour only after extensive prompt engineering, manual filtering, and rework.

This is an AI-suitability problem of the **translation** type: the human is the bottleneck between a brand's visual identity (logo, prior assets, aesthetic conventions) and the next image that needs to fit inside it. Off-the-shelf generation models do not natively understand what "on-brand" means for a specific business. They pattern-match on stylistic surface features.

The opportunity statement:

> *For small business owners producing marketing creative, who lose hours rewriting prompts and filtering generations to match their brand, BrandCanvas uses reference-conditioned image generation to produce two on-brand candidates from a simple description — turning brand consistency from a manual filtering task into a one-step generation.*

This prototype is the consumer entry point of a larger product topology. Pomelli (Google Labs) represents the down-market endpoint — auto-discovering brand DNA from a URL for users with no curated assets. Hightouch's Content Assembly represents the up-market endpoint — structured brand context plus measurable fidelity for enterprise marketing teams. BrandCanvas sits between them.

---

## 2. Scope decisions

The product is structured as a three-stage flow that separates one-time brand setup from repeated image generation.

**Stage 1 — Welcome.** A three-card orientation screen explains the flow: set up the brand, describe the image, get on-brand creatives. Single CTA into setup.

**Stage 2 — Brand DNA setup.** The user provides a brand name, uploads a logo, and uploads up to 5 reference images that populate the brand's asset library. One-time configuration. Commit CTA into the generation screen.

**Stage 3 — Generate.** A prompt input plus a reference picker tray that opens when the user wants to include specific brand assets in the generation. The system produces 2 candidates per request via Gemini Flash Image (nano banana 2). A regenerate action and an expandable "constructed prompt" view round out the screen.

**In scope:**

- Three-stage flow as described above
- Logo + up to 5 reference image uploads, persisted across the session
- Reference picker tray that surfaces uploaded assets at generation time
- Single text prompt input
- 2 image candidates per generation, regenerate action
- Expandable view showing the constructed prompt sent to the model
- One sample F&B brand visible on the welcome screen as a non-interactive placeholder, signaling the curated-brand pattern as a deferred direction

**Out of scope (deliberate):**

| Deferred | Why |
|---|---|
| Color palette and font extraction in brand setup | References carry the color and style signal more reliably than user-provided hex values. Adding pickers that don't materially affect output is decoration. Moved to the up-market next step as part of structured brand context. |
| URL-based brand inference (Pomelli direction) | Inferring brand DNA from a scraped website is a separate model judgment problem. Documented as the down-market next step. |
| Campaign/idea generation | Adjacent product surface, not what's being asked. |
| Multiple aspect ratios | Defaults to square for v1 to keep the generation surface focused. |
| Auth, payments, persistence beyond session | Brief excludes. |
| Brand-fidelity scoring | Requires a separate model or embedding pipeline. Documented as the up-market next step. |

**The scoping principle:** Every feature in this prototype either (a) is required by the user flow, or (b) gives the user meaningful control over the output. Nothing else earned its place.

---

## 3. Designing for a probabilistic system

Image generation is fundamentally probabilistic. The same brand context plus the same prompt will produce different outputs each time, and the model's "respect" for the brand varies by prompt type. Users coming from deterministic software (Canva, Figma, Photoshop) expect predictable outcomes — a brand-consistent generation tool that quietly produces different results every time creates more friction than it removes.

Four design moves address this directly:

**(a) Brand setup is separated from generation.** Asking the user to define the brand once (Stage 2) and then generate many times (Stage 3) does two things. It signals that the brand is a *durable artifact* the system understands, not a per-prompt accessory. And it amortizes the setup cost across many generations, so the friction sits where it belongs — at the beginning, not on every request.

**(b) Two outputs, not one.** Generating two candidates per request gives the user a real choice and acknowledges the inherent variance in generative models. The user picks the better one or regenerates. Inconsistency is a fundamental constraint of probabilistic systems — surfacing it through choice is more useful than hiding it behind a single "Generate" button that produces silent randomness.

**(c) The reference picker is explicit.** When the user generates, they can choose which brand assets to include as references through a tray that opens from the prompt area. This gives them control over how the model is conditioned — a product shot for product-focused prompts, a lifestyle image for lifestyle prompts. Surfacing this control teaches the user how the system works and makes the brand asset library feel like a usable tool, not a hidden setting.

**(d) The constructed prompt is visible.** An expandable section in the UI shows exactly what got sent to the model — the system prompt, the user's description, the references being passed. For users who want more control, this is the first place to look when an output isn't landing. It also creates a learning surface: users start to understand which descriptions yield better outputs, which makes them more effective over time.

---

## 4. The system prompt strategy

The master prompt is structured around six load-bearing components, in order of priority:

| # | Section | What it does | Why it's there |
|---|---|---|---|
| 1 | **Identity** | "You generate brand-consistent campaign images by treating uploaded references as the brand's approved visual corpus." | Anchors the model's job — not "make a good image," but "extend this specific brand." |
| 2 | **Reference-fidelity rule** | The reference images define the brand's color palette, photographic style, subject treatment, and tone. Generated images must remain stylistically consistent with them. | The single most important constraint. Without it, the model pattern-matches on prompt content and ignores references. |
| 3 | **Logo handling rule** | If the prompt implies the logo should appear, place it discreetly without distorting it. If the prompt does not imply it, omit it. | Logo placement is a known nano banana 2 failure mode — fabrication, distortion, or over-inclusion. |
| 4 | **Subject novelty rule** | When the prompt requests a subject not present in the references, preserve the brand's visual treatment (lighting, color palette, framing conventions) on the new subject. | The hardest case — extending brand to subjects the model has never seen in this brand's context. |
| 5 | **Output format** | Generate two distinct variations. Vary composition or framing across the two, not just minor pixel differences. | Forces meaningful diversity in the two outputs so the user has a real choice. |
| 6 | **Refusal behavior** | If the prompt is incompatible with the brand context (e.g., harmful content, contradictory style request), generate a best-effort interpretation and flag the conflict. | Designs for failure rather than producing silently wrong output. |

The prompt was iterated three times during development. v1 (a generic "create an on-brand image" instruction) failed on subject novelty cases and produced inconsistent logo placement. v2 added explicit reference-fidelity and logo rules and improved both. v3 added the subject novelty rule after testing revealed the model would default to generic photography for any subject not appearing in references. Each iteration was driven by a specific failure observed in the eval set.

---

## 5. Evaluation approach

The eval set is designed as a **reusable test harness**, not a one-time check. It covers five prompt categories that stress different aspects of brand fidelity:

- **Reference-aligned** — the most common SMB use case
- **Reference-adjacent** — extending the brand to related subjects
- **Reference-conflicting** — preserving brand fidelity under tension
- **Logo fidelity** — placement and text rendering
- **Subject novelty** — the model's weakest mode, where brand evaporates without structured context

Each prompt is run multiple times to account for the model's inherent variance. Brand context is held constant across runs (same logo, same references, same brand name) so only the user prompt varies.

The set is built to grow: every prompt that fails in real production becomes a permanent test case, preventing regressions and surfacing systematic failure modes over time. The full eval set, prompts, observations, and implications for the product roadmap are documented in a separate `BrandCanvas-Evals.md`.

The eval results point at one large investment for v2: **brand fidelity needs to become measurable, not just qualitative.** Today's eval is human-reviewed; the scaled version is automated via embedding similarity between generated outputs and the brand's asset library, with low-fidelity generations rejected before they reach the user. Users forgive software bugs; they rarely forgive bad creative output. That's what makes brand-fidelity scoring the right next investment up-market.

---

## 6. What I'd build next

This prototype is the consumer entry point. The natural product expansion runs in two directions, each solving different model judgment problems.

**Down-market — URL-based brand inference (the Pomelli direction):**

Instead of asking users to upload references, scrape a URL and infer brand DNA — extract color palette, font conventions, photographic style, and a curated reference set automatically. The hard model judgment problem here is **inference quality from messy web data**: most SMB websites have inconsistent imagery, stock photos mixed with real product shots, and dated assets. Solving this would mean a near-zero-friction onboarding for SMBs and is the most obvious next step. The brand DNA structure already in this prototype (name + logo + asset library) becomes the destination object the inference layer populates. Timeline estimate: 2-3 weeks for a credible prototype.

**Up-market — measurable brand fidelity (the Hightouch direction):**

Extend the brand DNA object beyond logo and references — add explicit color palette, font conventions, approved subject types, and brand voice as structured fields. Then add a brand-fidelity score computed via embedding similarity between generated outputs and the brand's asset library, with low-fidelity generations rejected before they reach the user. The hard model judgment problem here is **making brand fidelity measurable**: today it's a vibe; for enterprise teams it has to be a number. Solving this is what makes brand-consistent generation viable at the volume marketing teams need. Timeline estimate: 6-8 weeks for a credible prototype.

The two directions clarify the brand-fidelity question itself. Down-market, the problem is *getting enough context to be useful*. Up-market, the problem is *making the context measurable*. A consumer-grade product probably picks one. An ambitious product solves both, with structured brand context (up-market) serving as the destination for inferred DNA (down-market).

---

## 7. What I used AI tools for, and where I overrode them

Claude Code was used to scaffold the Streamlit app, wire the nano banana 2 SDK, and handle the upload/state management. Routine work; minimal overrides.

Three places I explicitly overrode the AI tools:

1. **The system prompt structure.** Initial Claude Code suggestions produced a long, generic "be helpful and creative" prompt. Replaced it with the six-component structure above, with each section anchored to a specific observed failure mode.

2. **The constructed-prompt visibility feature.** Claude Code defaulted to hiding the prompt construction inside a function. Exposed it in the UI deliberately so the model's behavior is legible to the user and to the evaluator.

3. **The evaluation taxonomy.** AI tools defaulted to running a few happy-path tests. Replaced with the five-category failure-mode taxonomy and ran 10 cases offline. The taxonomy itself was the harder PM judgment than any of the prompt engineering.

Everything else — UI layout, dark theme, Streamlit components — was vibe-coded with light editing.
