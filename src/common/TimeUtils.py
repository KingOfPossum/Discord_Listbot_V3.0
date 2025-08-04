from datetime import datetime

class TimeUtils:
    """Utility class for time-related functions."""

    @staticmethod
    def get_current_year() -> int:
        """
        :return: the current year as an integer
        """
        return datetime.now().year

    @staticmethod
    def get_current_year_formated() -> str:
        """
        Returns the current year formatted as a two-digit string.
        :return: the current year as a two-digit string (e.g., "23" for 2023).
        """
        return datetime.now().strftime("%y")