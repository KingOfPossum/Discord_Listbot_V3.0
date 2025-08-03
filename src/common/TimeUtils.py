from datetime import datetime

class TimeUtils:
    @staticmethod
    def get_current_year() -> int:
        return datetime.now().year

    @staticmethod
    def get_current_year_formated() -> str:
        return datetime.now().strftime("%y")