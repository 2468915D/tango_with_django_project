from django.db import models

# Create your models here.

class Catergory(models.Model):
	name = models.CharField(max_length=128, unique=True)

	class Meta:
		verbose_name_plural = "Catergories"

	def __str__(self):
		return self.name


class Page(models.Model):
	catergory = models.ForeignKey(Catergory, on_delete=models.CASCADE)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.title