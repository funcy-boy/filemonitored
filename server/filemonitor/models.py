from django.db import models


# Create your models here.

class change_dir(models.Model):
	id = models.AutoField(primary_key=True)
	src_dir = models.CharField(max_length=255)
	ipaddr = models.CharField(max_length=15)
	change_time = models.CharField(max_length=30)
	add_time = models.CharField(max_length=30)
	event_type = models.CharField(max_length=10)

# def __str__(self):
# 	return self.src_dir, self.ipaddr, self.change_time, self.add_time,self.event_type
