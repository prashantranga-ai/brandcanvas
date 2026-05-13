# BrandCanvas — Evaluation Set

A reusable test harness for verifying brand-fidelity behavior across the failure modes that matter most in production. Each prompt category targets a specific aspect of model judgment; together, the set provides a structured view of where Nano Banana 2 holds and where it breaks for this product.

The set is designed to grow: every prompt that fails in real use becomes a permanent test case, preventing regressions and surfacing systematic failure modes over time.

---

## Brand context (held constant across all evals)

- **Brand name:** Vanilla Bite Bakery
- **Logo:** Stylized "VB" mark with full "Vanilla Bite Bakery" wordmark
- **Reference images:**
  - Cookies (product category)
  - Floral wedding cake (product category, premium SKU)
  - Bakery interior with owner-figure holding a tray of breads (style + lifestyle)
- **Model:** `gemini-2.5-flash-image` (GA Nano Banana 2)
- **Output:** 1024×1024 square, 2 candidates per prompt
- **System prompt:** 5-section structure (identity, reference fidelity, logo handling, subject novelty, edge cases)

---

## The 5 categories

| Category | What it tests | Why it matters for the product |
|---|---|---|
| **Reference-aligned** | Prompts close to what references show | The most common SMB use case — generating variations of what the brand already shows |
| **Reference-adjacent** | Prompts the references gesture at but don't show directly | The next-most-common case — extending the brand to related subjects |
| **Reference-conflicting** | Prompts stylistically incompatible with references | Tests whether the model preserves brand fidelity under tension |
| **Logo fidelity** | Logo placement and text rendering | Highest visible-failure mode; brand recognition depends on this |
| **Subject novelty** | Subjects with no overlap with references | The model's weakest mode; reveals the floor of brand preservation |

---

## Eval prompts and observations

### Category 1 — Reference-aligned

#### Prompt 1A
**Prompt:** "Photograph of a coffee cup on a wooden table, soft natural lighting"
**References selected:** None (logo only)
**Expected behavior:** Clean output. Logo appears naturally on the cup. Brand style not strongly tested since no references are passed.
**Findings:** Logo placement worked very well — appeared naturally on the cup. Output was clean and product-photography-grade.
**Takeaway:** Strong baseline. The logo-always-include rule from the system prompt is working as designed for simple compositions. This is the production-ready floor: any prompt that simplifies to "product on surface" should hit this quality bar.

#### Prompt 1B
**Prompt:** "Photograph of a coffee cup on a wooden table, soft natural lighting"
**References selected:** Cookie reference
**Expected behavior:** Cookies should appear prominently as the hero product alongside the coffee cup. Brand style (warm, soft) should match the reference.
**Findings:** Cookies appeared in the output but were not prominent enough. The coffee cup remained the primary subject; cookies were relegated to a secondary element. The user intent when uploading a product-category reference is that the product becomes the hero — not a background detail.
**Takeaway:** Confirms a real production gap — **product prominence**. When a product-category reference is passed, the system currently includes the product but doesn't elevate it. This is a system-prompt tuning problem with a clear path: stronger language in Section 2 of the system prompt explicitly elevating referenced products to hero status when they appear in the prompt context.

---

### Category 2 — Logo fidelity

#### Prompt 2A
**Prompt:** "Photograph of a new branch opening in downtown Toronto"
**References selected:** None
**Expected behavior:** Storefront scene with brand signage. The logo-always rule should place the logo prominently on signage. Text rendering for "Vanilla Bite Bakery" should be legible.
**Findings:** Direction was solid but the result felt generic. The logo was clear and visible on signage, but the overall scene didn't reinforce brand identity strongly. The branding read more as "a bakery storefront" than "Vanilla Bite Bakery specifically."
**Takeaway:** Logo placement works mechanically; brand identity expression at scene level is the gap. Without product references, the model has no signal beyond the logo to express "this specific brand." Suggests **passing at least one product or lifestyle reference even for environmental prompts**, or building an "auto-suggest references based on prompt type" feature.

