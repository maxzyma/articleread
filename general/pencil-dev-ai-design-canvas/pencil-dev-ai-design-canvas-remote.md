# 最近火了一个产品：Pencil.dev

> 来源：微信公众号 InkFlow惜阅，2026-01-23
> 原文链接：https://mp.weixin.qq.com/s/_3qhUfNJX_o4TVUvsJrhJQ

这两周，一个叫 Pencil.dev 的产品突然在开发者和设计圈同时刷屏。有着近20年的产品设计背景，现在以一个独立开发者的视角一起与大家来聊聊这个产品。

![文章配图](https://mmbiz.qpic.cn/mmbiz_jpg/De5rakickIy8jkLlmzyQ9FcK7rDciadKaxLVNuL2xwkwfFh9GiaxicRl8ibV8gZWQfNQekfw9eN4aExSMysTbGpjKSA/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=0)

它不是一个普通的 AI 设计工具，也不是 Cursor 的一个小插件。

> AI 时代，设计与开发第一次真正走进同一个工作空间。
>
> 我第一次觉得，AI 不只是帮我写代码，而是真的在一起做东西。

很多人第一次看到 Pencil 的反应是好奇，第二次是怀疑，真正用过之后，反应往往变成："这东西不太像升级，而像换了一种工作方式。"

如果你最近刷 X、YouTube，或者在 Cursor / Claude / Codex 相关社区里混过，大概率已经看到过 Pencil 的官方演示视频：

> 📹 [观看官方演示视频（时长 01:19）](https://mpvideo.qpic.cn/0b2ewqa3maabr4ak653s5fuvdngdw22adnqa.f10002.mp4?dis_k=6edcf7e2b00cbf46ba64e98d9d347953&dis_t=1769427452&play_scene=10120&auth_info=B4DN+ZVQPgQYmu+hwXBzPw4uahdUQntxYFIiHUg8RX88fExML1xja3poRTc3U2QFBA==&auth_key=cf6fb46c27dc2aae121281355a7115b9&vid=wxv_4354669162816815106&format_id=10002&support_redirect=0&mmversion=false)

在代码编辑器里直接出现一个设计画布
通过自然语言修改界面结构
设计在变，代码也在同步变

第一次看到时，很多人的反应是：

> "这看起来有点像 Figma，但又明显不一样。"

![Figma 界面](https://mmbiz.qpic.cn/mmbiz_png/De5rakickIy8jkLlmzyQ9FcK7rDciadKaxmmf0H8U15PvL1ib8DTrzeAI8wiciaPtKWTUY7hkkvib9OPArzkAVX76kQg/640?wx_fmt=png&from=appmsg&watermark=1#imgIndex=1)

![Pencil 界面](https://mmbiz.qpic.cn/mmbiz_jpg/De5rakickIy8jkLlmzyQ9FcK7rDciadKaxibOafNsYstqJLQwicXv94pN6FcWbL9R3ibp2L1maaI4ZMSy60E34Wpz7A/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=2)

而真正用过之后，反应往往会变成：

> "不对，这东西改变的不是效率，而是工作方式。"

这篇文章，我会尽量用**非营销、非教程、但足够深入**的方式，把 Pencil 这件事一次讲清楚：

它到底是什么？
谁在做？
它和 Figma + IDE 的本质区别在哪？
为什么它能突然爆火？
以及：我们以后应该怎么用这类工具？

---

## 一、为什么这个产品会突然火？先看一个所有人都经历过的问题

在理解 Pencil 之前，我们得先承认一件老事实：

**UI/UX 设计和前端开发，一直合作得并不优雅。**

哪怕是在最成熟的团队里，这个过程通常也是这样的：

- 设计在 Figma 里反复调整
- 开发在 IDE 里逐像素还原
- 一个看似很小的改动：
  - 设计要改一次
  - 代码要跟着改一次
  - 中间还要来回对齐

这不是谁的问题，而是工具结构决定的结果。

如果你做过产品、写过前端，或者在创业团队待过，你一定对下面这个场景不陌生。

- 设计在 Figma 里反复调
- 开发在 IDE 里一行行还原
- 一个小改动：
  - 设计要改一次
  - 代码要改一次
  - 有时还要对一轮

表面看，这是"协作问题"。

但更深一层，其实是**工具范式的问题**：

> 设计工具服务的是"表达"，开发工具服务的是"实现"，它们从来不在同一个系统里。

于是，设计稿变成了"中间产物"，开发的很大一部分精力，花在了**翻译设计**上。

AI 出现之后，这个问题并没有立刻被解决。

大多数 AI 工具做的是：

- 帮你生成代码
- 帮你生成设计稿

但它们依然是**两套系统**。

Pencil 的出现，第一次正面挑战了这件事。

---

## 二、Pencil.dev 到底是什么？一句话讲清楚

如果只用一句话描述 Pencil：

> Pencil 是一个基于 MCP 的 AI 设计画布，它让你在代码编辑器里，用自然语言和可视化方式，同时完成 UI 设计与代码生成。

它不是：

- Figma 的 AI 插件
- 代码生成器的升级版

而是：

> 一个"AI 可以读写的设计画布"，并且这个画布，直接活在 IDE 里。

这也是很多人第一次意识到：

> 原来设计不一定要在设计工具里发生。

以下是桌面端的 Pencil，可以看出是为 Cursor 与 Claude 贴身开发的产品：

![Pencil 桌面端](https://mmbiz.qpic.cn/mmbiz_jpg/De5rakickIy8jkLlmzyQ9FcK7rDciadKaxoSHib3kblC6AUlXmQY4Myg2scGKDJYQaftrOm3rvKzXxzNS1W1RoLmQ/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=3)

下面我们再来看看 Cursor 插件版：

![Pencil Cursor 插件](https://mmbiz.qpic.cn/mmbiz_jpg/De5rakickIy8jkLlmzyQ9FcK7rDciadKaxNmDwEzaDXFxJlQSy9BescVtxmcov46oFtKqEnAYTVCHxv0H0jDzBCA/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=4)

---

## 三、幕后是谁？为什么是他们能做成这件事

在聊技术之前，必须先讲人。

因为 Pencil 并不是 Cursor 官方产品，而是来自一家独立初创公司。

### 1. 公司背景

- **产品**：Pencil.dev
- **公司**：High Agency, Inc.
- **总部**：美国加州 Covina

### 2. 核心创始人：Tom Krcha

Tom Krcha 的履历非常有代表性：

- 曾任 **Around**（新一代视频会议工具）产品负责人（后被 Miro 收购）
- 联合创立 **Alter**（虚拟形象技术公司，后被 Google 收购）

他长期关注的不是"功能堆叠"，而是：

> 如何降低人和复杂工具之间的摩擦。

这点，在 Pencil 上体现得非常明显。

### 3. 资本与生态

Pencil 是 **a16z Speedrun（游戏与 AI 加速器）** 项目成员，并获得早期投资。

这意味着，它从一开始就不是"玩具"，而是被当成**新一代工作范式工具**来设计的。

---

## 四、真正的核心：Pencil 的三大创新

如果你只把 Pencil 当成一个"效率工具"，你会低估它。

它真正做的，是对**技术架构、工作流和生态成本**的三重重构。

### 一）技术架构革命：设计第一次进入编程协议层

#### 1. MCP 协议整合

Pencil 并没有自己发明一套封闭系统，而是选择站在 **MCP（Model Context Protocol）** 之上。

MCP 的意义，用一句人话讲是：

> 它让 AI 不只能"聊天"，而是能"操作真实工具"。

![MCP 协议](https://mmbiz.qpic.cn/mmbiz_jpg/De5rakickIy8jkLlmzyQ9FcK7rDciadKaxB1xNb97LWg4xsNRx7Ekd4tjKLk3ciaA3YxqE2icU1qaoNIGvrrU1tJXg/640?wx_fmt=jpeg&from=appmsg&watermark=1#imgIndex=5)

基于 MCP，Pencil 实现了：

- 设计资产与代码库实时同步
- 跨 IDE 使用（VS Code、Cursor 等 10+ 主流环境）
- 设计状态成为 AI 的"**可读写上下文**"

这一步，本质上解决的是：

> 为什么设计永远和开发环境割裂？

Pencil 的答案是：

> 别在设计工具里做设计，直接在开发环境里做。

#### 2. 动态渲染引擎

Pencil 画布里看到的不是"预览图"，而是**可运行代码的实时映射**。

- 设计变更 → 即时生成可运行代码
- 原生支持 React / Tailwind / Next.js 等技术栈

在官方演示中，5 分钟完成完整 App UI 流程并非噱头，而是架构决定的结果。

---

### 二）工作流突破：从"操作软件"到"表达判断"

#### 1. Vibe Design（氛围设计）

Pencil 最让人震撼的一点，不是快，而是**自然**。

你可以直接说：

- "紫色有点多"
- "这里显得太重了"
- "能不能更像苹果一点"

AI 会把这种**非结构化表达**，转译成：

- 设计调整
- 组件变化
- 代码修改

这背后，是内置的多套设计系统模板，以及对审美节奏的模型理解。

你负责判断"对不对"，AI 负责实现"怎么做"。

#### 2. 从设计到部署的闭环

在传统流程中：

> 设计 → 开发 → 修 bug → 再改设计

而在 Pencil 的目标中：

> 设计画布本身，就是生产线的一部分。

在 Next.js 实测案例中：

- 页面结构
- 组件拆分
- 路由与状态

几乎没有手写代码。

---

### 三）生态与成本结构的改变

#### 1. 成本优势是结构性的

Pencil 支持第三方 API，不强制绑定 Claude 官方套餐，对个人和中小团队非常友好。

实际使用中：

- 设计 + 开发人力成本下降约 **80%**
- 单日产出提升可达 **10–12 倍**

这并不是因为人更拼，而是**翻译成本被消灭了**。

#### 2. 新角色正在出现

一个有趣的变化是：

> "提示词设计师"正在成为新角色。

这个角色的核心能力不是软件操作，而是：

- 审美判断
- 结构理解
- 表达能力

---

## 五、实战视角：Pencil 适合在什么时候用？

一个非常重要的判断是：

> Pencil 不是为了替代 Figma，而是替代"前期混乱"。

最适合 Pencil 的场景包括：

- 想法还不清晰
- 快速原型
- 独立开发
- 小团队探索阶段

而在高保真视觉、复杂设计系统、多设计师协作场景下，Figma 依然更强。

---

## 六、我们以后应该怎么用这类工具？

Pencil 的意义，不在于它本身能活多久，而在于它释放的信号：

> AI 正在从"建议者"，变成"工具操作者"。

这意味着：

- 写代码的人，更像导演
- 做设计的人，更像判断者
- 工具的边界，正在消失

最重要的一点是：

> 当试错成本足够低，"边做边想"，会成为更主流的工作方式。

---

## 最后，把所有线索收拢成一句话

Pencil 并不是一个完美的产品，它也**一定不会**成为最终形态。

但它第一次让很多普通人**清晰地感受到一件事**：

> 设计和开发，可能真的不需要再是两个世界。

当 AI 能够：

- 读懂你的判断
- 操作你的工具
- 在同一个空间里同时处理设计与代码

我们面对的，就不再是"效率提升"，而是**工作范式的切换**。

如果说过去十年，最重要的能力是：

> 把事情做得更专业。

那么接下来，越来越重要的能力可能是：

> 更快地把想法推进成一个真实存在的东西。

而 Pencil，让这件事第一次变得足够具体，也足够可感。

这，正是它值得被认真讨论的原因。

> 这篇文章不是在推荐某个工具，而是在记录一种正在发生的变化。
>
> 如果你已经试过 Pencil.dev，欢迎说说你的真实感受；
>
> 如果你还没试过，也可以说说：你现在最痛苦的设计 / 开发环节是什么？

**THE END**
