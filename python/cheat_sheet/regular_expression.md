- Meta-Character
    - *：重复 0 或多次
    - +：至少出现一次
    - ?：重复 0 或 1 次
    - .：表示任意字符
    - {m}：必须出现 m 次
    - {m,n}：出现 m 到 n 次
    - {m,}：至少出现 m 次

- Disable greedy behavior: meta-character 最后添加 `?`

- Character Sets
    - []：方括号中的字符均为候选
    - [^]：加上 `^` 符号，方括号中的为排除项
    - [a-z]：使用 `-` 表示候选字符范围
    - [a-zA-Z]：多个候选字符范围
    - [\u4e00-\u9fa5]：汉字

- Escape Codes
    - \d：表示一个数字
    - \D：表示一个非数字
    - \s：whitespace (tab，space，newline)
    - \S：non-whitespace
    - \w：表示一个字母或数字
    - \W：不是字母或者数字
使用 raw strings，斜杠可以不用转义，提高可读性，如： r'\d+'

- Anchoring：定义模板所要匹配的位置
    - ^：字符串或者行的开始位置
    - $：字符串或者行的末尾
    - \A：字符串的开始位置
    - \Z：字符串的末尾
    - \b：空白字符应该处于字符的起始或末尾处
    - \B：与 \b 相反

## Links:
- https://pymotw.com/3/re/index.html
- http://www.cnblogs.com/zxin/archive/2013/01/26/2877765.html