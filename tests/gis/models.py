from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.backends.signals import connection_created

from tastypie.utils import now

#def setup_spatialite(sender, connection, *args, **kwargs):
#    if 'spatialite' in connection.__class__.__module__:
#        
#        import ipdb
#        ipdb.set_trace()
#        cur.cursor.execute("SELECT InitSpatialMetaData();")
#    

#connection_created.connect(setup_spatialite)

class GeoNote(models.Model):
    user = models.ForeignKey(User, related_name='notes')
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)

    points = models.MultiPointField(null=True, blank=True)
    lines = models.MultiLineStringField(null=True, blank=True)
    polys = models.MultiPolygonField(null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated = now()
        return super(GeoNote, self).save(*args, **kwargs)


class AnnotatedGeoNote(models.Model):
    note = models.OneToOneField(GeoNote, related_name='annotated', null=True)
    annotations = models.TextField()

    def __unicode__(self):
        return u"Annotated %s" % self.note.title
