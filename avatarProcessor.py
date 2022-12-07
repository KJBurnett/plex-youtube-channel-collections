import os
import subprocess

# Internal modules
import utils


def getChannelAvatarsAndBanners(channelFolder: str, ytdlpProcessPath: str) -> bool:
    if not channelFolder or not ytdlpProcessPath:
        print(
            "No valid channelFolder or ytdlpProcessPath found. Skipping avatar download."
        )
        return False  # No valid inputs. Fail Early.

    channelGuid = utils.getGuidFromTitle(channelFolder)
    channelUrl = f"https://youtube.com/channel/{channelGuid}"

    downloadSuccess = downloadAvatarsAndBannersFromChannel(
        channelFolder, channelUrl, ytdlpProcessPath
    )
    return downloadSuccess


def downloadAvatarsAndBannersFromChannel(
    channelFolder: str, channelUrl: str, ytdlpProcessPath: str
) -> bool:
    downloadPath = os.path.join(channelFolder, "images")

    if os.path.exists(downloadPath):
        print("images/ already exists. Skipping.")
        return False  # If an images/ dir already exists, then we've already collected the avatars. Skip.
    else:
        print("Downloading avatars and banners from channel to images/")
        os.mkdir(downloadPath)

    projectPath = os.getcwd()

    # Temporarily change the current working directory, to properly download the images.
    os.chdir(downloadPath)

    subprocess.run(
        [
            f"{ytdlpProcessPath}",
            f"{channelUrl}",
            "--write-all-thumbnails",
            "--playlist-items",
            "0",
        ]
    )

    # Set the current working directory back to the project path.
    os.chdir(projectPath)

    return True
