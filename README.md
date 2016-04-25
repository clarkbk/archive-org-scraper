## Purpose

Scrape a Webshots user's photos from the Internet Archive (archive.org).

Images are saved in folders in an `/output` directory inside the project, each corresponding to a Webshots album. Each folder also contains a text file with album metadata.

## Configuration

Install requirements and set environment variables.

In the command line:

```bash
$ mkvirtualenv archive-org-scraper
$ pip install -r requirements.text
$ touch .env
```

In `.env`:

```bash
source ~/.virtualenvs/archive-org-scraper/bin/activate
export WEBSHOTS_USER=…
```

## Use

Source required environment variables, and then:

```bash
$ python run.py
```
