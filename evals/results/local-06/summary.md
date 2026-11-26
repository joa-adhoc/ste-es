## sonnet

| metric | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|
| n | 87 | 87 | 87 | 87 | 87 |
| reader_coverage | 87/87 | 87/87 | 87/87 | 87/87 | 87/87 |
| comprehension | 0.946 | 0.956 | 0.954 | 0.933 | 0.935 |
| comprehension_not_stated | 0.015 | 0.015 | 0.015 | 0.019 | 0.019 |
| followup_rate | 0.37 | 0.37 | 0.31 | 0.32 | 0.36 |
| reader_agreement | 0.85 | 0.83 | 0.87 | 0.85 | 0.86 |
| followup_types | {'dato': 30, 'aclaracion': 2} | {'aclaracion': 2, 'ejemplo': 2, 'dato': 28} | {'dato': 24, 'ejemplo': 1, 'aclaracion': 2} | {'ejemplo': 1, 'dato': 25, 'aclaracion': 2} | {'aclaracion': 2, 'ejemplo': 2, 'dato': 27} |
| answer_first | 0.94 | 0.93 | 0.99 | 0.94 | 0.9 |
| tokens_to_understand_total | 162058 | 123800 | 145869 | 135175 | 142975 |
| tokens_to_understand_median | 1620 | 1142 | 1387 | 1305 | 1353 |
| output_tokens_median | 1256 | 808 | 1140 | 854 | 1065 |
| input_tokens_median | 28240 | 28238 | 28355 | 28348 | 28372 |
| words_total_median | 369 | 300 | 359 | 315 | 319 |
| words_median | 301 | 265 | 307 | 277 | 282 |
| facts_kept | 0.984 | 0.982 | 0.982 | 0.975 | 0.977 |
| conditions_kept | 0.992 | 0.992 | 1.0 | 0.988 | 0.992 |
| contradicted | 0 | 0 | 0 | 0 | 0 |
| incorrect | 35 | 33 | 28 | 27 | 25 |
| violations_per100 | 0.75 | 1.1 | 0.76 | 1.33 | 1.36 |
| voseo_share | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| diagram_rate_structure | 0 | 0 | 0 | 0 | 0 |
| diagram_rate_flat | 0 | 0 | 0 | 0 | 0 |
| diagram_errors | 0 | 0 | 0 | 0 | 0 |

Change vs `baseline` (per-case median, 95% CI):


By group of cases:

**flow**

| metric | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|
| n | 27 | 27 | 27 | 27 | 27 |
| followup_rate | 0.7 | 0.7 | 0.59 | 0.67 | 0.78 |
| facts_kept | 0.994 | 0.994 | 1.0 | 0.994 | 0.994 |
| conditions_kept | 0.989 | 1.0 | 1.0 | 0.989 | 0.989 |
| incorrect | 0 | 2 | 1 | 2 | 3 |
| words_median | 438 | 384 | 429 | 403 | 402 |
| diagram_rate | 0 | 0 | 0 | 0 | 0 |

**precision**

| metric | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|
| n | 12 | 12 | 12 | 12 | 12 |
| followup_rate | 0 | 0 | 0 | 0 | 0 |
| facts_kept | 0.902 | 0.922 | 0.882 | 0.882 | 0.902 |
| conditions_kept | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| incorrect | 7 | 5 | 5 | 5 | 6 |
| words_median | 252.5 | 234.5 | 257.5 | 255.0 | 249.0 |
| diagram_rate | 0 | 0 | 0 | 0 | 0 |

**conditional**

| metric | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|
| n | 9 | 9 | 9 | 9 | 9 |
| followup_rate | 0.67 | 0.67 | 0.67 | 0.56 | 0.56 |
| facts_kept | 1.0 | 1.0 | 1.0 | 0.97 | 1.0 |
| conditions_kept | 1.0 | 1.0 | 1.0 | 0.963 | 1.0 |
| incorrect | 7 | 5 | 3 | 4 | 3 |
| words_median | 212 | 143 | 215 | 120 | 154 |
| diagram_rate | 0 | 0 | 0 | 0 | 0 |

**report**

| metric | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|
| n | 12 | 12 | 12 | 12 | 12 |
| followup_rate | 0.08 | 0 | 0 | 0 | 0.08 |
| facts_kept | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| conditions_kept | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| incorrect | 3 | 4 | 0 | 4 | 2 |
| words_median | 178.5 | 157.0 | 175.0 | 141.0 | 147.5 |
| diagram_rate | 0 | 0 | 0 | 0 | 0 |

**other**

| metric | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|
| n | 27 | 27 | 27 | 27 | 27 |
| followup_rate | 0.22 | 0.26 | 0.19 | 0.19 | 0.15 |
| facts_kept | 0.993 | 0.979 | 0.986 | 0.979 | 0.972 |
| conditions_kept | 0.987 | 0.973 | 1.0 | 0.987 | 0.987 |
| incorrect | 18 | 17 | 19 | 12 | 11 |
| words_median | 331 | 279 | 319 | 304 | 290 |
| diagram_rate | 0 | 0 | 0 | 0 | 0 |


