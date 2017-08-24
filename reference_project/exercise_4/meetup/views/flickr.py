import json
import xml.etree.ElementTree as ET

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import flickrapi


api_key = '5ac39364a64252aaeb97a467c3795cab'
api_secret = '3bd589618b4a4590'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')
(token, frob) = flickr.get_token_part_one(perms='read')
if not token:
    raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))


def createurl(farm_id, server_id, photo_id, secret):
    url = ("http://farm{farm}.staticflickr.com/{server}/{photo}_{secret}.jpg"
           "".format(farm=farm_id, server=server_id, photo=photo_id,
                     secret=secret))
    return url


def getphotos(tags_to_search):
    photos = flickr.photos_search(text=tags_to_search, per_page=10,
                                  sort='relevance')
    urls = []
    for child in photos:
        for photo in child:
            url = createurl(photo.attrib['farm'], photo.attrib['server'],
                            photo.attrib['id'], photo.attrib['secret'])
            urls.append(url)
    return urls


@login_required
def flickr_get_image_list(request, query):
    links = getphotos(query)
    return HttpResponse(json.dumps(links), content_type="application/json")
