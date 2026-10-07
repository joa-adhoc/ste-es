## sonnet

| métrica | breve | nucleo | nucleo_plus | completo_sin_diag | completo |
|---|---|---|---|---|---|
| n | 36 | 36 | 36 | 36 | 36 |
| followup_rate | 0.58 | 0.58 | 0.44 | 0.67 | 0.42 |
| followup_types | {'dato': 14, 'ejemplo': 4, 'aclaracion': 2, 'resumen': 1} | {'aclaracion': 5, 'ejemplo': 8, 'dato': 7, 'resumen': 1} | {'dato': 10, 'aclaracion': 2, 'ejemplo': 4} | {'ejemplo': 6, 'dato': 14, 'aclaracion': 3, 'resumen': 1} | {'ejemplo': 6, 'dato': 7, 'aclaracion': 2} |
| answer_first | 0.53 | 0.47 | 0.83 | 0.56 | 0.53 |
| tokens_to_understand_median | 1418.0 | 1533.0 | 1054.5 | 1558.5 | 1395.5 |
| output_tokens_median | 685.5 | 691.5 | 703.0 | 815.5 | 936.5 |
| input_tokens_median | 20089.5 | 20300.5 | 20385.5 | 24648.5 | 26100.5 |
| words_total_median | 259.5 | 240.5 | 255.0 | 238.0 | 218.0 |
| words_median | 258.5 | 233.0 | 237.0 | 228.0 | 167.5 |
| facts_kept | 0.964 | 0.985 | 0.985 | 0.964 | 0.974 |
| conditions_kept | 0.954 | 0.981 | 0.991 | 0.954 | 0.981 |
| contradicted | 0 | 0 | 0 | 0 | 0 |
| incorrect | 16 | 8 | 8 | 15 | 10 |
| violations_per100 | 0.64 | 0.33 | 0.3 | 0.2 | 0.19 |
| voseo_share | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| diagram_rate_structure | 0 | 0 | 0 | 0 | 1 |
| diagram_rate_flat | 0 | 0 | 0 | 0 | 0.93 |
| diagram_errors | 0 | 0 | 0 | 0 | 2 |

Cambio contra `breve` (mediana por caso, IC 95%):

- nucleo_vs_breve: {'tokens_to_understand': {'median': 0.078, 'ci95': [0.002, 0.204], 'n': 36}, 'words_total': {'median': -0.028, 'ci95': [-0.101, 0.023], 'n': 36}}
- nucleo_plus_vs_breve: {'tokens_to_understand': {'median': 0.074, 'ci95': [0.004, 0.102], 'n': 36}, 'words_total': {'median': 0.016, 'ci95': [-0.054, 0.071], 'n': 36}}
- completo_sin_diag_vs_breve: {'tokens_to_understand': {'median': 0.102, 'ci95': [0.009, 0.216], 'n': 36}, 'words_total': {'median': -0.013, 'ci95': [-0.121, 0.02], 'n': 36}}
- completo_vs_breve: {'tokens_to_understand': {'median': 0.206, 'ci95': [0.042, 0.349], 'n': 36}, 'words_total': {'median': -0.073, 'ci95': [-0.198, 0.032], 'n': 36}}

Preferencia a ciegas (cada brazo contra `breve`):

- completo: {'completo': 14, 'tie': 0, 'breve': 22, 'n': 36}
- nucleo_plus: {'nucleo_plus': 16, 'tie': 1, 'breve': 19, 'n': 36}
- completo_sin_diag: {'completo_sin_diag': 12, 'tie': 0, 'breve': 24, 'n': 36}
- nucleo: {'nucleo': 11, 'tie': 0, 'breve': 25, 'n': 36}
