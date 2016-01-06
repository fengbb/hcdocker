#-*-coding:utf-8-*-
def my_split(string,delimiter,begin_end=" "):
        string = string.strip(begin_end)
        a = string.find(delimiter)
        first_word = string[:a]
        result = []
        result.append(first_word)
        b = a
        while b <= len(string) and b != -1:
                while string[a] == delimiter:
                        a = a + 1
                b = string.find(delimiter,a)
                if b != -1:
                        res = string[a:b]
                else:
                        res = string[a:]
                a = b
                result.append(res)
        return result

s1 = '&adfs    sdfjklsj  dd de&'  #如果仅是拆除空格s1.split()可以搞定
print (my_split(s1," ","&"))
s2 = '  jkj**jkjk*jkkk****d '
print (my_split(s2,"*"))
s3 = ' wang__chuan_____bo  '
print (my_split(s3,'_'))
s4 = '   wang..xiao.....yuan '
print (my_split(s4,'.'))