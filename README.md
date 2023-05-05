# CDJTrackPrepare

A Python package to automatically fix technical compatibility issues with Pionner CDJs, including the WAV header byte
bug (see https://forums.pioneerdj.com/hc/en-us/community/posts/360059172771-E-8305-Unsupported-File-Format?page=1#community_comment_360010288271).

## Installation

Clone this repository to your computer ``git clone https://github.com/TheBlueCookie/CDJTrackPrepare.git``.

Make sure to have ``ffmpeg.exe`` (available here: https://ffmpeg.org/) in the same directory or added to ``PATH``. 

## Usage

The supported audio file specifications for a CDJ Nexus 2000 are saved in ``supported_files.py``. If you need to adapt them or add different ones, e.g. for a CDJ 3000, strictly stick to the same syntax.

The most straightforward usage is shown in ``demo.py``, consisting of three main parts: scraping the library, i.e. searching for all relevant files, followed by diagnosing them and fixing all issues found during the diagnosis. 

**The current version replaces files, it does not copy them! Even though files in principle cannot get corrupted by the script, use at your own risk.**

So far, only MP3 and WAV files are handled by the script, all other file formats are ignored. 