#### Prompt 2B
**Prompt:** "Photograph of a new branch opening in downtown Toronto. Include the hero product of my store."
**References selected:** Floral wedding cake
**Expected behavior:** Storefront + hero product visibility. Tests two things at once: logo placement on signage AND product prominence when explicitly invoked. Should be stronger on product prominence than 1B since "hero product" is explicit in the prompt.
**Findings:** Output generally landed well — the downtown "grand opening" atmosphere came through, the logo handling worked. But product placement felt slightly off — the cake came across as part of a wall poster rather than naturally displayed within the bakery environment. Slightly staged or plastic-feeling.
**Takeaway:** Explicit "hero product" language helped — the cake was unmistakably part of the scene, not hidden as in 1B. But **product integration into environments** is a separate gap from prominence. The model places products into scenes; it doesn't always integrate them convincingly. A future improvement could be scene-aware product placement, possibly via a second-pass compositing step.

---

### Category 3 — Reference-adjacent

#### Prompt 3A
**Prompt:** "Photograph of the product in a wedding setting"
**References selected:** Floral wedding cake reference
**Expected behavior:** Wedding cake should be the hero, styled to match the reference (floral motifs, color palette). Wedding setting provides context without overshadowing the product.
**Findings:** Cake style matched the reference well — floral motifs and color palette carried through. The wedding setting felt coherent and the logo was placed naturally. The product could have been more strongly highlighted — same prominence pattern as 1B.
**Takeaway:** Reference-adjacent prompts work well for **style matching**. The hero-product gap appears again — even when the reference is the primary subject ("the product in a wedding setting"), the model treats it as one element among many rather than the centerpiece. This is the third instance of the prominence pattern; it's clearly the dominant gap.

#### Prompt 3B *(to run)*
**Prompt:** "A morning scene of fresh croissants and a cup of coffee at a bakery"
**References selected:** Cookies, lifestyle interior
**Expected behavior:** Croissants are a new product type not in references but adjacent to the bakery category. The brand style (warm, natural) should apply. Tests whether the bakery brand extends to related pastries.
**Findings:** *[to run]*
**Takeaway:** *[to complete]*

#### Prompt 3C *(to run)*
**Prompt:** "Display window of a small artisan bakery from the outside, warm afternoon light"
**References selected:** Lifestyle interior
**Expected behavior:** Bakery exterior matching the interior aesthetic of the reference. Signage should include the brand logo/name.
**Findings:** *[to run]*
**Takeaway:** *[to complete]*

---

### Category 4 — Reference-conflicting

#### Prompt 4A *(to run)*
**Prompt:** "A futuristic neon-lit photo of cakes in a cyberpunk setting"
**References selected:** Floral wedding cake
**Expected behavior:** Maximum stylistic conflict — artisan bakery vs cyberpunk. Tests the model's resolution behavior at the extreme.
**Findings:** *[to run]*
**Takeaway:** *[to complete]*

---

### Category 5 — Subject novelty

#### Prompt 5A *(to run)*
**Prompt:** "A team meeting in a conference room, professional setting"
**References selected:** Cookies, lifestyle interior
**Expected behavior:** No people in formal settings appear in references. Brand style likely evaporates.
**Findings:** *[to run]*
**Takeaway:** *[to complete]*

#### Prompt 5B *(to run)*
**Prompt:** "Aerial view of a vineyard at sunset"
**References selected:** Cookies, lifestyle interior
**Expected behavior:** Maximally distant subject from a bakery brand. Tests the floor — what's the minimum brand connection the model preserves when the subject is unrelated?
**Findings:** *[to run]*
**Takeaway:** *[to complete]*

---

## Aggregate observations

Based on the four prompts run so far (1A, 1B, 2A, 2B, 3A), three patterns are emerging clearly. The remaining prompts will sharpen these and test the edge categories.

**1. The hero-product gap is the dominant pattern.**

This appeared in three of four substantive tests — 1B (cookies on a coffee table), 2B (cake at a Toronto opening), and 3A (cake in a wedding setting). The pattern is consistent: when a product-category reference is uploaded and the prompt is product-related, the model *includes* the product but does not *elevate* it. Cookies appear behind the coffee cup. The cake reads as a wall poster instead of the scene's centerpiece. Floral cake in the wedding shot is recognizable but not the focal point.

Why this matters: when a small business uploads a product reference, the intent is almost always "this product should be the hero," not "this product is one element among many." The current system prompt treats references as visual signals to incorporate, not as subjects to emphasize. The next obvious system-prompt revision should add explicit language elevating product-category references to hero status when they semantically match the prompt's subject.

