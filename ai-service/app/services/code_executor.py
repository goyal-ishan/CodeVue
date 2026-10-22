import os
import re
import json
import tempfile
import subprocess
import httpx
from typing import Any, Dict, List

# Normalize endpoint path for both local Docker and public Piston
raw_url = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston").rstrip("/")
PISTON_API_URL = raw_url if raw_url.endswith("/execute") else f"{raw_url}/execute"

LANGUAGE_CONFIG = {
    "python": {"language": "python", "version": "*", "file_name": "solution.py"},
    "cpp": {"language": "c++", "version": "*", "file_name": "solution.cpp"},
    "java": {"language": "java", "version": "*", "file_name": "Main.java"},
}


# =========================================================================
# Python Test Harness
# =========================================================================
def _build_python_harness(user_code: str, test_cases: List[Dict[str, Any]]) -> str:
    """Wrap candidate Python code with an automated test runner."""
    return f"""
{user_code}

import json
import sys

test_cases = {json.dumps(test_cases)}
results = []

sol = Solution()
method_name = None
for attr in dir(sol):
    if not attr.startswith("_") and callable(getattr(sol, attr)):
        method_name = attr
        break

if not method_name:
    print(json.dumps({{"error": "No valid solution method found in Solution class"}}))
    sys.exit(0)

target_func = getattr(sol, method_name)

for idx, tc in enumerate(test_cases):
    inp = tc.get("input", {{}})
    expected = tc.get("expected_output")
    try:
        if isinstance(inp, dict):
            actual = target_func(**inp)
        else:
            actual = target_func(inp)

        # Allow flexible order for array comparisons
        passed = False
        if actual == expected:
            passed = True
        elif isinstance(actual, list) and isinstance(expected, list):
            try:
                passed = sorted(actual) == sorted(expected)
            except Exception:
                passed = False

        results.append({{
            "test_case": idx + 1,
            "passed": passed,
            "input": inp,
            "expected": expected,
            "actual": actual,
            "status": "PASSED" if passed else "WRONG_ANSWER"
        }})
    except Exception as e:
        results.append({{
            "test_case": idx + 1,
            "passed": False,
            "input": inp,
            "expected": expected,
            "actual": None,
            "error": str(e),
            "status": "RUNTIME_ERROR"
        }})

print("__CODEVUE_RESULTS_START__")
print(json.dumps(results))
print("__CODEVUE_RESULTS_END__")
"""


# =========================================================================
# C++ Test Harness
# =========================================================================
def _to_cpp_literal(val: Any) -> str:
    """Format Python values into valid C++ literals."""
    if isinstance(val, bool):
        return "true" if val else "false"
    elif isinstance(val, (int, float)):
        return str(val)
    elif isinstance(val, str):
        return json.dumps(val)
    elif isinstance(val, list):
        return "{" + ", ".join(_to_cpp_literal(x) for x in val) + "}"
    return "0"


def _build_cpp_harness(user_code: str, test_cases: List[Dict[str, Any]]) -> str:
    """Wrap candidate C++ code with standard headers and main() test runner."""
    headers = """
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <sstream>

using namespace std;

template<typename T>
void print_json(const T& val) { cout << val; }
void print_json(bool val) { cout << (val ? "true" : "false"); }
void print_json(const string& val) { cout << "\\"" << val << "\\""; }
void print_json(char val) { cout << "\\"" << val << "\\""; }

template<typename T>
void print_json(const vector<T>& vec) {
    cout << "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        print_json(vec[i]);
        if (i + 1 < vec.size()) cout << ", ";
    }
    cout << "]";
}
"""
    method_match = re.search(
        r"(?:[A-Za-z0-9_<>:&*]+)\s+([A-Za-z0-9_]+)\s*\(([^)]*)\)", user_code
    )
    method_name = method_match.group(1) if method_match else "twoSum"

    tests_logic = []
    for idx, tc in enumerate(test_cases):
        inp = tc.get("input", {})
        expected = tc.get("expected_output")

        if isinstance(inp, dict):
            args_list = ", ".join(_to_cpp_literal(v) for v in inp.values())
        else:
            args_list = _to_cpp_literal(inp)

        expected_literal = _to_cpp_literal(expected)
        test_case_num = idx + 1
        comma = "," if idx > 0 else ""

        tests_logic.append(f"""
    {{
        auto actual = sol.{method_name}({args_list});
        auto expected = {expected_literal};
        bool passed = (actual == expected);
        cout << "{comma}{{\\"test_case\\": {test_case_num}, \\"passed\\": " << (passed ? "true" : "false")
             << ", \\"status\\": \\"" << (passed ? "PASSED" : "WRONG_ANSWER") << "\\", "
             << "\\"expected\\": ";
        print_json(expected);
        cout << ", \\"actual\\": ";
        print_json(actual);
        cout << "}}";
    }}
""")

    runner = f"""
{headers}

{user_code}

int main() {{
    Solution sol;
    cout << "__CODEVUE_RESULTS_START__\\n[";
    {"".join(tests_logic)}
    cout << "]\\n__CODEVUE_RESULTS_END__" << endl;
    return 0;
}}
"""
    return runner


