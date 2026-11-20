import cmseekdb.basic as cmseek  # All the basic functions
import cmseekdb.core as core
from flask import Flask, request, jsonify

app = Flask(__name__)

global _verbose
_verbose = False  # Verbose mode for API, so that it prints more info to the console

@app.route('/')
def index():
    return jsonify({
        "service": "CMSeeK API",
        "status": "ok",
        "description": "CMSeeK API for scanning websites and detecting the underlying CMS and related metadata.",
        "endpoints": {
            "GET /health": "Check whether the API service is running correctly.",
            "POST /scan": "Scan a target URL and return detection results in JSON format."
        },
        "example": {
            "method": "POST",
            "path": "/scan",
            "body": {
                "url": "https://example.com",
                "cua": "Mozilla/5.0 (compatible; CMSeeK API)"
            }
        },
        "notes": {
            "url_required": "The 'url' field is required for the scan endpoint.",
            "cua_optional": "The 'cua' field is optional and is used as the custom User-Agent string for the request. It will default to a random User-Agent if not provided."
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    # Not really sure what to check here, but we can at least return a simple status message
    return jsonify({"status": "healthy"}), 200

@app.route('/scan', methods=['POST'])
def scan_endpoint():
    global _verbose
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "Missing required parameter: url"}), 400

    try:
        # Validate the URL format before proceeding
        if not cmseek.validate_url(url):
            return jsonify({"error": "Invalid URL format. Please provide a valid target URL."}), 400
        # Set up Results dir while also checking if the URL is valid, all from process url
        target = cmseek.process_url(url)
        if target == '0':
            return jsonify({"error": "Invalid URL format. Please provide a valid target URL."}), 400

        # Yuh we can actually put anything in the cua field
        cua = data.get('cua') or cmseek.randomua("ohicantypeanythinginherethatsprettycoolilikecatsbtw")
        if _verbose:
            # Run the scan while not suppressing output to the console, maybe someone will find it useful
            result = core.main_proc(target, cua, should_return=True, silent=False)
        else:
            # Well supress the output to console and still get the result
            result = core.main_proc(target, cua, should_return=True, silent=True)

        if not result:
            # Fallback if scan failed for some reason
            return jsonify({"error": "Scan could not be completed."}), 500

        if result.get("success") is False:
            # We use success to flag if its a 400 errir or 200 succes, 500 is reseved for internal server errors
            return jsonify({
                "site": url,
                "target": target,
                "result": result,
                "status": "failed"
            }), 400

        return jsonify({
            "site": url,
            "target": target,
            "result": result,
            "status": "success"
        }), 200
    except Exception as exc:
        return jsonify({
            "error": "Scan failed",
            "details": str(exc),
            "site": url
        }), 500


def start(port: int, host: str, verbose: bool = False):
    # We use _verbose cause verbose is already used in the func, also use it as a global so other endpoints can use it too
    global _verbose
    _verbose = bool(verbose)
    print(cmseek.bold + cmseek.fgreen + f"API Mode Enabled - Running on Port {port} and Host {host}" + cmseek.cln)
    print("")
    app.run(host=host, port=port, debug=False)
