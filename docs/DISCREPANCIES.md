# Discrepancies — iOS vs Android things that should match

Everything that differs between the two apps but **should be the same**. Each row says what the right value is, how we know, and which app needs the fix, so the Apps team can work through it later. Differences that are intentional platform conventions (SF Symbols vs Material, 44 pt vs 48 dp) are not listed here; they live in the registry as "Core + variant".

- Sources: iOS TroncKit @ `e30ad2585` · Android android-tribpub @ `1cfb069a6` · migration sheet "Tribpub-MNG App Migrations" (tab Production, Primary / Secondary color)
- Data: `data/brand-color-resolution.json` (`scripts/resolve_brand_colors.py`), `data/color-platform-comparison.json`
- Figma (Core file): Color · Market Palettes → **06 · Brand color source of truth**

Status: `OPEN` (cause unknown, ask Apps team) · `KNOWN` (right value known, fix not scheduled) · `TICKETED` · `FIXED`
Fix on: `iOS` · `Android` · `both` · `?`

## How we decide the right value

1. **Migration sheet wins.** If the sheet's Primary / Secondary color matches either app, that is the source of truth.
2. **iOS 2-decimal drift.** TroncKit stores each color channel as a 2-decimal fraction, so `0x22` (0.133) becomes 0.13 and comes back as `0x21`. When iOS = Android after that rounding, Android holds the authored value. This explains 32 of the 34 pairs the sheet could check.
3. Anything else is `OPEN` until the Apps team answers.

## Brand colors

| ID | What differs | Should be | Fix on | Evidence | Status |
|----|--------------|-----------|--------|----------|--------|
| DSC-01 | iOS brand color off by 1 in a channel (2-decimal drift) in 36 markets: SGVT, SIT, TB, TBCP, TCCDR, TCHW, TCV, TDC, TDPS, TEBT, TETS, TFMT, TGT, TJA, TLADN, TLS, TLTC, TMCH, TMD, TMJ, TMS, TNH, TOD, TPM, TR, TRH, TROT, TRR, TSCS, TSEB, TSS, TTH, TTT, TVR, TVTH, TWDD | Android / sheet hex (e.g. `#ab4022`, not `#ab4021`) | iOS | Sheet matches Android in all sheet-covered markets; the rest follow the drift rule. TWDD is 1 unit off without fitting the rule; sheet confirms Android. Invisible on screen. Fix: store hex strings instead of 2-decimal floats. | KNOWN |
| DSC-02 | **TLR** Loveland: iOS uses red `#ab4021` | `#4e5dca` | iOS | Sheet = Android. iOS value is TLS Lowell Sun's red (the next market alphabetically). | KNOWN |
| DSC-03 | **TUDJ** Ukiah: iOS uses `#408fcc` | `#32408f` | iOS | Sheet = Android. iOS value is TVR Vacaville's blue (the next market alphabetically). | KNOWN |
| DSC-04 | **TBE** Broomfield: iOS uses `#0070b8` | `#4351af` | iOS | Sheet = Android. | KNOWN |
| DSC-05 | **TEPTG** Estes Park: Android uses green `#3e8e75`; iOS `#33408f` | `#32408f` | both | Sheet `#32408f`; iOS is that value with 2-decimal drift. | KNOWN |
| DSC-06 | **TSAR** Saratogian: iOS bar `#ffffff`, button and selected tab template blue `#004e87` | Bar `#f5f5f5`, secondary `#00919e` | iOS | Sheet = Android (sheet note: secondary matches the logo). Button color (`action`) still to confirm. | KNOWN |
| DSC-07 | **MC** Morning Call: Android button `#4fa8d1` | `#539cc4` | Android | Sheet = iOS. Android value is HC Hartford's blue. Selected-tab color still OPEN. | KNOWN |
| DSC-08 | **SIT** Sonoma Index-Tribune: selected tab Android `#149ce5`, iOS `#ffeb00` | `#ffea00` | both | Sheet secondary `#ffea00`; iOS is it with drift. | KNOWN |
| DSC-09 | Template blue on iOS: TBAN, TBH, TCE, TDB, TDF, TLBPT, TMI, TRDF, TSPPP, TT show `#004e87` (and black / `#9dd1f5` tabs) where Android shows each market's own color | ? (likely Android) | ? | Sheet has no color for these markets. | OPEN |
| DSC-10 | SCNG group PSN, TPE, TSBS, TWDN: iOS red `#b01f36` bar with orange `#ff6900` button and tab; Android `#a6371e` bar and button, black tab | ? | ? | Sheet has no color for these markets. SGVT has the same orange button on iOS. | OPEN |
| DSC-11 | Smaller open differences: TBHS bar `#b01f36` vs `#c00030`; TDCD `#5b9bc8` vs `#4891b3`; OCR `#b04f0f` vs `#ac4e0f`; TSV bar black vs `#557fba`; TOP button and tab `#004e87` vs `#5ab1c3`; TEBT button `#6bd1e6` vs `#557fba`; TDP `#f7a430` vs `#daa520`; TDLW and TOP bar off by 1–2 units (no drift pattern) | ? | ? | Not in the sheet, or the sheet color matches neither app. | OPEN |
| DSC-12 | Selected tab only: DP `#005f7e` vs `#4fa8d1`; TIVDB `#000000` vs `#807c7c`; TMN `#000000` vs `#6bd1e6`; OS `#15919d` vs `#00919e`; MC `#539cc4` vs `#4fa8d1` | ? | ? | No secondary color in the sheet. | OPEN |
| DSC-13 | **TPD** Press Democrat: sheet says `#9e0b0f` / `#ffea00`; both apps use black bar and gray `#999999` | ? | ? | Sheet row is marked WIP; only the iOS section header uses `#9e0b0f`. | OPEN |
| DSC-14 | Legacy markets OS, SS, NYDN: the sheet's Primary (`#004e87`, `#000000`, `#ec2127`) appears in neither app | ? | ? | Sheet column may mean something else for the legacy template. | OPEN |
| DSC-15 | Breaking-news red: iOS `#ff0000` (71) / `#d80000` (6), Android `#cf000e` | `#cf000e` (proposed) | iOS | PLAT-03. iOS `#ff0000` fails 4.5:1 with white. | KNOWN (pending PLAT-03) |
| DSC-16 | BS tab bar: iOS white with black unselected icons, Android black with white | ? | ? | BS is decommissioned Nov 1 2026; may not need a fix. | OPEN |
| DSC-17 | Bar text: TIVDB iOS `#cccccc` vs `#ffffff`; OS iOS `#333333` vs `#000000`; TDP unselected tab iOS `#999999` vs `#ffffff` | ? | ? | | OPEN |

