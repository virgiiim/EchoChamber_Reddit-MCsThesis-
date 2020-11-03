import bz2
import json
import sys
import lzma

"""filtra i commenti, eliminando quelli che non appartengono ai subreddit selezionati; genera file per ogni mese, commenti e submission separate
   argomento1: numero del mese in due cifre
   argomento2: percorso del file
   argomento3: b,c o s, a seconda se si vogliono selezionare sia commenti che submission -(b)oth-, solo (c)ommenti, solo (s)ubmission
"""


def filtra_commenti(my_file):
    # filtra i commenti per subreddit (in base a my_subr); genera il file

    all_dicts = []
    filetype = my_file.rsplit(".")[-1]

    if filetype == "bz2":
        comm_file = bz2.BZ2File(my_file)
    elif filetype == "xz":
        comm_file = lzma.open(my_file)
    else:
        print("ERRORE: tipo file non valido")

    while True:
        line = comm_file.readline()
        if len(line) == 0:
            break
        comment = json.loads(line)

        try:

            subr = comment["subreddit"]
            if subr in my_subr:
                if comment["body"] != "[deleted]":
                    diz = {"author": comment["author"], "subreddit": comment["subreddit"], "score": comment["score"],
                           "controversiality": comment["controversiality"], "gilded": comment["gilded"],
                           "body": comment["body"], "created_utc": comment["created_utc"],
                           "id": comment["id"], "parent_id": comment["parent_id"]}

                    all_dicts.append(diz)

        except KeyError:
            pass

    with open("filtered_subrs/small_commenti_filtrati" + sys.argv[1], "w") as outfile:
        jsonData = json.dump(all_dicts, outfile, indent=1)
        if type(jsonData) == str:
            outfile.write(jsonData)


def filtra_submission(my_file):
    # filtra le submission per subreddit (in base a my_subr); genera il file

    all_dicts = []
    filetype = my_file.rsplit(".")[-1]

    if filetype == "bz2":
        comm_file = bz2.BZ2File(my_file)
    elif filetype == "xz":
        comm_file = lzma.open(my_file)
    else:
        print("ERRORE: tipo file non valido")

    while True:
        line = comm_file.readline()
        if len(line) == 0:
            break
        subm = json.loads(line)

        try:

            subr = subm["subreddit"]

            if subr in my_subr:
                diz = {"author": subm["author"], "subreddit": subm["subreddit"], "score": subm["score"],
                       "gilded": subm["gilded"], "body": subm["title"], "created_utc": subm["created_utc"],
                       "id": subm["id"]}

                all_dicts.append(diz)

        except KeyError:
            pass

    with open("filtered_subrs/small_submission_filtrate" + sys.argv[1], "w") as outfile:
        jsonData = json.dump(all_dicts, outfile, indent=1)
        if type(jsonData) == str:
            outfile.write(jsonData)


if len(sys.argv) < 2:
    print("ERRORE: inserire data e percorso")

my_subr = ["The_Donald", "Trumpgret", "hillaryclinton", "politics", "Feminism", "MensRights",
           "news", "Libertarian", "Conservative", "worldnews", "science", "movies", "Music",
           "blog", "books", "television", "gadgets", "sports", "soccer", "Futurology", "history",
           "personalfinance", "technology", "atheism", "europe", "relationships", "Games", "lgbt"]

path = sys.argv[2] + "/"

print("sto lavorando su {}...\n".format("2017-" + sys.argv[1]))

# provvisorio - si dovrebbe fare un controllo per file (estensione); il file di dicembre è in formto .xz, gli altri .bz2

if sys.argv[1] == "12":
    filetype = ".xz"
else:
    filetype = ".bz2"

if sys.argv[3] == "b":
    filtra_commenti(path + "RC_2017-" + sys.argv[1] + filetype)
    filtra_submission(path + "RS_2017-" + sys.argv[1] + filetype)
elif sys.argv[3] == "c":
    filtra_commenti(path + "RC_2017-" + sys.argv[1] + filetype)
elif sys.argv[3] == "s":
    filtra_submission(path + "RS_2017-" + sys.argv[1] + filetype)
else:
    print("ERRORE! Inserire b(oth), c(omments) o s(ubmissions)")

print("\nFINITO!\n")
