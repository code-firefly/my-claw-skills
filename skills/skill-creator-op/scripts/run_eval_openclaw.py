#!/usr/bin/env python3
"""
Run skill evaluation for OpenClaw.

This script helps organize and run evaluations using OpenClaw's sessions_spawn.
Unlike Claude Code's run_eval.py (which uses claude -p), this script prepares
the eval structure but relies on the agent to actually spawn sessions.

Usage:
    # Step 1: Prepare eval structure
    python scripts/run_eval_openclaw.py --prepare --eval-set evals/evals.json --output-dir eval-results/iteration-1

    # Step 2: The agent will spawn sessions for each test case
    # (This is done manually or via a parent agent using sessions_spawn)

    # Step 3: Run grader to evaluate results
    python scripts/run_eval_openclaw.py --grade --output-dir eval-results/iteration-1
"""

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Any


def load_eval_set(eval_set_path: Path) -> tuple[str, list[dict[str, Any]]]:
    """Load evaluation set from JSON file.

    Returns:
        (skill_name, evals_list) where evals_list is the list of test cases
    """
    data = json.loads(eval_set_path.read_text())

    # Handle both formats:
    # 1. { "skill_name": "...", "evals": [...] }
    # 2. Direct list of evals
    if isinstance(data, dict) and "evals" in data:
        return data["skill_name"], data["evals"]
    elif isinstance(data, list):
        # Direct list, assume skill name is "unknown" or extract from first item
        skill_name = data[0].get("skill_name", "unknown") if data else "unknown"
        return skill_name, data
    else:
        # Assume it's the old format (dict with evals)
        return data.get("skill_name", "unknown"), data.get("evals", [])


