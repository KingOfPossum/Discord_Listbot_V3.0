from dataclasses import dataclass

@dataclass(frozen=False)
class TimeEntry:
    """
    Represents a time entry in the database.
    Data stored includes user, activity and the time spent on that activity
    """
    user_id: int
    activity: str
    time_spent: int

    def __str__(self) -> str:
        return f"TimeEntry: \n" \
                f"  User: {self.user_id}\n" \
                f"  Activity: {self.activity}\n" \
                f"  Time Spent: {self.time_spent} seconds\n"