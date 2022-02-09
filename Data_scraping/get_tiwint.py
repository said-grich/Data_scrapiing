from datetime import datetime

from black import json
import twint
def twitterScrapper(h):
    c = twint.Config()
    c.Search=h+" hotel"
    c.Store_csv = True
    c.Output=h+".csv"
    c.Lang = "en"
    c.Pandas = True
    twint.run.Search(c)
    tw_list=[];
    Tweets_df = twint.storage.panda.Tweets_df
    for ind in Tweets_df.index:
        date=Tweets_df['date'][ind]
        date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date = date.strftime("%B %Y")
        text=Tweets_df['tweet'][ind].replace("'",' ')
        text=text.replace('"',' ');
        print(text)
        res={
        "name": Tweets_df['name'][ind],
        "nationality": "twitter",
        "number_of_nights": "nan",
        "clinet_type": "nan",
        "room_type": "nan",
        "review_date": "nan",
        "visite_date": date,
        "text":text ,
        "score": "5"
        }
        tw_list.append(res)
    return tw_list
if __name__=='__main__':
    list=['argana agadir','wazo','syvo'];
    for h in list:
       data= twitterScrapper(h);
       print(data);
