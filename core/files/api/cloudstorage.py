"""
Google Cloud Storage interface for Merkabah

# TODO: Create upload_url async
# 
"""
from __future__ import absolute_import
from merkabah.core.files.api import Filesystem
from merkabah.lib import cloudstorage as gcs
from google.appengine.ext import blobstore


my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)

class Cloudstorage(Filesystem):
    """
    
    Note: We conceptually treat the GCS bucket like a drive. As such, you instanciate the class with the drive and all files are relative to that.
    """
    
    def __init__(self, bucket):
        self.DEFAULT_UPLOAD_FOLDER = '/tmp'
        self.bucket = bucket
    
    def create_upload_url(self, success_path, upload_path=None):
        """
        Returns the url to upload a file to. This currently uses blobstore to upload the file.
        Currently, there is no way to set the ACL, filename, etc of the file. As such, by default
        we're moving it to /tmp so you can move it where ever later.

        #TODO: Allow async version
        #TODO: if trailing slash is required by framework (Django, etc) ensure that it is present
            on upload_path
        """

        upload_path = '%s%s' % (self.bucket, self.DEFAULT_UPLOAD_FOLDER)

        url = blobstore.create_upload_url(success_path, gs_bucket_name=upload_path)
        
        # Append trailing slash so django won't blow up?
        return "%s" % url
    
    '''
    def get_uploads(self, ):
        """
        Helper 
        # You don't need this if your views are webapps(2), you can use self.get_uploads.
        
        """
    '''

    def read(self, filename):
        """
        """
        gcs_file = gcs.open(filename)

        return gcs_file.read()

    def write(self, filename, content, content_type):
        """
        TODO: Check if filename has leading slash.
        """
        
        # Prep the filename
        filename = "/%s/%s" % (self.bucket, filename)

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)

        gcs_file = gcs.open(filename,
                            'w',
                            content_type=content_type,
                            options={'x-goog-acl': 'public-read',
                                     'x-goog-meta-bar': 'bar'},
                            retry_params=write_retry_params)
        gcs_file.write(content)
        gcs_file.close()

        return filename


    def get_full_url(self, filename, secure=False):
        """
        Given a filename, return a full url for this.
        
        TODO: Allow the domain name to be customized such as bucket.example.com/filename
        """

        return "https://commondatastorage.googleapis.com%s" % filename
    
    def get_files(self):
        page_size = 10
        stats = gcs.listbucket('/%s' % self.bucket, max_keys=page_size)
        return stats