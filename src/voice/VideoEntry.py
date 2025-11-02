import dataclasses

@dataclasses.dataclass
class VideoEntry:
    """
    Represents a video entry with following properties:
     url : The url of the video.\n
     title : The title of the video.\n
     video_id : The id of the video.\n
     duration: The duration of the video.\n
     current_playtime : How long has the video been played.\n
     thumbnail_url : The url of the thumbnail of the video.
    """
    url: str
    title: str
    video_id: str
    duration: int
    current_playtime: int
    thumbnail_url: str

    @classmethod
    def new(cls,url,title,video_id,duration):
        """
        Creates a new VideoEntry object.
        :param url: The url of the video. Also used to create the thumbnail_url.
        :param title: The title of the video.
        :param video_id: The id of the video.
        :param duration: The duration of the video.
        :return: A new VideoEntry object.
        """
        return cls(url,title,video_id,duration,0,f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg")

    def __str__(self):
        return f"URL: {self.url}\nTitle: {self.title}\nVideo ID: {self.video_id}\nThumbnail URL: {self.thumbnail_url}\nDuration: {self.duration}"