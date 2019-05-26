import time
t = time.time()  # 时间戳
t = time.localtime(t)  # 通过time.localtime将时间戳转换成时间组
t = time.strftime("%Y-%m-%d", t)  # 再将时间组转换成指定格式

a = '2019-01-01'
print(a.split('-'))