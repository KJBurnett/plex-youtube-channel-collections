import unittest
import avatarProcessor


class test_avatarProcessor(unittest.TestCase):
    def test_downloadAvatarsAndBannersFromChannel(self):
        channelUrl = "https://youtube.com/channel/UC21Kozr_K0yDM-VjoihG9Aw"
        youtubePath = "J:\\Youtube\\youtube-dlp.exe"
        # channelFolder = "J:\\Youtube\\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]"
        channelFolder = r"C:\Users\kyler\Workspace\plex-youtube-channel-collections"
        self.assertEqual(1, 1)
        avatarProcessor.downloadAvatarsAndBannersFromChannel(
            channelFolder, channelUrl, youtubePath
        )

    def test_getChannelAvatarsAndBanners(self):
        channelFolder = ""
        youtubePath = ""
        result = avatarProcessor.getChannelAvatarsAndBanners(channelFolder, youtubePath)


if __name__ == "__main__":
    unittest.main()
