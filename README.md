**Arachnovel - Light Crawler**
===============================
## The lighter novel crawler
This is meant to be a Lightnovel-Crawler alternative for android users.  
arachnovel aims to be lightweight, segfault free, and with easier way to add support for other novel websites.

## How to use
This should be fairly easy to understand for those with terminal experience but basically
```bash
git clone this_repo
cd this_repo
python main.py -h

# or better yet just add a symlink to bin
git clone https://github.com/SoreScythe/Arachnovel
cd Arachnovel
ln -s main.py /usr/bin/arachnovel
arachnovel -h
```

## Why This Project
I wrote this mainly to have a lightnovel-crawler that won't suddenly segfault in the middle of downloading novels.  
The other not so minor reason would be that I cannot understand(atleast during those segfault days, not sure about now) the code of lightnovel crawler which led me to try and create a version that is more easily readable for me while learning python.  
This project started months ago and has been the victim of my, often passionate but, not so daily bursts of passion to code.  
I started working on this during my early days of discovering wuxia novels and when I first ventured into termux.  
Various versions have been written which I've unfortunately yeeted to the void of my filesystem.  
Those versions are not the most portable anyways so probably good riddance.

## Project Goals
- [ ] Fix the bug during chapter downloads where KeyboardInterrupts get caught by the async Fetch function
- [ ] Improve code readability.
- [ ] Add support for major websites.
- [ ] Finalize the download cmd arguments and have every parameter working.
- [ ] Add support for querying for novel title on all supported websites.

