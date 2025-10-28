import dataclasses

@dataclasses.dataclass
class VideoEntry:
    url: str
    title: str
    video_id: str
    duration: int
    thumbnail_url: str

    @classmethod
    def new(cls,url,title,video_id,duration):
        return cls(url,title,video_id,duration,f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg")

    def __str__(self):
        return f"URL: {self.url}\nTitle: {self.title}\nVideo ID: {self.video_id}\nThumbnail URL: {self.thumbnail_url}\nDuration: {self.duration}"