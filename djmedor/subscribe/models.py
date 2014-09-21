# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Cooperator(models.Model):
    """ Describes a cooperator """
    COUNTRY_CHOICES = (
        ('be', _(u'Belgique')),
        ('fr', _(u'France')),
        ('lu', _(u'Luxembourg'))
    )

    TITLE_CHOICES = (
        (0, _(u'Madam')),
        (1, _(u'Sir'))
    )

    SHARE_CHOICES = (
        (1, u'1 (20)'),
        (2, u'2 (40)'),
        (3, u'3 (60)'),
        (4, u'4 (80)'),
        (5, u'5 (100)'),
        (6, u'6 (120)')
    )

    first_name = models.CharField('prénom', max_length=30)
    last_name = models.CharField('nom de famille', max_length=30)
    email = models.EmailField('courriel')
    birth_date = models.DateTimeField('date de naissance')
    title = models.BooleanField('civilité', default=False, choices=TITLE_CHOICES)

    nationality = models.CharField('nationalité', max_length=2, choices=COUNTRY_CHOICES)
    id_number = models.CharField("N° d'identité nationale", max_length=30)

    street = models.CharField('rue', max_length=30)
    number = models.CharField('numéro', max_length=10) # 27 bis
    letterbox = models.PositiveSmallIntegerField('boîte postale', max_length=30, null=True, blank=True)
    city = models.CharField('ville', max_length=30)
    zip_code = models.PositiveSmallIntegerField('code postal', max_length=5)
    country = models.CharField('pays', max_length=2, choices=COUNTRY_CHOICES)
    phone_number = PhoneNumberField(blank=True, verbose_name='téléphone')
    share_number = models.PositiveSmallIntegerField('nombre de parts', choices=SHARE_CHOICES)


    class Meta:
        pass

    def __unicode__(self):
        pass

    def communication(self):
        invoice_nbr = 2014101234
        nbr = "{:010d}{:02d}".format(invoice_nbr, invoice_nbr % 97)
        return "+++{}/{}/{}+++".format(nbr[:3], nbr[3:6], nbr[6:])



    @models.permalink
    def get_absolute_url(self):
        pass
        #return ('view_or_url_name' )
