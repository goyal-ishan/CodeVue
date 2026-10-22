QEUSTION_BANK = {
# =========================================================================
# Arrays & Strings
# =========================================================================
"two-sum": {
"id": "two-sum",
"title": "Two Sum",
"topic": "arrays-strings",
"difficulty": "Easy",
"duration_seconds": 25 * 60,
"description": (
"Given an integer array nums and an integer target, find and return "
"the indices of the two elements that sum up to target. You may assume "
"that each test input has strictly one valid solution, and you cannot "
"use the exact same element index twice."
),
"constraints": [
"2 <= nums.length <= 10^4",
"-10^9 <= nums[i] <= 10^9",
"-10^9 <= target <= 10^9",
"Exactly one valid solution exists.",
],
"examples": [
{
"input": "nums = [2, 7, 11, 15], target = 9",
"output": "[0, 1]",
"explanation": "nums[0] + nums[1] equals 9, so [0, 1] is returned.",
},
{
"input": "nums = [3, 2, 4], target = 6",
"output": "[1, 2]",
"explanation": "nums[1] + nums[2] equals 6, so [1, 2] is returned.",
},
],
"starter_code": {
"cpp": "class Solution {\npublic:\n    vector twoSum(vector& nums, int target) {\n        // Your code here\n    }\n};",
"python": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        # Your code here\n        pass",
"java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Your code here\n        return new int[]{};\n    }\n}",
},
"test_cases": [
{"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected_output": [0, 1]},
{"input": {"nums": [3, 2, 4], "target": 6}, "expected_output": [1, 2]},
],
},

"best-time-to-buy": {
    "id": "best-time-to-buy",
    "title": "Best Time to Buy and Sell Stock",
    "topic": "arrays-strings",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "You are provided an array prices where prices[i] denotes the price "
        "of a given asset on day i. Find the maximum profit achievable by picking "
        "a single day to purchase the asset and selecting a strictly later day "
        "to sell it. If no profit is possible, return 0."
    ),
    "constraints": [
        "1 <= prices.length <= 10^5",
        "0 <= prices[i] <= 10^4",
    ],
    "examples": [
        {
            "input": "prices = [7, 1, 5, 3, 6, 4]",
            "output": "5",
            "explanation": "Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6 - 1 = 5.",
        },
        {
            "input": "prices = [7, 6, 4, 3, 1]",
            "output": "0",
            "explanation": "Prices continuously fall; no profitable trade exists.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"prices": [7, 1, 5, 3, 6, 4]}, "expected_output": 5},
        {"input": {"prices": [7, 6, 4, 3, 1]}, "expected_output": 0},
    ],
},

"best-time-to-buyII": {
    "id": "best-time-to-buyII",
    "title": "Best Time to Buy and Sell Stock II",
    "topic": "arrays-strings",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "You are given an integer array prices. On any day, you may decide to "
        "buy or sell the stock. You may hold at most one share at any given time, "
        "but you can buy and sell on the same day. Determine the maximum cumulative "
        "profit you can achieve."
    ),
    "constraints": [
        "1 <= prices.length <= 3 * 10^4",
        "0 <= prices[i] <= 10^4",
    ],
    "examples": [
        {
            "input": "prices = [7, 1, 5, 3, 6, 4]",
            "output": "7",
            "explanation": "Buy day 2 (1), sell day 3 (5) = +4. Buy day 4 (3), sell day 5 (6) = +3. Total = 7.",
        },
        {
            "input": "prices = [1, 2, 3, 4, 5]",
            "output": "4",
            "explanation": "Buy day 1 (1) and sell day 5 (5), profit = 4.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int maxProfit(vector<int>& prices) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def maxProfit(self, prices: list[int]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int maxProfit(int[] prices) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"prices": [7, 1, 5, 3, 6, 4]}, "expected_output": 7},
        {"input": {"prices": [1, 2, 3, 4, 5]}, "expected_output": 4},
    ],
},

"maximum-subarray": {
    "id": "maximum-subarray",
    "title": "Maximum Subarray",
    "topic": "arrays-strings",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an integer array nums, locate the contiguous subarray containing "
        "at least one number that possesses the largest sum, and return that sum."
    ),
    "constraints": [
        "1 <= nums.length <= 10^5",
        "-10^4 <= nums[i] <= 10^4",
    ],
    "examples": [
        {
            "input": "nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]",
            "output": "6",
            "explanation": "The subarray [4, -1, 2, 1] has the greatest sum of 6.",
        },
        {
            "input": "nums = [5, 4, -1, 7, 8]",
            "output": "23",
            "explanation": "The entire array sums to 23.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int maxSubArray(vector<int>& nums) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def maxSubArray(self, nums: list[int]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int maxSubArray(int[] nums) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, "expected_output": 6},
        {"input": {"nums": [1]}, "expected_output": 1},
    ],
},

"majority-element": {
    "id": "majority-element",
    "title": "Majority Element",
    "topic": "arrays-strings",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "Given an array nums of size n, return the majority element. The majority "
        "element is the value that appears strictly more than n / 2 times. You may "
        "assume that the majority element is guaranteed to exist."
    ),
    "constraints": [
        "n == nums.length",
        "1 <= n <= 5 * 10^4",
        "-10^9 <= nums[i] <= 10^9",
    ],
    "examples": [
        {
            "input": "nums = [3, 2, 3]",
            "output": "3",
            "explanation": "3 appears 2 times, which exceeds 3 / 2 = 1.5.",
        },
        {
            "input": "nums = [2, 2, 1, 1, 1, 2, 2]",
            "output": "2",
            "explanation": "2 appears 4 times, which is greater than 7 / 2 = 3.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int majorityElement(vector<int>& nums) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def majorityElement(self, nums: list[int]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int majorityElement(int[] nums) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"nums": [3, 2, 3]}, "expected_output": 3},
        {"input": {"nums": [2, 2, 1, 1, 1, 2, 2]}, "expected_output": 2},
    ],
},

# =========================================================================
# Greedy & Constructive
# =========================================================================
"assign-cookies": {
    "id": "assign-cookies",
    "title": "Assign Cookies",
    "topic": "greedy-constructive",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "Assume you want to satisfy children with cookies. Each child i has a "
        "greed factor g[i], which is the minimum size of cookie that satisfies "
        "them. Each cookie j has size s[j]. If s[j] >= g[i], you can assign cookie j "
        "to child i. Each child can get at most one cookie. Maximize the number of "
        "content children."
    ),
    "constraints": [
        "1 <= g.length <= 3 * 10^4",
        "0 <= s.length <= 3 * 10^4",
        "1 <= g[i], s[j] <= 2^31 - 1",
    ],
    "examples": [
        {
            "input": "g = [1, 2, 3], s = [1, 1]",
            "output": "1",
            "explanation": "You have 2 cookies of size 1. You can only satisfy the child with greed factor 1.",
        },
        {
            "input": "g = [1, 2], s = [1, 2, 3]",
            "output": "2",
            "explanation": "Both children can easily be satisfied.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int findContentChildren(vector<int>& g, vector<int>& s) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def findContentChildren(self, g: list[int], s: list[int]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int findContentChildren(int[] g, int[] s) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"g": [1, 2, 3], "s": [1, 1]}, "expected_output": 1},
        {"input": {"g": [1, 2], "s": [1, 2, 3]}, "expected_output": 2},
    ],
},

"jump-game": {
    "id": "jump-game",
    "title": "Jump Game",
    "topic": "greedy-constructive",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "You are given an integer array nums where you initially start at the first "
        "index. Each element nums[i] represents your maximum jump distance from that "
        "position. Return true if you can reach the last index, or false otherwise."
    ),
    "constraints": [
        "1 <= nums.length <= 10^4",
        "0 <= nums[i] <= 10^5",
    ],
    "examples": [
        {
            "input": "nums = [2, 3, 1, 1, 4]",
            "output": "true",
            "explanation": "Jump 1 step from index 0 to 1, then 3 steps to the last index.",
        },
        {
            "input": "nums = [3, 2, 1, 0, 4]",
            "output": "false",
            "explanation": "You will always arrive at index 3 where jump length is 0, blocking further progress.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    bool canJump(vector<int>& nums) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def canJump(self, nums: list[int]) -> bool:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public boolean canJump(int[] nums) {\n        // Your code here\n        return false;\n    }\n}",
    },
    "test_cases": [
        {"input": {"nums": [2, 3, 1, 1, 4]}, "expected_output": True},
        {"input": {"nums": [3, 2, 1, 0, 4]}, "expected_output": False},
    ],
},

# =========================================================================
# Dynamic Programming
# =========================================================================
"climbing-stairs": {
    "id": "climbing-stairs",
    "title": "Climbing Stairs",
    "topic": "dynamic-programming",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "You are ascending a staircase that takes n steps to reach the top. "
        "Each time, you may choose to climb either 1 or 2 steps. Determine "
        "how many distinct ways exist to reach the summit."
    ),
    "constraints": [
        "1 <= n <= 45",
    ],
    "examples": [
        {
            "input": "n = 2",
            "output": "2",
            "explanation": "Two ways: 1 step + 1 step, or 2 steps directly.",
        },
        {
            "input": "n = 3",
            "output": "3",
            "explanation": "Three ways: (1+1+1), (1+2), or (2+1).",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int climbStairs(int n) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int climbStairs(int n) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"n": 2}, "expected_output": 2},
        {"input": {"n": 3}, "expected_output": 3},
    ],
},

