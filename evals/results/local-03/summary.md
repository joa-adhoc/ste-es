## sonnet

| metric | baseline | ste_es |
|---|---|---|
| n | 54 | 54 |
| reader_coverage | 54/54 | 54/54 |
| comprehension | 0.96 | 0.96 |
| comprehension_not_stated | 0.0 | 0.006 |
| followup_rate | 0.69 | 0.54 |
| reader_agreement | 0.81 | 0.78 |
| followup_types | {'ejemplo': 5, 'dato': 28, 'aclaracion': 4} | {'dato': 17, 'aclaracion': 10, 'ejemplo': 2} |
| answer_first | 0.31 | 0.89 |
| tokens_to_understand_total | 92471 | 78148 |
| tokens_to_understand_median | 1937.0 | 1644.0 |
| output_tokens_median | 960.5 | 1024.5 |
| input_tokens_median | 20070.5 | 21628.5 |
| words_total_median | 355.0 | 226.0 |
| words_median | 348.0 | 194.0 |
| facts_kept | 0.997 | 0.983 |
| conditions_kept | 0.994 | 0.982 |
| contradicted | 0 | 0 |
| incorrect | 28 | 5 |
| violations_per100 | 0.56 | 0.37 |
| voseo_share | 0.98 | 1.0 |
| diagram_rate_structure | 0 | 0.93 |
| diagram_rate_flat | 0 | 0.19 |
| diagram_errors | 0 | 0 |

Change vs `baseline` (per-case median, 95% CI):

- ste_es_vs_baseline: {'tokens_to_understand': {'median': -0.137, 'ci95': [-0.18, -0.091], 'n': 54}, 'words_total': {'median': -0.358, 'ci95': [-0.378, -0.307], 'n': 54}}

Blind preference (each arm vs `baseline`):

- ste_es: {'ste_es': 31, 'tie': 0, 'baseline': 23, 'n': 54}
