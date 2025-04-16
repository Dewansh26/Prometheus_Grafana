from flask import Flask, jsonify, request, render_template
import requests
import socket
import json
import os
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows all domains; adjust it if you need more security

HISTORY_FILE = "history.json"

def is_valid_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

def log_ip(ip):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    if ip not in history:
        history.insert(0, ip)
        history = history[:5]
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ip-lookup')
def ip_lookup():
    return render_template('ip_lookup.html')

@app.route('/dns-lookup')
def dns_lookup():
    return render_template('dns_lookup.html')

@app.route('/api/lookup')
def lookup():
    ip = request.args.get('ip')
    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    # If user enters domain, resolve to IP
    if not is_valid_ip(ip):
        try:
            ip = socket.gethostbyname(ip)
        except:
            return jsonify({"error": "Invalid IP or domain"}), 400

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            log_ip(ip)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "API failed", "details": str(e)}), 500

@app.route('/api/resolve_domain')
def resolve_domain():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Domain required"}), 400

    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        geolocation_data = response.json()
        if geolocation_data['status'] == 'success':
            return jsonify({
                "status": "success",
                "domain": domain,
                "ip": ip,
                "country": geolocation_data.get('country', 'N/A'),
                "city": geolocation_data.get('city', 'N/A'),
                "region": geolocation_data.get('regionName', 'N/A'),
                "zip": geolocation_data.get('zip', 'N/A'),
                "timezone": geolocation_data.get('timezone', 'N/A'),
                "isp": geolocation_data.get('isp', 'N/A'),
                "lat": geolocation_data.get('lat', 0),
                "lon": geolocation_data.get('lon', 0)
            })
        else:
            return jsonify({"error": "Failed to retrieve geolocation data"}), 500
    except socket.gaierror:
        return jsonify({"error": "Domain not found"}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/api/history')
def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    