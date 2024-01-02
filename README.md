# plex-youtube-channel-collections
Generate unique collections for each youtube channel folder stored locally.
This project is currently in development. Please use at your own risk. 
The plexapi can sometimes be finicky and I am still fine-tuning the best way to create smart collection metadata without upsetting the plex client.
I have not experienced any client-breaking bugs, but sometimes you may have to manually delete automatically created collections in plex and retry.
As always, please ensure to do a test sandbox of your videos first, or at the very least make a backup of your videos before trying to modify them.
This tooling does not (should not lol) make any physical changes to your local video files. All changes are done on the Plex-end.

#youtubearchive
When archiving youtube videos, It's difficult to have a proper UI experience to watch the youtube videos and channels that we've archived.
This project aims to utilize tools available in Plex to make a usable watching experience for Youtube channels archived utilizing yt-dlp.

![image](https://github.com/KJBurnett/plex-youtube-channel-collections/assets/9143189/793d7219-6012-402e-9efb-6e7ac30cf58c)


## Environment Setup
- Install the requirements.txt with `py -m pip install -r requirements.txt` located in this project.
- Written and tested with python 3.10.x and 3.11.x
- I enforce black formatter :D -> Install "Black Formatter" in the VSCode Market
- Fill out the required environment variables in the vscode [launch.json](https://github.com/KJBurnett/plex-youtube-channel-collections/blob/main/.vscode/launch.json)  


Example Configuration:
```json
        {
            "name": "[LOCAL SERVER] main script run",
            "type": "python",
            "request": "launch",
            "program": "main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "PLEX_URL": "https://localhost:32400", // 32400 is the default Plex port, but yours may be different.
                "PLEX_TOKEN": "<Insert-Plex-Token>", // See https://tinyurl.com/get-plex-token 
                "YOUTUBE_PATH": "Z:\\Youtube",
                "YOUTUBE_LIBRARY_NAME": "Youtube", // Set this to what you named your Youtube Library in Plex.
                "MEDIA_TYPE": "movie", // In the Plex Library Creation UI, choose "Other Videos" for the Library video file types.
                "YOUTUBE_VIDEO_EXTENSION": ".mkv",
                "SECONDS_TO_WAIT": "3600",
                "PYTHONWARNINGS": "ignore:Unverified HTTPS request",
                "OPTIMIZE_SCANS": "true", // OPTIONAL
                "DOWNLOAD_AVATARS_AND_BANNERS": "true", // OPTIONAL
                "YTDLP_PROCESS_PATH": "J:\\Youtube\\youtube-dlp.exe" // OPTIONAL
            }
        }
```

You can also simply input a config.json (a template has been provided in the project root) as an argument to load the necessary variables.
```json
{
    "PLEX_URL": "https://localhost:32400",
    "PLEX_TOKEN": "<Insert-Plex-Token>",
    "YOUTUBE_PATH": "C:\\Youtube",
    "YOUTUBE_LIBRARY_NAME": "Youtube",
    "MEDIA_TYPE": "movie",
    "YOUTUBE_VIDEO_EXTENSION": ".mkv",
    "SECONDS_TO_WAIT": "3600",
    "PYTHONWARNINGS": "ignore:Unverified HTTPS request",
    "OPTIMIZE_SCANS": "true",
    "DOWNLOAD_AVATARS_AND_BANNERS": "true",
    "YTDLP_PROCESS_PATH": "C:\\user\\youtube-dlp.exe"
}
```
This can be called by running `python main.py config.json` in your terminal.

## Creating a local Youtube Library
- This project heavily relies on code from the [yt-dlp project](https://github.com/yt-dlp/yt-dlp), FFMPEG, and Plex
- Download the latest [yt-dlp](https://github.com/yt-dlp/yt-dlp#installation)
- Place the exe in your youtube library folder. Example: Z:\Youtube
- Place the [config.conf](https://github.com/KJBurnett/plex-youtube-channel-collections/blob/main/config.conf) in Z:\Youtube, and ensure the commands point to your new youtube folder Z:\Youtube  
```
--batch-file "Z:\Youtube\channel_list.txt"  
--download-archive "Z:\Youtube\downloaded.txt"  
--output "Z:\Youtube\%(uploader)s [%(channel_id)s]/%(upload_date)s - %(title)s - (%(duration)ss) [%(id)s].%(ext)s"  
--ffmpeg-location "Z:\Youtube\ffmpeg\bin"  
Note: These configurations are very extensive. If you want to speed up downloads, disable --get-comments. 
```
- Create a channel_list.txt file with a list of youtube channel urls you want to download
- Run `Z:\Youtube\yt-dlp.exe --config-location "Z:\Youtube\config.conf"`

## Create a .plexignore file in your Youtube Library
- It's recommended that you create a `.plexignore` file in your Youtube directory to explicitly ignore *.temp.mkv files. This ensures Plex does not attempt to scan temp mkvs while the yt-dlp script runs.
- Create file: `Z:\Youtube\.plexignore` and fill the fil contents with
```
# Ignore all temp mkv files, these are generated by yt-dlp and should be automatically deleted.
*.temp.mkv
```

## After Downloading The Youtube Channels
- Ensure you have a Plex Server running, and create a dedicated library named "Youtube" and point the library to Z:\Youtube
- After Plex has finished scanning the videos, the library will be completely disorganized. This is expected, we now need to create the collections.
- Run [main.py](https://github.com/KJBurnett/plex-youtube-channel-collections/blob/main/main.py) config.json  
This can take some time as the script pings your PlexServer for every video metadata in your Z:\Youtube library.
Once completed, you should be able to find under the [Collections](https://support.plex.tv/articles/201273953-collections/) tab a collection for every youtube channel in the library.
Additionally, you will find the video files's `modified date` property to be changed to match the original Youtube video upload date.
When I tested first-time runs, it takes about 15 minutes to generate the initial collection libraries. Then, for cron-job updates, it only takes about 5 minutes to run, as it only needs to download youtube channel avatars and banners, and create collections on the initial run.

---

### ROADMAP
- ✅ Optimize youtube channel scans. Currently we check the PlexServer for every single video in a channel folder. Even if the video was already added to the collection. Idea: After successfully parsing and adding videos to a Plex Collection, serialize the list and store it as a txt file in each respective channel. We can read in thefile every time the script runs so we only scan for new youtube video additions to the channel folder.
- ✅ Add more error retry checks. Currently the script will keep going if a video fails. But we should produce a log file of all of the video files it failed to load into Plex. Historically this is usually due to some weird special character in the youtubeVideo's file name.
- ✅ Create in-depth documentation for utilizing yt-dlp in conjunction with this script. The video files must be organized and titled correctly or this script will not work.
- ✅ Add a flag to automatically pull the Youtube Channl avatar and banner, and automatically set the Plex Collection cover art to these images (super cool)
- ✅ Implement unit tests using pytest
- ✅ Add Github Actions to Pull Requests
