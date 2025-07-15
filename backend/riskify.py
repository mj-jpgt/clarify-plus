#!/usr/bin/env python3
"""
Clarify+ NumiCraft Module (riskify.py)

This module analyzes text to find and interpret numerical risk data.
It extracts risk-related numbers (e.g., percentages, "X in Y" formats)
and generates visual and textual aids to improve risk literacy.
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

import matplotlib.pyplot as plt
from rich.console import Console

# Regular expressions to find different formats of risk data
RISK_PATTERNS = {
    "percentage": re.compile(r'(\d{1,3}(?:\.\d+)?)\s?%'),
    "x_in_y": re.compile(r'(\d+)\s+(?:in|out of)\s+([\d,]+)')
}

BERLIN_NUMERACY_QUESTIONS = [
    {
        "id": "bnt_1",
        "question": "Imagine we are throwing a five-sided die 50 times. On average, out of these 50 throws how many times would this five-sided die show an odd number (1, 3 or 5)?",
        "answer": 30,
        "unit": "out of 50 throws"
    },
    {
        "id": "bnt_2",
        "question": "Out of 1,000 people in a small town 500 are members of a choir. Out of these 500 members in the choir 100 are men. Out of the 500 inhabitants that are not in the choir 300 are men. What is the probability that a randomly drawn man is a member of the choir?",
        "answer": 25,
        "unit": "%"
    },
    {
        "id": "bnt_3",
        "question": "Imagine we are throwing a loaded die (6 sides). The probability that the die shows a 6 is twice as high as the probability of each of the other numbers. On average, out of these 70 throws, how many times would the die show the number 6?",
        "answer": 20,
        "unit": "out of 70 throws"
    }
]

class Riskify:
    """Analyzes text to find and interpret numerical risk data."""

    def __init__(self, verbose: bool = False):
        """Initialize the Riskify analyzer."""
        self.verbose = verbose

    def run(self, text: str, artifacts_dir: Optional[Path] = None) -> Dict:
        """
        Run the full risk analysis on the given text.
        This is the primary entry point for API usage.
        """
        if self.verbose:
            print(f"Running risk analysis on text ({len(text)} characters)...")
        
        analysis_results = self.analyze_text(text, artifacts_dir)

        if self.verbose:
            print("Risk analysis complete.")

        return analysis_results

    def analyze_text(self, text: str, artifacts_dir: Optional[Path] = None) -> Dict:
        """Find, analyze, and generate artifacts for all risk-related numbers."""
        found_risks = []

        # Find percentages
        for match in RISK_PATTERNS["percentage"].finditer(text):
            risk_item = {
                "type": "percentage",
                "value": float(match.group(1)),
                "context": self._get_context(text, match),
            }
            if artifacts_dir:
                icon_path = artifacts_dir / f"risk_{len(found_risks)}_icon.png"
                self.generate_icon_array(risk_item["value"], str(icon_path))
                risk_item["icon_array_path"] = str(icon_path)
            risk_item["mcq"] = self.generate_mcq(risk_item)
            found_risks.append(risk_item)

        # Find "X in Y" formats
        for match in RISK_PATTERNS["x_in_y"].finditer(text):
            x_val = int(match.group(1).replace(',', ''))
            y_val = int(match.group(2).replace(',', ''))
            risk_item = {
                "type": "x_in_y",
                "x": x_val,
                "y": y_val,
                "value": (x_val / y_val) * 100 if y_val != 0 else 0,
                "context": self._get_context(text, match),
            }
            if artifacts_dir:
                icon_path = artifacts_dir / f"risk_{len(found_risks)}_icon.png"
                self.generate_icon_array(risk_item["value"], str(icon_path))
                risk_item["icon_array_path"] = str(icon_path)
            risk_item["mcq"] = self.generate_mcq(risk_item)
            found_risks.append(risk_item)
        
        if self.verbose:
            print(f"Found {len(found_risks)} risk statements.")

        return {"risks": found_risks}

    def _get_context(self, text: str, match: re.Match, window: int = 50) -> str:
        """Extract the context (surrounding text) for a given match."""
        start = max(0, match.start() - window)
        end = min(len(text), match.end() + window)
        return text[start:end].strip().replace('\n', ' ')

    def generate_icon_array(self, risk_value: float, output_path: str) -> str:
        """
        Generate and save a 10x10 icon array representing the risk.
        """
        if not (0 <= risk_value <= 100):
            if self.verbose:
                print(f"Warning: Risk value {risk_value} is outside the 0-100 range. Clamping.")
            risk_value = max(0, min(100, risk_value))

        color_unaffected = '#d3d3d3'
        color_affected = '#0072b2'

        x_coords = [i % 10 for i in range(100)]
        y_coords = [i // 10 for i in range(100)]

        num_affected = round(risk_value)
        colors = [color_affected] * num_affected + [color_unaffected] * (100 - num_affected)

        fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
        ax.scatter(x_coords, y_coords, c=colors, s=100, marker='s')

        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        plt.tight_layout(pad=0)
        
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

        if self.verbose:
            print(f"Generated icon array at {output_path}")

        return output_path

    def get_berlin_numeracy_questions(self) -> List[Dict[str, Any]]:
        """Returns the set of Berlin Numeracy Test questions."""
        # Return a copy to prevent modification of the original list
        return [q.copy() for q in BERLIN_NUMERACY_QUESTIONS]

    def score_berlin_numeracy_test(self, user_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scores user responses to the Berlin Numeracy Test.
        
        Args:
            user_responses: A list of dicts, each with 'id' and 'answer'.
        """
        score = 0
        detailed_responses = []
        question_map = {q['id']: q for q in BERLIN_NUMERACY_QUESTIONS}

        for resp in user_responses:
            q_id = resp.get('id')
            user_answer = resp.get('answer')
            correct_q = question_map.get(q_id)

            if correct_q and user_answer is not None:
                is_correct = (user_answer == correct_q['answer'])
                if is_correct:
                    score += 1
                detailed_responses.append({
                    "question": correct_q['question'],
                    "user_answer": user_answer,
                    "correct_answer": correct_q['answer'],
                    "is_correct": is_correct
                })

        return {"score": score, "total": len(BERLIN_NUMERACY_QUESTIONS), "responses": detailed_responses}

    def generate_mcq(self, risk_data: Dict) -> Dict:
        """Generates a multiple-choice question to test understanding of the risk."""
        risk_type = risk_data.get("type")
        risk_value = risk_data.get("value")

        if risk_type is None or risk_value is None:
            return {}

        question_text = f"The statement mentions a risk of {risk_value:.1f}%. This is the same as..."
        
        correct_answer_val = round(risk_value)
        correct_answer = f"{correct_answer_val} people out of 100."
        
        distractor1_val = 100 - correct_answer_val
        distractor1 = f"{distractor1_val} people out of 100."
        
        distractor2_val = correct_answer_val
        distractor2 = f"{distractor2_val} people out of 1,000."
        
        distractor3 = "It is impossible to say from the information given."

        choices = [
            {"text": correct_answer, "is_correct": True},
            {"text": distractor1, "is_correct": False},
            {"text": distractor2, "is_correct": False},
            {"text": distractor3, "is_correct": False},
        ]
        random.shuffle(choices)

        return {
            "question": question_text,
            "choices": choices
        }


