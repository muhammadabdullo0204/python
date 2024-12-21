from flask import Flask, request, jsonify
from flask_cors import CORS  
import subprocess
import tempfile
import os

app = Flask(__name__)
CORS(app)  


@app.route('/run_code', methods=['POST'])
def run_code():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')

    try:
        if language == 'python':
            output = run_python(code)
        elif language == 'cpp':
            output = run_cpp(code)
 
        else:
            return jsonify({"error": "Unsupported language"}), 400
        
        return jsonify({"output": output}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_python(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
        temp_file.write(code.encode())
        temp_file.close()
        result = subprocess.run(['python3', temp_file.name], capture_output=True, text=True)  # Use python3 instead of python
        os.remove(temp_file.name)
        return result.stdout if result.returncode == 0 else result.stderr

def run_cpp(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.cpp') as temp_file:
        temp_file.write(code.encode())
        temp_file.close()
        executable = temp_file.name.replace('.cpp', '')
        subprocess.run(['g++', temp_file.name, '-o', executable], capture_output=True, text=True)
        os.remove(temp_file.name)
        result = subprocess.run([executable], capture_output=True, text=True)
        os.remove(executable)
        return result.stdout if result.returncode == 0 else result.stderr


if __name__ == '__main__':
    app.run(debug=True)
