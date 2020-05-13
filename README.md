# Daily Highlight 📖

Get a daily push notification containing one of your Kindle book highlights!

Only your highlights that are set to 'visible' will be retrieved from your
GoodReads account. Note that this does not use the
[GoodReads API](https://www.goodreads.com/api) as this does not support getting
highlights.

### Prerequisites
* [Python3](https://www.python.org/download/releases/3.0/)
* [pipenv](https://pypi.org/project/pipenv/)

### Setup

1. **Installation**

   Clone this repo and run:
   ```bash
   pipenv sync
   ```
1. **Create the IFTTT applet**

   1. If you don't already have one, sign up for an
      [IFTTT account](https://ifttt.com/) and download and login to the IFTTT
      app on the device you want to receive the push notification on
   1. [Create](https://ifttt.com/create) a new IFTTT applet
   1. For _This_, select the _Webhooks_ service and choose
      _Receive a web request_
   1. Enter `daily_highlight` as the Event Name and click _Create Trigger_
   1. For _That_, select the _Notifications_ service and choose
      _Send a rich notification from the IFTTT app_
   1. Change the _Title_ field to `{{Value1}}`
   1. Change the _Message_ field to `{{Value2}}`
   1. Change the _Image URL_ field to `{{Value3}}`
   1. Click _Create Action_ and then _Finish_
1. **Get your IFTTT Webhook API key**
   1. Go to your [Webhook Settings](https://ifttt.com/maker_webhooks/settings)
   1. Copy the API key listed as part of the URL
      (`https://maker.ifttt.com/use/<API-KEY>`) for use below

### Usage

1. Create a `.env` file in the root of the repo containing your GoodReads User
   ID and the IFTTT Webhook API key you retrieved above. You can find your
   GoodReads User ID by logging in to your account, going to the
   [My Kindle Highlights Notes & Highlights](https://www.goodreads.com/notes)
   page and then copying the ID that appears in the URL (e.g
   `https://www.goodreads.com/notes/<USER ID>-<NAME>`).
   ```bash
   $ cat .env

   GOODREADS_USER_ID=...
   IFTTT_API_KEY=...
   ```
1. To get a highlight sent to you via a push notification, run:
   ```bash
   pipenv run python send-highlight.py
   ```

Note that the environmental variables can also be stored in a `.env` file if
preferred.

### Getting a daily highlight

To get a highlight sent to you every day, you can use crontab on a device of
your choice. For example, to get a highlight at
[9am each weekday morning](https://crontab.guru/#0_9_*_*_1-5), edit your
crontab with `crontab -e` and add:
```
0 9 * * 1-5 cd ~/<path-to-repo>/daily-highlight && pipenv run python send-highlight.py
```
