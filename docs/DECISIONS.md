# Decisions

Design-system decisions with the rule, the date, who made it and what changed. Proposed decisions still under discussion are in `docs/PLATFORM-OWNERSHIP.md` (PLAT-) and `docs/IMPROVEMENTS.md`. Fixes the apps need are in `docs/DISCREPANCIES.md`.

| ID | Decision | Date | By |
|---|---|---|---|
| DEC-01 | Brand colors: the migration sheet wins when it matches an app; otherwise Android, because iOS rounds each color channel to 2 decimals | 2026-10-21 | Karl |
| DEC-02 | Brand colors: where the Cluster Audit web color is close to our value (ΔE < 0.05), use the web color. Where it's far, keep our earlier choice. Where neither settles it, the brand stays open | 2026-10-21 | Karl |

## DEC-01 · Migration sheet + iOS drift rule

- **Source:** "Tribpub-MNG App Migrations" → Production → Primary / Secondary color (`data/source/migration-sheet-brand-colors.json`; project reference `references/migration-sheet-brand-colors.md`).
- **Rule:** 1) If the sheet's color matches either app, it is the value. 2) If iOS equals Android after rounding each channel to 2 decimals (`0x22` → 0.13 → `0x21`), Android holds the authored value. 3) Otherwise open.
- **Why:** the sheet matched Android in every near-identical pair it covered; the rounding explains 32 of the 34 pairs it could check.
- **Applied by:** `scripts/resolve_brand_colors.py` → `data/brand-color-resolution.json`. Replaces proposal PLAT-02.

## DEC-02 · Align with Cluster Audit web colors when close

- **Source:** "_Adabel's Cluster Audit - MAIN" → colors → `{{PropertyColor}}` (WordPress / ARC web colors), read once on 2026-10-21 (`data/source/cluster-audit-web-colors.json`). Not a live source; don't re-read it without a new decision.
- **Rule:** applied to each brand's main color (bar, or the button for the legacy Tribune markets whose bar is white/black). The button follows the bar where the app already uses the same color for both.
  - Close (OKLab ΔE < 0.05, same color family, slightly different shade) → use the web color.
  - Far (ΔE ≥ 0.05) → keep the DEC-01 value.
  - Brand still open and web color far from both apps → stays open.
- **Why:** moves the apps toward the shared web theme colors (fewer palettes to manage) without changing any brand to a visibly different color.
- **Applied by:** `scripts/apply_web_alignment.py` (run after `resolve_brand_colors.py`). Each changed role keeps the earlier value under `previous`.

### Changed to the web color (27)

| Code | Brand | Role | Was | Now | ΔE | Was open? |
|---|---|---|---|---|---|---|
| TBH | Boston Herald | navbar | — (open) | #00538a | 0.015 | yes |
| TCCDR | Canon City Daily Record | navbar | #353f8a | #32408f | 0.009 |  |
| TCE | Chico Enterprise Record | navbar | — (open) | #32408f | 0.046 | yes |
| TETS | Eureka Times Standard | navbar | #353f8a | #32408f | 0.009 |  |
| TGT | Greeley Tribune | navbar | #536e7f | #44687f | 0.028 |  |
| TJA | Journal Advocate | navbar | #353f8a | #32408f | 0.009 |  |
| TLBPT | Long Beach Press-Telegram | navbar | — (open) | #32408f | 0.032 | yes |
| TLADN | Los Angeles Daily News | navbar | #ab4022 | #b93611 | 0.029 |  |
| TLS | Lowell Sun News for Mobile | navbar | #ab4022 | #b93611 | 0.029 |  |
| TMD | Macomb Daily | navbar | #3f5177 | #3a527a | 0.008 |  |
| TMI | Marin Independent Journal News | navbar | — (open) | #32408f | 0.046 | yes |
| NYDN | New York Daily News | action | #4591e0 | #4492e0 | 0.003 |  |
| TOD | Oneida Daily Dispatch | navbar | #b92111 | #b93611 | 0.028 |  |
| OS | Orlando Sentinel | action | — (open) | #15919d | 0.0 | yes |
| PSN | Pasadena Star News | navbar | — (open) | #b93611 | 0.038 | yes |
| TRDF | Redlands Daily Facts | navbar | — (open) | #32408f | 0.032 | yes |
| TSCS | Santa Cruz Sentinel | navbar | #353f8a | #32408f | 0.009 |  |
| TSEB | Sentinel and Enterprise | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TMJ | The Morning Journal | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TMS | The Morning Sun | navbar | #3f5177 | #3a527a | 0.008 |  |
| TNH | The News Herald | navbar | #ab4022 | #b93611 | 0.029 |  |
| TPM | The Pottstown Mercury | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TPE | The Press-Enterprise | navbar | — (open) | #b93611 | 0.038 | yes |
| TSBS | The San Bernardino Sun | navbar | — (open) | #b93611 | 0.038 | yes |
| TTH | The Times Herald | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TRR | The Troy Record | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TWDN | Whittier Daily News | navbar | — (open) | #b93611 | 0.038 | yes |

### Already identical (10)

BS, CT, DP, TEPTG, TFMT, HC, MC, SS, TUDJ, VP

### Kept: web color too far (15)

| Code | Brand | Kept | Web | ΔE |
|---|---|---|---|---|
| TIVDB | Inland Valley Daily Bulletin | #004e87 | #32408f | 0.052 |
| TLTC | Longmont Times-Call for Mobile | #007cba | #32408f | 0.169 |
| TLR | Loveland Reporter Herald | #4e5dca | #32408f | 0.126 |
| TMCH | Monterey County Herald | #3c6292 | #32408f | 0.099 |
| TRE | Reading Eagle | #004e87 | #b93611 | 0.298 |
| TROT | Royal Oak Tribune | #013a67 | #3a527a | 0.099 |
| SGVT | San Gabriel Valley Tribune | #b11e35 | #b93611 | 0.058 |
| TSAR | Saratogian | #f5f5f5 | #b93611 | 0.477 |
| TDC | The Daily Camera | #007639 | #32408f | 0.244 |
| TEBT | The East Bay Times | #557fba | #006394 | 0.119 |
| TMN | The Mercury News | #004e87 | #006394 | 0.064 |
| TR | The Reporter for Mobile | #007cba | #b93611 | 0.299 |
| TVR | Vacaville Reporter | #408fcb | #32408f | 0.229 |
| TVTH | Vallejo Times Herald News | #8d092d | #32408f | 0.229 |
| TWDD | Woodland Daily Democrat | #007639 | #32408f | 0.244 |

### Still open: web color far from both apps (9)

| Code | Brand | iOS | Android | Web | ΔE to nearest |
|---|---|---|---|---|---|
| TDB | Daily Breeze | #004e87 | #2e6c90 | #0a5962 | 0.079 |
| TDF | Daily Freeman | #004e87 | #1b6bad | #b93611 | 0.289 |
| TDLW | Daily Local Weschester | #1591b7 | #1591b5 | #b93611 | 0.296 |
| TDCD | Delaware County Daily Times | #5b9bc8 | #4891b3 | #b93611 | 0.278 |
| OCR | Orange County Register | #b04f0f | #ac4e0f | #0a5962 | 0.235 |
| TSPPP | St. Paul Pioneer Press | #004e87 | #557fba | #0065a8 | 0.08 |
| TDP | The Denver Post | #f7a430 | #daa520 | #7d161e | 0.393 |
| TOP | The Oakland Press | #0b151e | #0b151d | #3a527a | 0.252 |
| TT | The Trentonian | #004e87 | #357dad | #b93611 | 0.273 |
