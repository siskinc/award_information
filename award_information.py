import pymysql
import requests
from bs4 import BeautifulSoup
import db_info
import copy
class lottery_results:

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




award_urls = {}

root_url = 'http://caipiao.163.com'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}


def get_awards_urls(url):
  resp = requests.get(url=url,headers=headers)
  bs = BeautifulSoup(resp.content.decode('utf8'), 'html.parser')
  first_tags = bs.find_all('td', class_='first')
  period_tags = bs.find_all('td', class_='period')
  urls = {}
  for index in range(len(first_tags)):
    name = first_tags[index].find('a')
    award_url = period_tags[index].find('a')
    if name is not None and award_url is not None:
      # 删掉url后面多余的部分
      value = 'http://caipiao.163.com' + award_url['href']
      value = value[:value.rfind('/')]
      urls[name.string] = value
  return urls

def get_awarfs_info(awards_urls):
  lrs = []
  for award_name, award_url in awards_urls.items():
    lr = lottery_results(name=award_name)
    resp = requests.get(url=award_url,headers=headers)
    content = resp.content.decode('utf8')
    bs = BeautifulSoup(content, 'html.parser')
    try:
      infos = bs.find_all('span',class_="iSelectBox")[1].find('div').find_all('a')
    except:
      continue
    for info in infos:
      try:
        lr.bonus = info['bonus']
        lr.matchball = info['matchball']
        lr.pool = info.get('pool','')
        lr.sale = info['sale']
        lr.time = info['time']
        lr.trem = info.string
        lrs.append(copy.copy(lr))
      except:
        print(info)
        continue
  return lrs

def add2db(lrs):
  connect = pymysql.connect(host=db_info.host,\
                  port=3306,\
                  user=db_info.db_user,\
                  password=db_info.db_password,\
                  db=db_info.db_name,\
                  charset='utf8mb4')

  with connect.cursor() as cursor:
    sql = "insert into welfarelottery_welfarelottery (name, trem, time, sale, pool, matchboll, bonus) " \
          "values ('%s','%s','%s','%s','%s','%s','%s')"
    for lr in lrs:
      #先判断数据库是否已经有该条记录
      cursor.execute("select count(*) from welfarelottery_welfarelottery where name = '%s' and trem = '%s'"\
                     % (lr.name, lr.trem))
      result = int(cursor.fetchone()[0])
      if result > 0:
        continue
      data = (lr.name, lr.trem, lr.time, lr.sale, lr.pool if lr.pool is not '' else '0', lr.matchball, lr.bonus)
      cursor.execute(sql % data)
  connect.commit()
  connect.close()

if __name__ == '__main__':
  url = 'http://caipiao.163.com/award/'
  award_urls = get_awards_urls(url)
  lrs = get_awarfs_info(award_urls)
  add2db(lrs)

