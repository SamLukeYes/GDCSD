# Geometry Dash Custom Song Downloader
A program aiming to accelerate Geometry Dash custom song downloading using Aria2

## How to use
**NOTE: dev branch may contain incomplete features. Please only use master branch, except for development use.**

Before running GDCSD, please make sure you have installed [Python](https://python.org) (tested on 3.7 and 3.8) and [Aria2](https://aria2.github.io). If you're using Windows, you might need to add the absolute paths of `aria2c.exe` and `python.exe` to `PATH`.

    USAGE: python gdcsd.py <command> [args]
        
    Defined commands:

        info            Display copyright infomation and current download directory
        dl              Download songs by ID and store them in custom song download directory
        set             Set custom song download directory, recommended to be the same as GD's
        reset           Reset custom song download directory to default
        clean           Clean song info cache
        help            Display this message
        
    Other commands: Execute a system command in custom song download directory.