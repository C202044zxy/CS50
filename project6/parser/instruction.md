

本次 `project` 的目的是用 `nltk` 去 `phrase` 一句 `context-free` 的自然语言，下面将按照代码顺序介绍 `nltk` 的使用方法，其中 `phrase` 的意思是用树形结构来讲语法结构可视化。

## 构建解释器

```python
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
```

上面是构建 `context-free grammar` 的解释器，其中 `Nonterminals` 代表非终端（表示语法的抽象符号），`Terminal` 代表终端（表示自然语言中的单词）

```python
NONTERMINALS = """
S -> NP VP
NP -> N | Det NP
VP -> V | V NP
"""
```

上面表示了解释器所应用的非终端解释规则，每个规则用行分隔。第一行表示 `Sentence` 可以被解释为 `noun phrase` 和 `verb phrase`，第二行表示 `noun phrase` 可以被 `noun` 或者 `determiner noun` 解释（用符号 `|` 分隔），第三行表示 `verb phrase` 可以被 `verb` 或者 `verb noun phrase` 解释。

```python
TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
"""
```

上面表示了终端的解释规则，也就是把一些非终端符号给映射到一些具体的单词上面。

把两个规则合并起来（字符串的合并），然后就可以构建解释器了。

你可以随意的改写规则或者符号名称，但是要注意避免 `over-generating`（即解释出来的结果有很多种）

## 解释语句

```python
try:
	trees = list(parser.parse(s))
except ValueError as e:
	print(e)
    return
```

因为解释不一定成功，所以用 `try-except` 语句。注意解释的结果可能有多种，需要用 `list` 存下来。

```python
tree.subtrees() # 可以用来取出所有子树
tree.flatten() # 将子树扁平化，即把树形结构转化为自然语言的语句
```

然后就没啥需要注意的了，完结撒花。

