from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import json

app = Flask(__name__)

PMD_PATH = "./pmd-bin-7.17.0/bin/run.sh"
RULESET = "rulesets/apex/quickstart.xml"

@app.route("/run", methods=["POST"])
def run_pmd():
    data = request.get_json() or {}
    classes = data.get("classes", [])

    combined_violations = []
    warnings_list = []

    for cls in classes:
        name = cls.get("name", "UnknownClass")
        source_code = cls.get("source", "")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".cls", mode="w", encoding="utf-8") as tmp:
            tmp.write(source_code)
            tmp_path = tmp.name

        # Run PMD
        result = subprocess.run([
            "java", "-cp", "./pmd-bin-7.17.0/lib/*",
            "net.sourceforge.pmd.PMD",
            "-d", tmp_path,
            "-R", RULESET,
            "-f", "json"
        ], capture_output=True, text=True)

        os.remove(tmp_path)

        try:
            parsed_output = json.loads(result.stdout) if result.stdout else {}
            files = parsed_output.get("files", [])
            for f in files:
                for v in f.get("violations", []):
                    v["className"] = name
                    combined_violations.append(v)
        except Exception as e:
            combined_violations.append({"parseError": str(e), "className": name})

        if result.stderr:
            warnings_list.append(f"Class {name}: {result.stderr.strip()}")

    return jsonify({
        "violations": combined_violations,
        "warnings": warnings_list
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