def prepare_eval_structure(
    eval_set: list[dict[str, Any]],
    skill_name: str,
    output_dir: Path,
    eval_set_path: Path,
    create_baseline: bool = True,
) -> dict[str, Any]:
    """Prepare directory structure for evaluation.

    Creates:
    - output_dir/
      - baseline/          # Results without the skill
      - with_skill/         # Results with the skill
      - eval_set.json       # Copy of eval set for reference

    For each test case in eval_set, creates:
    - baseline/test_<id>/
      - transcript.md      # Placeholder
      - outputs/           # Placeholder
    - with_skill/test_<id>/
      - transcript.md      # Placeholder
      - outputs/           # Placeholder
    """
    output_dir = Path(output_dir)
    baseline_dir = output_dir / "baseline"
    with_skill_dir = output_dir / "with_skill"

    # Create directories
    for d in [output_dir, baseline_dir, with_skill_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Copy eval set for reference
    shutil.copy(eval_set_path, output_dir / "eval_set.json")

    # Create structure for each test case
    for item in eval_set:
        test_id = item["id"]
        test_name = f"test_{test_id:03d}"

        for variant_dir in [baseline_dir, with_skill_dir]:
            test_dir = variant_dir / test_name
            test_dir.mkdir(exist_ok=True)

            # Create placeholders
            (test_dir / "transcript.md").write_text(f"# Test {test_id}\n\n*Transcript will be populated by the agent*\n")
            (test_dir / "outputs").mkdir(exist_ok=True)

            # Copy any input files
            for file_path in item.get("files", []):
                src = Path(file_path)
                if src.exists():
                    shutil.copy(src, test_dir / src.name)

    return {
        "output_dir": str(output_dir),
        "skill_name": skill_name,
        "test_cases": len(eval_set),
        "baseline_dir": str(baseline_dir),
        "with_skill_dir": str(with_skill_dir),
    }


def generate_session_spawn_instructions(
    eval_set: list[dict[str, Any]],
    skill_name: str,
    output_dir: Path,
    variant: str = "with_skill",  # or "baseline"
) -> str:
    """Generate instructions for the agent to spawn evaluation sessions.

    Returns a markdown string that tells the agent:
    1. How to use sessions_spawn for each test case
    2. Where to save the transcript and outputs
    3. What skill to load (if variant is "with_skill")
    """
    instructions = [
        f"# Evaluation Instructions: {variant}",
        "",
        f"**Skill:** {skill_name}",
        f"**Output Directory:** {output_dir}",
        "",
        "## Task",
        "",
        "For each test case below, spawn an OpenClaw sub-session and run the prompt. "
        "Save the results to the specified directory.",
        "",
        f"## Session Spawn Parameters",
        "",
        f"- Use `runtime=\"acp\"`",
        f"- Use `mode=\"run\"` (one-shot execution)",
        f"- Set appropriate `timeoutSeconds` based on the task complexity (default: 300)",
        "",
        f"{'- The skill \"{skill_name}\" will be automatically available' if variant == 'with_skill' else '- Run without the skill (baseline)'}",
        "",
        "## Test Cases",
        "",
    ]

    for item in eval_set:
        test_id = item["id"]
        test_name = f"test_{test_id:03d}"
        target_dir = output_dir / variant / test_name

        instructions.append(f"### Test {test_id}: {item.get('name', 'Untitled')}")
        instructions.append("")
        instructions.append(f"**Prompt:** {item['prompt']}")
        instructions.append("")
        instructions.append(f"**Expected Output:** {item['expected_output']}")
        instructions.append("")

        if item.get("files"):
            instructions.append("**Input Files:**")
            for f in item["files"]:
                src = Path(f)
                instructions.append(f"- {src.name} (located in {target_dir})")
            instructions.append("")

        instructions.append(f"**Save Results To:** `{target_dir}/`")
        instructions.append("- `transcript.md` - Full conversation transcript")
        instructions.append("- `outputs/` - Any generated files")
        instructions.append("")

        instructions.append("```markdown")
        instructions.append("# How to run this test case")
        instructions.append("")
        instructions.append("Use sessions_spawn with the following parameters:")
        instructions.append("")
        instructions.append("```")
        instructions.append(f"sessions_spawn(")
        instructions.append(f'    task="{item["prompt"]}",')
        instructions.append(f'    runtime="acp",')
        instructions.append(f'    mode="run",')
        instructions.append(f'    timeoutSeconds=300,')
        instructions.append(f"    cwd=\"{target_dir}\",")
        instructions.append(f")")
        instructions.append("```")
        instructions.append("")
        instructions.append("Then save the transcript and outputs.")
        instructions.append("")
        instructions.append("---")
        instructions.append("")

    return "\n".join(instructions)


def generate_grader_instructions(
    output_dir: Path,
    eval_set_path: Path,
) -> str:
    """Generate instructions for the grader agent."""
    instructions = [
        "# Grader Instructions",
        "",
        f"**Evaluation Results:** {output_dir}",
        f"**Eval Set:** {eval_set_path}",
        "",
        "## Task",
        "",
        "Read the eval set and evaluate the outputs in both `baseline/` and `with_skill/` directories. "
        "Follow the grading criteria in `agents/grader.md`.",
        "",
        "## Process",
        "",
        "1. Load the eval set from `eval_set.json`",
        "2. For each test case, compare baseline vs with_skill results",
        "3. For each assertion in the eval set, determine PASS/FAIL",
        "4. Generate grading.json in each test directory",
        "",
        "## Output Format",
        "",
        "Save results as `grading.json` in each test directory following the schema in `references/schemas.md`.",
        "",
        "## Expected Structure",
        "",
        "```",
        f"{output_dir}/",
        "  ├── eval_set.json",
        "  ├── baseline/",
        "  │   └── test_001/",
        "  │       ├── transcript.md",
        "  │       ├── outputs/",
        "  │       └── grading.json",
        "  └── with_skill/",
        "      └── test_001/",
        "          ├── transcript.md",
        "          ├── outputs/",
        "          └── grading.json",
        "```",
    ]

    return "\n".join(instructions)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw skill evaluation helper")
    parser.add_argument("--action", required=True, choices=["prepare", "spawn-instructions", "grade-instructions"],
                       help="Action to perform")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-name", help="Skill name (overrides the one in eval_set.json)")
    parser.add_argument("--output-dir", required=True, help="Output directory for results")
    parser.add_argument("--variant", choices=["baseline", "with_skill"], default="with_skill",
                       help="Variant for spawn instructions")
    args = parser.parse_args()

    eval_set_path = Path(args.eval_set)
    output_dir = Path(args.output_dir)
    loaded_skill_name, eval_set = load_eval_set(eval_set_path)

    # Determine skill name (command-line arg overrides file)
    skill_name = args.skill_name or loaded_skill_name

    if args.action == "prepare":
        print("Preparing evaluation structure...")
        result = prepare_eval_structure(eval_set, skill_name, output_dir, eval_set_path)
        print(json.dumps(result, indent=2))
        print(f"\n✓ Eval structure prepared at: {output_dir}")
        print(f"  - Test cases: {result['test_cases']}")
        print(f"  - Baseline: {result['baseline_dir']}")
        print(f"  - With skill: {result['with_skill_dir']}")

    elif args.action == "spawn-instructions":
        print("Generating session spawn instructions...")
        instructions = generate_session_spawn_instructions(eval_set, skill_name, output_dir, args.variant)
        instructions_file = output_dir / f"{args.variant}_instructions.md"
        instructions_file.write_text(instructions)
        print(f"✓ Instructions saved to: {instructions_file}")
        print(f"\nTo run the evaluation, send these instructions to an agent with sessions_spawn access.")

    elif args.action == "grade-instructions":
        print("Generating grader instructions...")
        instructions = generate_grader_instructions(output_dir, eval_set_path)
        instructions_file = output_dir / "grader_instructions.md"
        instructions_file.write_text(instructions)
        print(f"✓ Grader instructions saved to: {instructions_file}")
        print(f"\nTo grade the results, send these instructions to an agent with grader capabilities.")


if __name__ == "__main__":
    main()
