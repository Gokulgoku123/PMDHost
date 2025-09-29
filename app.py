from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"status": "ok", "msg": "PMD API is running"}

@app.route("/run", methods=["POST"])
def run_pmd():
    data = request.get_json() or {}
    classes = data.get("classes", [])

    # Instead of real PMD, just echo back the input
    combined_violations = []
    for cls in classes:
        combined_violations.append({
            "rule": "DummyRule",
            "message": f"Simulated violation in {cls.get('name')}",
            "line": 1,
            "severity": "Low",
            "className": cls.get("name", "UnknownClass")
        })

    return jsonify({
        "violations": combined_violations,
        "warnings": ["⚠️ Java not yet integrated on Railway"]
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