"coin-change": {
    "id": "coin-change",
    "title": "Coin Change",
    "topic": "dynamic-programming",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an integer array coins representing different coin denominations "
        "and an integer amount representing a target sum of money, compute the fewest "
        "coins needed to make up that amount. If that amount of money cannot be "
        "formed by any combination of the coins, return -1. Assume an infinite supply "
        "of each coin type."
    ),
    "constraints": [
        "1 <= coins.length <= 12",
        "1 <= coins[i] <= 2^31 - 1",
        "0 <= amount <= 10^4",
    ],
    "examples": [
        {
            "input": "coins = [1, 2, 5], amount = 11",
            "output": "3",
            "explanation": "11 = 5 + 5 + 1 (3 coins total).",
        },
        {
            "input": "coins = [2], amount = 3",
            "output": "-1",
            "explanation": "An odd amount cannot be constructed using only coins of denomination 2.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int coinChange(vector<int>& coins, int amount) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def coinChange(self, coins: list[int], amount: int) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int coinChange(int[] coins, int amount) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"coins": [1, 2, 5], "amount": 11}, "expected_output": 3},
        {"input": {"coins": [2], "amount": 3}, "expected_output": -1},
    ],
},

# =========================================================================
# Graphs
# =========================================================================
"number-of-islands": {
    "id": "number-of-islands",
    "title": "Number of Islands",
    "topic": "graphs",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an m x n 2D binary grid grid where '1' represents land and '0' "
        "represents water, return the number of islands. An island is surrounded by "
        "water and is formed by connecting adjacent lands horizontally or vertically."
    ),
    "constraints": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 300",
        "grid[i][j] is '0' or '1'.",
    ],
    "examples": [
        {
            "input": 'grid = [["1","1","0"],["1","1","0"],["0","0","1"]]',
            "output": "2",
            "explanation": "One large island in the top-left corner and one single land cell in the bottom right.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def numIslands(self, grid: list[list[str]]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int numIslands(char[][] grid) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {
            "input": {"grid": [["1", "1", "0"], ["1", "1", "0"], ["0", "0", "1"]]},
            "expected_output": 2,
        },
    ],
},

