from twitter import OAuth
from twitter.api import Twitter
import module
import fields

# TODO hide these
con_key = 'f5z6uqPM9N87KLJqYIZDg'
con_secret = 'U52jwVDHn2bMXV5utkY7pTg1sptSwSNDRMP4sZNtGE'
acc_token = '2349175134-ashz2TRocXgOtEw9HGQDBt101hKrl0Bs4VMRw5R'
acc_token_secret = 'HNJ4vRivioSCNI0tNCpYi0TArynG0kz47S9JABIN2eTXC'

twitter = Twitter(auth=OAuth(acc_token, acc_token_secret,
    con_key, con_secret))

class Twitter(module.Base):
    public_name = 'Twitter'
    class tweet(fields.io.Writable, fields.io.Readable,
            fields.syntax.String, fields.persistant.Volatile,
            fields.Base):
        def write(self, value):
            if len(value) >= 128: # magic number FTW
                return False
            twitter.statuses.update(status=value)
            return True
