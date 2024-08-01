#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[5]:


import re
import numpy as np
from countrycode import countrycode
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number
import nltk
from nltk.corpus import stopwords
from tqdm.notebook import tqdm_notebook
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from pathlib import Path
from nltk.corpus import stopwords
import nltk
import spacy
import string
from pprint import pprint


# # Configuration

# In[2]:


plt.rcParams["figure.figsize"] = (10, 10)
pd.set_option('display.max_colwidth', None)


# In[3]:


argentina_area_codes = pd.read_csv("./argentina-area-codes.csv")


# In[ ]:


argentina = geopandas.read_file("./localidades.shp")
argentina.plot()


# In[5]:


nltk.download("stopwords")


# ## Load toxicity model

# In[6]:


from detoxify import Detoxify
model = Detoxify('multilingual')

def get_toxicity(message):
  return model.predict(message)["toxicity"]


# # Read from file

# ## Read from pickel file if exists

# In[6]:


path = Path("./Chat_as_DF.pkl")
if path.is_file():
    after_process = pd.read_pickle(path)
    print(u'\u2713')


# In[9]:


after_process


# ## Read from txt file

# In[4]:


splitted_chat = []
with open("./chats/chats.txt", "r") as chat:
    all_chat = chat.read().replace("\n", " ")
    splitted_chat = re.findall("\d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2} - \+[()\d\w\s-]+: [\s\S]*?(?=\d{1,2}\/\d{1,2}\/\d{4}, \d{1,2}:\d{2} - \+|$)", all_chat)


# In[ ]:


def get_argentina_region(code):
    rows = argentina_area_codes[argentina_area_codes["code"] == code]
    if len(rows):
        return list(rows["localidad"]), rows.iloc[-1]["provincia"]
    else:
        return None, None


# In[5]:


def process_line(line):
    #10/3/2024, 12:44 - +54 9 11 3763-1285: Muchas Gracias !!! Ya compre entradas.
    regex_result = re.search("^(\d{1,2}\/\d{1,2}\/\d{4}), (\d\d:\d\d) - (\+(\d*) (?:9 (\d*)|([()\d\w\s-]*))([()\d\w\s-]*)): ([\s\S]*)$", line)
    Message_Raw = line
    date = regex_result.group(1)
    time = regex_result.group(2)
    phone_number = phonenumbers.parse(regex_result.group(3))
    country = region_code_for_number(phone_number)
    argentina_town,argentina_province = get_argentina_region(int(regex_result.group(5))) if country == "AR" else (None,None)
    message = regex_result.group(8)
    toxicity = get_toxicity(message)
    date = datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
    return pd.DataFrame([{
            "User": phone_number,
            "plain_phone_number": regex_result.group(3),
            "Country": country,
            "Message_Raw": Message_Raw,
            "Argentina_Province": argentina_province,
            "Argentina_Location": argentina_town,
            "Message_Clean": message,
            "Message_Only_Text": message.lower() ,
            "Toxicity": toxicity,
            "Date": date,
            "Hour": date.hour,
            "Day_of_Week": date.weekday()
           }])


# In[6]:


after_process = pd.DataFrame()
with tqdm_notebook(total=len(splitted_chat)) as progress_bar:
    for line in splitted_chat:
        try:
            processed_line = process_line(line)
            after_process = pd.concat([after_process, processed_line])
        except Exception as err:
            print(f"EXCEPTION {err} on line {line}")
            pass
        finally:
            progress_bar.update(1)

after_process.to_pickle("Chat_as_DF.pkl")


# # Data processing

# In[8]:


first_interaction_for_each_person = after_process.groupby("plain_phone_number").first().reset_index()


# In[9]:


messages_by_person = after_process.groupby("plain_phone_number")


# In[10]:


keys = set(after_process["plain_phone_number"])


# In[11]:


