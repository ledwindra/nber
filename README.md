# Introduction
This repository aims to analyze the trends of research topics in the field of economics by scraping the whole working papers published by the National Bureau of Economic Research. Everyone, including economics professors, public policy professionals, students, can take the benefit from this repository for free.

# Technical guide
You can run the following snippet code on your machine to clone the repository:

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

Before proceeding, you may want to use virtual environment, so that won't mess up the package versioning installed globally on your local machine.

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

After installing all the dependencies, you can run the Python script by running the following snippet on the terminal:

```bash
# --start and --end can be any number, such that start < end.
python --start=1 --end=33843
```


# Analysis
What can be done from this dataset? Well, let's take a look at `/notebook/index.ipynb`. 📙

# Permission
1. NBER
Check its [<strong>robots.txt</strong>](http://data.nber.org/robots.txt). Everybody is not disallowed to get `/papers/` tag.

2. RePEc
Coming from its open API: <strong>http://citec.repec.org/api.html</strong>

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

# Closing
I hope you find this repository useful. Feel free to contact me by submitting issues or pull requests. All errors are mine. Thank you.
