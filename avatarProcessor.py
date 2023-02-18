import os
import subprocess
from plexapi.server import Collection

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


def setPlexCollectionPoster(
    collection: Collection, channelName: str, channelFolder: str, youtubeLibrary: str
) -> None:
    # We specifically want the jpg that endswith avatar_uncropped
    # Example image name: "TheStradman [UC21Kozr_K0yDM-VjoihG9Aw].avatar_uncropped.jpg"
    imagesFolder = os.path.join(channelFolder, "images")
    foundImages = [
        image
        for image in os.listdir(imagesFolder)
        if image.endswith("avatar_uncropped.jpg")
    ]

    # Find a jpg in the channel's images folder that endswith ".avatar_uncropped".
    # If no image is found, skip uploading.
    if len(foundImages) > 0:
        print(
            f"Uploading image '{foundImages[0]}' to collection '{channelName}' posters."
        )
        imagePath = os.path.join(imagesFolder, foundImages[0])
        collection.uploadPoster(filepath=imagePath)
        print("Success")
    else:
        print(
            f"No images ending with '.avatar_uncropped.jpg' found. Skipping poster creation for collection '{channelName}'"
        )
