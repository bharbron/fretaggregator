from sqlalchemy.orm.exc import NoResultFound
from urlparse import urlparse, parse_qs

def get_one_or_create(session, model, **kwargs):
  try:
    return session.query(model).filter_by(**kwargs).one()
  except NoResultFound:
    return model(**kwargs)
    
def get_video_id(url):
  """
  Parses the url being submitted by a user,
  validates that it is a valid youtube link,
  and returns the video_id portion of the url
  Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
  """
  query = urlparse(url)
  if query.hostname == 'youtu.be':
    return query.path[1:]
  if query.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
    if query.path == '/watch':
      p = parse_qs(query.query)
      return p['v'][0]
    if query.path[:7] == '/embed/':
      return query.path.split('/')[2]
    if query.path[:3] == '/v/':
      return query.path.split('/')[2]
  # fail?
  return None