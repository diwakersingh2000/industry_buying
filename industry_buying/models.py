from django.db import models

# Create your models here.
class IndustryDataCollection(models.Model):
    Message =  models.CharField(max_length=1000, null=True )
    phone =  models.CharField(max_length=20, null=True )
    truth =  models.CharField(max_length=100, null=True )
    cube =  models.CharField(max_length=100, null=True )
    google =  models.CharField(max_length=100, null=True )
    google_spam =  models.CharField(max_length=100, null=True )
    google_not_spam =  models.CharField(max_length=100, null=True )
    ibm =  models.CharField(max_length=100, null=True )
    ibm_spam =  models.CharField(max_length=100, null=True )
    ibm_not_spam =  models.CharField(max_length=100, null=True )

    def __str__(self):
        return str(self.phone) + " "+ str(self.Message[:20])
