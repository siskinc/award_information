from logger import logger
import lottery
from lottery_op_sqls import welfare_lottery_insert,welfare_lottery_select_exit

class welfare_lottery_results(lottery.lottery):
  def __init__(self, name = '',trem = '', time = '', \
               sale = '', pool = '',\
               matchball = '', bonus = ''):
    """
    :param name
    :param trem: 期
    :param time: 开奖时间
    :param sale: 全国销量
    :param pool: 奖池奖金
    :param matchball: 开奖号码
    :param bonus: 开奖信息
    """
    self.__name = name
    self.__trem = trem
    self.__time = time
    self.__sale = sale
    self.__pool = pool
    self.__matchball = matchball
    self.__bonus = bonus

  def __str__(self):
    info = ' 类型: %s \n 期: %s \n 开奖时间: %s \n 全国销量: %s \n 奖池奖金: %s \n 开奖号码: %s \n 开奖信息: %s' \
      % (self.__name, self.__trem, self.__time, self.__sale, self.__pool, self.__matchball, self.__bonus)
    return info

  def __repr__(self):
    return self.__str__()

  def save(self, connect, cursor):
    cursor.execute(welfare_lottery_select_exit % (self.__name, self.__trem))
    result = int(cursor.fetchone()[0])
    if result > 0:
      return True
    data = (self.__name, self.__trem, self.__time, \
            self.__sale, self.__pool if self.__pool is not '' else '0', \
            self.__matchball, self.__bonus)
    logger.info('添加数据：\n\t 彩票类型: %s \t 期数：%s' % (self.__name, self.__trem))
    cursor.execute(welfare_lottery_insert % data)

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, name):
    self.__name = name

  # 期
  @property
  def trem(self):
    return self.__trem

  @trem.setter
  def trem(self, trem):
    self.__trem = trem

  # 开奖时间
  @property
  def time(self):
    return self.__time

  @time.setter
  def time(self, time):
    self.__time = time

  # 全国销量
  @property
  def sale(self):
    return self.__sale

  @sale.setter
  def sale(self, sale):
    self.__sale = sale

  # 奖池奖金
  @property
  def pool(self):
    return self.__pool

  @pool.setter
  def pool(self, pool):
    self.__pool = pool

  # 开奖号码
  @property
  def matchball(self):
    return self.__matchball

  @matchball.setter
  def matchball(self, matchball):
    self.__matchball = matchball

  #中奖信息
  @property
  def bonus(self):
    return self.__bonus
  @bonus.setter
  def bonus(self, bonus):
    self.__bonus = bonus