column_aggregation = {
    "avg_message_length": lambda x: np.mean(x["Message_Clean"].str.len()),
    "total_char_length": lambda x: np.sum(x["Message_Clean"].str.len()),
    "total_messages": lambda x: len(x)
}
messages_aggregated = pd.DataFrame()
for label, function in column_aggregation.items():
    messages_aggregated[label] = messages_by_person.apply(function)


# ## Message by person

# In[8]:


after_process[after_process["plain_phone_number"] == "+54 9 11 4420-7572"]


# # Metrics

# ## Messages sent by country

# In[ ]:


first_interaction_for_each_person.groupby(["Country"]).count().sort_values(ascending=False,by="User")


# ## Message sent by province

# In[ ]:


first_interaction_for_each_person.groupby(["Argentina_Province"]).count().sort_values(ascending=False,by="User")


# ## Messages by location

# In[ ]:


first_interaction_for_each_person["stringified_argentina_location"] = first_interaction_for_each_person["Argentina_Location"].astype(str)
first_interaction_for_each_person.groupby("stringified_argentina_location").count().sort_values(ascending=False, by="User")


# In[ ]:


messages_by_person["plain_phone_number"].count().sort_values(ascending=False).head(20).plot(kind="bar")


# ## Get messages for a person

# In[ ]:


print(after_process[after_process["plain_phone_number"] == "54 9 221 602-2258"]["Message_Clean"])


# ## Day with max number of messages for each person

# In[ ]:


max_messages_on_a_day_per_person = after_process.groupby(["plain_phone_number", after_process["Date"].dt.date]).count().sort_values(by="Hour").groupby(level=0).tail(1).sort_values(ascending=False, by="Hour")

max_messages_on_a_day_per_person["Date"].reset_index(name="Total messages")


# ## Day of the week with most messages for each person

# In[ ]:


import calendar

messages_by_day_of_week = after_process.groupby(["plain_phone_number", after_process["Date"].dt.weekday]).count().sort_values(by="Hour")["Date"]

matrix_of_messages = messages_by_day_of_week.unstack()
matrix_of_messages.columns = map(lambda x: calendar.day_name[x],matrix_of_messages.columns)
matrix_of_messages.style.background_gradient(cmap="RdYlGn")


# ## Top 10 days with higher number of messages

# In[ ]:


higher_number_of_messages = after_process.groupby(after_process["Date"].dt.date).count()

for day in higher_number_of_messages.nlargest(columns="Hour", n=10).iterrows():
    print(f'Day (YYYY-MM-dd): {day[0]} - Number of messages: {day[1]["Hour"]}')


# ## Hour with the higher number of messages overall

# In[ ]:


higher_number_of_messages_of_hour = after_process.groupby(after_process["Date"].dt.hour).count()


print(f'Hour: {higher_number_of_messages_of_hour.idxmax()["Date"]} - Number of messages: {higher_number_of_messages.max()["Date"]}')


# ## Most messages in an hour

# In[ ]:


higher_number_of_messages = after_process.groupby([after_process["Date"].dt.date, after_process["Date"].dt.hour]).count()

print(f'Day (YYYY-MM-dd): {higher_number_of_messages.idxmax()["Date"][0]} - Hour: {higher_number_of_messages.idxmax()["Date"][1]} - Number of messages: {higher_number_of_messages.max()["Date"]}')


# ## Messages per hour

# In[ ]:


messages_per_hour = after_process.groupby("Hour")["Hour"].count().plot(kind="bar")


# ## Messages per day of the week

# In[ ]:


messages_per_hour = after_process.groupby(after_process["Date"].dt.isocalendar().day)["Hour"].count().plot(kind="bar", color="green")


# ## Messages per week of the each year

# In[ ]:


after_process.groupby([after_process["Date"].dt.month, after_process["Date"].dt.year])["Hour"].count().unstack(level=1).plot(kind="bar", color="dodgerblue", subplots=True)


# ## Message metrics per person

# ## Average length per person

# In[16]:


messages_aggregated.sort_values("avg_message_length",ascending=False).style.background_gradient(cmap="RdYlGn")


