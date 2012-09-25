import logging
import os
from tempfile import NamedTemporaryFile

from django.core.files import File
from celery.task import task

from localshop.apps.packages import models
import urllib2


@task
def download_file(pk):
    release_file = models.ReleaseFile.objects.get(pk=pk)
    logging.info("Downloading %s", release_file.url)
    remotefile = urllib2.urlopen(release_file.url)
    # Store the content in a temporary file
    tmp_file = NamedTemporaryFile()
    tmp_file.write(remotefile.read())

    logging.info("Wrote response to tmp_file:%s", tmp_file.name)
    # Write the file to the django file field
    filename = os.path.basename(release_file.url)
    logging.info("Saving to file:%s", filename)
    release_file.distribution.save(filename, File(tmp_file))
    release_file.save()
    logging.info("Complete")
