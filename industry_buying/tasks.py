import pandas as pd
from celery import shared_task
from industry_buying.models import IndustryDataCollection

@shared_task
def populate_db_with_csv_data():
    df=pd.read_csv('cunique.csv',sep=',')
    row_iter = df.iterrows()
    objs = [
        IndustryDataCollection(
            Message = row["Message"],
            phone = row["phone"],
            cube = row["cube"],
            google = row["google"],
            google_spam = row["google_spam"],
            google_not_spam = row["google_not_spam"],
            ibm = row["ibm"],
            ibm_spam = row["ibm_spam"],
            ibm_not_spam = row["ibm_not_spam"]
        )
        for index, row in row_iter
    ]
    IndustryDataCollection.objects.bulk_create(objs)
    return
    