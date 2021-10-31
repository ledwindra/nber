# About ✌🏽
Hello world 🌏! Are you an economist, or economics student, or just a random person like me who is interested in economics? Do you want to write a paper, a thesis, or just ramble on some stuffs but don't have any fresh ideas on what should be the topic? Worry no more! Because, this repository is for you!

# TL;DR

I migrated all datasets to Dropbox and thus repository size decresases significatnly. Alas, in order to be downloadable, a folder must be less than [20 GB AND has fewer 10,000 total files](https://help.dropbox.com/installs-integrations/sync-uploads/download-entire-folders). So you have to click `Save to Dropbox` and sync to your local machine. Following are the URLs:
- Paper summary (JSON): [link](https://www.dropbox.com/sh/dx2vbms2zgei7eb/AAA5PsnLBJtQyeEowFxeCMqqa?dl=0 )
- Whole paper (plain text): [link](https://www.dropbox.com/sh/qxzcsj7b72gw9pv/AAB3Gywycgd_DrQYroGipBGAa?dl=0)

# Do it yourself
You can run the codes on your machine by cloning or downloading this repository.

```bash
# if you clone then .git directory will be included on your machine
git clone https://github.com/ledwindra/nber.git
cd nber

# if you download as zip, then .git direcotry won't be included on your machine
# preferable if you don't want to know about the nitty-gritty details about git
wget https://github.com/ledwindra/nber/archive/refs/heads/main.zip
unzip nber-main
cd nber-main 
```

When it's all ready, you may want to use virtual environment before installing all of the required packages so that won't affect your globally installed packages on your machine.

```bash
# create a virtual environment -> .venv is the folder, you can change
python -m venv .venv

# this applies for linux/macos
source .venv/bin/activate

# windows
env/Scripts/activate.bat

# install packages
pip install --upgrade pip
pip install -r requirements.txt 
```

# Use case
What can be done from this dataset? Well, let's take a look at `/notebook/index.ipynb`. 📙

# Permission
1. NBER
Check its [<strong>robots.txt</strong>](http://data.nber.org/robots.txt). Everybody is not disallowed to get `/papers/` tag.

2. RePEc
Coming from its open API: <strong>http://citec.repec.org/api.html</strong>

3. Wikipedia
Check [<strong>robots.txt</strong>](https://en.wikipedia.org/robots.txt):

```
User-agent: *
Allow: /w/api.php?action=mobileview&
Allow: /w/load.php?
Allow: /api/rest_v1/?doc
Disallow: /w/
Disallow: /api/
Disallow: /trap/
Disallow: /wiki/Special:
Disallow: /wiki/Spezial:
Disallow: /wiki/Spesial:
Disallow: /wiki/Special%3A
Disallow: /wiki/Spezial%3A
Disallow: /wiki/Spesial%3A
```

We're using <strong>https://en.wikipedia.org/wiki/</strong> so it's safe.

# Closing
If you have read up to this line, thank you for bearing with me. Hope this is useful for your purpose! 😎 🍻
