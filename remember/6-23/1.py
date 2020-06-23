#replace函数
#返回字符串中的 old（旧字符串） 替换成 new(新字符串)后生成的新字符串，如果指定第三个参数max，则替换不超过 max 次。
#str.replace(old, new[, max])
#str = "this is string example....wow!!! this is really string";
#print str.replace("is", "was");
#print str.replace("is", "was", 3);
#结果
#thwas was string example....wow!!! thwas was really string
#thwas was string example....wow!!! thwas is really string

#split函数 
#通过指定分隔符对字符串进行切片，如果参数 num 有指定值，则分隔 num+1 个子字符串
#str.split(str="", num=string.count(str))
#str = "Line1-abcdef \nLine2-abc \nLine4-abcd";
#print str.split( );       # 以空格为分隔符，包含 \n
#print str.split(' ', 1 ); # 以空格为分隔符，分隔成两个
#结果
#['Line1-abcdef', 'Line2-abc', 'Line4-abcd']
#['Line1-abcdef', '\nLine2-abc \nLine4-abcd']


#join函数
#str = "-";
#seq = ("a", "b", "c"); # 字符串序列
#print str.join( seq );
#结果
#a-b-c