# ## Amount of characters written by each person

# In[18]:


messages_aggregated.sort_values("total_char_length",ascending=False).style.background_gradient(cmap="RdYlGn")


# ## Total messages per person

# In[ ]:


messages_aggregated.sort_values("total_messages",ascending=True).style.background_gradient(cmap="RdYlGn")


# ## Who laugh the most?

# In[13]:


def is_laugh(message):
    reg = re.compile(r"^.*\b[JjeEiIAakKSs]{3,}\b.*$")
    is_jj = re.compile(r"^.*\b[jJ][jJ]\b.*$")
    return bool(reg.match(message)) and bool(not is_jj.match(message))


# In[14]:


count_laughs = pd.DataFrame(keys, columns=["person"])
count_laughs["laugh_count"] = 0

for person, messages in messages_by_person:
    person = person
    messages = messages
    laugh_count_for_person = messages["Message_Clean"].apply(is_laugh).sum()
    count_laughs.loc[count_laughs['person'] == person, 'laugh_count'] += laugh_count_for_person

count_laughs.sort_values("laugh_count", ascending=False).head(20).plot(kind="bar", x="person", y="laugh_count")


# In[23]:


average_laughs = pd.DataFrame(keys, columns=["person"])
for _, item in count_laughs.iterrows():
    person = item["person"]
    average_laughs.loc[average_laughs['person'] == person, 'laugh_average'] = count_laughs.loc[count_laughs["person"] == person, "laugh_count"].iloc[0] / len(messages_by_person.get_group(person))

average_laughs.sort_values("laugh_average", ascending=False).head(20).plot(kind="bar", x="person", y="laugh_average")


# ## Average toxicity by person

# In[45]:


toxic_messages = after_process.groupby("plain_phone_number").mean(numeric_only=True)
toxic_messages["Toxicity"].sort_values(ascending=False).head(10).plot(kind="bar")


# ### Top 10 most toxic messages

# In[98]:


after_process.nlargest(10, "Toxicity")[["Message_Clean", "Toxicity","plain_phone_number","Date"]].reset_index()


# In[60]:


spanish_stopwords = stopwords.words("spanish")
spanish_stopwords.extend(["q", "dsp", "si", "<", ">", "multimedia", "omitido", "omitida", "\u200eaudio", "\u200eimagen", "\u200esticker", "\u200evideo", "\u200egif", "", "Hola", "t", "d", ""])


# In[63]:


nltk.download("punkt")
get_ipython().system('python -m spacy download es_core_news_sm')


# In[64]:


nlp = spacy.load("es_core_news_sm")


# In[65]:


def lemmatize(message):
    return [token.lemma_ for token in nlp(message)]

def remove_word(word):
    return word in spanish_stopwords or is_laugh(word) or len(word) <= 3

def process_message(message):
    return [ token for token in nltk.word_tokenize(message.translate(str.maketrans('', '', string.punctuation))) if not remove_word(token.lower()) ]


# In[66]:


process_message("Hola, como estas vos?")


# In[67]:


messages_without_stopwords = []
for index, message in after_process.iterrows():
    new_message = message.copy()
    new_message["Message_Only_Text"] = " ".join(process_message(message["Message_Only_Text"]))
    messages_without_stopwords.append(new_message)


# ## Most frequently used words per person

# In[89]:


messages_per_person_without_stopwords = {key: [] for key in keys}

for person, messages in messages_by_person:
    for message in messages.iterrows():
        new_message = process_message(message[1]["Message_Only_Text"])
        messages_per_person_without_stopwords[person].extend(new_message)


# In[82]:


most_used_words = dict.fromkeys(keys, 0)
for person in messages_per_person_without_stopwords:
    most_used_words[person] = Counter(messages_per_person_without_stopwords[person])


# In[102]:


Counter(messages_per_person_without_stopwords["+54 9 11 4420-7572"]).most_common(10)


# In[88]:


messages_per_person_without_stopwords


# In[ ]:




