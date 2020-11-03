import json
import os

"""seleziona solo gli utenti che hanno un numero di attività minimo; genera un file coi nomi utente"""


class utente(object):

    def __init__(self, uid):
        
        self.diz_activities = {}
        self.cleaned_diz = {}
        self.uid = uid

    def add_activity(self, activity, is_submission):
        
        subreddit = activity['subreddit']
        
        if is_submission:
            if subreddit not in self.diz_activities:
                self.diz_activities[subreddit] = [0,1]
            else:
                self.diz_activities[subreddit][1] += 1
        else:        
            if subreddit not in self.diz_activities:
                self.diz_activities[subreddit] = [1,0]
            else:
                self.diz_activities[subreddit][0] += 1

    def remove_small(self):
        
        for k,v in self.diz_activities.items():
            if (v[0]+v[1]) >= 10:
                self.cleaned_diz[k] = v            
                
    def get_diz(self):
        
        return self.cleaned_diz


path = "filtered_subrs/"
diz_all_users = {}

for filename in os.listdir(path):
    print(filename)
    with open(path+filename) as fileinp:
        data = json.load(fileinp)
        print("n records:",len(data))
        
        is_submission = filename.split("_")[1] == "submission"
        
        for activity in data:
            auth = activity['author']
            if  auth != "[deleted]" and auth != "AutoModerator":
                if auth not in diz_all_users:
                    diz_all_users[auth] = utente(auth)
                
                diz_all_users[auth].add_activity(activity, is_submission)
        print(filename, "finito!")

for author in diz_all_users.keys():
    diz_all_users[author].remove_small()

with open("selected_usernames", "w") as file_users:
    for k,v in diz_all_users.items():
        if len(v.get_diz()) > 2:
            file_users.write(k + "\n")
