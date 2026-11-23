# Design notes

## Why this exists
Three production attempts at one 5s shot with a reference-driven video
generator failed the same way: identity drift over time, a mirrored prop,
and a different-looking character after an edit seam. The generator was
not misused — per-frame resynthesis is its architecture. The fix is to
remove per-frame synthesis from the identity path entirely.

## Stages
1. build_model: multi-view image-to-3D (TRELLIS/Hunyuan3D adapters),
   views supplied from the character sheet; seed + params logged.
2. clean: mesh cleanup, retopology target ~30–60k tris for the body,
   props (briefcase, badge, backpack) kept as separate rigid meshes so
   they can never morph or swap clasps mid-shot.
3. texture: project canonical art onto visible faces; inferred regions
   painted from the sheet's palette; texture locked by hash.
4. rig: biped skeleton fitted to the model's proportions; facial
   controls = eyelids, jaw, brows (the expressions in the sheet).
5. motion: a small reusable library — walk cycle, idle, nod, fist pump,
   speaking jaw loop; shots are assembled from library clips.
6. render: Blender Eevee, locked scene kits (sets are models too, so
   backgrounds cannot drift either).
7. qc: turntable render + angle diffs vs canonical art; face-ratio and
   prop-side checks are pass/fail gates, same discipline as
   lockframe-generator's BENCHMARK.md.

## Efficiency contract
- One-time cost: model build + cleanup + rig (hours, once per character).
- Per shot after that: pose/motion selection + render (minutes).
- No per-shot generation lottery, no 4-round regeneration budget.
