"""
Filestystem Interfaces for Merkabah

"""
from __future__ import absolute_import
import logging
from google.appengine.ext.blobstore import parse_file_info, parse_blob_info
import cgi

class Filesystem(object):
    """
    Base Filesystem Class. To add a Filesystem, extend this class and implement its methods
    """
    
    def get_uploads(self, request, field_name=None, populate_post=False):
        """Get uploads sent to this handler.
        Modified to support GCS from: https://gist.github.com/harperreed/305322

        Args:
          field_name: Only select uploads that were sent as a specific field.
          populate_post: Add the non blob fields to request.POST

        Returns:
          A list of BlobInfo or FileInfo records corresponding to each upload.
          Empty list if there are no blob-info records for field_name.
        """

        if hasattr(request,'__uploads') == False:
            request.META['wsgi.input'].seek(0) 
            fields = cgi.FieldStorage(request.META['wsgi.input'], environ=request.META)

            request.__uploads = {}
            if populate_post:
                request.POST = {}

            for key in fields.keys():
                field = fields[key]
                if isinstance(field, cgi.FieldStorage) and 'blob-key' in field.type_options:
                    logging.warning(field.type_options)

                    if field.type_options['blob-key'].find('encoded_gs_file:') == 0:
                        # This is a Cloud Store Upload
                        file_info = parse_file_info(field)
                        logging.warning(file_info)
                        request.__uploads.setdefault(key, []).append(file_info)
                    else:
                        # This is the normal blobstore upload
                        blob_info = parse_blob_info(field)
                        request.__uploads.setdefault(key, []).append(blob_info)

                if populate_post:
                    request.POST[key] = field.value

        if field_name:
            try:
                return list(request.__uploads[field_name])
            except KeyError:
                return []
        else:
            results = []
            for uploads in request.__uploads.itervalues():
                results += uploads
            return results
        