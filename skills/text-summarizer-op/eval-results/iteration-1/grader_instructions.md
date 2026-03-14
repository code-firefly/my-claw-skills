# Grader Instructions

**Evaluation Results:** eval-results/iteration-1
**Eval Set:** evals/evals.json

## Task

Read the eval set and evaluate the outputs in both `baseline/` and `with_skill/` directories. Follow the grading criteria in `agents/grader.md`.

## Process

1. Load the eval set from `eval_set.json`
2. For each test case, compare baseline vs with_skill results
3. For each assertion in the eval set, determine PASS/FAIL
4. Generate grading.json in each test directory

## Output Format

Save results as `grading.json` in each test directory following the schema in `references/schemas.md`.

## Expected Structure

```
eval-results/iteration-1/
  ├── eval_set.json
  ├── baseline/
  │   └── test_001/
  │       ├── transcript.md
  │       ├── outputs/
  │       └── grading.json
  └── with_skill/
      └── test_001/
          ├── transcript.md
          ├── outputs/
          └── grading.json
```