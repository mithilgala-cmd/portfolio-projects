"""Two Sum solution with hash-map lookup."""

from typing import List

class Solution:
    def two_sum(self, nums: List[int], target: int) -> List[int]:
        """Return indices of two numbers that sum to target.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        num_map: dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], i]
            num_map[num] = i
        return []

    # Backward-compatible alias for LeetCode-style naming.
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        return self.two_sum(nums, target)
