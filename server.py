# File: server.py

from flask import Flask, request, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

script_process = None

@app.route('/run-script', methods=['POST'])
def run_script():
    global script_process
    script_path = "./script.sh"
    
    if not os.path.exists(script_path):
        return jsonify({"error": "Script not found"}), 404

    if script_process and script_process.poll() is None:
        return jsonify({"error": "Script is already running"}), 400

    try:
        script_process = subprocess.Popen(["bash", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({"message": "Script started successfully", "pid": script_process.pid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop-script', methods=['POST'])
def stop_script():
    global script_process
    
    if script_process is None or script_process.poll() is not None:
        return jsonify({"error": "No script is currently running"}), 400

    try:
        script_process.terminate()
        script_process.wait()  # Wait for process to terminate
        return jsonify({"message": "Script stopped successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

