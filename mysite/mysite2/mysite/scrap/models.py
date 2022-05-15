from django.db import models

# Create your models here.

class RawInfo(models.Model):
    ztb_type = models.IntegerField(null=True)
    subclass = models.CharField(max_length=50)
    site = models.CharField(max_length=255,null=True)
    page_url = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    craw_status = models.IntegerField(null=True)
    duration = models.IntegerField(null=True)
    issue_time = models.DateTimeField(null=True)
    remark = models.CharField(max_length=100)
    process_status = models.IntegerField(null=True)
    creation_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    modified_time = models.DateTimeField(null=True)

