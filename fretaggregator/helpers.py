from .database import session

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
    
  