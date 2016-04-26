from django.db import models

class User(models.Model):
    email = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    def __str__(self):
        return self.email

class Site(models.Model):
    name = models.CharField(max_length=200)
    krajina = models.CharField(max_length=250)
    oblast = models.CharField(max_length=250)
    rajon = models.CharField(max_length=250)

    rozpl = models.IntegerField(default=0)
    ploshch = models.IntegerField(default=0)

    toppotype = models.CharField(max_length=30)
    geomorform = models.CharField(max_length=250)
    vysotnadrm = models.IntegerField(default=0)
    vysotnadrm = models.IntegerField(default=0)

    chron = models.CharField(max_length=250)
    nvchron = models.CharField(max_length=250)
    data = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

