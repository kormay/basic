import time

'''判断是否是一个有效的日期字符串'''
def is_valid_date(str):
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False
