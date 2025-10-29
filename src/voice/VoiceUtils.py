
class VoiceUtils:
    @staticmethod
    def convert_seconds_to_time(seconds:int) -> str:
        """
        Converts seconds into a more readable format.
        hours:minutes:seconds
        :param seconds: The number of seconds.
        :return: The formated string.
        """
        hours = seconds // 3600
        minutes = (seconds // 60) % 60
        seconds = seconds % 60

        return f"{hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}" if hours > 0 else f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"