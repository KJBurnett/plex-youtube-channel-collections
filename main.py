# 11/25/2022
# Kyler Burnett

import json
import os
import sys
from plexapi.server import PlexServer
from plexapi.collection import Collection
from plexapi.video import Movie
import requests
import time
from datetime import datetime


# def updateModifiedTime(videoPath: str):
#     date = getDateFromTitle(videoPath)
#     modTime = time.mktime(date.timetuple())

#     os.utime(fileLocation, (modTime, modTime))


def setDatesFromTitles(videoObjects: list[Movie], channelFolder: str) -> list[Movie]:
    for videoObject in videoObjects:
        videoObject.originallyAvailableAt = getDateFromTitle(videoObject.title)
        videoPath = f"{os.path.join(channelFolder, videoObject.title)}.mkv"
        modTime = time.mktime(getDateFromTitle(videoObject.title).timetuple())
        os.utime(
            videoPath,
            (modTime, modTime),
        )
    return videoObjects


# Expected file name format: "20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY]"
# Split by first whitespace to get the date string.
# Then, parse the year, month, and day out of the singular no-space string.
# returns a datetime object, as required by plexapi.video.originallyAvailableAt
def getDateFromTitle(title: str) -> datetime:
    date = title.split(" ")[0]
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])
    return datetime(year, month, day)


# Get a list of videos from the channelFolder by finding all files with the YOUTUBE_VIDEO_EXTENSION
# strip the video of its extension, and remove the filepath. Plex only needs the file name.
# Example:
# Before: "Z:\Youtube\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]\20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY].mkv"
# After: "20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY]"
def getVideosFromChannelFolder(channelFolder: str) -> list[str]:
    # TODO: Ensure this returns the desired videos list.
    videos = [
        os.path.basename(video.replace(".mkv", ""))
        for video in os.listdir(channelFolder)
        if video.endswith(".mkv")
    ]
    return videos


# Return the channel name from the cahnnelFolder.
# Example:
# Before: "Z:\\Youtube\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]"
# After: "TheStradman"
def getChannelNameFromFolder(channelFolder: str) -> str:
    return os.path.basename(channelFolder).split(" [")[0]


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
    plex: PlexServer, channelVideos: list[str], mediaType: str, youtubeLibrary: str
) -> list[Movie]:
    plexVideoObjects = []

    counter = 1
    for video in channelVideos[:10]:
        # Find existence of video in the plex library.
        # TODO: Ensure this works. Messed with it a lot.
        print(f"[{counter}/{len(channelVideos)}] Searching for {video}")
        counter += 1
        videoObject = searchPlexForVideo(plex, video, mediaType, youtubeLibrary)
        if videoObject:
            plexVideoObjects.append(videoObject[0])
            print("Video found in Plex!")
        else:
            print("Error. Video was not found in Plex.")
    return plexVideoObjects


def searchPlexForVideo(
    plex: PlexServer, video: str, mediaType: str, youtubeLibrary: str
):
    maxRetries = 5
    attempt = 1
    waitInSeconds = 2
    querySucess = False
    videoObject = None
    while attempt <= maxRetries and not querySucess:
        try:
            videoObject = plex.search(
                video, mediatype=mediaType, sectionId=youtubeLibrary
            )
            querySucess = True
        except Exception as e:
            print(
                f"Error. The Plex server likely timed out from too many requests. Waiting for {waitInSeconds} before trying again.\nAttempt {attempt}/{maxRetries}\n Caught Exception: {e}"
            )
            attempt += 1
            time.sleep(waitInSeconds)
            waitInSeconds = (
                waitInSeconds * 2
            )  # Increase the wait time if we have to wait again.
    return videoObject


def addVideosToPlexCollection(
    plex: PlexServer, videoObjects, youtubeLibrary: str, channelName: str
) -> None:
    # Check to see if the collection already exists.
    collectionResults = plex.search(
        channelName, mediatype="collection", sectionId=youtubeLibrary
    )

    if collectionResults:
        collection = collectionResults[0]
        collection.addItems(videoObjects)
        collection.sortUpdate(sort="custom")
    else:
        print(f"The collection does not exist. Creating a collection for {channelName}")
        # TODO: Remove newCollection. Required now for debugging.
        newCollection = plex.createCollection(
            title=channelName, section=youtubeLibrary, items=videoObjects, sort="custom"
        )


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

    # Start a PlexServer API session.
    session = requests.Session()
    session.verify = False
    plex = PlexServer(baseurl, token, session)

    # ===== Let's get to work ===== #
    validChannelFolders = getValidChannelFolders(youtubePath)

    # for validChannelFolder in validChannelFolders:
    #     channelName = getChannelNameFromFolder(channelFolder=validChannelFolder)
    #     channelVideos = getVideosFromChannelFolder(channelFolder=validChannelFolder)

    #     videoObjects = findYoutubeVideosInPlex(
    #         channelVideos, mediaType, sectionId=youtubeLibrary
    #     )
    #     addToPlexCollection(plex, videoObjects, youtubeLibrary, channelName)

    # ======================================== #
    # For testing/debugging
    channelFolder = "Z:\Youtube\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]"

    channelName = getChannelNameFromFolder(channelFolder=channelFolder)
    channelVideos = getVideosFromChannelFolder(channelFolder=channelFolder)

    videoObjects = findYoutubeVideosInPlex(
        plex, channelVideos, mediaType, youtubeLibrary
    )
    # This sorts the videos in Descending order.
    # Mimicking Youtube's video listing, most recent to oldest.
    videoObjects.sort(key=lambda video: video.title, reverse=True)

    # We must parse the date out of the youtube video title and apply it to the plex object
    # otherwise, we won't be able to properly sort by release date.
    videoObjects = setDatesFromTitles(videoObjects, channelFolder)

    addVideosToPlexCollection(plex, videoObjects, youtubeLibrary, channelName)
