# plex-youtube-channel-collections
Generate unique collections for each youtube channel folder stored locally

#youtubearchive
When archiving youtube videos, It's difficult to have a proper UI experience to watch the youtube videos and channels that we've archived.
This project aims to utilize tools available in Plex to make a usable watching experience for Youtube channels archived utilizing yt-dlp.

# TODO
- Optimize youtube channel scans. Currently we check the PlexServer for every single video in a channel folder. Even if the video was already added to the collection. Idea: After successfully parsing and adding videos to a Plex Collection, serialize the list and store it as a txt file in each respective channel. We can read in thefile every time the script runs so we only scan for new youtube video additions to the channel folder.
- Add more error retry checks. Currently the script will keep going if a video fails. But we should produce a log file of all of the video files it failed to load into Plex. Historically this is usually due to some weird special character in the youtubeVideo's file name.
- Create in-depth documentation for utilizing yt-dlp in conjunction with this script. The video files must be organized and titled correctly or this script will not work.

# Environment Setup
- Install the requirements.txt with `py -m pip install -r requirements.txt` located in this project.
- Written and tested with python 3.10.x and 3.11.x
- I enforce black formatter :D -> Install "Black Formatter" in the VSCode Market
