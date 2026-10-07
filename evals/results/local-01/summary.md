## sonnet

| métrica | baseline | breve | nucleo | completo |
|---|---|---|---|---|
| n | 36 | 36 | 36 | 36 |
| words_median | 335.0 | 258.5 | 233.0 | 167.5 |
| output_tokens_median | 910.0 | 685.5 | 691.5 | 936.5 |
| facts_kept | 0.995 | 0.964 | 0.985 | 0.974 |
| conditions_kept | 0.991 | 0.954 | 0.981 | 0.981 |
| contradicted | 0 | 0 | 0 | 0 |
| incorrect | 18 | 16 | 8 | 10 |
| violations_per100 | 0.61 | 0.65 | 0.33 | 0.19 |
| voseo_share | 1.0 | 0.99 | 1.0 | 1.0 |
| diagram_rate_structure | 0 | 0 | 0 | 1 |
| diagram_rate_flat | 0 | 0 | 0 | 0.93 |
| diagram_errors | 0 | 0 | 0 | 2 |

Largo de `completo` contra cada brazo (mediana del cambio por caso, IC 95%):

- words_completo_vs_baseline: {'median': -0.362, 'ci95': [-0.438, -0.33], 'n': 36}
- words_completo_vs_breve: {'median': -0.203, 'ci95': [-0.308, -0.122], 'n': 36}
- words_completo_vs_nucleo: {'median': -0.171, 'ci95': [-0.242, -0.102], 'n': 36}

Preferencia a ciegas (`completo` contra cada brazo):

- baseline: {'completo': 18, 'tie': 0, 'baseline': 18, 'n': 36}
- nucleo: {'completo': 15, 'tie': 0, 'nucleo': 21, 'n': 36}
- breve: {'completo': 13, 'tie': 0, 'breve': 23, 'n': 36}
