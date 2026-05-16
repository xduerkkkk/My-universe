
Phase 6 — Unified evaluation & error analysis complete.

New files:

┌───────────────────────────────┬──────────────────────────────────────────────────────────┐

│ File │ Description │

├───────────────────────────────┼──────────────────────────────────────────────────────────┤

│ │ build_model_comparison () — reads per-model metrics JSON, │

│ src/eval/compare_results. py │ produces overall & class-level Markdown comparison │

│ │ tables + JSON summary. Handles missing files gracefully │

│ │ (logs warning, marks "Missing"). │

├───────────────────────────────┼──────────────────────────────────────────────────────────┤

│ │ analyze_prediction_errors () — classifies each token │

│ src/eval/error_analysis. py │ error into 6 types (O↔entity, QA confusion, header │

│ │ confusion, boundary error, other). Extracts up to 5 │

│ │ error cases per type with context windows. │

├───────────────────────────────┼──────────────────────────────────────────────────────────┤

│ │ Orchestration script — calls compare + error analysis, │

│ scripts/06_analyze_results. py │ prints file status, generates experiment log. 5 CLI │

│ │ args. │

├───────────────────────────────┼──────────────────────────────────────────────────────────┤

│ │ Allows report/tables/* and report/experiment_log. md to │

│ .gitignore (updated) │ be committed while still ignoring other report/ │

│ │ contents. │

└───────────────────────────────┴──────────────────────────────────────────────────────────┘

Reused (unchanged):

- src/eval/metrics. py — no changes needed.

Verified with existing data:

=== File Status ===

text_only metrics: EXISTS predictions: EXISTS

text_layout metrics: MISSING predictions: MISSING

layoutlmv3 metrics: EXISTS predictions: EXISTS

┌──────────────┬───────────┬────────────┐

│ │ Text-Only │ LayoutLMv3 │

├──────────────┼───────────┼────────────┤

│ Entity F1 │ 0.2971 │ 0.5546 │

├──────────────┼───────────┼────────────┤

│ Total errors │ 2255 │ 1098 │

└──────────────┴───────────┴────────────┘

Error type distribution works correctly for both models. text_layout correctly flagged as

missing everywhere.

Lightweight checks passed:

- compare_results import — OK

- error_analysis import — OK

- 06_analyze_results. py --help — OK

No training was run. The orchestration script is ready for you to run manually with python

funsd_experiment/scripts/06_analyze_results. py.


  File: scripts/07_run_full_experiments. ps1
  Description: PowerShell pipeline runner. Executes 5 stages sequentially (3 trainings + analysis

    + log update). Each stage logs timestamps + stdout/stderr to a timestamped file. Supports    
    -SkipTextOnly, -SkipTextLayout, -SkipLayoutLMv3, -SkipAnalysis flags. Stops on first failure.
    ────────────────────────────────────────
  File: scripts/07_update_experiment_log. py
  Description: Reads metrics JSONs for all 3 models, writes structured report/experiment_log. md  
    with model configs, hyper-params, overall metrics table, per-class table. Handles missing    
    models gracefully (shows "Metrics pending (TODO)").

  Existing files fixed:
  - src/eval/compare_results. py — fixed Markdown table separator || → |
  - 07_update_experiment_log. py — same separator fix

  .gitignore coverage verified:
  - funsd_experiment/outputs/ — ignored (checkpoints, logs, metrics, predictions, analysis)      
  - funsd_experiment/data/prepared/ — ignored
  - funsd_experiment/data/processed/ — ignored
  - data/funsd_raw/ — ignored
  - report/tables/* + report/experiment_log. md — tracked (committable)

  Lightweight checks passed:
  - PowerShell script with all -Skip flags — runs all 5 stages (4 skipped, log updater passes)   
  - 07_update_experiment_log. py — reads existing metrics, writes correct experiment log

  ---
  To run formal training, open PowerShell in the repo root and execute:

  .\funsd_experiment\scripts\07_run_full_experiments. ps1

  Or skip specific stages:

  # Re-run only Text+Layout
  .\funsd_experiment\scripts\07_run_full_experiments. ps1 -SkipTextOnly -SkipLayoutLMv3
  .\funsd_experiment\scripts\07_run_full_experiments. ps1 -SkipAnalysis

  The log file will be written to
  funsd_experiment/outputs/logs/full_experiment_YYYYMMDD_HHmmss. log.
