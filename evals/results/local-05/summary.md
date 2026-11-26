## sonnet

| metric | conventions | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|---|
| n | 24 | 24 | 24 | 24 | 24 | 24 |
| reader_coverage | 24/24 | 24/24 | 24/24 | 24/24 | 24/24 | 24/24 |
| comprehension | 0.75 | 0.854 | 0.743 | 0.771 | 0.764 | 0.792 |
| comprehension_not_stated | 0.097 | 0.056 | 0.139 | 0.097 | 0.111 | 0.083 |
| followup_rate | 0.96 | 1 | 1 | 0.88 | 0.92 | 1 |
| reader_agreement | 0.96 | 0.96 | 1 | 0.88 | 0.92 | 0.96 |
| followup_types | {'aclaracion': 23} | {'aclaracion': 21, 'dato': 3} | {'aclaracion': 24} | {'aclaracion': 19, 'dato': 2} | {'aclaracion': 20, 'ejemplo': 1, 'dato': 1} | {'aclaracion': 22, 'dato': 2} |
| answer_first | 0.71 | 0.79 | 0.71 | 0.92 | 0.88 | 0.88 |
| tokens_to_understand_total | 156646 | 156458 | 138351 | 151525 | 143604 | 152026 |
| tokens_to_understand_median | 6166.5 | 5836.5 | 5273.0 | 6092.0 | 5608.0 | 5493.5 |
| output_tokens_median | 3525.0 | 3300.0 | 2929.0 | 3345.5 | 3258.0 | 3170.0 |
| input_tokens_median | 28199.0 | 28687.0 | 28604.0 | 28723.0 | 28795.0 | 28816.0 |
| words_total_median | 674.5 | 627.5 | 586.0 | 618.0 | 610.5 | 604.0 |
| words_median | 557.5 | 541.0 | 515.5 | 544.0 | 520.5 | 523.0 |
| facts_kept | 0.726 | 0.741 | 0.733 | 0.763 | 0.696 | 0.763 |
| conditions_kept | 0.651 | 0.683 | 0.667 | 0.683 | 0.571 | 0.683 |
| contradicted | 0 | 0 | 0 | 0 | 1 | 0 |
| incorrect | 20 | 21 | 15 | 18 | 23 | 17 |
| violations_per100 | 1.13 | 0.81 | 1.13 | 0.72 | 1.2 | 1.32 |
| voseo_share | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| diagram_rate_structure | 0 | 0 | 0 | 0 | 0 | 0 |
| diagram_rate_flat | 0 | 0 | 0 | 0 | 0 | 0 |
| diagram_errors | 0 | 0 | 0 | 0 | 0 | 0 |

Change vs `baseline` (per-case median, 95% CI):


By group of cases:

**functional**

| metric | conventions | conventions_v3 | conventions_concise | conventions_v4 | conventions_v5 | conventions_v6 |
|---|---|---|---|---|---|---|
| n | 24 | 24 | 24 | 24 | 24 | 24 |
| followup_rate | 0.96 | 1 | 1 | 0.88 | 0.92 | 1 |
| facts_kept | 0.726 | 0.741 | 0.733 | 0.763 | 0.696 | 0.763 |
| conditions_kept | 0.651 | 0.683 | 0.667 | 0.683 | 0.571 | 0.683 |
| incorrect | 20 | 21 | 15 | 18 | 23 | 17 |
| words_median | 557.5 | 541.0 | 515.5 | 544.0 | 520.5 | 523.0 |
| diagram_rate | 0 | 0 | 0 | 0 | 0 | 0 |


Blind preference (each arm vs `baseline`):


Blind preference (each arm vs `conventions`):

- conventions_v3: {'conventions_v3': 15, 'tie': 0, 'conventions': 9, 'n': 24, 'by_group': {'functional': {'conventions_v3': 15, 'tie': 0, 'conventions': 9, 'n': 24}}}
- conventions_v4: {'conventions_v4': 15, 'tie': 0, 'conventions': 9, 'n': 24, 'by_group': {'functional': {'conventions_v4': 15, 'tie': 0, 'conventions': 9, 'n': 24}}}
- conventions_concise: {'conventions_concise': 12, 'tie': 0, 'conventions': 12, 'n': 24, 'by_group': {'functional': {'conventions_concise': 12, 'tie': 0, 'conventions': 12, 'n': 24}}}

Blind preference (each arm vs `conventions_concise`):

- conventions_v3: {'conventions_v3': 11, 'tie': 0, 'conventions_concise': 13, 'n': 24, 'by_group': {'functional': {'conventions_v3': 11, 'tie': 0, 'conventions_concise': 13, 'n': 24}}}
- conventions_v4: {'conventions_v4': 15, 'tie': 0, 'conventions_concise': 9, 'n': 24, 'by_group': {'functional': {'conventions_v4': 15, 'tie': 0, 'conventions_concise': 9, 'n': 24}}}
- conventions_v6: {'conventions_v6': 15, 'tie': 0, 'conventions_concise': 9, 'n': 24, 'by_group': {'functional': {'conventions_v6': 15, 'tie': 0, 'conventions_concise': 9, 'n': 24}}}
- conventions_v5: {'conventions_v5': 15, 'tie': 0, 'conventions_concise': 9, 'n': 24, 'by_group': {'functional': {'conventions_v5': 15, 'tie': 0, 'conventions_concise': 9, 'n': 24}}}

Blind preference (each arm vs `conventions_v3`):

- conventions_v4: {'conventions_v4': 13, 'tie': 0, 'conventions_v3': 11, 'n': 24, 'by_group': {'functional': {'conventions_v4': 13, 'tie': 0, 'conventions_v3': 11, 'n': 24}}}

Blind preference (each arm vs `conventions_v4`):

- conventions_v5: {'conventions_v5': 12, 'tie': 0, 'conventions_v4': 12, 'n': 24, 'by_group': {'functional': {'conventions_v5': 12, 'tie': 0, 'conventions_v4': 12, 'n': 24}}}

Blind preference (each arm vs `conventions_v5`):

- conventions_v6: {'conventions_v6': 10, 'tie': 0, 'conventions_v5': 14, 'n': 24, 'by_group': {'functional': {'conventions_v6': 10, 'tie': 0, 'conventions_v5': 14, 'n': 24}}}