# --- CLI App ---

def main():
    """Main function to run the NumiCraft analysis from the command line."""
    parser = argparse.ArgumentParser(description="NumiCraft: Risk Literacy Analysis Tool")
    parser.add_argument("source", help="Path to a text file, PDF, or text string to analyze.")
    parser.add_argument("-o", "--output", dest="output_path", type=Path, help="Output JSON file path.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument("--numeracy-test", action="store_true", help="Run the Berlin Numeracy Test interactively.")
    
    args = parser.parse_args()
    console = Console()
    riskify = Riskify(verbose=args.verbose)

    text = ""
    source_path = Path(args.source)
    if source_path.is_file():
        if args.verbose:
            console.log(f"Reading from file: {source_path}")
        text = source_path.read_text(encoding="utf-8")
    else:
        if args.verbose:
            console.log("Analyzing provided text string.")
        text = args.source

    if not text:
        console.log("[red]Error: Input text is empty.[/red]")
        sys.exit(1)

    artifacts_dir = None
    if args.output_path:
        artifacts_dir = args.output_path.parent / f"{args.output_path.stem}_artifacts"
        artifacts_dir.mkdir(exist_ok=True)

    analysis_results = riskify.run(text, artifacts_dir=artifacts_dir)

    if args.numeracy_test:
        console.print("\n[bold]Berlin Numeracy Test[/bold]")
        console.print("Please answer the following three questions. Do not use a calculator.")
        
        questions = riskify.get_berlin_numeracy_questions()
        user_responses = []
        for q in questions:
            console.print(f"\n[bold]Question:[/] {q['question']}")
            try:
                user_input = console.input(f"Your answer ({q['unit']}): ")
                user_responses.append({"id": q['id'], "answer": int(user_input)})
            except (ValueError, TypeError):
                console.print("[red]Invalid input. Skipping question.[/red]")
                user_responses.append({"id": q['id'], "answer": None})

        numeracy_results = riskify.score_berlin_numeracy_test(user_responses)
        analysis_results['berlin_numeracy_test'] = numeracy_results
        console.print(f"\n[bold]Your Berlin Numeracy Score: {numeracy_results['score']} out of {numeracy_results['total']}[/bold]")

    if args.output_path:
        args.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2)
        console.log(f"[bold green]Results saved to {args.output_path}[/bold green]")
    else:
        console.print(analysis_results)

if __name__ == "__main__":
    main()
