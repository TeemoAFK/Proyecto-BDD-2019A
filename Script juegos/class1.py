import couchdb  # Libreria de CouchDB (requiere ser instalada primero)
from tweepy import \
    Stream  # tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json  # Libreria para manejar archivos JSON

ckey = "Lz3BzqoqPJA7hrLE7XnYOncdH"
csecret = "1MRn8ElY8Ea24HBSXCvIrVTR0rx3vWA8WFOgEtaTH8SfBQ4uY1"
atoken = "742503304056459264-a8gYllNQEpKAP3O8f73cUgUcoyIdZ0D"
asecret = "LO4oZ55UiXWBlFPuvub78TcDt1vTjAzNYaOecOMMXoK6q"

class listener(StreamListener):
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["text"] = str(dictTweet['text'])
            cadena = str(dictTweet['text'])
            if 'fornite' in cadena:
                print("Guardado " + "=> " + dictTweet["text"])
                doc = db.save(dictTweet)  # Aqui se guarda el tweet en la base de couchDB
            if 'Fornite' in cadena:
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
    db = server.create('fornite')
except:
    db = server['fornite']

twitterStream.filter(locations=[-93.37,-17.83,-53.36,25.41])