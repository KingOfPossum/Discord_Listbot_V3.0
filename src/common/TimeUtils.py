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

    @staticmethod
    def get_current_date_formated() -> str:
        """
        Returns the current date formatted as a string in the format "YYYY-MM-DD".
        :return: the current date as a string.
        """
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def convert_to_readable_form(date: str):
        """
        Converts a date string in the format "YYYY-MM-DD" to a more readable format "DD.MM.YYYY".
        :param date: the date string in the format "YYYY-MM-DD".
        :return: The converted date string in the format "DD.MM.YYYY".
        """
        formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S.%f"]
        for fmt in formats:
            try:
                dt = datetime.strptime(date, fmt)
                return dt.strftime("%d.%m.%Y")
            except ValueError:
                continue
        return date

    @staticmethod
    def timestamp_to_date(timestamp: int) -> str:
        """
        Converts a Unix timestamp to a date string in the format "YYYY-MM-DD".
        :param timestamp: The Unix timestamp to convert.
        :return: The converted date string in the format "YYYY-MM-DD".
        """
        return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")

    @staticmethod
    def convert_to_hours(seconds:int) -> float:
        """
        Converts seconds to hours.
        :param seconds: The number of seconds to convert.
        :return: The equivalent number of hours.
        """
        return round(seconds / 3600, 1)

    @staticmethod
    def convert_to_minutes(seconds:int) -> int:
        """
        Converts seconds to minutes.
        :param seconds: The number of seconds to convert.
        :return: The equivalent number of minutes.
        """
        return seconds // 60