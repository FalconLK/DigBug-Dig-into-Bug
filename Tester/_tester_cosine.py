# from similarity.jarowinkler import JaroWinkler
# jarowinkler = JaroWinkler()
# print(jarowinkler.similarity('My string', 'My tsring'))
# print(jarowinkler.similarity('My string', 'My ntrisg'))
#
#
# from similarity.longest_common_subsequence import LongestCommonSubsequence
# lcs = LongestCommonSubsequence()
# # Will produce 4.0
# print(lcs.distance('AGCAT', 'GAC'))
# # Will produce 1.0
# print(lcs.distance('AGCAT', 'AGCT'))
#


# s0 = 'My first string'
# s1 = 'My fiher string...'

from similarity.cosine import Cosine
import os
from utils import read_file
result_dict = dict()
cosine = Cosine(2)
base_path = os.path.dirname(os.path.abspath(__file__))
for result in read_file(base_path + '/MATH-727.txt').splitlines():
    str_1 = 'code:step code:embed code:rung code:kutta code:integr code:dormand code:princ code:adapt code:size code:comput code:type code:check code:rang code:extrem code:evalu code:function code:afterward code:fail code:gragg code:bulirsch code:stoer code:truncat'
    print (result)
    str_2 = result
    p0 = cosine.get_profile(str_1)
    p1 = cosine.get_profile(str_2)
    result_dict[result] = cosine.similarity_profiles(p0, p1)
    print(cosine.similarity_profiles(p0, p1))

sorted_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
print (sorted_dict)

print (sorted_dict[0][0])


