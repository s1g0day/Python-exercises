import random
import string

# 生成随机的字符串（大小写英文字母、数字组成）
random_str1 = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
print(random_str1)

生成随机的无重复字符的字符串
random_str2 = ''.join(random.sample(string.ascii_letters + string.digits, 20))
print(random_str2)
