import numpy as np
import pandas as pd
import os
import datetime
from scipy import stats

"""genera le features degli utenti a partire dalla cartella dei file; costruisce un file utente-features"""

path = "filtered_subrs/"
selected_usernames = pd.read_csv("selected_usernames", names=["name"])
list_df = []

# legge i file nella cartella e inserisce i dati in un df

for filename in os.listdir(path):
    print("Working on {}".format(filename))

    df_small = pd.read_json(path + filename)
    df_small = df_small[df_small["author"].isin(list(selected_usernames["name"]))]

    if filename.split("_")[1] == "submission":
        df_small["is_submission"] = True
    else:
        df_small["is_submission"] = False

    list_df.append(df_small)
    print("{} completed! Df-size = {}".format(filename, df_small.size))

df = pd.concat(list_df)
df = df.fillna(0)
df["text_length"] = df["body"].apply(lambda x: len(x))


def get_month(tstamp):
    return int(datetime.datetime.fromtimestamp(int(tstamp)).strftime('%m'))


df["month"] = df["created_utc"].apply(lambda x: get_month(x))


class utente():

    def __init__(self, name):

        self.name = name
        self.distrib_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.distrib_subr = {}
        self.n_controversial = 0
        self.n_gilded = 0
        self.n_comments = 0
        self.n_submission = 0
        self.tot_activities = 0
        self.all_scores = []
        self.tot_text_length = 0

    def extract_features(self, controversiality, gilded, is_submission, score, subreddit, text_length, month):
        # iterativamente aggiorna i campi

        if controversiality:
            self.n_controversial += 1
        if gilded:
            self.n_gilded += 1

        if is_submission:
            self.n_submission += 1
        else:
            self.n_comments += 1

        self.tot_activities += 1

        self.all_scores.append(int(score))
        self.tot_text_length += text_length

        if subreddit not in self.distrib_subr:
            self.distrib_subr[subreddit] = 1
        else:
            self.distrib_subr[subreddit] += 1

        self.distrib_month[int(month) - 1] += 1

    def transform_features(self):
        # costruisce nuove features

        self.fraction_controversial = self.n_controversial / self.tot_activities
        self.fraction_gilded = self.n_gilded / self.tot_activities
        self.fraction_submission = self.n_submission / self.tot_activities
        self.avg_text_length = self.tot_text_length / self.tot_activities

        self.all_scores = sorted(self.all_scores)
        self.min_score = self.all_scores[0]
        self.max_score = self.all_scores[-1]
        self.avg_score = np.mean(self.all_scores)
        self.std_score = np.std(self.all_scores)

        self.avg_attivita_mese = np.mean(self.distrib_month)
        self.n_mesi_inattivita = self.distrib_month.count(0)
        self.std_attivita_mese = np.std(self.distrib_month)
        self.month_kurtosis = stats.kurtosis(self.distrib_month)
        self.month_skewedness = stats.skew(self.distrib_month)

        self.subr_list = sorted(list(self.distrib_subr.values()))
        self.n_attivita_favourite_subr = self.subr_list[-1]
        self.n_subr = len(self.subr_list)
        self.avg_attivita_subr = np.mean(self.subr_list)
        self.std_attivita_subr = np.std(self.subr_list)
        self.subr_kurtosis = stats.kurtosis(self.subr_list)
        self.subr_skewedness = stats.skew(self.subr_list)

    def get_user_features(self):

        return (self.name, self.tot_activities, self.fraction_submission, self.fraction_controversial,
                self.fraction_gilded, self.avg_text_length, self.min_score, self.max_score, self.avg_score,
                self.std_score, self.avg_attivita_mese, self.n_mesi_inattivita, self.std_attivita_mese,
                self.month_kurtosis, self.month_skewedness, self.n_attivita_favourite_subr, self.n_subr,
                self.avg_attivita_subr, self.std_attivita_subr, self.subr_kurtosis, self.subr_skewedness)


diz_users = {}

for index, row in df.iterrows():

    if row["author"] not in diz_users:
        diz_users[row["author"]] = utente(row["author"])

    diz_users[row["author"]].extract_features(row["controversiality"], row["gilded"], row["is_submission"],
                                              row["score"],
                                              row["subreddit"], row["text_length"], row["month"])

new_rows = []

for user in diz_users.values():
    user.transform_features()
    new_rows.append(user.get_user_features())

new_cols = ["name", "tot_activities", "%_submission", "%_controversial", "%_gilded", "avg_text_length", "min_score",
            "max_score", "avg_score", "std_score", "avg_attivita_mese", "n_mesi_inattivita", "std_attivita_mese",
            "month_kurt", "month_skew", "n_attivita_fav_subr", "n_subr", "avg_attivita_subr", "std_attivita_subr",
            "subr_kurt", "subr_skew"]

print("FINISHED!")

df_new = pd.DataFrame(new_rows, columns=new_cols)

df_new.to_csv("utenti_features.csv", index=False)