# =========================================================================
# Java Test Harness
# =========================================================================
def _to_java_literal(val: Any) -> str:
    """Format Python values into valid Java literals and array instantiations."""
    if isinstance(val, bool):
        return "true" if val else "false"
    elif isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        return f"{val}d"
    elif isinstance(val, str):
        return json.dumps(val)
    elif isinstance(val, list):
        if len(val) == 0:
            return "new int[]{}"
        first = val[0]
        if isinstance(first, int):
            return "new int[]{" + ", ".join(_to_java_literal(x) for x in val) + "}"
        elif isinstance(first, str):
            return "new String[]{" + ", ".join(_to_java_literal(x) for x in val) + "}"
        elif isinstance(first, list):
            return "new int[][]{" + ", ".join(_to_java_literal(x) for x in val) + "}"
        else:
            return "new Object[]{" + ", ".join(_to_java_literal(x) for x in val) + "}"
    return "null"


def _build_java_harness(user_code: str, test_cases: List[Dict[str, Any]]) -> str:
    """
    Wrap candidate Java Solution with reflection and runner logic in Main.java.
    """
    # Ensure Solution is not declared 'public' so Main can be the public entry point
    clean_code = re.sub(r"public\s+class\s+Solution", "class Solution", user_code)

    # Detect method name inside Solution
    method_match = re.search(
        r"(?:public\s+)?[A-Za-z0-9_<>\[\]]+\s+([A-Za-z0-9_]+)\s*\([^)]*\)",
        clean_code,
    )
    method_name = method_match.group(1) if method_match else "twoSum"

    tests_logic = []
    for idx, tc in enumerate(test_cases):
        inp = tc.get("input", {})
        expected = tc.get("expected_output")

        if isinstance(inp, dict):
            args_list = ", ".join(_to_java_literal(v) for v in inp.values())
        else:
            args_list = _to_java_literal(inp)

        expected_literal = _to_java_literal(expected)
        test_case_num = idx + 1
        comma = "," if idx > 0 else ""

        tests_logic.append(f"""
        try {{
            var actual = sol.{method_name}({args_list});
            var expected = {expected_literal};
            boolean passed = isEqual(actual, expected);
            System.out.print("{comma}{{\\"test_case\\": {test_case_num}, \\"passed\\": " + passed +
                ", \\"status\\": \\"" + (passed ? "PASSED" : "WRONG_ANSWER") + "\\", " +
                "\\"expected\\": " + toJson(expected) + ", \\"actual\\": " + toJson(actual) + "}}");
        }} catch (Throwable t) {{
            System.out.print("{comma}{{\\"test_case\\": {test_case_num}, \\"passed\\": false, \\"status\\": \\"RUNTIME_ERROR\\", \\"error\\": \\"" + cleanMsg(t.toString()) + "\\"}}");
        }}
""")

    runner = f"""
import java.util.*;
import java.io.*;

{clean_code}

public class Main {{
    static String cleanMsg(String msg) {{
        if (msg == null) return "Error";
        return msg.replace("\\"", "'").replace("\\n", " ");
    }}

    static String toJson(Object obj) {{
        if (obj == null) return "null";
        if (obj instanceof int[]) return Arrays.toString((int[]) obj);
        if (obj instanceof long[]) return Arrays.toString((long[]) obj);
        if (obj instanceof double[]) return Arrays.toString((double[]) obj);
        if (obj instanceof boolean[]) return Arrays.toString((boolean[]) obj);
        if (obj instanceof Object[]) return Arrays.deepToString((Object[]) obj);
        if (obj instanceof String) return "\\"" + obj + "\\"";
        return String.valueOf(obj);
    }}

    static boolean isEqual(Object a, Object b) {{
        if (a == null && b == null) return true;
        if (a == null || b == null) return false;
        if (a instanceof int[] && b instanceof int[]) {{
            int[] arrA = ((int[]) a).clone();
            int[] arrB = ((int[]) b).clone();
            Arrays.sort(arrA);
            Arrays.sort(arrB);
            return Arrays.equals(arrA, arrB);
        }}
        if (a instanceof Object[] && b instanceof Object[]) return Arrays.deepEquals((Object[]) a, (Object[]) b);
        return a.equals(b);
    }}

    public static void main(String[] args) {{
        Solution sol = new Solution();
        System.out.print("__CODEVUE_RESULTS_START__\\n[");
        {"".join(tests_logic)}
        System.out.println("]\\n__CODEVUE_RESULTS_END__");
    }}
}}
"""
    return runner


