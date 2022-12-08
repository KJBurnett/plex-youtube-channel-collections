import utils
import os


# If given a bad title, expect the returned guid value to be
# the exact same as the input value. In this case, 'badTitle'
# result should equal badTitle as it could not parse any guid from it.
def test_getGuidFromTitle_if_bad_title():
    badTitle = "1234569gf043jf034j f09j43 f9034"
    result = utils.getGuidFromTitle(badTitle)
    assert badTitle == result


def test_getGuidFromTitle_if_valid_title():
    validTitle = os.path.join("Z:", "Youtube", "TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]")

    expectedResult = "UC21Kozr_K0yDM-VjoihG9Aw"
    result = utils.getGuidFromTitle(validTitle)
    assert result == expectedResult


def test_getChannelNameFromFolder():
    bogusChannelFolder = os.path.join(
        "Z:", "Youtube", "TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]"
    )
    expectedResult = "TheStradman"
    result = utils.getChannelNameFromFolder(bogusChannelFolder)
    assert result == expectedResult


def test_getFileNamesFromDirectory_if_valid_directory(mocker):
    bogusDirectory = "hiIAmBogus"
    expectedResult = [
        os.path.join(
            "Z:",
            "Youtube",
            "TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]",
            "20120727 - Ferrari Dino 246 GTS - (81s) [qZbpzYNEziY].mkv",
        )
    ]
    mocker.patch("utils.getFileNamesFromDirectory", return_value=expectedResult)
    result = utils.getFileNamesFromDirectory(bogusDirectory)
    assert result == expectedResult


def test_getFileNamesFromDirectory_if_directory_is_not_valid():
    bogusDirectory = "hiIAmBogusAndShouldNotExist"
    expectedResult = []
    result = utils.getFileNamesFromDirectory(bogusDirectory)
    assert result == expectedResult
