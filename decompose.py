#!/usr/bin/env python3
"""
HW3 (Version 2.0.0) - Super simple 3NF / BCNF task.

You only need to fill in two functions below:
- solve_3nf(...)
- solve_bcnf(...)
We already read the JSON file for you and print the result.
No fancy Python features, just lists and dicts.
"""
import json
import sys
from pathlib import Path

# Keep this version as-is
ASSIGNMENT_VERSION = (2, 0, 0)  # v2.0.0


def solve_3nf(relation_name, attributes, functional_dependencies):
    """
    TODO: Return the 3NF decomposition.

    Inputs:
      - relation_name: a string like "R"
      - attributes: a list of strings, e.g. ["A", "B", "C"]
      - functional_dependencies: a list of dicts, each like:
            {"left": ["A", "B"], "right": ["C"]}
        The right side always has exactly ONE attribute.

    Return:
      A list of relations. Each relation is a list of attribute names.
      Example: [["A","B"], ["B","C"]]
    """
    # Replace the code below with your own solution.
    raise NotImplementedError("Please implement solve_3nf()")


def solve_bcnf(relation_name, attributes, functional_dependencies):
    """
    TODO: Return the BCNF decomposition.

    Inputs:
      - relation_name: a string like "R"
      - attributes: a list of strings, e.g. ["A", "B", "C"]
      - functional_dependencies: a list of dicts, each like:
            {"left": ["A", "B"], "right": ["C"]}
        The right side always has exactly ONE attribute.

    Return:
      A list of relations. Each relation is a list of attribute names.
      Example: [["A","B"], ["B","C"]]
    """
    # Replace the code below with your own solution.
    raise NotImplementedError("Please implement solve_bcnf()")


def _read_input_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    relation_name = data.get("relationName", "R")
    attributes = data.get("attributes", [])
    fds = data.get("functionalDependencies", [])
    return relation_name, attributes, fds


def _validate_input(attributes, fds):
    if not attributes:
        raise ValueError("attributes must be a non-empty list")
    for i, fd in enumerate(fds):
        if "left" not in fd or "right" not in fd:
            raise ValueError(f"FD #{i} must have 'left' and 'right'")
        if not fd["left"] or not fd["right"]:
            raise ValueError(f"FD #{i} must have non-empty left and right")
        if len(fd["right"]) != 1:
            raise ValueError(f"FD #{i} right side must have exactly one attribute")
        # Basic attribute name check
        for a in fd["left"] + fd["right"]:
            if a not in attributes:
                raise ValueError(f"FD #{i} contains unknown attribute '{a}'")


def main():
    # Usage: python3 decompose_v2.py path/to/test.json
    if len(sys.argv) != 2:
        print("Usage: python3 decompose_v2.py path/to/test.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        sys.exit(1)

    relation_name, attributes, fds = _read_input_json(str(input_path))
    _validate_input(attributes, fds)

    # Students implement both functions
    result = {
        "3nf": solve_3nf(relation_name, attributes, fds),
        "bcnf": solve_bcnf(relation_name, attributes, fds),
    }

    # We just print the result as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


