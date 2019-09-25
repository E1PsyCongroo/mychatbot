# Mychatbot
a music chatbot on Telegram supported by Rasa NLU

## Telegram
- [Telegram bot API](https://core.telegram.org/bots/api) : The Bot API is an HTTP-based interface created for developers keen on building bots for Telegram
- [pyTelegramBot API](https://github.com/eternnoir/pyTelegramBotAPI) : A simple, but extensible Python implementation for the Telegram Bot API.

## Rasa NLU
- use data 'rasa_train.json' to train the model
- rasa pipline:`pretrained_embeddings_spacy`:
  -  "SpacyNLP"
  -  "SpacyTokenizer"
  -  "SpacyFeaturizer"
  -  "RegexFeaturizer"
  -  "CRFEntityExtractor"
  -  "EntitySynonymMapper"
  -  "SklearnIntentClassifier"
  
## APIs & Database
- [AudD API](https://rapidapi.com/AudD/api/audd): AudD® Music Recognition API recognizes music by sound from files and microphone recordings with noise. 
- [Deezer API](https://rapidapi.com/deezerdevs/api/deezer-1): Deezer is the No. 1 site for listening to music on demand.
- sqlite3 for Database

## note
- view the final result by "Music chatbot_by Xuanhe Chen.mp4"
- all of the API keys and databases have benn removed for security

## Doc
Chinese version doc is avaliable [`Doc.pdf`](https://github.com/E1PsyCongroo/mychatbot/blob/master/Doc.pdf)
