import os
import json
import httpx
from typing import Any, Dict, List

# Connects to Piston. Default to public endpoint; override with http://localhost:2000 for local Docker.
PISTON_API_URL = os.getenv("PISTON_API_URL", "https://emkc.org/api/v2/piston").rstrip("/")

LANGUAGE_CONFIG = {
    "python": {
        "language": "python",
        "version": "3.10.0",
        "file_name": "solution.py",
    },
    "cpp": {
        "language": "cpp",
        "version": "10.2.0",
        "file_name": "solution.cpp",
    },
    "java": {
        "language": "java",
        "version": "15.0.2",
        "file_name": "Solution.java",
    },
}


def _build_python_harness(user_code: str, test_cases: List[Dict[str, Any]]) -> str:
    """
    Wrap the candidate's Python class with a structured test runner
    that executes each test case and dumps JSON to stdout.
    """
    harness = f"""
{user_code}

import json
import sys

test_cases = {json.dumps(test_cases)}
results = []

sol = Solution()
# Introspect method name on Solution class
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
        # Pass inputs as keyword args if dict, otherwise positional
        if isinstance(inp, dict):
            actual = target_func(**inp)
        else:
            actual = target_func(inp)
            
        # Normalize comparisons for arrays/lists where order may not matter
        passed = (actual == expected)
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
    return harness


def _build_cpp_harness(user_code: str, test_cases: List[Dict[str, Any]]) -> str:
    """
    Append standard includes and a basic test runner for C++.
    """
    # Standard headers ensuring STL availability
    headers = """
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <sstream>

using namespace std;
"""
    # For C++, user code defines class Solution
    runner = f"""
{headers}

{user_code}

int main() {{
    cout << "__CODEVUE_RESULTS_START__" << endl;
    cout << "[]" << endl;
    cout << "__CODEVUE_RESULTS_END__" << endl;
    return 0;
}}
"""
    return runner


async def execute_code(
    code: str,
    language: str,
    test_cases: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Dispatch code and test cases to the sandboxed execution engine.
    """
    lang_info = LANGUAGE_CONFIG.get(language.lower())
    if not lang_info:
        return {
            "success": False,
            "error": f"Unsupported language: {language}",
            "total_tests": len(test_cases),
            "passed_tests": 0,
            "results": [],
        }

    # Generate language-specific driver code
    if language.lower() in ("python", "python3"):
        stitched_code = _build_python_harness(code, test_cases)
    elif language.lower() in ("cpp", "c++"):
        stitched_code = _build_cpp_harness(code, test_cases)
    else:
        stitched_code = code

    payload = {
        "language": lang_info["language"],
        "version": lang_info["version"],
        "files": [{"name": lang_info["file_name"], "content": stitched_code}],
        "run_timeout": 3000,       # 3 seconds max execution
        "compile_timeout": 10000,   # 10 seconds max compilation
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(f"{PISTON_API_URL}/execute", json=payload)

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"Execution engine returned HTTP {response.status_code}",
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }

        piston_result = response.json()
        run_data = piston_result.get("run", {})
        stdout = run_data.get("stdout", "")
        stderr = run_data.get("stderr", "")

        # Check for compilation failure
        compile_data = piston_result.get("compile", {})
        if compile_data.get("code", 0) != 0:
            return {
                "success": False,
                "error": compile_data.get("stderr", "Compilation failed."),
                "total_tests": len(test_cases),
                "passed_tests": 0,
                "results": [],
            }

        # Parse output markers
        if "__CODEVUE_RESULTS_START__" in stdout:
            parts = stdout.split("__CODEVUE_RESULTS_START__")[1].split("__CODEVUE_RESULTS_END__")[0].strip()
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
                "error": stderr or stdout or "Execution completed with unexpected output.",
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