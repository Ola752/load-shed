from enum import Enum
from functools import total_ordering  # for enum (RunType) ordering


@total_ordering
class DebugMode(Enum):
    No = 0  # default
    VeryBrief = 1  # only metadata (function name, parameters, total time)
    Brief = 2  # VeryBrief + time at each big step
    Detail = 3  # Brief + counting for each small step
    VeryDetail = 4  # Detail + variables (for debugging)

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


debug_mode = DebugMode.No
# T_highest = 80
# T_medium_high = 60
# T_medium_low = 40
# T_lowest = 20

T_level2 = 66
T_level1 = 33


