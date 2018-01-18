import lottery
from logger import logger
import lottery_op_sqls
class meta_high_frequency_lottery:

  def __init__(self, trem, data_award, value3, value4, value5 = None):
    self.__trem = trem
    self.__data_award = data_award
    self.__value3 = value3
    self.__value4 = value4
    self.__value5 = value5

  def __str__(self):
    return '期：%s 开奖号码: %s value3: %s value4: %s' % (self.__trem, self.__data_award, \
                                            self.__value3, self.__value4) \
      +((' value5: %s' % self.__value5) if self.__value5 != None else '')

  def save(self, cursor, type_trem_id):
    cursor.execute(lottery_op_sqls.meta_high_frequency_lottery_select_exit % (self.__trem, type_trem_id))
    result = int(cursor.fetchone()[0])
    if result > 0:
      return True
    if self.__value5 == None:
      data = (self.__trem, self.__data_award, self.__value3, self.__value4, type_trem_id)
      cursor.execute(lottery_op_sqls.meta_high_frequency_lottery_insert % data)
    else:
      data = (self.__trem, self.__data_award, self.__value3, self.__value4, self.__value5, type_trem_id)
      cursor.execute(lottery_op_sqls.meta_high_frequency_lottery_insert_value5 % data)


  def __repr__(self):
    return self.__str__()

  @property
  def trem(self):
    return self.__trem

  @trem.setter
  def trem(self, trem):
    self.__trem = trem

  @property
  def data_award(self):
    return self.__data_award

  @data_award.setter
  def data_award(self, data_award):
    self.__data_award = data_award

  @property
  def value3(self):
    return self.__value3

  @value3.setter
  def value3(self, value3):
    self.__value3 = value3

  @property
  def value4(self):
    return self.__value4

  @value4.setter
  def value4(self, value4):
    self.__value4 = value4

  @property
  def value5(self):
    return self.__value5

  @value4.setter
  def value5(self, value5):
    self.__value5 = value5


class high_frequency_lottery(lottery.lottery):

  def __init__(self,name, trem = '', meta_high_frequency_lotterys = None):
    self.__meta_high_frequency_lotterys = meta_high_frequency_lotterys
    self.__name = name
    self.__trem = trem

  def __str__(self):
    return '彩票种类: %s \n\r 期数: %s\n\r 内容:%s\n\r' % (self.__name, self.__trem, self.__meta_high_frequency_lotterys)

  def __repr__(self):
    return self.__str__()

  def save(self, connect, cursor):
    cursor.execute(lottery_op_sqls.high_frequency_lottery_select_exit % (self.__name, self.__trem))
    result = int(cursor.fetchone()[0])
    if result <= 0:
      data = (self.__name, self.__trem)
      cursor.execute(lottery_op_sqls.high_frequency_lottery_insert % data)
      cursor.execute(lottery_op_sqls.high_frequency_lottery_select_exit % (self.__name, self.__trem))

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, name):
    self.__name = name

  @property
  def mhfls(self):
    return self.__meta_high_frequency_lotterys;

  @mhfls.setter
  def mhfls(self, mhfls):
    self.__meta_high_frequency_lotterys = mhfls

  @property
  def trem(self):
    return self.__trem

  @trem.setter
  def trem(self, trem):
    self.__trem = trem