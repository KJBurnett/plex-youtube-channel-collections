import re
import os


def getGuidFromTitle(title: str) -> str:
    if "[" in title and title.endswith("]"):
        m = re.findall(r"\[(.*?)\]", title)
        if m is not None:
            return m[len(m) - 1]  # Return the last [ ] group in the string.
    return title


# Return the channel name from the cahnnelFolder.
# Example:
# Before: "Z:\\Youtube\\TheStradman [UC21Kozr_K0yDM-VjoihG9Aw]"
# After: "TheStradman"
def getChannelNameFromFolder(channelFolder: str) -> str:
    return os.path.basename(channelFolder).split(" [")[0]


# Returns a list of file names from the supplied folderPath.
# If the folderPath does not exist, return an empty array.
def getFileNamesFromDirectory(folderPath: str) -> list[str]:
    if os.path.exists(folderPath):
        return os.listdir(folderPath)
    return []
