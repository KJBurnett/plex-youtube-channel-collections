import main
from datetime import datetime
import os


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


# # TODO: Mock the functionality within optimizeScans=True
# def test_getVideosFromChannelFolder_if_optimizeScans_is_true(mocker):
#     bogusChannelFolder = "hiIAmBogus"
#     bogusVideoTitle = "Z:\\Youtube\\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]\\20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY].mkv"
#     bogusFilesList = [bogusVideoTitle]
#     expectedResult = ["20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY]"]
#     mocker.patch("utils.getFileNamesFromDirectory", return_value=bogusFilesList)
#     result = main.getVideosFromChannelFolder(bogusChannelFolder, optimizeScans=True)
#     assert result == expectedResult
