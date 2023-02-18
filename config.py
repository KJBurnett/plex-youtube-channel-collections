class Config:
    def __init__(
        self,
        youtubeLibrary,
        extension,
        mediaType,
        baseurl,
        token,
        youtubePath,
        optimizeScans,
        ytdlpProcessPath,
        downloadAvatarsAndBanners,
    ):
        self.youtubeLibrary = youtubeLibrary
        self.extension = extension
        self.mediaType = mediaType
        self.baseurl = baseurl
        self.token = token
        self.youtubePath = youtubePath
        self.optimizeScans = optimizeScans
        self.ytdlpProcessPath = ytdlpProcessPath
        self.downloadAvatarsAndBanners = downloadAvatarsAndBanners
