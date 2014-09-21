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

    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'))
    birth_date = models.DateTimeField(_('birth date'))
    title = models.BooleanField(_('title'), default=False, choices=TITLE_CHOICES)

    nationality = models.CharField(_('nationality'), max_length=2, choices=COUNTRY_CHOICES)
    id_number = models.CharField(_('ID number'), max_length=30)

    street = models.CharField(_('street'), max_length=30)
    number = models.CharField(_('number'), max_length=10) # 27 bis
    letterbox = models.PositiveSmallIntegerField(_('letterbox'), max_length=30, null=True, blank=True)
    city = models.CharField(_('city'), max_length=30)
    zip_code = models.PositiveSmallIntegerField(_('zip code'), max_length=5)
    country = models.CharField(_('nationality'), max_length=2, choices=COUNTRY_CHOICES)
    phone_number = PhoneNumberField(blank=True)
    share_number = models.PositiveSmallIntegerField(_('share number'), choices=SHARE_CHOICES)


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
