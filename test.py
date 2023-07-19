# from os.path import exists
# import pandas as pd

# if exists('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-prising-prediction/housing_price.csv'):
#     df = pd.read_csv('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-prising-prediction/housing_price.csv', index_col=0)
#     homes_dict = df.to_dict('list')
#     num_of_exam = df.shape[0]
# else:
#     homes_dict = {}
#     num_of_exam = 0

# print(df.head())
# print(num_of_exam)
# print(list(homes_dict.keys()))
# print(homes_dict['Diện tích sử dụng'])

def longestPalindrome(s):
    """
    :type s: str
    :rtype: str
    """
    cursor = 0
    max_len = 0
    max_start = 0
    max_end = 0

    # if len(s) == 1:
    #     return s
    # if len(s) == 2:
    #     if s[0] != s[1]:
    #         return s[0]
    #     else:
    #         return s
    
    for cursor in range(0, 2*len(s)-1):
        if cursor%2==0: #odd number of element
            start = cursor//2 - 1
            end = cursor//2 + 1
        else: #even number of element
            start = cursor//2
            end = cursor//2 + 1

        while start>=0 and end<=len(s)-1:
            if(s[start]==s[end]):
                length = end - start +1
                if length > max_len:
                    max_len = length
                    max_start = start
                    max_end = end
            else:
                break
            
            start -=1
            end +=1
    return s[max_start:max_end+1]
s = 'abac'
print('longest is: ', longestPalindrome(s))