## sonnet

| metric | baseline | ste_es | ste_es_v3 | concise | conventions | conventions_v3 | conventions_concise |
|---|---|---|---|---|---|---|---|
| n | 87 | 87 | 87 | 87 | 87 | 87 | 87 |
| reader_coverage | 87/87 | 87/87 | 87/87 | 87/87 | 87/87 | 87/87 | 87/87 |
| comprehension | 0.96 | 0.923 | 0.95 | 0.943 | 0.952 | 0.948 | 0.944 |
| comprehension_not_stated | 0.019 | 0.034 | 0.027 | 0.042 | 0.023 | 0.019 | 0.027 |
| followup_rate | 0.48 | 0.48 | 0.45 | 0.44 | 0.54 | 0.61 | 0.51 |
| reader_agreement | 0.79 | 0.79 | 0.86 | 0.79 | 0.85 | 0.76 | 0.76 |
| followup_types | {'dato': 35, 'aclaracion': 5, 'ejemplo': 2} | {'aclaracion': 19, 'dato': 20, 'ejemplo': 3} | {'dato': 26, 'aclaracion': 11, 'ejemplo': 2} | {'aclaracion': 12, 'dato': 26} | {'dato': 39, 'ejemplo': 2, 'aclaracion': 6} | {'dato': 43, 'aclaracion': 9, 'ejemplo': 1} | {'aclaracion': 7, 'dato': 36, 'ejemplo': 1} |
| answer_first | 0.55 | 0.89 | 0.97 | 0.76 | 0.66 | 0.86 | 0.79 |
| tokens_to_understand_total | 130295 | 105735 | 104534 | 91021 | 144548 | 136991 | 115474 |
| tokens_to_understand_median | 1169 | 1258 | 913 | 745 | 1695 | 1711 | 1171 |
| output_tokens_median | 890 | 774 | 671 | 593 | 1069 | 886 | 757 |
| input_tokens_median | 21500 | 22920 | 22225 | 21982 | 27780 | 28262 | 27948 |
| words_total_median | 330 | 183 | 229 | 222 | 304 | 267 | 240 |
| words_median | 308 | 169 | 209 | 211 | 295 | 260 | 224 |
| facts_kept | 0.984 | 0.959 | 0.975 | 0.968 | 0.986 | 0.984 | 0.982 |
| conditions_kept | 0.988 | 0.971 | 0.979 | 0.975 | 0.988 | 0.988 | 0.992 |
| contradicted | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| incorrect | 47 | 13 | 22 | 32 | 47 | 41 | 45 |
| violations_per100 | 0.86 | 0.51 | 0.33 | 0.92 | 0.59 | 0.48 | 0.52 |
| voseo_share | 0.85 | 1.0 | 1.0 | 0.86 | 1.0 | 1.0 | 1.0 |
| diagram_rate_structure | 0 | 1 | 0.63 | 0 | 0 | 0 | 0 |
| diagram_rate_flat | 0 | 0.18 | 0.02 | 0 | 0 | 0 | 0 |
| diagram_errors | 0 | 1 | 1 | 0 | 0 | 0 | 0 |

Change vs `baseline` (per-case median, 95% CI):

