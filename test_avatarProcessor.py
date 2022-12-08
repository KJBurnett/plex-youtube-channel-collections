import avatarProcessor


def test_downloadAvatarsAndBannersFromChannel(mocker):
    channelUrl = "https://youtube.com/channel/UC21Kozr_K0yDM-VjoihG9Aw"
    ytdlpPath = "J:\\Youtube\\youtube-dlp.exe"
    channelFolder = "J:\\Youtube\\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]"

    # We must mock this function, otherwise it will make network calls.
    mocker.patch(
        "avatarProcessor.downloadAvatarsAndBannersFromChannel", return_value=True
    )
    result = avatarProcessor.downloadAvatarsAndBannersFromChannel(
        channelFolder, channelUrl, ytdlpPath
    )
    assert result == True


def test_getChannelAvatarsAndBanners_if_empty_params():
    channelFolder = ""
    ytdlpProcessPath = ""
    result = avatarProcessor.getChannelAvatarsAndBanners(
        channelFolder, ytdlpProcessPath
    )
    assert result == False  # Should return False as no usable parameters were given.
