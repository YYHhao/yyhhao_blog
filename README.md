# yyhhao_blog
myblog

## Markdown 兼容与本地预览

本站通过 Zensical 构建，并在博客端启用 `blog_markdown` 兼容扩展，所有文章自动生效，无需逐篇改写或让 AI 审核格式。

* 段落后可以直接写 `*`、`-`、`+` 列表，或从 `1.` 开始的有序列表，不强制空行。
* 句子中可以使用 `$$...$$`，按展示公式渲染，不再残留美元符号；`$...$` 仍用于行内公式。
* 独立的 `$$` 公式块、代码围栏、行内代码和缩进代码保持原有规则，代码内容不会被自动改写。
* 这些是针对常见写法的兼容，不表示支持所有编辑器插件的私有语法。

在仓库根目录安装依赖、预览：

```bash
python -m pip install -r requirements.txt
python -m zensical serve
```

本地和 GitHub Actions 使用同一份依赖版本及扩展。每次发布前自动执行 `python -m unittest discover -s tests`，检查列表、公式及代码块是否正确解析。

以下写法仍推荐用于提高跨平台兼容性，但不再需要手动给每个列表补空行：

* 嵌套列表每层缩进四个空格；标题与正文之间也留空行。
* 句子中的公式使用 `$...$`；独立公式使用 `$$...$$`，整个公式块前后留空行，公式内部不要留空行。
* 使用代码围栏展示代码，并注明语言；不要在代码块内部为排版添加空行或改变缩进。

正确示例：

````markdown
### 解法思路

假设执行 k 次操作，相当于：

* 所有服务器降低 $kB$。
* 中心服务器额外降低 $A-B$。

至少需要 $\lceil (h-kB)/(A-B) \rceil$ 次。

独立公式写成：

$$
\left\lceil \frac{h-kB}{A-B} \right\rceil
$$

1. 第一步。
2. 第二步。

    - 子步骤一。
    - 子步骤二。
````

数学公式由 `pymdownx.arithmatex` 和本仓库兼容扩展预处理，再由 KaTeX 渲染。标准块公式写法见 [Arithmatex 官方文档](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/#input-format)。

同步源码后，需要等 GitHub Actions 的 `Documentation` 工作流构建、部署成功，线上页面才会更新。该工作流只监听 `main` 和 `master` 分支；发布内容是构建生成的 `site` 目录，修改时应编辑 `docs` 中的源文件。若部署成功后仍显示旧页面，再尝试强制刷新浏览器。
