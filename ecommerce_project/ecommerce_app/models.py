from django.db import models


# Item table
class Item(models.Model):
    item_name = models.CharField(max_length=30)
    no_of_items = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.item_name)


# Order table
class Order(models.Model):
    item_name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=50)
    email_id = models.EmailField()

    def __unicode__(self):
        return u'%s' % (self.quantity)

