"""
Flask Web Server for CARPRICE AI (Stitch Frontend Integration)
Configured for local execution and web deployment (Port 7860).
Run with: python server.py
"""

import os
import sys
import threading
import webbrowser
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_from_directory

# Configure UTF-8 for console output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Project root setup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from src.predict import CarPricePredictor, USD_TO_INR

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize ML Predictor
predictor = CarPricePredictor()


@app.route('/')
def home():
    """Serves the main Stitch valuation studio dashboard."""
    return render_template('index.html')


@app.route('/graphs/<path:filename>')
def serve_graphs(filename):
    """Serves EDA and model evaluation graphs directly to the frontend."""
    graphs_dir = os.path.join(PROJECT_ROOT, 'graphs')
    return send_from_directory(graphs_dir, filename)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Accepts vehicle specification payload, generates ML prediction,
    and returns formatted Indian Rupee (₹ INR) results.
    """
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({'error': 'No input payload provided'}), 400

        # Predict price in USD and INR
        usd_price = predictor.predict(data)
        inr_price = usd_price * USD_TO_INR
        
        # Indian formatting
        if inr_price >= 10000000:
            lakh_str = f"₹ {inr_price / 10000000:.2f} Cr"
        else:
            lakh_str = f"₹ {inr_price / 100000:.2f} Lakh"

        rmse_inr = 665.62 * USD_TO_INR
        low_inr = max(125000.0, inr_price - rmse_inr)
        high_inr = inr_price + rmse_inr

        low_str = f"₹ {low_inr / 100000:.2f} Lakh"
        high_str = f"₹ {high_inr / 100000:.2f} Lakh"
        rmse_str = f"₹ {rmse_inr:,.0f}"

        # Cohort distribution metrics
        low_cohort = f"₹ {(inr_price * 0.82) / 100000:.2f} Lakh"
        med_cohort = f"₹ {(inr_price * 0.96) / 100000:.2f} Lakh"

        return jsonify({
            'success': True,
            'price_inr': round(inr_price, 2),
            'price_usd': round(usd_price, 2),
            'prediction_inr': round(inr_price, 2),
            'prediction_usd': round(usd_price, 2),
            'price_lakh_str': lakh_str,
            'price_inr_formatted': f"₹ {inr_price:,.0f}",
            'low_range_str': low_str,
            'high_range_str': high_str,
            'rmse_inr_str': rmse_str,
            'low_cohort_str': low_cohort,
            'median_cohort_str': med_cohort,
            'vehicle': f"{data.get('make_year', 2020)} {data.get('brand', '')} {data.get('model', '')}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict_bulk', methods=['POST'])
def api_predict_bulk():
    """
    Accepts bulk list of car dictionaries, returns evaluated prices in INR.
    """
    try:
        req_data = request.get_json(force=True)
        cars = req_data.get('cars', req_data) if isinstance(req_data, dict) else req_data
        if not isinstance(cars, list):
            return jsonify({'error': 'Payload must be a list of vehicles'}), 400

        results = []
        total_inr = 0.0
        for c in cars:
            usd = predictor.predict(c)
            inr = usd * USD_TO_INR
            total_inr += inr
            results.append({
                'brand': c.get('brand', ''),
                'model': c.get('model', ''),
                'make_year': c.get('make_year', 2022),
                'price_usd': round(usd, 2),
                'price_inr': round(inr, 2),
                'price_lakh': round(inr / 100000, 2),
                'price_inr_formatted': f"₹ {inr:,.0f}"
            })

        return jsonify({
            'success': True,
            'count': len(results),
            'total_inr': round(total_inr, 2),
            'total_lakh': round(total_inr / 100000, 2),
            'cars': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/model-comparison', methods=['GET'])
def api_comparison():
    """Returns actual benchmark comparison table."""
    csv_path = os.path.join(PROJECT_ROOT, 'results', 'model_comparison.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df['MAE_INR'] = (df['MAE'] * USD_TO_INR).round(0)
        df['RMSE_INR'] = (df['RMSE'] * USD_TO_INR).round(0)
        return jsonify(df.to_dict(orient='records'))
    return jsonify([])


def open_browser(port):
    """Opens browser automatically after short delay."""
    url = f"http://localhost:{port}"
    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    # Default to 7860 (standard local demo port) or PORT env
    port = int(os.environ.get('PORT', 7860))
    is_cloud = os.environ.get('CLOUD_ENV') is not None or os.environ.get('DOCKER') is not None
    
    print(f"================================================================")
    print(f"   CARPRICE AI - STITCH FRONTEND SERVER (INDIAN RUPEES INR)     ")
    print(f"   Listening on: http://0.0.0.0:{port}                          ")
    print(f"================================================================")
    
    # Auto-open desktop browser only in local mode
    if not is_cloud:
        threading.Timer(1.2, open_browser, args=[port]).start()
        
    app.run(host='0.0.0.0', port=port, debug=False)
