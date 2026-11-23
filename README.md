# LockFrame 3D — Character-Locked 3D Pipeline

**Build the character once. Reuse it forever. No per-shot redraws.**

Generative video models re-synthesize every frame, so a character's face,
stripes and props drift — worst in close-ups, at edit seams, and late in a
clip. LockFrame 3D takes the opposite route used by real 3D production:

1. **Model once** — turn the canonical character art (front / side / back
   views) into one textured 3D model with open image-to-3D models
   (TRELLIS / Hunyuan3D class), guided by *all* supplied views, not one.
2. **Project the original art** — the visible-side texture is projected
   from the user's own reference images, so the front of the character is
   the user's pixels, not a reinterpretation.
3. **Rig once** — one skeleton, one set of facial controls, reused by
   every shot and every episode.
4. **Perform by animation, not generation** — walk cycles, gestures and
   lip-sync are keyframed / motion-applied to the locked model. A render
   cannot "become another cat": there is only one cat.
5. **Render fast** — Blender Eevee; a 5-second shot renders in minutes on
   CPU, seconds-to-minutes on GPU. Per-shot cost after setup ≈ zero.

## Honesty box (read before the stars)

- Parts of the character that no reference image shows (e.g. the exact
  back of the head from a single front photo) must be *inferred* by the
  model builder. Supplying front/side/back art — as a character sheet
  does — shrinks inference to a minimum, but inference never reaches
  zero. Anyone promising "pixel-identical from one photo, all angles"
  is selling you a redraw with better marketing.
- AI-built meshes have messy topology. Expect a cleanup + retopology
  pass before rigging, and budget one approval round on the turntable:
  the model is approved **once**, then never re-judged per shot.

## Pipeline

```
views (front/side/back) ──► build_model ──► clean/retopo ──► project_texture
        ──► rig ──► motion library (walk / nod / gestures / mouth)
        ──► scene kit (locked sets) ──► render shot ──► QC vs canonical
```

QC renders a turntable + three canonical angles and diffs them against
the reference art (face width ratio, prop side, stripe layout) before a
human ever sees the model.

## Status

v0.1 — pipeline scaffolding, first character build in progress
(橘大福 / Ju Dafu, from the series 《橘猫打工记》).

MIT License.