"course-schedule": {
    "id": "course-schedule",
    "title": "Course Schedule",
    "topic": "graphs",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "There are numCourses courses labeled from 0 to numCourses - 1. You are given "
        "an array prerequisites where prerequisites[i] = [a, b] indicates that you must "
        "take course b before course a. Return true if you can finish all courses, "
        "or false if a circular dependency makes it impossible."
    ),
    "constraints": [
        "1 <= numCourses <= 2000",
        "0 <= prerequisites.length <= 5000",
        "prerequisites[i].length == 2",
        "0 <= a_i, b_i < numCourses",
        "All pairs prerequisites[i] are unique.",
    ],
    "examples": [
        {
            "input": "numCourses = 2, prerequisites = [[1, 0]]",
            "output": "true",
            "explanation": "To take course 1 you should take course 0. This is linear and achievable.",
        },
        {
            "input": "numCourses = 2, prerequisites = [[1, 0], [0, 1]]",
            "output": "false",
            "explanation": "Both courses depend cyclically on each other.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public boolean canFinish(int numCourses, int[][] prerequisites) {\n        // Your code here\n        return false;\n    }\n}",
    },
    "test_cases": [
        {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected_output": True},
        {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "expected_output": False},
    ],
},

# =========================================================================
# Number Theory
# =========================================================================
"count-primes": {
    "id": "count-primes",
    "title": "Count Primes",
    "topic": "number-theory",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an integer n, return the number of prime numbers that are strictly "
        "less than n."
    ),
    "constraints": [
        "0 <= n <= 5 * 10^6",
    ],
    "examples": [
        {
            "input": "n = 10",
            "output": "4",
            "explanation": "There are 4 prime numbers less than 10: 2, 3, 5, 7.",
        },
        {
            "input": "n = 0",
            "output": "0",
            "explanation": "No primes exist strictly below 0.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int countPrimes(int n) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def countPrimes(self, n: int) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int countPrimes(int n) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"n": 10}, "expected_output": 4},
        {"input": {"n": 0}, "expected_output": 0},
        {"input": {"n": 1}, "expected_output": 0},
    ],
},

# =========================================================================
# Trees & Advanced DS
# =========================================================================
"maximum-depth": {
    "id": "maximum-depth",
    "title": "Maximum Depth of Binary Tree",
    "topic": "trees-advanced-ds",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "Given the root of a binary tree, return its maximum depth. The maximum depth "
        "is the number of nodes along the longest path from the root node down to "
        "the farthest leaf node."
    ),
    "constraints": [
        "The number of nodes in the tree is in the range [0, 10^4].",
        "-100 <= Node.val <= 100",
    ],
    "examples": [
        {
            "input": "root = [3, 9, 20, null, null, 15, 7]",
            "output": "3",
            "explanation": "The path 3 -> 20 -> 15 gives depth 3.",
        },
        {
            "input": "root = [1, null, 2]",
            "output": "2",
            "explanation": "The path 1 -> 2 gives depth 2.",
        },
    ],
    "starter_code": {
        "cpp": "/**\n * struct TreeNode {\n *     int val;\n *     TreeNode *left;\n *     TreeNode *right;\n *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n * };\n */\nclass Solution {\npublic:\n    int maxDepth(TreeNode* root) {\n        // Your code here\n    }\n};",
        "python": "# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def maxDepth(self, root: Optional[TreeNode]) -> int:\n        # Your code here\n        pass",
        "java": "/**\n * public class TreeNode {\n *     int val;\n *     TreeNode left;\n *     TreeNode right;\n *     TreeNode(int x) { val = x; }\n * }\n */\nclass Solution {\n    public int maxDepth(TreeNode root) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"tree": [3, 9, 20, None, None, 15, 7]}, "expected_output": 3},
        {"input": {"tree": []}, "expected_output": 0},
    ],
},

