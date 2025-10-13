from django.db import models
from django.urls import reverse

# Create your models here.

class Period(models.Model):
  title =  models.CharField(max_length=200, null=True)
  message_for = models.TextField( null=True)
  message_against = models.TextField( null=True)

  class Meta:  
    ordering = ['id']


  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('detail_page', args=[str(self.id)])
  



class YearlyPeriod(models.Model):
  title =  models.CharField(max_length=200, null=True)
  message_for = models.TextField( null=True)
  message_against = models.TextField( null=True)

  class Meta:  
    ordering = ['id']


  def __str__(self):
    return self.title

  
  class Meta:  
    ordering = ['-id']  # Order by created_at descending  