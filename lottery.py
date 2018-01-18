import abc

class lottery(object):

  def save(self, connect, cursor):
    """save to db"""
    # 先判断数据库是否已经有该条记录
    return