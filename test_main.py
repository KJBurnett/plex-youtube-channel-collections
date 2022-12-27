import main
from datetime import datetime
import os

bogusChannelList = [
    "SAM THE COOKING GUY",
    "Siger miller",
    ".plexignore",
    "100 Percent Zelda [UC4It_xPxQyCpyTJshlAQSgA]",
    "888MF [UCxZKNOKKTDX78PsQaOhEpKQ]",
    "Andres Vidoza [UCC_NjLEb2Sley94py4vSYTA]",
    "Andrew Ethan Zeng [UCgDqL4yzXb4BflimZaxL4Vg]",
    "AnonAysi [UCa-goA4IvB7xTmaUmfKbvXg]",
    "AutoTrader [UC7Dh_sbcNd4BCXQkAqPM1AQ]",
    "B-Rogue [UCx1d0tHfcaqj0tRz2gzugyQ]",
    "BeardMeatsFood [UCc9CjaAjsMMvaSghZB7-Kog]",
    "Ben Awad [UC-8QAzbLcRglXeN_MY9blyw]",
    "BKXC [UC3DFdy_qc-cqgKCyQTHLGzA]",
    "Buff Dudes [UCKf0UqBiCQI4Ol0To9V0pKQ]",
    "Burlacher [UCdcRo3w9qpfD5CucWwelHtA]",
    "Byte Review [UCg3tygBbdzyLEZ4lPMpCAFw]",
    "Cars with Luke [UCwgzx-E7BXya5thqTVFPCrg]",
    "Luke Terry [UCw5saOR2GRV2ivHqNxvWnOg]",
    "Modern Vintage Gamer [UCjFaPUcJU1vwk193mnW_w1w]",
    "Mortismal Gaming [UCEQ7KR9enYdQsB6kcMnw0NA]",
    "MrBeast [UCX6OQ3DkcsbYNE6H8uQQuVA]",
    "NEScRETRO [UCUMnu8kcIbyCQpInX3EmBJQ]",
    "Netflix [UCWOA1ZGywLbqmigxE4Qlvuw]",
    "New folder",
    "RGT 85 [UCA5RGaQc-a8tIX_AqTTmWdw]",
    "illiminate [UCEngeu7blnMQ6bOS2TRQLRw]",
    "Insider [UCHJuQZuzapBh-CuhRYxIZrg]",
    "Istvan Gabor [UCQ49ViT3bz5Pu12vL6juvww]",
    "iviegatron [UCRV61BpqSoGV4VD1NoxkW7A]",
    "J1mmy [UCqCg6nlsQdulY4W1-peSjsQ]",
    "Jeff Su [UCwAnu01qlnVg1Ai2AbtTMaA]",
    "Johns Garage [UCxJtJFLjHzSan_o4Z8hwLnA]",
    "Josh Neuman [UCMaHobSU33-_hCM6ASjGNZQ]",
    "JR Garage [UCeTagg7gemi1jhFKhY6gcNw]",
    "Kevin Vo [UCylJTidpT4YIClSUW6yV33Q]",
    "KrackdGamer [UCyxfOdMFT8v0WM95AyHLFWQ]",
    "League Mango [UCU7-s-FjWDnpF1oQEvycNQA]",
    "Linus Tech Tips [UCXuqSBlHAE6Xw-yeJA0Tunw]",
    "Stefan Lewis [UCxswUTu1DV0yyGIAaX_rwcA]",
    "theRadBrad [UCpqXJOEqGS-TCnazcHCo0rA]",
    "TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]",
]


# We expect the date to be prefixed to the title,
# and it must be in YYYYMMDD format to work, as expected from yt-dlp.
def test_getDateFromTitle_if_valid_title():
    bogusTitle = "20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY]"
    expectedResult = datetime(2012, 7, 27)
    result = main.getDateFromTitle(bogusTitle)
    assert result == expectedResult


# TODO: Must be mocked.
# def test_setDatesFromTitles():


def test_getVideosFromChannelFolder_if_optimizeScans_is_false(mocker):
    bogusChannelFolder = "hiIAmBogus"
    bogusVideoTitle = os.path.join(
        "Z:",
        "Youtube",
        "TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]",
        "20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY].mkv",
    )
    bogusFilesList = [bogusVideoTitle]
    expectedResult = ["20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY]"]
    mocker.patch("utils.getFileNamesFromDirectory", return_value=bogusFilesList)
    result = main.getVideosFromChannelFolder(bogusChannelFolder, optimizeScans=False)
    assert result == expectedResult


def test_getValidChannelFolders(mocker):
    youtubePath = "J:\\Youtube"
    mocker.patch("utils.getDirectoriesFromFilePath", return_value=bogusChannelList)

    result = main.getValidChannelFolders(youtubePath)
    expectedResult = filter(
        lambda folder: "[" in folder and folder.endswith("]"), bogusChannelList
    )
    expectedResult = list(expectedResult)
    expectedResult = [os.path.join(youtubePath, folder) for folder in expectedResult]

    assert result == expectedResult


def test_getValidChannelFolders_if_onlyChannels(mocker):
    youtubePath = "J:\\Youtube"
    onlyChannels = "J:\\Youtube\\plex_channels.txt"
    bogusOnlyChannelsGuids = [
        "UC21Kozr_K0yDM-VjoihG9Aw",
        "UCxswUTu1DV0yyGIAaX_rwcA",
        "UCdcRo3w9qpfD5CucWwelHtA",
        "UCwgzx-E7BXya5thqTVFPCrg",
        "UCw5saOR2GRV2ivHqNxvWnOg",
    ]
    expectedResult = [
        "J:\\Youtube\\Burlacher [UCdcRo3w9qpfD5CucWwelHtA]",
        "J:\\Youtube\\Cars with Luke [UCwgzx-E7BXya5thqTVFPCrg]",
        "J:\\Youtube\\Luke Terry [UCw5saOR2GRV2ivHqNxvWnOg]",
        "J:\\Youtube\\Stefan Lewis [UCxswUTu1DV0yyGIAaX_rwcA]",
        "J:\\Youtube\\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]",
    ]

    mocker.patch("utils.getDirectoriesFromFilePath", return_value=bogusChannelList)
    mocker.patch("main.getOnlyChannelsGuids", return_value=bogusOnlyChannelsGuids)
    result = main.getValidChannelFolders(
        youtubePath=youtubePath, onlyChannels=onlyChannels
    )

    assert result == expectedResult


# # TODO: Mock the functionality within optimizeScans=True
# def test_getVideosFromChannelFolder_if_optimizeScans_is_true(mocker):
#     bogusChannelFolder = "hiIAmBogus"
#     bogusVideoTitle = "Z:\\Youtube\\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]\\20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY].mkv"
#     bogusFilesList = [bogusVideoTitle]
#     expectedResult = ["20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY]"]
#     mocker.patch("utils.getFileNamesFromDirectory", return_value=bogusFilesList)
#     result = main.getVideosFromChannelFolder(bogusChannelFolder, optimizeScans=True)
#     assert result == expectedResult
