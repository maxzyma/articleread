# 像写代码一样自动化生成短视频

> 来源：微信公众号 小 G，2026-01-22
> 原文链接：https://mp.weixin.qq.com/s/0bgrBvh-ebQo0nxdOtVwTw

## 核心观点

**Remotion 推出 Agent Skills，结合 Claude Code 实现对话式自动化视频生成**——无需手动编写代码，通过几轮对话即可创建专业级视频，大幅降低"用代码制作视频"的门槛。

---

## 背景：什么是 Remotion？

作为一名内容创作者，偶尔会有做演示视频需求，或者想搞点酷炫可视化数据作为演示。但每次使用 After Effects 这种专业软件时，面对复杂的参数设置，既耗时又耗力。

后来在 GitHub 上找到了 **Remotion** 这个开源工具，通过**编写代码**的方式制作视频，实现：

- 像素级精准控制
- 组件复用
- 批量自动化生成

这是传统视频剪辑软件无法做到的代码化能力。


![Remotion 演示](https://mmbiz.qpic.cn/mmbiz_png/uDRkMWLia28hbxINQkibDkjOgPiaQUicDtugfiaxCb0Ughza4nUeZynia2NTaticAQGIqpHtDGgILQtwIkXyHciaXP4ib8w/640?wx_fmt=png)


但它的上手门槛并不低，要求得懂 React 代码，还得会写 CSS 布局，让绝大部分人望而却步。

---

## Agent Skills：对话式视频生成

直到最近，这一门槛被拉低了。Remotion 团队在 X 上宣布推出 **Agent Skills**，并晒出一条酷炫的演示视频。


![Agent Skills 演示](https://mmbiz.qpic.cn/mmbiz_gif/uDRkMWLia28hbxINQkibDkjOgPiaQUicDtugJPgibceY0p3hAiat3fdnpAlKcWI8taQiaSMTxZC2Ehgc9A4yFNgPDTXZQ/640?wx_fmt=gif)


同时分享了视频制作的整个过程，在 Claude Code 上简单几轮对话，便创建出来了。

### 1. **发布反响**

这条消息一经发布，瞬间引爆了整个 AI 技术圈：

- **推文浏览量**：500 多万
- **社区反馈**：Video editors are cooked（视频剪辑师要慌了）

### 2. **实测效果**

| 案例 | 时间 | 提示词数量 | 输出 |
|------|------|-----------|------|
| 数据可视化视频 | 30 分钟 | 4-5 个 | 完整视频 |
| 产品宣传视频 | 几分钟 | 1 条 | 30 秒视频（含背景音乐、转场、品牌配色、产品演示） |


![数据可视化案例](https://mmbiz.qpic.cn/mmbiz_png/uDRkMWLia28hbxINQkibDkjOgPiaQUicDtug6ojlRfHGQ93oDku5GC2UdE6KmNCawxTZZyQRavmiblUhOYngfhsLyDQ/640?wx_fmt=png)


包括背景音乐、转场特效、品牌配色、产品演示等等元素，说实话确实惊艳。


![产品视频案例](https://mmbiz.qpic.cn/mmbiz_png/uDRkMWLia28hbxINQkibDkjOgPiaQUicDtugQUxw3ibcs0KZibAeDelZkwB2miansRS0CoLnWhUdX5SNBocSLkPuYdgnw/640?wx_fmt=png)


---

## 使用方式

### 前置要求

上手使用还是存在一点门槛，需要：
1. 稍微懂点编程知识
2. 本地安装好 Remotion
3. 本地安装好 Claude Code

### 安装命令

```bash
npx skills add remotion-dev/skills
```

安装后，就可以在终端里对 Claude 发号施令了。

官方还提供了安装使用过程的演示视频（时长 01:14）供参考。

---

## 注意事项

### 1. **渲染原理**

无论是由人写代码还是由 AI 写代码，它底层依然是**把组件一帧一帧地截屏合成**。

- **复杂画面**：渲染导出时比较吃内存
- **导出速度**：不一定比专业软件快

### 2. **开源协议**

Remotion **不采用常见的 MIT 协议**，而是采用一种特殊的公司许可证。

| 使用场景 | 授权要求 |
|---------|---------|
| 个人开发者 | 免费 ✅ |
| 非营利组织 | 免费 ✅ |
| 小团队（3 人以下） | 免费 ✅ |
| 大公司使用 | 需要商业授权 |
| 商业化视频生成服务 | 需要商业授权 |

---

## 总结

如果你受够了传统视频剪辑软件的繁琐，想要尝试一种更高效、更智能的创作方式，那现在的 Remotion 值得一试。

它让"用代码控制视频"这种硬核能力，变得前所未有的平易近人。

---

## 参考资源

- GitHub 项目：https://github.com/remotion-dev/remotion
- Claude Code 技能：`npx skills add remotion-dev/skills`