"level-order": {
    "id": "level-order",
    "title": "Binary Tree Level Order Traversal",
    "topic": "trees-advanced-ds",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given the root of a binary tree, return the level order traversal of its "
        "nodes' values (i.e., from left to right, level by level)."
    ),
    "constraints": [
        "The number of nodes in the tree is in the range [0, 2000].",
        "-1000 <= Node.val <= 1000",
    ],
    "examples": [
        {
            "input": "root = [3, 9, 20, null, null, 15, 7]",
            "output": "[[3], [9, 20], [15, 7]]",
            "explanation": "Level 0: [3], Level 1: [9, 20], Level 2: [15, 7].",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<vector<int>> levelOrder(TreeNode* root) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def levelOrder(self, root: Optional[TreeNode]) -> list[list[int]]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public List<List<Integer>> levelOrder(TreeNode root) {\n        // Your code here\n        return new ArrayList<>();\n    }\n}",
    },
    "test_cases": [
        {"input": {"tree": [3, 9, 20, None, None, 15, 7]}, "expected_output": [[3], [9, 20], [15, 7]]},
        {"input": {"tree": []}, "expected_output": []},
    ],
},

# =========================================================================
# Two Pointers
# =========================================================================
"valid-palindrome": {
    "id": "valid-palindrome",
    "title": "Valid Palindrome",
    "topic": "two-pointers",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "A phrase is a palindrome if, after converting all uppercase letters into "
        "lowercase letters and removing all non-alphanumeric characters, it reads the "
        "same forward and backward. Given a string s, return true if it is a palindrome, "
        "or false otherwise."
    ),
    "constraints": [
        "1 <= s.length <= 2 * 10^5",
        "s consists only of printable ASCII characters.",
    ],
    "examples": [
        {
            "input": 's = "A man, a plan, a canal: Panama"',
            "output": "true",
            "explanation": '"amanaplanacanalpanama" is a palindrome.',
        },
        {
            "input": 's = "race a car"',
            "output": "false",
            "explanation": '"raceacar" is not a palindrome.',
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    bool isPalindrome(string s) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public boolean isPalindrome(String s) {\n        // Your code here\n        return false;\n    }\n}",
    },
    "test_cases": [
        {"input": {"s": "A man, a plan, a canal: Panama"}, "expected_output": True},
        {"input": {"s": "race a car"}, "expected_output": False},
    ],
},

"is-subsequence": {
    "id": "is-subsequence",
    "title": "Is Subsequence",
    "topic": "two-pointers",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "Given two strings s and t, return true if s is a subsequence of t, or "
        "false otherwise. A subsequence of a string is a new string formed from "
        "the original string by deleting some (can be none) of the characters without "
        "disturbing the relative positions of the remaining characters."
    ),
    "constraints": [
        "0 <= s.length <= 100",
        "0 <= t.length <= 10^4",
        "s and t consist only of lowercase English letters.",
    ],
    "examples": [
        {
            "input": 's = "abc", t = "ahbgdc"',
            "output": "true",
            "explanation": "All characters of s appear in t in order.",
        },
        {
            "input": 's = "axc", t = "ahbgdc"',
            "output": "false",
            "explanation": "'x' does not appear in t.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    bool isSubsequence(string s, string t) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def isSubsequence(self, s: str, t: str) -> bool:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public boolean isSubsequence(String s, String t) {\n        // Your code here\n        return false;\n    }\n}",
    },
    "test_cases": [
        {"input": {"s": "abc", "t": "ahbgdc"}, "expected_output": True},
        {"input": {"s": "axc", "t": "ahbgdc"}, "expected_output": False},
    ],
},

"two-sum-ii": {
    "id": "two-sum-ii",
    "title": "Two Sum II - Input Array Is Sorted",
    "topic": "two-pointers",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given a 1-indexed array of integers numbers that is already sorted in "
        "non-decreasing order, find two numbers such that they add up to a specific "
        "target number. Return the indices of the two numbers added by one as an integer "
        "array [index1, index2] of length 2. Your solution must use O(1) additional space."
    ),
    "constraints": [
        "2 <= numbers.length <= 3 * 10^4",
        "-1000 <= numbers[i] <= 1000",
        "numbers is sorted in non-decreasing order.",
        "-1000 <= target <= 1000",
        "Exactly one valid solution exists.",
    ],
    "examples": [
        {
            "input": "numbers = [2, 7, 11, 15], target = 9",
            "output": "[1, 2]",
            "explanation": "The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<int> twoSum(vector<int>& numbers, int target) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def twoSum(self, numbers: list[int], target: int) -> list[int]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int[] twoSum(int[] numbers, int target) {\n        // Your code here\n        return new int[]{};\n    }\n}",
    },
    "test_cases": [
        {"input": {"numbers": [2, 7, 11, 15], "target": 9}, "expected_output": [1, 2]},
        {"input": {"numbers": [2, 3, 4], "target": 6}, "expected_output": [1, 3]},
    ],
},

"container-with-most-water": {
    "id": "container-with-most-water",
    "title": "Container With Most Water",
    "topic": "two-pointers",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "You are given an integer array height of length n. There are n vertical "
        "lines drawn such that the two endpoints of the ith line are (i, 0) and "
        "(i, height[i]). Find two lines that together with the x-axis form a container, "
        "such that the container contains the most water. Return the maximum amount of water."
    ),
    "constraints": [
        "n == height.length",
        "2 <= n <= 10^5",
        "0 <= height[i] <= 10^4",
    ],
    "examples": [
        {
            "input": "height = [1, 8, 6, 2, 5, 4, 8, 3, 7]",
            "output": "49",
            "explanation": "The lines at index 1 and 8 enclose area min(8, 7) * (8 - 1) = 7 * 7 = 49.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int maxArea(vector<int>& height) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def maxArea(self, height: list[int]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int maxArea(int[] height) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}, "expected_output": 49},
        {"input": {"height": [1, 1]}, "expected_output": 1},
    ],
},

"3sum": {
    "id": "3sum",
    "title": "3Sum",
    "topic": "two-pointers",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] "
        "such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0. "
        "Notice that the solution set must not contain duplicate triplets."
    ),
    "constraints": [
        "3 <= nums.length <= 3000",
        "-10^5 <= nums[i] <= 10^5",
    ],
    "examples": [
        {
            "input": "nums = [-1, 0, 1, 2, -1, -4]",
            "output": "[[-1, -1, 2], [-1, 0, 1]]",
            "explanation": "Distinct triplets that sum to 0 are [-1, 0, 1] and [-1, -1, 2].",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<vector<int>> threeSum(vector<int>& nums) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def threeSum(self, nums: list[int]) -> list[list[int]]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public List<List<Integer>> threeSum(int[] nums) {\n        // Your code here\n        return new ArrayList<>();\n    }\n}",
    },
    "test_cases": [
        {"input": {"nums": [-1, 0, 1, 2, -1, -4]}, "expected_output": [[-1, -1, 2], [-1, 0, 1]]},
        {"input": {"nums": [0, 1, 1]}, "expected_output": []},
    ],
},

# =========================================================================
# Sliding Window
# =========================================================================
"minimum-size-subarray-sum": {
    "id": "minimum-size-subarray-sum",
    "title": "Minimum Size Subarray Sum",
    "topic": "sliding-window",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an array of positive integers nums and a positive integer target, return "
        "the minimal length of a subarray whose sum is greater than or equal to target. "
        "If there is no such subarray, return 0 instead."
    ),
    "constraints": [
        "1 <= target <= 10^9",
        "1 <= nums.length <= 10^5",
        "1 <= nums[i] <= 10^4",
    ],
    "examples": [
        {
            "input": "target = 7, nums = [2, 3, 1, 2, 4, 3]",
            "output": "2",
            "explanation": "The subarray [4, 3] has the minimal length 2 with sum >= 7.",
        },
        {
            "input": "target = 11, nums = [1, 1, 1, 1, 1, 1, 1, 1]",
            "output": "0",
            "explanation": "Total sum is 8, which never reaches 11.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int minSubArrayLen(int target, vector<int>& nums) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def minSubArrayLen(self, target: int, nums: list[int]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int minSubArrayLen(int target, int[] nums) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"target": 7, "nums": [2, 3, 1, 2, 4, 3]}, "expected_output": 2},
        {"input": {"target": 11, "nums": [1, 1, 1, 1]}, "expected_output": 0},
    ],
},

"longest-substring-without-repeating": {
    "id": "longest-substring-without-repeating",
    "title": "Longest Substring Without Repeating Characters",
    "topic": "sliding-window",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given a string s, find the length of the longest substring without repeating "
        "characters."
    ),
    "constraints": [
        "0 <= s.length <= 5 * 10^4",
        "s consists of English letters, digits, symbols and spaces.",
    ],
    "examples": [
        {
            "input": 's = "abcabcbb"',
            "output": "3",
            "explanation": 'The answer is "abc", with the length of 3.',
        },
        {
            "input": 's = "bbbbb"',
            "output": "1",
            "explanation": 'The answer is "b", with the length of 1.',
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int lengthOfLongestSubstring(String s) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"s": "abcabcbb"}, "expected_output": 3},
        {"input": {"s": "bbbbb"}, "expected_output": 1},
    ],
},

