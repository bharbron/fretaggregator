from .database import session
import urlparse

def get_or_add(model, **kwargs):
  """
  Given a db model and keyword arguments for that model,
  either fetch the object from the database if it exists,
  or add it to the database if it doesn't
  """
  item = session.query(model).filter_by(**kwargs).first()
  if item:
    return item
  else:
    item = model(**kwargs)
    session.add(item)
    return item
    
def parse_url(url):
  """
  Parses the url being submitted by a user,
  validates that it is a valid youtube link,
  and returns only the relevant part of the
  url that we need to save
  """
  pass


#borrowed from stackoverflow
def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None