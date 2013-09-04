"""
MERKABAH FILE UTILITIES

This provides a wrapper around the file storage so it is more transparent
"""
import logging
import settings
from django import http
from google.appengine.api import urlfetch

from google.appengine.ext import blobstore
import cloudstorage as gcs

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
            
            logging.warning(field.type_options)

            if isinstance(field, cgi.FieldStorage) and 'blob-key' in field.type_options:
                # TODO: Differentiate between cloudstorage and blogstore 'blob-key': 'encoded_gs_file:....'                

                fileinfo_info = blobstore.parse_file_info(field)
                
                logging.warning(fileinfo_info)

                request.__uploads.setdefault(key, []).append(fileinfo_info)
                if populate_post:
                    request.POST[key] = [str(fileinfo_info.gs_object_name)]
                
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



'''
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
'''

def rescale(img_data, width, height, halign='middle', valign='middle'):
  from google.appengine.api import images
  """Resize then optionally crop a given image.

  Attributes:
    img_data: The image data
    width: The desired width
    height: The desired height
    halign: Acts like photoshop's 'Canvas Size' function, horizontally
            aligning the crop to left, middle or right
    valign: Verticallly aligns the crop to top, middle or bottom

  """

  image = images.Image(img_data)      

  desired_wh_ratio = float(width) / float(height)
  wh_ratio = float(image.width) / float(image.height)

  if desired_wh_ratio > wh_ratio:
    # resize to width, then crop to height
    image.resize(width=width)
    image.execute_transforms()
    trim_y = (float(image.height - height) / 2) / image.height
    if valign == 'top':
      image.crop(0.0, 0.0, 1.0, 1 - (2 * trim_y))
    elif valign == 'bottom':
      image.crop(0.0, (2 * trim_y), 1.0, 1.0)
    else:
      image.crop(0.0, trim_y, 1.0, 1 - trim_y)
  else:
    # resize to height, then crop to width
    image.resize(height=height)
    image.execute_transforms()
    trim_x = (float(image.width - width) / 2) / image.width
    if halign == 'left':
      image.crop(0.0, 0.0, 1 - (2 * trim_x), 1.0)
    elif halign == 'right':
      image.crop((2 * trim_x), 0.0, 1.0, 1.0)
    else:
      image.crop(trim_x, 0.0, 1 - trim_x, 1.0)

  return image.execute_transforms()


def delete_file(filename):
    try:
      gcs.delete(filename)
    except gcs.NotFoundError:
      pass


def read_file(filename):
    blob_concat = ""
    
    gcs_file = gcs.open(filename)
    return gcs_file.read()

def read_blob(blob_key):
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
    

def fetch_file(url):
    """
    Method to import a file and write it to designated file storage
    """


    # Set our api key
    gcs.common.set_access_token(settings.GOOGLE_API_TOKEN)
    
    file_api_class = Cloudstorage

    dest_filename = file_api_class.make_filename(url)

    # Step 1: Fetch the url
    rpc = urlfetch.create_rpc()
    urlfetch.make_fetch_call(rpc, url)
    result = rpc.get_result()
    status = result.status_code

    if not status == 200:
        raise Exception("Attempted to fetch url %s and received status code %s" % (url, status))
    
    # Step 2: Create 
    data = result.content
    content_type = result.headers.get('content-type', None)
    
    dest_filename = Cloudstorage.make_filename(url)

    return file_api_class.write_file(dest_filename, data, content_type)

def make_thumbnail(url):
    """
    Method to import a file and write it to designated file storage
    """
    
    # Set our api key
    gcs.common.set_access_token(settings.GOOGLE_API_TOKEN)
    
    file_api_class = Cloudstorage

    dest_filename = file_api_class.make_filename(url, prefix='thumbs/')

    # Step 1: Fetch the url
    rpc = urlfetch.create_rpc()
    urlfetch.make_fetch_call(rpc, url)
    result = rpc.get_result()
    status = result.status_code

    if not status == 200:
        raise Exception("Attempted to fetch url %s and received status code %s" % (url, status))
    
    # Step 2: Create 
    data = result.content
    
    data = rescale(data, 300, 500)

    content_type = result.headers.get('content-type', None)

    return file_api_class.write_file(dest_filename, data, content_type)    


class Cloudstorage(object):

    @staticmethod
    def make_filename(source_filename, prefix=None):
        """
        
        """

        filename = source_filename.split('/')[-1]
        filename = filename.lower()
        filename = filename.replace(' ', '_')

        bucket = '/dim-media'
        
        if prefix:
            filename = "%s%s" % (prefix, filename)

        filename = bucket + '/sdk/%s' % filename

        return filename        
    
    @staticmethod
    def write_file(filename, data, content_type):
        """
        """
        gcs.common.set_access_token(settings.GOOGLE_API_TOKEN)

        logging.error(filename)
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename,
                            'w',
                            content_type=content_type,
                            options={'x-goog-acl': 'public-read',
                                     'x-goog-meta-writer': 'merkabah'},
                            retry_params=write_retry_params)

        gcs_file.write(data)
        gcs_file.close()
        return filename




'''
def fetch_file(url):
    """
    Method to import and item from a remote source and put it into blobstore
    """
    from google.appengine.ext import blobstore
    from django import http
    from google.appengine.api import files, urlfetch
    from django.core import urlresolvers

    rpc = urlfetch.create_rpc()
    urlfetch.make_fetch_call(rpc, url)

    result = rpc.get_result()
    if result.status_code == 200:
        file_data = result.content
        content_type = result.headers.get('content-type', None)

        # Create the file
        file_name = files.blobstore.create(mime_type=content_type)        


        with files.open(file_name, 'a') as f:
            f.write(file_data)

        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)

        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(file_name)

        return blob_key

'''

'''
def send_blob(request, blob_key_or_info, content_type=None, save_as=None):
    """Send a blob-response based on a blob_key.

    Sets the correct response header for serving a blob.  If BlobInfo
    is provided and no content_type specified, will set request content type
    to BlobInfo's content type.

    Args:
      blob_key_or_info: BlobKey or BlobInfo record to serve.
      content_type: Content-type to override when known.
      save_as: If True, and BlobInfo record is provided, use BlobInfos
        filename to save-as.  If string is provided, use string as filename.
        If None or False, do not send as attachment.

      Raises:
        ValueError on invalid save_as parameter.
    """

    CONTENT_DISPOSITION_FORMAT = 'attachment; filename="%s"'
    if isinstance(blob_key_or_info, blobstore.BlobInfo):
      blob_key = blob_key_or_info.key()
      blob_info = blob_key_or_info
    else:
      blob_key = blob_key_or_info
      blob_info = None

    #logging.debug(blob_info)
    response = HttpResponse()
    response[blobstore.BLOB_KEY_HEADER] = str(blob_key)

    if content_type:
      if isinstance(content_type, unicode):
        content_type = content_type.encode('utf-8')
      response['Content-Type'] = content_type
    else:
      del response['Content-Type']

    def send_attachment(filename):
      if isinstance(filename, unicode):
        filename = filename.encode('utf-8')
      response['Content-Disposition'] = (CONTENT_DISPOSITION_FORMAT % filename)

    if save_as:
      if isinstance(save_as, basestring):
        send_attachment(save_as)
      elif blob_info and save_as is True:
        send_attachment(blob_info.filename)
      else:
        if not blob_info:
          raise ValueError('Expected BlobInfo value for blob_key_or_info.')
        else:
          raise ValueError('Unexpected value for save_as')

    return response
'''
