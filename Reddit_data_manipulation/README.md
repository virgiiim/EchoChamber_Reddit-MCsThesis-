# REDDIT ANALYSIS (Iannini)
Creazione dei profili - gli output degli script sono tutti csv: 

1. attraverso filtra_per_subreddit.py sono selezionati solo i post dei seguenti subreddit: 

    "The_Donald", "Trumpgret", "hillaryclinton", "politics", "Feminism", "MensRights", "news", "Libertarian", "Conservative", "worldnews", "science", "movies", "Music","blog","books", "television","gadgets", "sports", "soccer", "Futurology", "history", "personalfinance", "technology", "atheism", "europe", "relationships", "Games", "lgbt"

2. con seleziona_utenti.py vengono filtrati gli utenti per numero di attività: per ogni utente vengono considerati come subreddit in cui questo ha partecipato solo i subreddit con un numero minimo di attività (submission + commenti) uguale a 10. Infine, vengono selezionati solo gli utenti che hanno almeno 3 subreddit che hanno superato il primo filtro.

3. get_features_utenti.py genera le features seguenti:

    "name", "tot_activities", "%_submission", "%_controversial", "%_gilded", "avg_text_length", "min_score", "max_score", "avg_score", "std_score", "avg_attivita_mese", "n_mesi_inattivita", "std_attivita_mese", "month_kurt", "month_skew", "n_attivita_fav_subr", "n_subr", "avg_attivita_subr", "std_attivita_subr", "subr_kurt", "subr_skew"

4. text_processing.py - non utilizzato per il clutering - "leggendo" i commenti, genera un file per il testo normalizzato tramite stemming + sostituzione delle Named Entities, e uno per il sentiment associato alle entità nominate rilevate; per sentiment analysis si è utilizzato Vader (NLTK), mentre per NE-recognition il tagger di Stanford (3 classi)