## Components and controls

| ID | What differs | Should be | Fix on | Evidence | Status |
|----|--------------|-----------|--------|----------|--------|
| DSC-20 | Primary button: iOS radius 4 (legacy 5 + 1 pt border), Open Sans Bold 14; Android square corners, system font, 60 dp tall | One Core spec (to design) | both | Same component on both paywalls. | OPEN |
| DSC-21 | Subscription option: iOS radius 8, Open Sans Bold 16; Android square, system 16sp | One Core spec | both | | OPEN |
| DSC-22 | Article text size: iOS 6 steps (slider), Android 4 steps (list) | Same number of steps | ? | The control can differ per platform; the scale should not. | OPEN |
| DSC-23 | Your News checkbox: iOS uses 8 per-market image sets; Android tints one control | One tinted checkbox | iOS | | KNOWN |
| DSC-24 | Continue button: iOS uses pre-colored PNGs (10 copies); Android a tinted button with radius 9 | Core primary button | iOS | | KNOWN |

## Icons

| ID | What differs | Should be | Fix on | Evidence | Status |
|----|--------------|-----------|--------|----------|--------|
| DSC-30 | Saved in special sections: Android uses a star, iOS a bookmark | Bookmark (Core Saved) | Android | PLAT-09 | KNOWN |
| DSC-31 | Text size: iOS smaller/larger glyphs, Android one glyph | One Core glyph + iOS variant | — | PLAT-08 | KNOWN |

## Log

- **2026-10-21** — Started. Brand colors checked against the migration sheet: 47 of 77 markets fully resolved, 30 have at least one open role.
