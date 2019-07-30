import couchdb  # Libreria de CouchDB (requiere ser instalada primero)
from tweepy import \
    Stream  # tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json  # Libreria para manejar archivos JSON

ckey = "qt7LQK9IYQWuFX69925Xobl4g"
csecret = "IBtPKNZvAqPmrBWDQ0cWKv5nHmTOXb1e2qZJJb455lPgNtBCp4"
atoken = "115946548-mxE9opv0ejiCsJmy0RMB0uq3mVLamoAhrUi3pn94"
asecret = "6A4iV1tlXOA4WsxQMMSewCyUnC72YBwax6Bn7FqubZ4ta"

class listener(StreamListener):
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["text"] = str(dictTweet['text'])
            cadena = str(dictTweet['text'])
            if 'dota2' in cadena:
                print("Guardado " + "=> " + dictTweet["text"])
                doc = db.save(dictTweet)  # Aqui se guarda el tweet en la base de couchDB
            if 'Dota2' in cadena:
                print("Guardado " + "=> " + dictTweet["text"])
                doc = db.save(dictTweet)  # Aqui se guarda el tweet en la base de couchDB
        except:
            print("Documento ya existe")
            pass
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
# Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    db = server.create('dota')
except:
    db = server['dota']

twitterStream.filter(locations=[-93.37,-17.83,-53.36,25.41])