"substring-concatenation": {
    "id": "substring-concatenation",
    "title": "Substring with Concatenation of All Words",
    "topic": "sliding-window",
    "difficulty": "Hard",
    "duration_seconds": 60 * 60,
    "description": (
        "You are given a string s and an array of strings words where all strings "
        "in words are of the same length. A concatenated string is a string that "
        "exactly contains all the strings of any permutation of words concatenated. "
        "Return an array of the starting indices of all concatenated substrings in s."
    ),
    "constraints": [
        "1 <= s.length <= 10^4",
        "1 <= words.length <= 5000",
        "1 <= words[i].length <= 30",
        "s and words[i] consist of lowercase English letters.",
    ],
    "examples": [
        {
            "input": 's = "barfoothefoobarman", words = ["foo","bar"]',
            "output": "[0, 9]",
            "explanation": 'Substrings starting at 0 ("barfoo") and 9 ("foobar") contain all words.',
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<int> findSubstring(string s, vector<string>& words) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def findSubstring(self, s: str, words: list[str]) -> list[int]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public List<Integer> findSubstring(String s, String[] words) {\n        // Your code here\n        return new ArrayList<>();\n    }\n}",
    },
    "test_cases": [
        {"input": {"s": "barfoothefoobarman", "words": ["foo", "bar"]}, "expected_output": [0, 9]},
    ],
},

"minimum-window-substring": {
    "id": "minimum-window-substring",
    "title": "Minimum Window Substring",
    "topic": "sliding-window",
    "difficulty": "Hard",
    "duration_seconds": 60 * 60,
    "description": (
        "Given two strings s and t of lengths m and n respectively, return the minimum "
        "window substring of s such that every character in t (including duplicates) is "
        "included in the window. If there is no such substring, return the empty string \"\"."
    ),
    "constraints": [
        "m == s.length",
        "n == t.length",
        "1 <= m, n <= 10^5",
        "s and t consist of uppercase and lowercase English letters.",
    ],
    "examples": [
        {
            "input": 's = "ADOBECODEBANC", t = "ABC"',
            "output": '"BANC"',
            "explanation": 'The minimum window substring "BANC" includes A, B, and C from string t.',
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    string minWindow(string s, string t) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def minWindow(self, s: str, t: str) -> str:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public String minWindow(String s, String t) {\n        // Your code here\n        return \"\";\n    }\n}",
    },
    "test_cases": [
        {"input": {"s": "ADOBECODEBANC", "t": "ABC"}, "expected_output": "BANC"},
        {"input": {"s": "a", "t": "aa"}, "expected_output": ""},
    ],
},

# =========================================================================
# Linked List
# =========================================================================
"linked-list-cycle": {
    "id": "linked-list-cycle",
    "title": "Linked List Cycle",
    "topic": "linked-list",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "Given head, the head of a linked list, determine if the linked list contains "
        "a cycle. A cycle exists if there is some node in the list that can be reached "
        "again by continuously following the next pointer. Return true if there is a "
        "cycle in the linked list, or false otherwise."
    ),
    "constraints": [
        "The number of the nodes in the list is in the range [0, 10^4].",
        "-10^5 <= Node.val <= 10^5",
    ],
    "examples": [
        {
            "input": "head = [3, 2, 0, -4], pos = 1",
            "output": "true",
            "explanation": "There is a cycle where the tail connects to the 1st node (0-indexed).",
        },
        {
            "input": "head = [1], pos = -1",
            "output": "false",
            "explanation": "There is no cycle in the linked list.",
        },
    ],
    "starter_code": {
        "cpp": "/**\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode(int x) : val(x), next(NULL) {}\n * };\n */\nclass Solution {\npublic:\n    bool hasCycle(ListNode *head) {\n        // Your code here\n    }\n};",
        "python": "# class ListNode:\n#     def __init__(self, x):\n#         self.val = x\n#         self.next = None\nclass Solution:\n    def hasCycle(self, head: Optional[ListNode]) -> bool:\n        # Your code here\n        pass",
        "java": "/**\n * class ListNode {\n *     int val;\n *     ListNode next;\n *     ListNode(int x) { val = x; next = null; }\n * }\n */\npublic class Solution {\n    public boolean hasCycle(ListNode head) {\n        // Your code here\n        return false;\n    }\n}",
    },
    "test_cases": [
        {"input": {"nodes": [3, 2, 0, -4], "pos": 1}, "expected_output": True},
        {"input": {"nodes": [1], "pos": -1}, "expected_output": False},
    ],
},

"add-two-numbers": {
    "id": "add-two-numbers",
    "title": "Add Two Numbers",
    "topic": "linked-list",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "You are given two non-empty linked lists representing two non-negative integers. "
        "The digits are stored in reverse order, and each of their nodes contains a single digit. "
        "Add the two numbers and return the sum as a linked list in reverse order."
    ),
    "constraints": [
        "The number of nodes in each linked list is in the range [1, 100].",
        "0 <= Node.val <= 9",
        "It is guaranteed that the list represents a number that does not have leading zeros.",
    ],
    "examples": [
        {
            "input": "l1 = [2, 4, 3], l2 = [5, 6, 4]",
            "output": "[7, 0, 8]",
            "explanation": "342 + 465 = 807.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {\n        // Your code here\n        return null;\n    }\n}",
    },
    "test_cases": [
        {"input": {"l1": [2, 4, 3], "l2": [5, 6, 4]}, "expected_output": [7, 0, 8]},
    ],
},

"merge-two-sorted-lists": {
    "id": "merge-two-sorted-lists",
    "title": "Merge Two Sorted Lists",
    "topic": "linked-list",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "You are given the heads of two sorted linked lists list1 and list2. "
        "Merge the two lists into one sorted list. The list should be made by splicing "
        "together the nodes of the first two lists. Return the head of the merged linked list."
    ),
    "constraints": [
        "The number of nodes in both lists is in the range [0, 50].",
        "-100 <= Node.val <= 100",
        "Both list1 and list2 are sorted in non-decreasing order.",
    ],
    "examples": [
        {
            "input": "list1 = [1, 2, 4], list2 = [1, 3, 4]",
            "output": "[1, 1, 2, 3, 4, 4]",
            "explanation": "Nodes spliced sequentially maintain non-decreasing order.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {\n        // Your code here\n        return null;\n    }\n}",
    },
    "test_cases": [
        {"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "expected_output": [1, 1, 2, 3, 4, 4]},
    ],
},

"copy-list-random-pointer": {
    "id": "copy-list-random-pointer",
    "title": "Copy List with Random Pointer",
    "topic": "linked-list",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "A linked list of length n is given such that each node contains an additional "
        "random pointer, which could point to any node in the list, or null. Construct "
        "a deep copy of the list."
    ),
    "constraints": [
        "0 <= n <= 1000",
        "-10^4 <= Node.val <= 10^4",
        "Node.random is null or is pointing to some node in the linked list.",
    ],
    "examples": [
        {
            "input": "head = [[7,null],[13,0],[11,4],[10,2],[1,0]]",
            "output": "[[7,null],[13,0],[11,4],[10,2],[1,0]]",
            "explanation": "A complete replica with brand new pointers is constructed.",
        },
    ],
    "starter_code": {
        "cpp": "/*\nclass Node {\npublic:\n    int val;\n    Node* next;\n    Node* random;\n    Node(int _val) { val = _val; next = NULL; random = NULL; }\n};\n*/\nclass Solution {\npublic:\n    Node* copyRandomList(Node* head) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':\n        # Your code here\n        pass",
        "java": "class Solution {\n    public Node copyRandomList(Node head) {\n        // Your code here\n        return null;\n    }\n}",
    },
    "test_cases": [
        {"input": {"nodes": [[7, None], [13, 0]]}, "expected_output": [[7, None], [13, 0]]},
    ],
},

"reverse-nodes-k-group": {
    "id": "reverse-nodes-k-group",
    "title": "Reverse Nodes in k-Group",
    "topic": "linked-list",
    "difficulty": "Hard",
    "duration_seconds": 60 * 60,
    "description": (
        "Given the head of a linked list, reverse the nodes of the list k at a time, "
        "and return the modified list. k is a positive integer and is less than or equal "
        "to the length of the linked list. Nodes left out of full groups remain in original order."
    ),
    "constraints": [
        "The number of nodes in the list is n.",
        "1 <= k <= n <= 5000",
        "0 <= Node.val <= 1000",
    ],
    "examples": [
        {
            "input": "head = [1, 2, 3, 4, 5], k = 2",
            "output": "[2, 1, 4, 3, 5]",
            "explanation": "First 2 nodes reversed, next 2 nodes reversed, last single node remains.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    ListNode* reverseKGroup(ListNode* head, int k) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public ListNode reverseKGroup(ListNode head, int k) {\n        // Your code here\n        return null;\n    }\n}",
    },
    "test_cases": [
        {"input": {"nodes": [1, 2, 3, 4, 5], "k": 2}, "expected_output": [2, 1, 4, 3, 5]},
    ],
},

# =========================================================================
# Stack
# =========================================================================
"valid-parentheses": {
    "id": "valid-parentheses",
    "title": "Valid Parentheses",
    "topic": "stack",
    "difficulty": "Easy",
    "duration_seconds": 25 * 60,
    "description": (
        "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', "
        "determine if the input string is valid. Open brackets must be closed by the same "
        "type of brackets in the correct order, and every close bracket has a corresponding open bracket."
    ),
    "constraints": [
        "1 <= s.length <= 10^4",
        "s consists of parentheses only '()[]{}'.",
    ],
    "examples": [
        {
            "input": 's = "()[]{}"',
            "output": "true",
            "explanation": "All bracket pairs open and close cleanly.",
        },
        {
            "input": 's = "(]"',
            "output": "false",
            "explanation": "Mismatched bracket types.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    bool isValid(string s) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def isValid(self, s: str) -> bool:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public boolean isValid(String s) {\n        // Your code here\n        return false;\n    }\n}",
    },
    "test_cases": [
        {"input": {"s": "()[]{}"}, "expected_output": True},
        {"input": {"s": "(]"}, "expected_output": False},
    ],
},

"simplify-path": {
    "id": "simplify-path",
    "title": "Simplify Path",
    "topic": "stack",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an absolute Unix-style file path path, convert it to the simplified "
        "canonical path. In a Unix-style file system, a period '.' refers to the current "
        "directory, a double period '..' refers to the directory up a level, and multiple "
        "consecutive slashes '//' are treated as a single slash '/'."
    ),
    "constraints": [
        "1 <= path.length <= 3000",
        "path consists of English letters, digits, period '.', slash '/' or '_'.",
        "path is a valid absolute Unix path.",
    ],
    "examples": [
        {
            "input": 'path = "/home/"',
            "output": '"/home"',
            "explanation": "Trailing slash is removed in canonical form.",
        },
        {
            "input": 'path = "/home//foo/"',
            "output": '"/home/foo"',
            "explanation": "Multiple consecutive slashes are replaced by a single slash.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    string simplifyPath(string path) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def simplifyPath(self, path: str) -> str:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public String simplifyPath(String path) {\n        // Your code here\n        return \"\";\n    }\n}",
    },
    "test_cases": [
        {"input": {"path": "/home/"}, "expected_output": "/home"},
        {"input": {"path": "/../"}, "expected_output": "/"},
    ],
},

"min-stack": {
    "id": "min-stack",
    "title": "Min Stack",
    "topic": "stack",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Design a stack that supports push, pop, top, and retrieving the minimum "
        "element in constant time O(1)."
    ),
    "constraints": [
        "-2^31 <= val <= 2^31 - 1",
        "Methods pop, top and getMin operations will always be called on non-empty stacks.",
        "At most 3 * 10^4 calls will be made to push, pop, top, and getMin.",
    ],
    "examples": [
        {
            "input": '["MinStack","push","push","push","getMin","pop","top","getMin"]\n[[],[-2],[0],[-3],[],[],[],[]]',
            "output": "[null,null,null,null,-3,null,0,-2]",
            "explanation": "MinStack retrieves -3, pops it, top becomes 0, and minimum updates to -2.",
        },
    ],
    "starter_code": {
        "cpp": "class MinStack {\npublic:\n    MinStack() {\n        \n    }\n    void push(int val) {\n        \n    }\n    void pop() {\n        \n    }\n    int top() {\n        \n    }\n    int getMin() {\n        \n    }\n};",
        "python": "class MinStack:\n    def __init__(self):\n        pass\n    def push(self, val: int) -> None:\n        pass\n    def pop(self) -> None:\n        pass\n    def top(self) -> int:\n        pass\n    def getMin(self) -> int:\n        pass",
        "java": "class MinStack {\n    public MinStack() {}\n    public void push(int val) {}\n    public void pop() {}\n    public int top() { return 0; }\n    public int getMin() { return 0; }\n}",
    },
    "test_cases": [
        {"input": {"operations": ["push", "push", "getMin"], "values": [[-2], [0], []]}, "expected_output": [None, None, -2]},
    ],
},

"evaluate-reverse-polish": {
    "id": "evaluate-reverse-polish",
    "title": "Evaluate Reverse Polish Notation",
    "topic": "stack",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "You are given an array of strings tokens that represents an arithmetic expression "
        "in Reverse Polish Notation. Evaluate the expression and return an integer that represents "
        "its value. Valid operators are '+', '-', '*', and '/'. Division truncates toward zero."
    ),
    "constraints": [
        "1 <= tokens.length <= 10^4",
        "tokens[i] is either an operator ('+', '-', '*', '/') or an integer in the range [-200, 200].",
    ],
    "examples": [
        {
            "input": 'tokens = ["2","1","+","3","*"]',
            "output": "9",
            "explanation": "((2 + 1) * 3) = 9",
        },
        {
            "input": 'tokens = ["4","13","5","/","+"]',
            "output": "6",
            "explanation": "(4 + (13 / 5)) = 6",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int evalRPN(vector<string>& tokens) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def evalRPN(self, tokens: list[str]) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int evalRPN(String[] tokens) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"tokens": ["2", "1", "+", "3", "*"]}, "expected_output": 9},
        {"input": {"tokens": ["4", "13", "5", "/", "+"]}, "expected_output": 6},
    ],
},

"basic-calculator": {
    "id": "basic-calculator",
    "title": "Basic Calculator",
    "topic": "stack",
    "difficulty": "Hard",
    "duration_seconds": 60 * 60,
    "description": (
        "Given a string s representing a valid mathematical expression, implement a basic "
        "calculator to evaluate it, and return the result of the evaluation. Note: You are "
        "not allowed to use any built-in eval functions. Supported tokens are '+', '-', '(', ')', and spaces."
    ),
    "constraints": [
        "1 <= s.length <= 3 * 10^5",
        "s consists of digits, '+', '-', '(', ')', and ' '.",
        "s represents a valid expression.",
    ],
    "examples": [
        {
            "input": 's = "1 + 1"',
            "output": "2",
            "explanation": "Simple binary addition.",
        },
        {
            "input": 's = "(1+(4+5+2)-3)+(6+8)"',
            "output": "23",
            "explanation": "Parentheses nesting evaluated strictly.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    int calculate(string s) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def calculate(self, s: str) -> int:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public int calculate(String s) {\n        // Your code here\n        return 0;\n    }\n}",
    },
    "test_cases": [
        {"input": {"s": "1 + 1"}, "expected_output": 2},
        {"input": {"s": "(1+(4+5+2)-3)+(6+8)"}, "expected_output": 23},
    ],
},

# =========================================================================
# Backtracking
# =========================================================================
"letter-combinations-phone": {
    "id": "letter-combinations-phone",
    "title": "Letter Combinations of a Phone Number",
    "topic": "backtracking",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given a string containing digits from 2-9 inclusive, return all possible "
        "letter combinations that the number could represent. Return the answer in any order. "
        "A mapping of digits to letters (just like on telephone buttons) is applied."
    ),
    "constraints": [
        "0 <= digits.length <= 4",
        "digits[i] is a digit in the range ['2', '9'].",
    ],
    "examples": [
        {
            "input": 'digits = "23"',
            "output": '["ad","ae","af","bd","be","bf","cd","ce","cf"]',
            "explanation": "2 maps to 'abc' and 3 maps to 'def'.",
        },
        {
            "input": 'digits = ""',
            "output": "[]",
            "explanation": "Empty input produces empty list.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<string> letterCombinations(string digits) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def letterCombinations(self, digits: str) -> list[str]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public List<String> letterCombinations(String digits) {\n        // Your code here\n        return new ArrayList<>();\n    }\n}",
    },
    "test_cases": [
        {"input": {"digits": "23"}, "expected_output": ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]},
        {"input": {"digits": ""}, "expected_output": []},
    ],
},

"combination-sum": {
    "id": "combination-sum",
    "title": "Combination Sum",
    "topic": "backtracking",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an array of distinct integers candidates and a target integer target, return "
        "a list of all unique combinations of candidates where the chosen numbers sum to target. "
        "You may return the combinations in any order. The same number may be chosen from "
        "candidates an unlimited number of times."
    ),
    "constraints": [
        "1 <= candidates.length <= 30",
        "2 <= candidates[i] <= 40",
        "All elements of candidates are distinct.",
        "1 <= target <= 40",
    ],
    "examples": [
        {
            "input": "candidates = [2,3,6,7], target = 7",
            "output": "[[2,2,3],[7]]",
            "explanation": "2 and 3 sum to 7 (2+2+3), and 7 itself sums to 7.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public List<List<Integer>> combinationSum(int[] candidates, int target) {\n        // Your code here\n        return new ArrayList<>();\n    }\n}",
    },
    "test_cases": [
        {"input": {"candidates": [2, 3, 6, 7], "target": 7}, "expected_output": [[2, 2, 3], [7]]},
    ],
},

"permutations": {
    "id": "permutations",
    "title": "Permutations",
    "topic": "backtracking",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an array nums of distinct integers, return all the possible permutations. "
        "You can return the answer in any order."
    ),
    "constraints": [
        "1 <= nums.length <= 6",
        "-10 <= nums[i] <= 10",
        "All the integers of nums are unique.",
    ],
    "examples": [
        {
            "input": "nums = [1, 2, 3]",
            "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]",
            "explanation": "All 3! = 6 unique permutations are enumerated.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<vector<int>> permute(vector<int>& nums) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def permute(self, nums: list[int]) -> list[list[int]]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public List<List<Integer>> permute(int[] nums) {\n        // Your code here\n        return new ArrayList<>();\n    }\n}",
    },
    "test_cases": [
        {"input": {"nums": [1, 2, 3]}, "expected_output": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]},
        {"input": {"nums": [0, 1]}, "expected_output": [[0, 1], [1, 0]]},
    ],
},

"subsets": {
    "id": "subsets",
    "title": "Subsets",
    "topic": "backtracking",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an integer array nums of unique elements, return all possible subsets "
        "(the power set). The solution set must not contain duplicate subsets. Return the "
        "solution in any order."
    ),
    "constraints": [
        "1 <= nums.length <= 10",
        "-10 <= nums[i] <= 10",
        "All the numbers of nums are unique.",
    ],
    "examples": [
        {
            "input": "nums = [1, 2, 3]",
            "output": "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]",
            "explanation": "All 2^3 = 8 subsets are returned.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    vector<vector<int>> subsets(vector<int>& nums) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def subsets(self, nums: list[int]) -> list[list[int]]:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public List<List<Integer>> subsets(int[] nums) {\n        // Your code here\n        return new ArrayList<>();\n    }\n}",
    },
    "test_cases": [
        {"input": {"nums": [1, 2, 3]}, "expected_output": [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]},
    ],
},

"word-search": {
    "id": "word-search",
    "title": "Word Search",
    "topic": "backtracking",
    "difficulty": "Medium",
    "duration_seconds": 40 * 60,
    "description": (
        "Given an m x n grid of characters board and a string word, return true if word "
        "exists in the grid. The word can be constructed from letters of sequentially adjacent "
        "cells, where adjacent cells are horizontally or vertically neighboring. The same letter "
        "cell may not be used more than once."
    ),
    "constraints": [
        "m == board.length",
        "n = board[i].length",
        "1 <= m, n <= 6",
        "1 <= word.length <= 15",
        "board and word consist of only lowercase and uppercase English letters.",
    ],
    "examples": [
        {
            "input": 'board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"',
            "output": "true",
            "explanation": "A contiguous sequence 'A' -> 'B' -> 'C' -> 'C' -> 'E' -> 'D' exists.",
        },
        {
            "input": 'board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"',
            "output": "false",
            "explanation": "Re-using the same cell 'B' is forbidden.",
        },
    ],
    "starter_code": {
        "cpp": "class Solution {\npublic:\n    bool exist(vector<vector<char>>& board, string word) {\n        // Your code here\n    }\n};",
        "python": "class Solution:\n    def exist(self, board: list[list[str]], word: str) -> bool:\n        # Your code here\n        pass",
        "java": "class Solution {\n    public boolean exist(char[][] board, String word) {\n        // Your code here\n        return false;\n    }\n}",
    },
    "test_cases": [
        {
            "input": {
                "board": [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]],
                "word": "ABCCED",
            },
            "expected_output": True,
        },
        {
            "input": {
                "board": [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]],
                "word": "ABCB",
            },
            "expected_output": False,
        },
    ],
},
}