# =========================================================================
# Main Execution Dispatcher
# =========================================================================
async def execute_code(
    code: str,
    language: str,
    test_cases: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Dispatch code and test cases to the sandboxed execution engine."""
    lang_key = language.lower()
    if lang_key in ("c++", "cpp"):
        lang_key = "cpp"
    elif lang_key in ("python", "python3"):
        lang_key = "python"
    elif lang_key in ("java", "java17"):
        lang_key = "java"

    lang_info = LANGUAGE_CONFIG.get(lang_key)
    if not lang_info:
        return {
            "success": False,
            "error": f"Unsupported language: {language}",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "results": [],
        }

    if lang_key == "python":
        stitched_code = _build_python_harness(code, test_cases)
    elif lang_key == "cpp":
        stitched_code = _build_cpp_harness(code, test_cases)
    elif lang_key == "java":
        stitched_code = _build_java_harness(code, test_cases)
    else:
        stitched_code = code

    payload = {
        "language": lang_info["language"],
        "version": lang_info["version"],
        "files": [{"name": lang_info["file_name"], "content": stitched_code}],
        "run_timeout": 3000,
        "compile_timeout": 10000,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(PISTON_API_URL, json=payload)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Execution engine returned HTTP {response.status_code}",
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }

        piston_result = response.json()
        compile_data = piston_result.get("compile", {})
        if compile_data and compile_data.get("code", 0) != 0:
            return {
                "success": False,
                "error": compile_data.get("stderr", "Compilation failed."),
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }

        run_data = piston_result.get("run", {})
        stdout = run_data.get("stdout", "")
        stderr = run_data.get("stderr", "")

        if "__CODEVUE_RESULTS_START__" in stdout:
            parts = (
                stdout.split("__CODEVUE_RESULTS_START__")[1]
                .split("__CODEVUE_RESULTS_END__")[0]
                .strip()
            )
            parsed_results = json.loads(parts)
            passed_count = sum(1 for r in parsed_results if r.get("passed"))

            return {
                "success": True,
                "total_tests": len(test_cases),
                "passed_tests": passed_count,
                "results": parsed_results,
                "stdout": stdout,
                "stderr": stderr,
            }
        else:
            return {
                "success": False,
                "error": stderr or stdout or "Execution produced unexpected output format.",
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }

    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Execution timed out (Time Limit Exceeded). Check for infinite loops.",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "results": [],
        }
    except Exception as ex:
        return {
            "success": False,
            "error": f"Execution service error: {str(ex)}",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "results": [],
        }


def _run_locally(stitched_code: str, lang_key: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # 1. Python Execution
            if lang_key == "python":
                file_path = os.path.join(tmpdir, "solution.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(stitched_code)
                proc = subprocess.run(
                    ["python", file_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                stdout, stderr = proc.stdout, proc.stderr

            # 2. C++ Compilation and Execution
            elif lang_key == "cpp":
                src_path = os.path.join(tmpdir, "solution.cpp")
                bin_path = os.path.join(tmpdir, "solution.exe" if os.name == "nt" else "solution")
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(stitched_code)

                compile_proc = subprocess.run(
                    ["g++", "-O2", src_path, "-o", bin_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if compile_proc.returncode != 0:
                    return {
                        "success": False,
                        "error": compile_proc.stderr,
                        "total_tests": len(test_cases),
                        "passed_tests": 0,
                        "results": [],
                    }

                run_proc = subprocess.run(
                    [bin_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                stdout, stderr = run_proc.stdout, run_proc.stderr

            # 3. Java Compilation and Execution
            elif lang_key == "java":
                src_path = os.path.join(tmpdir, "Main.java")
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(stitched_code)

                compile_proc = subprocess.run(
                    ["javac", src_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if compile_proc.returncode != 0:
                    return {
                        "success": False,
                        "error": compile_proc.stderr,
                        "total_tests": len(test_cases),
                        "passed_tests": 0,
                        "results": [],
                    }

                run_proc = subprocess.run(
                    ["java", "-cp", tmpdir, "Main"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                stdout, stderr = run_proc.stdout, run_proc.stderr

            else:
                return {
                    "success": False,
                    "error": f"Language '{lang_key}' is not configured for local execution.",
                    "total_tests": len(test_cases),
                    "passed_tests": 0,
                    "results": [],
                }

            # Parse CodeVue Test Harness Output Markers
            if "__CODEVUE_RESULTS_START__" in stdout:
                parts = (
                    stdout.split("__CODEVUE_RESULTS_START__")[1]
                    .split("__CODEVUE_RESULTS_END__")[0]
                    .strip()
                )
                parsed = json.loads(parts)
                return {
                    "success": True,
                    "total_tests": len(test_cases),
                    "passed_tests": sum(1 for r in parsed if r.get("passed")),
                    "results": parsed,
                    "stdout": stdout,
                }

            return {
                "success": False,
                "error": stderr or stdout or "Execution error occurred.",
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Time Limit Exceeded (TLE). Check for infinite loops.",
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }
        except FileNotFoundError as fnf:
            compiler_name = "g++" if lang_key == "cpp" else "javac" if lang_key == "java" else "python"
            return {
                "success": False,
                "error": f"Compiler not found: '{compiler_name}' is not installed or not in your system PATH.",
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }
        except Exception as ex:
            return {
                "success": False,
                "error": f"Local execution error: {str(ex)}",
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }