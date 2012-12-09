'''
MERKABAH FILE UTILITIES
'''
from google.appengine.ext import blobstore

def create_upload_url(url):
    return blobstore.create_upload_url(url)

def get_uploads(request, field_name=None, populate_post=False):
    import logging
    from google.appengine.ext import blobstore            
    import cgi
    """Get uploads sent to this handler.
    Args:
      field_name: Only select uploads that were sent as a specific field.
      populate_post: Add the non blob fields to request.POST
    Returns:
      A list of BlobInfo records corresponding to each upload.
      Empty list if there are no blob-info records for field_name.
      http://pastebin.com/9haziPhd
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
                blob_info = blobstore.parse_blob_info(field)
                
                request.__uploads.setdefault(key, []).append(blob_info)
                if populate_post:
                    request.POST[key] = [str(blob_info.key())]
                
            elif populate_post:
                request.POST[key] = []
                if isinstance(field, list):                
                    for item in field:
                        request.POST[key].append(item.value)
                else:
                    request.POST[key] = [field.value]
    
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
    