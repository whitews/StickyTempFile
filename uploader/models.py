import os
import hashlib
from string import join

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save

from StickyTempFile.settings import MEDIA_ROOT, CRAZY_HACK


def upload_file_path(instance, filename):
    upload_dir = join([MEDIA_ROOT, str(filename)], '')

    return upload_dir


class UploadedFile(models.Model):
    uploaded_file = models.FileField(upload_to=upload_file_path)
    original_filename = models.CharField(unique=False, null=False, blank=False, max_length=256)
    sha1 = models.CharField(unique=True, null=False, blank=False, max_length=40)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Save the original file name, since it may already exist on our side.
        Save the SHA-1 hash here as well.
        """

        self.original_filename = self.uploaded_file.name.split('/')[-1]

        # get the hash, and leave the file open/closed status the same as it came in
        if self.uploaded_file.closed:
            self.uploaded_file.open()
            file_hash = hashlib.sha1(self.uploaded_file.read())
            self.uploaded_file.close()
        else:
            file_hash = hashlib.sha1(self.uploaded_file.read())

        self.sha1 = file_hash.hexdigest()
        if self.sha1 in UploadedFile.objects.exclude(id=self.id).values_list('sha1', flat=True):
            if CRAZY_HACK:
                if hasattr(self.sample_file.file, 'temporary_file_path'):
                    temp_file_path = self.sample_file.file.temporary_file_path()
                    os.unlink(temp_file_path)

            raise ValidationError("An uploaded file with this SHA-1 hash already exists.")

    def save(self, *args, **kwargs):
        if hasattr(self.uploaded_file.file, 'temporary_file_path'):
            # part of the crazy hack to avoid accumulating temp files in /tmp
            # must be done before parent save() or else the FileField file is no longer a TemporaryUploadFile
            self.temp_file_path = self.uploaded_file.file.temporary_file_path()
        super(UploadedFile, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % (self.original_filename,)


# Crazy hack ahead...needed for some weird bug where temp upload files are getting stuck in /tmp
def remove_temp_file(sender, **kwargs):
    obj = kwargs['instance']
    if hasattr(obj, 'temp_file_path'):
        os.unlink(obj.temp_file_path)

if CRAZY_HACK:
    # connect crazy hack to post_save
    post_save.connect(remove_temp_file, sender=UploadedFile)