- ste_es_vs_baseline: {'tokens_to_understand': {'median': -0.187, 'ci95': [-0.251, -0.123], 'n': 87}, 'words_total': {'median': -0.41, 'ci95': [-0.438, -0.385], 'n': 87}}
- ste_es_v3_vs_baseline: {'tokens_to_understand': {'median': -0.191, 'ci95': [-0.26, -0.167], 'n': 87}, 'words_total': {'median': -0.277, 'ci95': [-0.301, -0.238], 'n': 87}}
- concise_vs_baseline: {'tokens_to_understand': {'median': -0.289, 'ci95': [-0.324, -0.222], 'n': 87}, 'words_total': {'median': -0.303, 'ci95': [-0.354, -0.264], 'n': 87}}
- conventions_vs_baseline: {'tokens_to_understand': {'median': 0.03, 'ci95': [-0.069, 0.151], 'n': 87}, 'words_total': {'median': -0.038, 'ci95': [-0.074, 0.0], 'n': 87}}
- conventions_v3_vs_baseline: {'tokens_to_understand': {'median': -0.047, 'ci95': [-0.091, 0.06], 'n': 87}, 'words_total': {'median': -0.107, 'ci95': [-0.162, -0.067], 'n': 87}}
- conventions_concise_vs_baseline: {'tokens_to_understand': {'median': -0.165, 'ci95': [-0.214, -0.081], 'n': 87}, 'words_total': {'median': -0.259, 'ci95': [-0.308, -0.229], 'n': 87}}

By group of cases:

**flow**

| metric | baseline | ste_es | ste_es_v3 | concise | conventions | conventions_v3 | conventions_concise |
|---|---|---|---|---|---|---|---|
| n | 27 | 27 | 27 | 27 | 27 | 27 | 27 |
| followup_rate | 0.89 | 0.78 | 0.78 | 0.7 | 0.96 | 1 | 0.89 |
| facts_kept | 1.0 | 0.987 | 0.981 | 0.981 | 0.994 | 0.994 | 1.0 |
| conditions_kept | 1.0 | 0.989 | 1.0 | 0.989 | 0.989 | 0.989 | 1.0 |
| incorrect | 19 | 6 | 7 | 15 | 6 | 5 | 10 |
| words_median | 381 | 191 | 260 | 282 | 352 | 337 | 280 |
| diagram_rate | 0 | 1 | 0.63 | 0 | 0 | 0 | 0 |

**precision**

| metric | baseline | ste_es | ste_es_v3 | concise | conventions | conventions_v3 | conventions_concise |
|---|---|---|---|---|---|---|---|
| n | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| followup_rate | 0.08 | 0.17 | 0 | 0 | 0 | 0.17 | 0.25 |
| facts_kept | 0.941 | 0.863 | 0.941 | 0.922 | 0.961 | 0.922 | 0.941 |
| conditions_kept | 1.0 | 0.967 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| incorrect | 9 | 1 | 2 | 2 | 2 | 3 | 8 |
| words_median | 228.0 | 117.0 | 160.0 | 146.5 | 223.0 | 188.5 | 168.0 |
| diagram_rate | 0 | 0.33 | 0.08 | 0 | 0 | 0 | 0 |

**conditional**

| metric | baseline | ste_es | ste_es_v3 | concise | conventions | conventions_v3 | conventions_concise |
|---|---|---|---|---|---|---|---|
| n | 9 | 9 | 9 | 9 | 9 | 9 | 9 |
| followup_rate | 0.33 | 0.56 | 0.56 | 0.44 | 0.11 | 0.56 | 0.22 |
| facts_kept | 0.97 | 0.97 | 0.879 | 0.909 | 0.97 | 1.0 | 1.0 |
| conditions_kept | 0.963 | 0.963 | 0.852 | 0.889 | 0.963 | 1.0 | 1.0 |
| incorrect | 0 | 1 | 2 | 3 | 10 | 9 | 8 |
| words_median | 168 | 93 | 107 | 113 | 184 | 170 | 134 |
| diagram_rate | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**report**

| metric | baseline | ste_es | ste_es_v3 | concise | conventions | conventions_v3 | conventions_concise |
|---|---|---|---|---|---|---|---|
| n | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| followup_rate | 0.25 | 0.25 | 0.25 | 0.25 | 0.5 | 0.5 | 0.42 |
| facts_kept | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| conditions_kept | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| incorrect | 6 | 3 | 4 | 4 | 9 | 4 | 5 |
| words_median | 195.0 | 118.5 | 161.5 | 143.0 | 239.0 | 217.5 | 147.0 |
| diagram_rate | 0 | 0.25 | 0 | 0 | 0 | 0 | 0 |

