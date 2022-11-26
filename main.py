# 11/25/2022
# Kyler Burnett

import json
import os
import sys
from plexapi.server import PlexServer
from plexapi.collection import Collection
import requests
import time

# Get a list of videos from the channelFolder by finding all files with the YOUTUBE_VIDEO_EXTENSION
# strip the video of its extension, and remove the filepath. Plex only needs the file name.
# Example:
# Before: "Z:\Youtube\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]\20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY].mkv"
# After: "20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY]"
def getVideosFromChannelFolder(channelFolder: str) -> list[str]:
    videos = [
        os.path.basename(video.replace(".mkv", ""))
        for video in os.listdir(channelFolder)
        if video.endswith(".mkv")
    ]
    return videos


# Return the channel name from the cahnnelFolder.
# Example:
# Before: "Z:\\Youtube\TheStradman"
# After: "TheStradman"
def getChannelNameFromFolder(channelFolder: str) -> str:
    return os.path.basename(channelFolder)


# Ensure we're looking at specifically Youtube Channel Folders.
# We determine this by ensuring there is a unique guid at the end of the folder name.
# Example:
# A valid channel folder: TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]
# An invalid channel folder: TheStradman
def getValidChannelFolders(youtubePath: str) -> list[str]:
    folders = os.listdir(youtubePath)
    validFolders = filter(
        lambda folder: "[" in folder and folder.endswith("]"), folders
    )
    # Note filter is an iterable, so we need to convert it back into a list.
    return list(validFolders)


# Search the Plex database for plex video objects of the youtube videos.
# We have to search the Plex database for every single video file name, and retrieve its Plex library object.
def findYoutubeVideosInPlex(
    channelVideos: list[str], mediaType: str, sectionId: str
) -> list[str]:
    plexVideoObjects = []

    testVideos = channelVideos[:50]

    for video in testVideos:
        # Find existence of video in the plex library.
        print("Searching for " + video)
        videoObject = plex.search(video, mediatype=mediaType, sectionId=youtubeLibrary)
        if len(videoObject):
            plexVideoObjects.append(videoObject[0])
            print("Video found in Plex!")
        else:
            print("Error. Video was not found in Plex.")
    return plexVideoObjects


def searchPlexForVideo(video: str, mediaType: str, sectionId: str):
    retries = 5
    waitInSeconds = 2
    querySucess = False
    videoObject = None
    while retries != 0 and not querySucess:
        try:
            videoObject = plex.search(
                video, mediatype=mediaType, sectionId=youtubeLibrary
            )
            querySucess = True
        except:
            retries -= 1
            time.sleep(waitInSeconds)
            waitInSeconds = (
                waitInSeconds * 2
            )  # Increase the wait time if we have to wait again.
    return videoObject


# Error checking for initial startup of the script.
# We require these environment variables to ensure a smooth and successful run.
def environmentVariableError(missingVariable: str) -> None:
    variables = {
        "YOUTUBE_LIBRARY_NAME": "The name of your Youtube library in Plex. eg: 'Youtube'",
        "YOUTUBE_VIDEO_EXTENSION": "The file extension of your Youtube videos. eg: '.mkv'",
        "MEDIA_TYPE": "The type of media your Youtube videos are classified as in Plex. eg: 'movie'",
        "PLEX_URL": "the url of your plex server. eg: 'https://192.168.1.25:32400'",
        "PLEX_TOKEN": "The token required to access your plex api. See https://tinyurl.com/get-plex-token",
        "YOUTUBE_PATH": "The filepath to your Youtube library. eg: 'Z:\\Youtube'",
    }
    errorMessage = f"\nError. Missing environment variable '{missingVariable}'. You must supply all required environment variables.\n\nRequired Environment Variables:{json.dumps(variables, indent=4, separators=(',', ': '))}"
    print(errorMessage)
    sys.exit()


if __name__ == "__main__":
    # Ensure the environment variables exist. Otherwise throw an error and quit.
    youtubeLibrary = os.environ.get("YOUTUBE_LIBRARY_NAME")
    if not youtubeLibrary:
        environmentVariableError("YOUTUBE_LIBRARY_NAME")
        sys.exit()
    extension = os.environ.get("YOUTUBE_VIDEO_EXTENSION")
    if not extension:
        environmentVariableError("YOUTUBE_VIDEO_EXTENSION")
        sys.exit()
    mediaType = os.environ.get("MEDIA_TYPE")
    if not mediaType:
        environmentVariableError("MEDIA_TYPE")
        sys.exit()
    baseurl = os.environ.get("PLEX_URL")
    if not baseurl:
        environmentVariableError("PLEX_URL")
        sys.exit()
    token = os.environ.get("PLEX_TOKEN")
    if not token:
        environmentVariableError("PLEX_TOKEN")
        sys.exit()
    youtubePath = os.environ.get("YOUTUBE_PATH")
    if not youtubePath:
        environmentVariableError("YOUTUBE_PATH")
        sys.exit()

    print("All environment variables successfully loaded.\n")

    # ===== Let's get to work ===== #
    validChannelFolders = getValidChannelFolders(youtubePath)

    # For testing/debugging
    channelFolder = "Z:\Youtube\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]"
    channelName = getChannelNameFromFolder(channelFolder=channelFolder)
    channelVideos = getVideosFromChannelFolder(channelFolder=channelFolder)

    # Start a PlexServer API session.
    session = requests.Session()
    session.verify = False
    plex = PlexServer(baseurl, token, session)

    videoObjects = findYoutubeVideosInPlex(
        channelVideos, mediaType, sectionId=youtubeLibrary
    )

    # Check to see if the collection already exists.
    collectionResults = plex.search(
        channelName, mediatype="collection", sectionId="Youtube"
    )

    if collectionResults:
        collection = collectionResults[0]
        result = collection.addItems(videoObjects)
    else:
        print("The collection does not exist. Creating...")
