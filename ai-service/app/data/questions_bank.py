QUESTION_BANK = {
    "two-sum": {
        "id": "two-sum",
        "title": "Two Sum",
        "topic": "arrays-strings",
        "difficulty": "Easy",
        "duration_seconds": 25 * 60,
        "description": (
            "Given an array of integers nums and an integer target, "
            "return the indices of two distinct elements whose sum "
            "equals target. Exactly one valid answer exists."
        ),
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Exactly one valid answer exists.",
            "You cannot use the same element twice.",
        ],
        "examples": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0,1]",
                "explanation": "nums[0] + nums[1] = 9.",
            },
            {
                "input": "nums = [3,2,4], target = 6",
                "output": "[1,2]",
                "explanation": "nums[1] + nums[2] = 6.",
            },
        ],
        "test_cases": [
            {
                "input": {"nums": [2, 7, 11, 15], "target": 9},
                "expected_output": [0, 1],
            },
            {
                "input": {"nums": [3, 2, 4], "target": 6},
                "expected_output": [1, 2],
            },
        ],
    },
}