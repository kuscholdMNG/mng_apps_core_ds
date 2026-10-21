# Architecture — how Core, iOS and Android fit together

Goal: put as much as possible in **Core**, and make it obvious where to go for anything platform-specific.

```
MNG Apps Core Design System      tokens · semantic icon list · component specs · patterns
   ├── MNG iOS Design System       native iOS builds + iOS-only items, all aliasing Core
   └── MNG Android Design System   native Android builds + Android-only items, all aliasing Core
```

## 1. One registry

`data/registry.json` lists every token, icon and component once:

```json
{ "id": "nav-bar", "type": "component", "owner": "core+variant",
  "core":    { "spec": "specs/nav-bar.md", "figma": "<node link>" },
  "ios":     { "native": "UINavigationBar", "figma": "<node link>" },
  "android": { "native": "Material top app bar", "figma": "<node link>" } }
```

Ownership chips in Figma, spec pages, repo indexes and any published style guide are generated from it, so they can't drift. Nobody types an owner label by hand.

## 2. Ownership: the Core-first test

| Question | Yes → |
|----------|-------|
| Do both apps do this job? | Core |
| Same parts and states? | Core spec (each platform may render natively) |
| Only values differ? | Core variable with a per-platform value (**Core + variant**) |
| OS requires it, or the feature exists on one app only? | **iOS only** / **Android only** |

Owner values: `core` · `core+variant` · `ios` · `android`. Chip colors are in CLAUDE.md.

## 3. Figma

**Variables**

| Collection | File | Holds |
|------------|------|-------|
| Primitives | Core | Raw colors (near-identical hexes merged), type scale, spacing, radius |
| Brand | Core | The 7 brand roles; one mode per palette (markets map to a palette) |
| System | Core | Colors identical in every market (≈62 iOS / 71 Android) |
| Platform overrides | iOS / Android | Aliases Core by default; stores only exceptions (e.g. Android `statusbar`, iOS `header`) |

Platform files never copy a Core value; they alias it.

**Components**: Core holds the spec (anatomy, states, tokens, content rules). iOS and Android hold the native build using Core tokens. Component names are identical across iOS and Android (`Nav bar`, `Button/Primary`, `Icon/Search`) so a mockup can move between platforms with Swap Library.

**Icons**: Core holds the semantic list and custom vectors (brands, gaps). iOS holds SF Symbols glyphs (mockup licence only), Android holds Material Symbols, named to match.

## 4. Wayfinding

- **Same page order in all three files**: Cover → Foundations (Color, Type, Spacing, Icons) → Components → Patterns. A platform page with nothing of its own says "Nothing platform-specific. Use Core → link".
- **Owner chip** on every documentation frame. Core items with a variant carry a *Platform notes* panel: "iOS → link · Android → link".
- Every platform page opens with **"Built on Core → link"**.
- Every Figma component has a **description and documentation link** to `specs/<id>.md`.

## 5. Repos and Claude

| Repo | Holds |
|------|-------|
| `mng_apps_core_ds` | Instructions, registry, source data, comparisons, `specs/<id>.md` for every Core item (with iOS / Android sections when needed) |
| `mng_apps_ios_ds` / `mng_apps_android_ds` | `specs/<id>.md` for platform-only items, plus a generated index linking back to Core |

Optional: a published Core style guide in Claude, generated from the registry, beside the existing iOS and Android guides.

## 6. Rollout

1. Approve the `PLAT-` decisions (colors, icons).
2. Clean up brand palettes; build Primitives / Brand / System variables.
3. Seed the registry from icons and color roles.
4. Pilot one component end-to-end in all three files and repos (nav bar or primary button), then fix the template.
5. Type, spacing, layout; then the rest of the components.
6. Governance: change Core first; platform changes cite the Core item; publish libraries with a changelog; log every session in PROGRESS.md.
