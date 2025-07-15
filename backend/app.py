#!/usr/bin/env python3
"""
Clarify+ Backend API (app.py)

This Flask application provides three endpoints:
1. /process: Runs the full analysis pipeline on a given URL.
2. /numeracy-questions: Returns the Berlin Numeracy Test questions.
3. /numeracy-score: Scores user responses to the numeracy test.
"""

import json
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from .scraper import Scraper
from .equicheck import EquiCheck
from .riskify import Riskify

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the analysis tools
scraper = Scraper(verbose=True)
equicheck = EquiCheck(verbose=True)
riskify = Riskify(verbose=True)

@app.route('/process', methods=['GET'])
def process_url():
    """
    Processes a URL to perform a full analysis.
    Expects a 'url' query parameter.
    e.g., /process?url=http://example.com
    """
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "'url' query parameter is required."}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            scraped_output_path = temp_path / "scraped_content.json"
            
            # 1. Scrape content
            scraper.run(url, scraped_output_path)
            with open(scraped_output_path, 'r', encoding='utf-8') as f:
                scraped_data = json.load(f)
            text_content = scraped_data.get("text", "")

            if not text_content:
                return jsonify({"error": "Could not extract text from the URL."}), 500

            # 2. Run EquiCheck analysis
            equicheck_results = equicheck.run(text_content)

            # 3. Run Riskify analysis
            riskify_artifacts_dir = temp_path / "riskify_artifacts"
            riskify_artifacts_dir.mkdir(exist_ok=True)
            riskify_results = riskify.run(text_content, artifacts_dir=riskify_artifacts_dir)

            # 4. Combine results
            final_results = {
                "source_url": url,
                "scraped_content": scraped_data,
                "equicheck_analysis": equicheck_results,
                "riskify_analysis": riskify_results
            }
            return jsonify(final_results)

    except Exception as e:
        app.logger.error(f"An error occurred during processing: {e}", exc_info=True)
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

@app.route('/numeracy-questions', methods=['GET'])
def get_numeracy_questions():
    """Returns the list of Berlin Numeracy Test questions."""
    try:
        questions = riskify.get_berlin_numeracy_questions()
        # Remove the answer before sending to the client
        for q in questions:
            del q['answer']
        return jsonify(questions)
    except Exception as e:
        app.logger.error(f"Error getting numeracy questions: {e}", exc_info=True)
        return jsonify({"error": "Could not retrieve numeracy questions."}), 500

@app.route('/numeracy-score', methods=['POST'])
def score_numeracy_test():
    """Scores the user's responses to the Berlin Numeracy Test."""
    user_responses = request.json
    if not user_responses or not isinstance(user_responses, list):
        return jsonify({"error": "Invalid or missing JSON payload."}), 400

    try:
        results = riskify.score_berlin_numeracy_test(user_responses)
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Error scoring numeracy test: {e}", exc_info=True)
        return jsonify({"error": "Could not score numeracy test."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
