# twitter-echo-bot
A little script that takes the latest tweets from an account and re-posts them on the bot's account. Powers @potusfollowbot

```
usage: bot.py [-h] [--no-post] [--twitter-key STRING]
              [--twitter-secret STRING] [--twitter-access-token STRING]
              [--twitter-access-secret STRING] [--follow-account STRING]

Echo Bot. Get some tweets and repost them to your account

optional arguments:
  -h, --help            show this help message and exit
  --no-post, -n         Don't repost the items, just print them
  --twitter-key STRING, -k STRING
                        The twitter api key
  --twitter-secret STRING, -s STRING
                        The twitter api secret
  --twitter-access-token STRING, -T STRING
                        The twitter access token
  --twitter-access-secret STRING, -S STRING
                        The access secret
  --follow-account STRING, -f STRING
                        The account to pull tweets from.
```

All arguments except for `--no-post` can use environment variables instead
Ex: `TWITTER_KEY`

For now the script just runs once. To continue reading from twitter I use
a cron script to run the bot every few minutes. Perhaps I'll make a main 
loop at some point.
