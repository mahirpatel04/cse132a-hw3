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
# need this for the find_candidate_keys function
from itertools import combinations

# Keep this version as-is
ASSIGNMENT_VERSION = (2, 0, 0)  # v2.0.0


def compute_closure(attrs, fds):
    """Little hlper function used to get closure of a set of attributes under given FDs"""
    
    
    closure = set(attrs)
    changed = True
    
    while changed:
        
        changed = False
        for fd in fds:
            left_set = set(fd["left"])
            if left_set.issubset(closure) and fd["right"][0] not in closure:
                closure.add(fd["right"][0])
                changed = True
    return closure


def is_superkey(attrs, all_attrs, fds):
    return compute_closure(attrs, fds) == set(all_attrs)


def find_candidate_keys(attributes, fds):
    """Find all candidate keys using a bottom-up approach."""
    
    
    # Try sets of increasing size
    for size in range(1, len(attributes) + 1):
        candidates = []
        for combo in combinations(attributes, size):
            if is_superkey(combo, attributes, fds):
                # Check if it's minimal (no subset is a superkey)
                is_minimal = True
                for smaller_size in range(1, size):
                    for sub_combo in combinations(combo, smaller_size):
                        if is_superkey(sub_combo, attributes, fds):
                            is_minimal = False
                            break
                    if not is_minimal:
                        break
                if is_minimal:
                    candidates.append(list(combo))
        if candidates:
            return candidates
    
    # If there is nokey found, all attributes form the key
    return [attributes]


def minimal_cover(fds, attributes):
    # Step 1: Make right sides singletons (already done in input)
    result = [{"left": fd["left"][:], "right": fd["right"][:]} for fd in fds]
    
    # Step 2: Remove redundant attributes from left sides
    changed = True
    while changed:
        changed = False
        for fd in result:
            if len(fd["left"]) > 1:
                for attr in fd["left"][:]:
                    # Try removing this attribute
                    left_without = [a for a in fd["left"] if a != attr]
                    if not left_without:
                        continue
                    
                    # Check if we can still derive right side
                    closure = compute_closure(left_without, result)
                    if fd["right"][0] in closure:
                        fd["left"] = left_without
                        changed = True
                        break
    
    # Step 3: Remove redundant FDs
    final_result = []
    for i, fd in enumerate(result):
        # Create FD list without this FD
        others = result[:i] + result[i+1:]
        # Check if this FD is derivable from others
        closure = compute_closure(fd["left"], others)
        if fd["right"][0] not in closure:
            final_result.append(fd)
    
    return final_result


def solve_3nf(relation_name, attributes, functional_dependencies):
    """
    Return the 3NF decomposition using synthesis algorithm.

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
    # Handle empty FD case
    if not functional_dependencies:
        return [attributes[:]]
    
    # Step 1: Find minimal cover
    min_cover = minimal_cover(functional_dependencies, attributes)
    
    # Step 2: Create a relation for each FD
    relations = []
    for fd in min_cover:
        relation = sorted(list(set(fd["left"] + fd["right"])))
        relations.append(relation)
    
    # Step 3: Remove redundant relations (those contained in others)
    non_redundant = []
    for i, r1 in enumerate(relations):
        is_subset = False
        
        for j, r2 in enumerate(relations):
            if i != j and set(r1).issubset(set(r2)):
                is_subset = True
                break
            
            
        if not is_subset:
            non_redundant.append(r1)
    
    # Step 4: Ensure at least one relation contains a candidate key
    keys = find_candidate_keys(attributes, functional_dependencies)
    has_key = False
    for relation in non_redundant:
        for key in keys:
            
            if set(key).issubset(set(relation)):
                has_key = True
                break
        if has_key:
            break
    
    if not has_key and keys:
        # Add a relation with a candidate key
        non_redundant.append(sorted(keys[0]))
    
    return non_redundant

def get_applicable_fds(relation_attrs, fds):
        attr_set = set(relation_attrs)
        applicable = []
        for fd in fds:
            if set(fd["left"]).issubset(attr_set) and fd["right"][0] in attr_set:
                applicable.append(fd)
        return applicable
    
def find_bcnf_violation(relation_attrs, fds):
        """Find a BCNF violation in the relation, if any."""
        applicable_fds = get_applicable_fds(relation_attrs, fds)
        for fd in applicable_fds:

            if not is_superkey(fd["left"], relation_attrs, applicable_fds):
                return fd
        return None
    
def decompose_relation(relation_attrs, fds):
    """Recursively decompose a relation to BCNF."""
    violation = find_bcnf_violation(relation_attrs, fds)
    if violation is None:
        # Already in the BCNF
        return [sorted(relation_attrs)]
    
    # Decompose based on the violation
    l = violation["left"]
    r = violation["right"]
    
    # R1 = left + right
    r1_attrs = list(set(l + r))
    
    # R2 = relation_attrs - right
    r2_attrs = [a for a in relation_attrs if a not in r]
    
    # Recursively decompose
    result = []
    result.extend(decompose_relation(r1_attrs, fds))
    result.extend(decompose_relation(r2_attrs, fds))
    
    return result


def solve_bcnf(relation_name, attributes, functional_dependencies):
    """
    Return the BCNF decomposition using the decomposition algorithm.

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

    
    # Handle empty FD case
    if not functional_dependencies:
        return [attributes[:]]
    
    return decompose_relation(attributes[:], functional_dependencies)


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