**other**

| metric | baseline | ste_es | ste_es_v3 | concise | conventions | conventions_v3 | conventions_concise |
|---|---|---|---|---|---|---|---|
| n | 27 | 27 | 27 | 27 | 27 | 27 | 27 |
| followup_rate | 0.41 | 0.41 | 0.37 | 0.44 | 0.52 | 0.48 | 0.37 |
| facts_kept | 0.979 | 0.944 | 0.993 | 0.972 | 0.986 | 0.986 | 0.965 |
| conditions_kept | 0.973 | 0.947 | 0.987 | 0.973 | 0.987 | 0.973 | 0.973 |
| incorrect | 13 | 2 | 7 | 8 | 20 | 20 | 14 |
| words_median | 328 | 187 | 214 | 203 | 311 | 285 | 256 |
| diagram_rate | 0 | 0.15 | 0 | 0 | 0 | 0 | 0 |


Blind preference (each arm vs `baseline`):

- conventions_v3: {'conventions_v3': 62, 'tie': 0, 'baseline': 25, 'n': 87, 'by_group': {'flow': {'conventions_v3': 22, 'tie': 0, 'baseline': 5, 'n': 27}, 'precision': {'conventions_v3': 9, 'tie': 0, 'baseline': 3, 'n': 12}, 'conditional': {'conventions_v3': 5, 'tie': 0, 'baseline': 4, 'n': 9}, 'report': {'conventions_v3': 9, 'tie': 0, 'baseline': 3, 'n': 12}, 'other': {'conventions_v3': 17, 'tie': 0, 'baseline': 10, 'n': 27}}}
- concise: {'concise': 65, 'tie': 0, 'baseline': 22, 'n': 87, 'by_group': {'flow': {'concise': 15, 'tie': 0, 'baseline': 12, 'n': 27}, 'precision': {'concise': 9, 'tie': 0, 'baseline': 3, 'n': 12}, 'conditional': {'concise': 6, 'tie': 0, 'baseline': 3, 'n': 9}, 'report': {'concise': 11, 'tie': 0, 'baseline': 1, 'n': 12}, 'other': {'concise': 24, 'tie': 0, 'baseline': 3, 'n': 27}}}
- conventions_concise: {'conventions_concise': 62, 'tie': 0, 'baseline': 25, 'n': 87, 'by_group': {'flow': {'conventions_concise': 20, 'tie': 0, 'baseline': 7, 'n': 27}, 'precision': {'conventions_concise': 11, 'tie': 0, 'baseline': 1, 'n': 12}, 'conditional': {'conventions_concise': 4, 'tie': 0, 'baseline': 5, 'n': 9}, 'report': {'conventions_concise': 9, 'tie': 0, 'baseline': 3, 'n': 12}, 'other': {'conventions_concise': 18, 'tie': 0, 'baseline': 9, 'n': 27}}}
- conventions: {'conventions': 46, 'tie': 0, 'baseline': 41, 'n': 87, 'by_group': {'flow': {'conventions': 17, 'tie': 0, 'baseline': 10, 'n': 27}, 'precision': {'conventions': 8, 'tie': 0, 'baseline': 4, 'n': 12}, 'conditional': {'conventions': 3, 'tie': 0, 'baseline': 6, 'n': 9}, 'report': {'conventions': 6, 'tie': 0, 'baseline': 6, 'n': 12}, 'other': {'conventions': 12, 'tie': 0, 'baseline': 15, 'n': 27}}}
- ste_es_v3: {'ste_es_v3': 60, 'tie': 0, 'baseline': 27, 'n': 87, 'by_group': {'flow': {'ste_es_v3': 18, 'tie': 0, 'baseline': 9, 'n': 27}, 'precision': {'ste_es_v3': 7, 'tie': 0, 'baseline': 5, 'n': 12}, 'conditional': {'ste_es_v3': 5, 'tie': 0, 'baseline': 4, 'n': 9}, 'report': {'ste_es_v3': 10, 'tie': 0, 'baseline': 2, 'n': 12}, 'other': {'ste_es_v3': 20, 'tie': 0, 'baseline': 7, 'n': 27}}}
- ste_es: {'ste_es': 54, 'tie': 0, 'baseline': 33, 'n': 87, 'by_group': {'flow': {'ste_es': 8, 'tie': 0, 'baseline': 19, 'n': 27}, 'precision': {'ste_es': 10, 'tie': 0, 'baseline': 2, 'n': 12}, 'conditional': {'ste_es': 6, 'tie': 0, 'baseline': 3, 'n': 9}, 'report': {'ste_es': 9, 'tie': 0, 'baseline': 3, 'n': 12}, 'other': {'ste_es': 21, 'tie': 0, 'baseline': 6, 'n': 27}}}

