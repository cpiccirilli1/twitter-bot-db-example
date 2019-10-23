import tweepy
import json
from quoteBase import QuoteBase as qb
import argparse


class Bot(qb):

    def __init__(self, db):
        qb.__init__(self, db)
        self.api = None
        self.me = None

    def credentials(self):
        """
        gets credentials from json and authenticates user.
        sets credentials as self.api. Must be called first.
        :return:
        """
        with open("secret.json", "r") as secret:
            k = json.load(secret)

        keys = k[0]
        auth = tweepy.OAuthHandler(keys["Consumer_Key"], keys["Consumer_Secret"])
        auth.set_access_token(keys["Access_Token"], keys["Access_Secret"])

        redirect_url = None
        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            print('Error! Failed to get request token.')

        try:
            self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            self.api.verify_credentials()
            self.me = self.api.me()
            print("Authentication OK")
        except Exception as e:
            print("Error during authentication:")
            print(str(e), str(e).__class__)

    def post_short_status(self, update):
        id, author, source, quote = update
        post_string = f"{quote} - {author}, {source}"
        try:
            self.api.update_status(post_string)
            print("Posted short status.")
        except tweepy.error.TweepError as e:
            a = str(e)
            print(a, a.__class__())

    def chunk_update(self, update_tuple):
        """
        Takes a string and breaks it up into chunks to be posted later.
        :param update:
        :return:
        """

        id, author, source, quote = update_tuple
        update = f"{quote} - {author}, {source}"
        sect = 140
        chunks = [update[i:i+sect] for i in range(0, len(update), sect)]
        return chunks

    def post_long_status(self, update):

        quote_chunks = self.chunk_update(update)
        for c in quote_chunks:
            try:
                self.api.update_status(c)
                print("posted long status")
            except tweepy.error.TweepError as e:
                a = str(e)
                print(a, a.__class__())

    def main(self):
        self.credentials()
        quote = self.get_random_quote()
        print(quote)
        if len(quote[3]) >= 140:
            print("long")
            self.post_long_status(quote)
        else:
            print("short")
            self.post_short_status(quote)


if __name__ == "__main__":
    b = Bot("quote.db")
    b.main()