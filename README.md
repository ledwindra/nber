![CodeQL](https://github.com/ledwindra/nber/workflows/CodeQL/badge.svg)

# About ✌🏽

Hello world :earth_asia:! Are you an economist, or economics student, or just a random person like me who is interested in economics? Do you want to write a paper, a thesis, or just ramble on some stuffs but don't have any fresh ideas on what should be the topic? Worry no more! Because, this repository is for you!

# Warning! ⚠️

Since this repository uses cron job from GitHub Actions to update the data, consequently the .git directory will eat up disk space. Hence, it is not advisable to clone this repository to your local machine. If you are interested to do something similar, just download this repository as a zipped file. You can do the following:

```bash
# download repository from main branch
wget https://github.com/ledwindra/nber/archive/main.zip
```

This won't include the .git directory and you can play around with the programs and data inside your local machine.

# Download data
If you don't want to run this locally and just want to get straight to the data, just chill, relax and, download them Enjoy! 🌞 ⛱ 🥥 🌴 😎.

1. [<strong>NBER</strong>](https://github.com/ledwindra/nber/raw/master/data/nber.zip)

|column_name|data_type|description|
|-|-|-|
|id|integer|NBER working paper ID|
|citation_title|string|Paper title|
|citation_author|string|Paper author(s). Can be more than one. Hence it is stored as an array|
|citation_date|date|Date of paper (not clear)|
|citation_publication_date|date|Date of paper being published|
|citation_technical_report_institution|string|Institution which publishes the report|
|citation_technical_report_number|string|Paper ID as in the website|
|citation_journal_title|string|Journal title|
|citation_journal_issn|string|ISSN number|
|citation_pdf_url|string|Paper URL for PDF version|
|topics|string|Paper topic(s). Can be more tan one. Hence it is stored as an array|
|abstract|string|Paper abstract|
|also_downloaded|string|Users who downloaded this paper also downloaded* these. Can be more than one. Hence it is stored as an array. The reason I use the URL because otherwise it won't catch other than the working papers. Users may also download something from `/chapters/`, which may be useful for analysis|
|total_cites|integer|Total citations made by the author(s). Source: http://citec.repec.org/api/plain/RePEc:nbr:nberwo:[NBER_ID]|
|cited_by|integer|Total citations made by another author(s) from the author(s). Source: http://citec.repec.org/api/plain/RePEc:nbr:nberwo:[NBER_ID]|
|reference|string|A list of reference papers for each NBER paper. It is obtained from http://citec.repec.org/api/amf/RePEc:nbr:nberwo:[NBER_ID]
|acknowledgement|string|Paper's acknowledgement (in paragraph)|

2. [<strong>NBER citations (from RePEc)</strong>](https://github.com/ledwindra/nber/raw/master/data/repec.zip)

|column_name|data_type|description|
|-|-|-|
|id|integer|NBER working paper ID|
|total_cites|integer|Total cites for each paper|
|cited_by|integer|Numbers of times each paper being cited by other researchers|
|reference|string|A list of references for each paper|

3. [<strong>Wikipedia</strong>](https://raw.githubusercontent.com/ledwindra/nber/master/data/wikipedia.csv)

Columns are not fixed because each economist may have different completeness of information.

# Use case
What can be done from this dataset? Well, let's take a look at `index.ipynb`. 📙

# Permission

1. NBER
Check its [<strong>`robots.txt`</strong>](http://data.nber.org/robots.txt)

Following is the snippet:

```
User-agent: *
Crawl-delay: 10

User-agent: *
Disallow: /fda/
Disallow: /contact/
Disallow: /confer/
Disallow: /~confer/
Disallow: /conf_papers/
Disallow: /c/
Disallow: /wpsubmit/
Disallow: /custom
Disallow: /confsubmit/
Disallow: /family/
Disallow: /1050/
Disallow: /cal/
Disallow: /cgi-bin/
Disallow: /nberhistory/historicalarchives/
Disallow: /xming*
Disallow: /taxex/
Disallow: /papers/mail
Disallow: /tmp/
Disallow: /server-status/
Disallow: /mrtg/
Disallow: /bb/
Disallow: /img/
Disallow: /pics
Disallow: /*.ris$
Disallow: /*.marc$
Disallow: /*.bib$
Disallow: /*palm*$
Disallow: /taxsim-calc*/
Disallow: /medicare/
Disallow: /*.pl/
Disallow: /arfpub/
Disallow: /pscp*
Disallow: /jobs/stateforms/
Disallow: /hcris/
```

Everybody is not disallowed to get `/papers/` tag. However, please scrape ethically by setting time interval between each request for 10 seconds (see `Crawl-delay: 10`).

2. RePEc

Coming from its open API: http://citec.repec.org/api.html

3. Wikipedia

Check [robots.txt](https://en.wikipedia.org/robots.txt):

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

We're using `https://en.wikipedia.org/wiki/` so it's safe.

# Closing

If you have read up to this line, thank you for bearing with me. Hope this is useful for your purpose! 😎 🍻
