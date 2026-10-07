## sonnet

| metric | baseline | terse | core_plus | core_diagrams | core_vocab | full_v1 |
|---|---|---|---|---|---|---|
| n | 54 | 54 | 54 | 54 | 54 | 54 |
| reader_coverage | 54/54 | 54/54 | 54/54 | 54/54 | 54/54 | 54/54 |
| comprehension | 0.96 | 0.969 | 0.96 | 0.954 | 0.972 | 0.957 |
| comprehension_not_stated | 0.0 | 0.006 | 0.0 | 0.0 | 0.0 | 0.0 |
| followup_rate | 0.69 | 0.65 | 0.52 | 0.59 | 0.54 | 0.57 |
| reader_agreement | 0.81 | 0.8 | 0.78 | 0.8 | 0.8 | 0.8 |
| followup_types | {'ejemplo': 5, 'dato': 28, 'aclaracion': 4} | {'dato': 28, 'ejemplo': 3, 'aclaracion': 4} | {'dato': 20, 'aclaracion': 6, 'ejemplo': 2} | {'dato': 25, 'ejemplo': 4, 'aclaracion': 3} | {'ejemplo': 4, 'aclaracion': 6, 'dato': 19} | {'ejemplo': 6, 'aclaracion': 7, 'dato': 18} |
| answer_first | 0.31 | 0.39 | 0.94 | 0.91 | 0.93 | 0.46 |
| tokens_to_understand_total | 92471 | 73448 | 70772 | 78670 | 69412 | 82064 |
| tokens_to_understand_median | 1937.0 | 1532.5 | 1425.5 | 1631.5 | 1287.5 | 1641.0 |
| output_tokens_median | 960.5 | 714.0 | 754.0 | 852.5 | 721.0 | 982.0 |
| input_tokens_median | 20070.5 | 20089.5 | 20385.5 | 20595.5 | 20529.5 | 26100.5 |
| words_total_median | 355.0 | 267.5 | 272.5 | 262.5 | 259.0 | 244.0 |
| words_median | 348.0 | 266.0 | 266.0 | 228.5 | 250.0 | 185.0 |
| facts_kept | 0.997 | 0.974 | 0.99 | 0.99 | 0.987 | 0.977 |
| conditions_kept | 0.994 | 0.97 | 0.994 | 0.982 | 0.976 | 0.976 |
| contradicted | 0 | 0 | 0 | 0 | 0 | 0 |
| incorrect | 28 | 25 | 14 | 20 | 14 | 14 |
| violations_per100 | 0.56 | 0.64 | 0.36 | 0.33 | 0.28 | 0.23 |
| voseo_share | 0.98 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| diagram_rate_structure | 0 | 0 | 0 | 0.81 | 0 | 1 |
| diagram_rate_flat | 0 | 0 | 0 | 0.22 | 0 | 0.93 |
| diagram_errors | 0 | 0 | 0 | 1 | 0 | 4 |

Change vs `terse` (per-case median, 95% CI):

- core_plus_vs_terse: {'tokens_to_understand': {'median': 0.062, 'ci95': [-0.011, 0.092], 'n': 54}, 'words_total': {'median': 0.006, 'ci95': [-0.05, 0.071], 'n': 54}}
- core_diagrams_vs_terse: {'tokens_to_understand': {'median': 0.048, 'ci95': [-0.021, 0.104], 'n': 54}, 'words_total': {'median': -0.059, 'ci95': [-0.088, 0.01], 'n': 54}}
- core_vocab_vs_terse: {'tokens_to_understand': {'median': -0.006, 'ci95': [-0.067, 0.07], 'n': 54}, 'words_total': {'median': -0.01, 'ci95': [-0.065, 0.059], 'n': 54}}
- full_v1_vs_terse: {'tokens_to_understand': {'median': 0.147, 'ci95': [0.044, 0.308], 'n': 54}, 'words_total': {'median': -0.053, 'ci95': [-0.142, -0.015], 'n': 54}}

Blind preference (each arm vs `terse`):

- core_vocab: {'core_vocab': 28, 'tie': 1, 'terse': 25, 'n': 54}
- core_plus: {'core_plus': 24, 'tie': 1, 'terse': 29, 'n': 54}
- full_v1: {'full_v1': 22, 'tie': 0, 'terse': 32, 'n': 54}
- core_diagrams: {'core_diagrams': 24, 'tie': 1, 'terse': 29, 'n': 54}

Blind preference (each arm vs `baseline`, plain Claude Code):

- core_vocab: {'core_vocab': 34, 'tie': 0, 'baseline': 20, 'n': 54}
- terse: {'terse': 33, 'tie': 0, 'baseline': 21, 'n': 54}
- core_plus: {'core_plus': 35, 'tie': 0, 'baseline': 19, 'n': 54}
- full_v1: {'full_v1': 24, 'tie': 0, 'baseline': 30, 'n': 54}
- core_diagrams: {'core_diagrams': 37, 'tie': 0, 'baseline': 17, 'n': 54}
