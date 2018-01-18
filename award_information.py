import pymysql
import requests
from bs4 import BeautifulSoup
import db_info
import copy
from lxml import etree
from logger import logger
from welfare_lottery_results import welfare_lottery_results
from high_frequency_lottery import high_frequency_lottery, meta_high_frequency_lottery
from datetime import datetime,timedelta
from lottery_op_sqls import high_frequency_lottery_select_id


welfare_lotterys = ('双色球', '大乐透', '3D', '排列3', '排列5', '七星彩', '七乐彩')

high_frequency_lotterys = ('11选5', '老11选5', '粤11选5', '好运11选5', '易乐11选5', \
                           '快3', '江苏快3', '新快3', '湖北快3', '易快3', '重庆时时彩')
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
      urls[name.string] = value
  return urls

# 获取BeautifulSoup对象
def get_bs(url):
  print('[' + str(datetime.now()) + ']' + '请求url:' + url)
  resp = requests.get(url=url, headers=headers)
  content = resp.content.decode('utf8')
  bs = BeautifulSoup(content, 'html.parser')
  return bs


#判断当前td是否为可爬取对象
def right_td(td):
  return not(td == None or td.strip() in ('', r'\xa0', '--', None))


def get_high_frequency_lotterys_info(awards_urls):
  hfls = []
  for award_name, award_url in awards_urls.items():
    # 判断是否在爬取范围内
    if award_name not in high_frequency_lotterys:
      continue
    hfl = high_frequency_lottery(name=award_name, trem=datetime.now().strftime('%Y%m%d'), meta_high_frequency_lotterys={})
    bs = get_bs(award_url)
    trs = bs.find_all('tr')
    value3 = trs[0].find_all('th')[2].string
    # print(value3)
    if value3 == '奇偶':
      # 遍历每一列
      for tr in trs[1:]:
        # 得到每一列中所有的td标签
        tds = tr.find_all('td')
        # 每四个td标签为一组数据，每个tr有四组
        for i in range(4):
          # print(tds[i*4].string, tds[i*4].get('data-award'), tds[i*4 + 2].string, tds[i*4 + 3].string)
          mhfl = meta_high_frequency_lottery(trem=tds[i*4].string,\
                                             data_award=tds[i*4].get('data-award'),\
                                             value3=tds[i*4 + 2].string,\
                                             value4=tds[i*4 + 3].string)
          if right_td(tds[i * 4].get('data-award','')):
            hfl.mhfls[tds[i*4].string] = mhfl

      hfls.append(hfl)
    elif value3 == '和值':
      # 遍历每一列
      for tr in trs[1:]:
        # 得到每一列中所有的td标签
        tds = tr.find_all('td')
        # 每四个td标签为一组数据，每个tr有四组
        for i in range(3):
          # print(tds[i*4].string, tds[i*4].get('data-award'), tds[i*4 + 2].string, tds[i*4 + 3].string)
          mhfl = meta_high_frequency_lottery(trem=tds[i * 4].string, \
                                             data_award=tds[i * 4].get('data-win-number'), \
                                             value3=tds[i * 4 + 2].string, \
                                             value4=tds[i * 4 + 3].string)
          if  right_td(tds[i * 4].get('data-win-number','')):
            hfl.mhfls[tds[i * 4].string] = mhfl
      hfls.append(hfl)
    elif value3 == '十位':
      # 遍历每一列
      for tr in trs[1:]:
        # 得到每一列中所有的td标签
        tds = tr.find_all('td')
        # 每四个td标签为一组数据，每个tr有四组
        for i in range(3):
          # print(tds[i*4].string, tds[i*4].get('data-award'), tds[i*4 + 2].string, tds[i*4 + 3].string)
          mhfl = meta_high_frequency_lottery(trem=tds[i * 5].string, \
                                             data_award=tds[i * 5].get('data-win-number'), \
                                             value3=tds[i * 5 + 2].string, \
                                             value4=tds[i * 5 + 3].string,
                                             value5=tds[i * 5 + 4].string)
          if right_td(tds[i * 5].get('data-win-number','')):
            hfl.mhfls[tds[i * 5].string] = mhfl
      hfls.append(hfl)
  print(hfls)
  return hfls



def get_welfare_awarfs_info(awards_urls):
  wlrs = []
  for award_name, award_url in awards_urls.items():
    # 判断是否在爬取范围内
    if award_name not in welfare_lotterys:
      continue
    lr = welfare_lottery_results(name=award_name)
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
        wlrs.append(copy.copy(lr))
      except:
        logger.error(info)
        continue
  return wlrs

def add2db(infos):
  connect = pymysql.connect(host=db_info.host,\
                  port=3306,\
                  user=db_info.db_user,\
                  password=db_info.db_password,\
                  db=db_info.db_name,\
                  charset='utf8mb4')
  with connect.cursor() as cursor:
    for info in infos:
      info.save(connect, cursor)
  connect.commit()
  connect.close()

def addmhlfs2db(infos):
  connect = pymysql.connect(host=db_info.host, \
                            port=3306, \
                            user=db_info.db_user, \
                            password=db_info.db_password, \
                            db=db_info.db_name, \
                            charset='utf8mb4')
  with connect.cursor() as cursor:
    for info in infos:
      count = cursor.execute(high_frequency_lottery_select_id % (info.name, info.trem))
      id = cursor.fetchone()[0]
      for mhfl in info.mhfls.values():
        mhfl.save(cursor, id)
  connect.commit()
  connect.close()

if __name__ == '__main__':
  begin = datetime.now()
  logger.info('launch')
  url = 'http://caipiao.163.com/award/'
  award_urls = get_awards_urls(url)
  wlrs = get_welfare_awarfs_info(award_urls)
  hfls = get_high_frequency_lotterys_info(award_urls)
  add2db(wlrs)
  add2db(hfls)
  addmhlfs2db(hfls)
  logger.info('leave')
  end = datetime.now()
  print(end-begin)
