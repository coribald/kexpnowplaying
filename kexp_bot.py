import urllib, json, time, tweepy
from datetime import datetime, timedelta
from time import gmtime, strftime
from user_vars import * 

url= "https://legacy-api.kexp.org/play/?limit=1"
last=""
post=""
last_enc=""
post_enc=""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def getTimeFormatted():
    q = datetime.now()
    i = q + timedelta(hours=0)
    return i.strftime('%Y-%m-%dT%H:%M:00Z')


def getNowPlaying():
    ti = getTimeFormatted()
    url2 = url + "&end_time=" + ti
    print str(url2)
    try:
        re = urllib.urlopen(url2)
        da = json.loads(re.read())
        print str(da)
    except:
        return 3
    try:
        ptid = da["results"][0]["playtype"]["playtypeid"]
        if ptid == 4:
            print "air break"
            return 4
        t = da["results"][0]["track"]["name"].encode('utf-8')
        print str(t)
        ar = da["results"][0]["artist"]["name"].encode('utf-8')
        print str(ar)
    except:
        print "artist or track json" 
        return 4
    try:    
        al = da["results"][0]["release"]["name"].encode('utf-8')
        print str(al)
    except:
        print "error parsing album, setting to none"
        al = "(No Album)"
        return ar + " - " + t
    try:
        y = str(da["results"][0]["releaseevent"]["year"]).encode('utf-8')
    except:
        y ="none"
        return ar + " - " + t + " - " + al
    print str(y)
    if y == "None":
        return ar + " - " + t + " - " + al
    else:
        return ar + " - " + t + " - " + al + " (" + y + ")"

def getLastTweet():
    l = api.user_timeline(screen_name="KEXPNowPlaying",count = 1)[0]
    return l.text

while True:
    now_playing = getNowPlaying()
    if now_playing == 4:
        time.sleep(10)
    elif now_playing == 3:
        time.sleep(3)
    else:
        try: 
            post_enc = now_playing
            print "new="+post_enc
        except:
            print "error getting/parsing now playing"
            print "failed on: " + str(now_playing)
        try:
            last = getLastTweet()
            last2 = last.encode('utf-8')
            last_enc = last2.replace("amp;","")
            print "last="+last_enc
        except:
            print "error getting last tweet"
            print "failed on: " + str(last)
        if last_enc != post_enc:
            print "new track detected. posting"
            try:
                api.update_status(status=post_enc)
            except Exception, e:
                print "error posting, details: "
                print str(e)
        else:
            print "track is already present. not posting."
        time.sleep(60)

