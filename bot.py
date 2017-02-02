import os
import sys
import tweepy
import sqlite3
from traceback import format_exc
from w3lib.html import replace_entities
import time
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(description="Echo Bot. Get some tweets and repost them to your account")
parser.add_argument( '--no-post','-n', dest="no_post", action="store_true",help="Don't repost the items, just print them")
parser.add_argument( '--twitter-key','-k',metavar='STRING',type=str, dest='twitter_key', help="The twitter api key", default=os.environ.get('TWITTER_KEY'))
parser.add_argument( '--twitter-secret', '-s',metavar='STRING',type=str,dest='twitter_secret',help="The twitter api secret", default=os.environ.get('TWITTER_SECRET'))
parser.add_argument( '--twitter-access-token','-T',metavar='STRING',type=str,dest='twitter_access_token', help="The twitter access token",default=os.environ.get('TWITTER_ACCESS_TOKEN'))
parser.add_argument( '--twitter-access-secret','-S', metavar='STRING', type=str,dest='twitter_access_secret', help="The access secret",default=os.environ.get('TWITTER_ACCESS_SECRET'))
parser.add_argument( '--follow-account','-f', metavar='STRING', type=str,dest='follow_account', help="The account to pull tweets from.", default=os.environ.get('FOLLOW_ACCOUNT'))
args = parser.parse_args()

conn = sqlite3.connect('potusfollowbot.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='last_tweet'");
tblrow = c.fetchone()

print "[{}] Bot started".format(datetime.now())

if not tblrow:
    c.execute('CREATE TABLE last_tweet (id string)')

c.execute('SELECT id FROM last_tweet')
tweetrow = c.fetchone()
last_id = None
if tweetrow:
    last_id = tweetrow[0]
else:
    c.execute('INSERT INTO last_tweet VALUES("NONE")')
    conn.commit()
auth = tweepy.OAuthHandler( args.twitter_key, args.twitter_secret )
auth.set_access_token(args.twitter_access_token, args.twitter_access_secret )

twitter = tweepy.API(auth)

read_args = {
    'screen_name': args.follow_account
}
if last_id:
    read_args['since_id'] = last_id

tweets = twitter.user_timeline( **read_args )


# can't list and then reverse so this creates the list and then we'll back through
output = [] 
for t in tweets:
    output.insert(0, t)

for twit in output:
    if str(twit.id) == last_id:
        print 'skipped {}'.format(twit.id)
        continue # skip the first one if they are the same

    last_id = str(twit.id)
    newtwit = replace_entities(twit.text)
    print twit.text
    try:
        if not args.no_post:
            twitter.update_status(newtwit)
    except tweepy.error.TweepError as e:
        try:
            code = e.message[0]['code']
        except(IndexError,KeyError):
            code = None

        if code == 186:
            # split the message and link
            _len_diff = (len(newtwit) - 138) #ensure we can add back a space
            (text, link) = newtwit.split('https')
            _fixtext = text[0:(len(text) - _len_diff)]
            _fixtext += ' https' + link

            time.sleep(1) # make sure we don't rate limit 
            try:
                twitter.update_status(newtwit)
            except:
                #screw it
                print "tweet too long, unfixable"
                print format_exc()
        elif code == 187:
            print "skipped duplicate {}".format(last_id)
        else:
            print format_exc()

c.execute('UPDATE last_tweet SET id=?', (last_id,) )
conn.commit()