**2. Logo placement works mechanically; brand identity expression is uneven.**

Logo handling — does the logo appear, is it the right size, is it not distorted — is solid across the runs. The logo appeared cleanly on the coffee cup (1A), on signage at the Toronto opening (2A and 2B), and integrated naturally into the wedding setting (3A).

What's weaker is **brand identity expression at scene level.** The 2A storefront felt generic — visually correct, but indistinguishable from any artisan bakery. Without a product reference passed alongside, the model has no signal beyond the logo to express "this specific brand." This suggests environmental and lifestyle prompts benefit from always passing at least one reference, and potentially a UX prompt to nudge users toward that.

**3. Explicit prompt language meaningfully helps product prominence — but not perfectly.**

1B versus 2B is a useful A/B. 1B with the cookie reference and no "hero" language: cookies appeared but were secondary. 2B with the cake reference and explicit "include the hero product" language: cake was clearly part of the scene, not background. The "hero product" phrase appears to anchor the model's attention.

But 2B also revealed a different gap: integration quality. The cake felt staged rather than naturally part of the bakery environment. So "hero product" language elevates *prominence* but doesn't necessarily solve *integration*. A future improvement would be scene-aware product placement, possibly via a second-pass compositing approach.

**4. What remains to be tested.**

The current observations are concentrated on reference-aligned, reference-adjacent, and logo fidelity cases. The categories most likely to surface architectural limits — reference-conflicting (4A) and subject novelty (5A, 5B) — are still to run. Subject novelty in particular is expected to be the model's weakest mode and will likely motivate the up-market direction (structured brand context, measurable brand fidelity).

**5. The next system-prompt revision should target one thing.**

Three of the five tests revealed the same gap. That's strong signal. The next system-prompt revision should focus narrowly on Section 2 — adding language that explicitly elevates product-category references to hero status when the prompt's subject matches. A focused revision is testable and measurable against the existing eval set; a broad rewrite risks regressing the behaviors that are already working.

---

## Implications for product roadmap

The observations point at specific, prioritized improvements. The ordering below reflects what the eval data supports:

1. **System-prompt revision: elevate product-category references to hero status.** The single highest-confidence change, supported by three of four substantive observations. A focused revision to Section 2 of the system prompt — adding explicit instruction to make the referenced product the visual centerpiece when the prompt's subject matches — should close the prominence gap. Re-running the existing eval set after the revision will confirm whether it worked without regressing other behaviors.

2. **Explicit reference tagging.** Let users mark each reference as "style" or "product category" during brand setup. Today the model infers from prompt language, which works but is imperfect (see 2A, where no product reference meant brand identity at scene level felt generic). Explicit tagging gives users control and reduces ambiguity. Likely worth a UX experiment to see whether users will actually do the tagging.

3. **Reference-suggestion UX.** For environmental or lifestyle prompts ("a new branch opening"), nudge users to include at least one product or lifestyle reference even when their prompt doesn't explicitly mention products. The 2A result showed that without product references, brand identity expression at scene level is weaker.

4. **Scene-aware product integration.** A separate gap from prominence (revealed by 2B's slightly-staged cake). Could be addressed via a second-pass compositing step or by adding integration-specific language to the system prompt. Lower confidence than items 1-3 and worth testing more.

5. **Logo and text fidelity for branded signage.** Image models struggle with rendering accurate text inside images. This is a known model-architecture limitation that prompt engineering won't fully solve. A non-prompt fix — separate logo compositing pass, or a dedicated text-rendering pipeline for signage — would be the right next investment for logo-critical use cases.

6. **Subject-novelty handling.** Once tested (5A, 5B), this will likely surface the most architectural gap. Closing it requires moving beyond "references as visual hints" to a structured brand model the system can apply to arbitrary new subjects. This is the up-market direction described in the PRD.

---

## How this set evolves

This eval set is a snapshot, not a deliverable. The intent is that it grows from production:

- Every user-reported failure becomes a permanent test case
- Categories may split or merge as patterns become clearer
- System-prompt revisions should be re-run against the full set before deploy to verify no regressions
- The set becomes the gate for moving the product from preview to GA — defined criteria for "good enough to ship"