Blind preference (each arm vs `concise`):

- ste_es_v3: {'ste_es_v3': 44, 'tie': 1, 'concise': 42, 'n': 87, 'by_group': {'flow': {'ste_es_v3': 12, 'tie': 0, 'concise': 15, 'n': 27}, 'precision': {'ste_es_v3': 6, 'tie': 0, 'concise': 6, 'n': 12}, 'conditional': {'ste_es_v3': 7, 'tie': 0, 'concise': 2, 'n': 9}, 'report': {'ste_es_v3': 8, 'tie': 0, 'concise': 4, 'n': 12}, 'other': {'ste_es_v3': 11, 'tie': 1, 'concise': 15, 'n': 27}}}

Blind preference (each arm vs `conventions`):

- conventions_v3: {'conventions_v3': 56, 'tie': 0, 'conventions': 31, 'n': 87, 'by_group': {'flow': {'conventions_v3': 17, 'tie': 0, 'conventions': 10, 'n': 27}, 'precision': {'conventions_v3': 6, 'tie': 0, 'conventions': 6, 'n': 12}, 'conditional': {'conventions_v3': 3, 'tie': 0, 'conventions': 6, 'n': 9}, 'report': {'conventions_v3': 10, 'tie': 0, 'conventions': 2, 'n': 12}, 'other': {'conventions_v3': 20, 'tie': 0, 'conventions': 7, 'n': 27}}}

Blind preference (each arm vs `conventions_concise`):

- conventions_v3: {'conventions_v3': 44, 'tie': 1, 'conventions_concise': 42, 'n': 87, 'by_group': {'flow': {'conventions_v3': 18, 'tie': 0, 'conventions_concise': 9, 'n': 27}, 'precision': {'conventions_v3': 3, 'tie': 0, 'conventions_concise': 9, 'n': 12}, 'conditional': {'conventions_v3': 4, 'tie': 0, 'conventions_concise': 5, 'n': 9}, 'report': {'conventions_v3': 6, 'tie': 0, 'conventions_concise': 6, 'n': 12}, 'other': {'conventions_v3': 13, 'tie': 1, 'conventions_concise': 13, 'n': 27}}}

Blind preference (each arm vs `ste_es`):

- ste_es_v3: {'ste_es_v3': 47, 'tie': 0, 'ste_es': 40, 'n': 87, 'by_group': {'flow': {'ste_es_v3': 18, 'tie': 0, 'ste_es': 9, 'n': 27}, 'precision': {'ste_es_v3': 7, 'tie': 0, 'ste_es': 5, 'n': 12}, 'conditional': {'ste_es_v3': 6, 'tie': 0, 'ste_es': 3, 'n': 9}, 'report': {'ste_es_v3': 3, 'tie': 0, 'ste_es': 9, 'n': 12}, 'other': {'ste_es_v3': 13, 'tie': 0, 'ste_es': 14, 'n': 27}}}
