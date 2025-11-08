# CSE 132A Homework 3 (v2.0.0) — 3NF and BCNF, made simple

## Overview

You will be given the functional dependencies. No sample data. Your job is to compute the 3NF and BCNF decompositions.

We made this version very small and friendly. You only edit two functions in `decompose_v2.py`.

## What you implement

Open `decompose_v2.py` and implement two functions. That’s it.

Inputs to both functions:
- relation_name: like `"R"`
- attributes: a list like `["A","B","C"]`
- functional_dependencies: a list of dicts like:
  - `{"left": ["A", "B"], "right": ["C"]}` (right side has exactly one attribute)

What to implement:
- `solve_3nf(relation_name, attributes, functional_dependencies)` → returns a list of relations (each a list of attributes)
- `solve_bcnf(relation_name, attributes, functional_dependencies)` → returns a list of relations (each a list of attributes)

Each relation is just a list of attributes. No need to name relations (`R1`, `R2`, ...). The program will print:
```json
{ "3nf": [...], "bcnf": [...] }
```

## How to run

Each test is a single JSON file in `v3/tests/`.

Examples (each test is one file):
```bash
python3 decompose_v2.py v3/tests/test_00_chain_abc.json
python3 decompose_v2.py v3/tests/multi_two_relations_independent_test_1_r2_de_f_f_e.json
```

## Input format

Each test JSON looks like this:
```json
{
  "relationName": "R",
  "attributes": ["A", "B", "C"],
  "functionalDependencies": [
    { "left": ["A"], "right": ["B"] },
    { "left": ["B"], "right": ["C"] }
  ]
}
```

## Output format

Print a JSON object with two keys, `"3nf"` and `"bcnf"`, where each value is a list of relations (each relation is a list of attribute names).

Example output:
```json
{
  "3nf":  [["A","B"], ["B","C"]],
  "bcnf": [["A","B"], ["B","C"]]
}
```

## Notes
- No type hints required.
- Keep it simple. Use lists and dicts.
- Version: 2.0.0 (shown in the file).

## Submission

Submit only `decompose_v2.py` on Gradescope for HW3.