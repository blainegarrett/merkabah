"""
Blobstore interface for Merkabah
"""
from __future__ import absolute_import
from __future__ import with_statement

from google.appengine.api import files
from google.appengine.ext import blobstore
from merkabah.core.files.api import Filesystem

class Blobstore(Filesystem):
    
    def __init__(self):
        pass

    def create_upload_url(self, success_path, upload_path=None):
        """
        Returns the url to upload a file to. This currently uses blobstore to upload the file.
        Currently, there is no way to set the ACL, filename, etc of the file. As such, by default
        we're moving it to /tmp so you can move it where ever later.

        #TODO: Allow async version
        """

        return blobstore.create_upload_url(success_path)

    def read(self, blob_key):
        """
        Read a blob given
        """

        blob_info = blobstore.BlobInfo.get(blob_key)
        if not blob_info:
            raise Exception('Blob Key does not exist: %s' % blob_key)

        blob_file_size = blob_info.size

        blob_concat = ""
        start = 0
        end = blobstore.MAX_BLOB_FETCH_SIZE - 1
        step = blobstore.MAX_BLOB_FETCH_SIZE - 1

        while(start < blob_file_size):
            blob_concat += blobstore.fetch_data(blob_key, start, end)
            temp_end = end
            start = temp_end + 1
            end = temp_end + step
        return blob_concat

    def write(self, filename, content, content_type):
        """
        This needs to be reworked to support larger files
        http://stackoverflow.com/questions/5638894/how-to-write-big-files-into-blobstore-using-experimental-api
        with files.open(file_name, 'a') as f:
            data = uploaded_file.read(65536)
            while data:
              f.write(data)
              data = uploaded_file.read(65536)
        """



        blob_filename = files.blobstore.create(mime_type=content_type)
        with files.open(blob_filename, 'a') as f:
            f.write(content)
        files.finalize(blob_filename)
        blob_key = files.blobstore.get_blob_key(blob_filename)

        return blob_key

    def get_full_url(self, filename, secure=False):
        """
        Given a filename, return a full url for this.
        
        TODO: Allow the domain name to be customized such as bucket.example.com/filename
        """

        return "https://commondatastorage.googleapis.com%s" % filename

