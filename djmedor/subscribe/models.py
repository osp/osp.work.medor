# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    """ Describes a cooperator or a subscriber"""
    COUNTRY_CHOICES = (
        ('BE', u'Belgique'),
        ('FR', u'France'),
        ('LU', u'Luxembourg')
    )

    TITLE_CHOICES = (
        (0, u'Madame'),
        (1, u'Monsieur')
    )

    first_name = models.CharField('prénom', max_length=30)
    last_name = models.CharField('nom de famille', max_length=30)
    email = models.EmailField('courriel')
    birth_date = models.DateTimeField('date de naissance')
    title = models.BooleanField('civilité', default=False, choices=TITLE_CHOICES)

    nationality = models.CharField('nationalité', max_length=2, choices=COUNTRY_CHOICES, default="BE")
    id_number = models.CharField("numéro d'identité nationale", max_length=30)

    street = models.CharField('rue', max_length=30)
    number = models.CharField('numéro', max_length=10) # 27 bis
    letterbox = models.PositiveSmallIntegerField('boîte postale', max_length=30, null=True, blank=True)
    city = models.CharField('ville', max_length=30)
    zip_code = models.PositiveSmallIntegerField('code postal', max_length=5)
    country = models.CharField('pays', max_length=2, choices=COUNTRY_CHOICES, default="BE")
    phone_number = PhoneNumberField(blank=True, verbose_name='numéro de téléphone')


    def __unicode__(self):
        return self.first_name

    def communication(self):
        invoice_nbr = 2014101234
        nbr = "{:010d}{:02d}".format(invoice_nbr, invoice_nbr % 97)
        return "+++{}/{}/{}+++".format(nbr[:3], nbr[3:6], nbr[6:])


class Subscription(models.Model):
    """ Describes a cooperation"""
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return self.communication

    def communication(self):
        invoice_nbr = 2014101234
        nbr = "{:010d}{:02d}".format(invoice_nbr, invoice_nbr % 97)
        return "+++{}/{}/{}+++".format(nbr[:3], nbr[3:6], nbr[6:])


class Cooperation(models.Model):
    """ Describes a cooperation"""
    SHARE_CHOICES = (
        (1, u'1 (€ 20)'),
        (2, u'2 (€ 40)'),
        (3, u'3 (€ 60)'),
        (4, u'4 (€ 80)'),
        (5, u'5 (€ 100)'),
        (6, u'6 (€ 120)')
    )

    person = models.ForeignKey(Person)
    share_number = models.PositiveSmallIntegerField('nombre de parts', choices=SHARE_CHOICES, default="1")

    def __unicode__(self):
        return self.first_name

    def communication(self):
        return self.communication
        nbr = "{:010d}{:02d}".format(invoice_nbr, invoice_nbr % 97)
        return "+++{}/{}/{}+++".format(nbr[:3], nbr[3:6], nbr[6:])