Blind preference (each arm vs `baseline`):


Blind preference (each arm vs `conventions_concise`):

- conventions_v3: {'conventions_v3': 25, 'tie': 0, 'conventions_concise': 62, 'n': 87, 'by_group': {'flow': {'conventions_v3': 9, 'tie': 0, 'conventions_concise': 18, 'n': 27}, 'precision': {'conventions_v3': 2, 'tie': 0, 'conventions_concise': 10, 'n': 12}, 'conditional': {'conventions_v3': 3, 'tie': 0, 'conventions_concise': 6, 'n': 9}, 'report': {'conventions_v3': 3, 'tie': 0, 'conventions_concise': 9, 'n': 12}, 'other': {'conventions_v3': 8, 'tie': 0, 'conventions_concise': 19, 'n': 27}}}
- conventions_v4: {'conventions_v4': 30, 'tie': 0, 'conventions_concise': 57, 'n': 87, 'by_group': {'flow': {'conventions_v4': 11, 'tie': 0, 'conventions_concise': 16, 'n': 27}, 'precision': {'conventions_v4': 5, 'tie': 0, 'conventions_concise': 7, 'n': 12}, 'conditional': {'conventions_v4': 2, 'tie': 0, 'conventions_concise': 7, 'n': 9}, 'report': {'conventions_v4': 5, 'tie': 0, 'conventions_concise': 7, 'n': 12}, 'other': {'conventions_v4': 7, 'tie': 0, 'conventions_concise': 20, 'n': 27}}}
- conventions_v6: {'conventions_v6': 45, 'tie': 2, 'conventions_concise': 40, 'n': 87, 'by_group': {'flow': {'conventions_v6': 12, 'tie': 0, 'conventions_concise': 15, 'n': 27}, 'precision': {'conventions_v6': 7, 'tie': 0, 'conventions_concise': 5, 'n': 12}, 'conditional': {'conventions_v6': 3, 'tie': 0, 'conventions_concise': 6, 'n': 9}, 'report': {'conventions_v6': 5, 'tie': 2, 'conventions_concise': 5, 'n': 12}, 'other': {'conventions_v6': 18, 'tie': 0, 'conventions_concise': 9, 'n': 27}}}
- conventions_v5: {'conventions_v5': 50, 'tie': 1, 'conventions_concise': 36, 'n': 87, 'by_group': {'flow': {'conventions_v5': 18, 'tie': 0, 'conventions_concise': 9, 'n': 27}, 'precision': {'conventions_v5': 6, 'tie': 0, 'conventions_concise': 6, 'n': 12}, 'conditional': {'conventions_v5': 6, 'tie': 0, 'conventions_concise': 3, 'n': 9}, 'report': {'conventions_v5': 8, 'tie': 1, 'conventions_concise': 3, 'n': 12}, 'other': {'conventions_v5': 12, 'tie': 0, 'conventions_concise': 15, 'n': 27}}}

Blind preference (each arm vs `conventions_v3`):

- conventions_v4: {'conventions_v4': 42, 'tie': 1, 'conventions_v3': 44, 'n': 87, 'by_group': {'flow': {'conventions_v4': 12, 'tie': 0, 'conventions_v3': 15, 'n': 27}, 'precision': {'conventions_v4': 8, 'tie': 0, 'conventions_v3': 4, 'n': 12}, 'conditional': {'conventions_v4': 3, 'tie': 0, 'conventions_v3': 6, 'n': 9}, 'report': {'conventions_v4': 7, 'tie': 1, 'conventions_v3': 4, 'n': 12}, 'other': {'conventions_v4': 12, 'tie': 0, 'conventions_v3': 15, 'n': 27}}}

Blind preference (each arm vs `conventions_v4`):

- conventions_v5: {'conventions_v5': 56, 'tie': 2, 'conventions_v4': 29, 'n': 87, 'by_group': {'flow': {'conventions_v5': 16, 'tie': 0, 'conventions_v4': 11, 'n': 27}, 'precision': {'conventions_v5': 5, 'tie': 0, 'conventions_v4': 7, 'n': 12}, 'conditional': {'conventions_v5': 7, 'tie': 0, 'conventions_v4': 2, 'n': 9}, 'report': {'conventions_v5': 7, 'tie': 1, 'conventions_v4': 4, 'n': 12}, 'other': {'conventions_v5': 21, 'tie': 1, 'conventions_v4': 5, 'n': 27}}}

Blind preference (each arm vs `conventions_v5`):

- conventions_v6: {'conventions_v6': 37, 'tie': 3, 'conventions_v5': 47, 'n': 87, 'by_group': {'flow': {'conventions_v6': 10, 'tie': 0, 'conventions_v5': 17, 'n': 27}, 'precision': {'conventions_v6': 8, 'tie': 0, 'conventions_v5': 4, 'n': 12}, 'conditional': {'conventions_v6': 1, 'tie': 0, 'conventions_v5': 8, 'n': 9}, 'report': {'conventions_v6': 5, 'tie': 2, 'conventions_v5': 5, 'n': 12}, 'other': {'conventions_v6': 13, 'tie': 1, 'conventions_v5': 13, 'n': 27}}}
