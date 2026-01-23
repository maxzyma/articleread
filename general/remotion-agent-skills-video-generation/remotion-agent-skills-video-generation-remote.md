# 像写代码一样自动化生成短视频

> 来源：微信公众号 小 G，2026-01-22
> 原文链接：https://mp.weixin.qq.com/s/0bgrBvh-ebQo0nxdOtVwTw

## 核心观点

**Remotion 推出 Agent Skills，结合 Claude Code 实现对话式自动化视频生成**——无需手动编写代码，通过几轮对话即可创建专业级视频，大幅降低"用代码制作视频"的门槛。

---

## 背景：什么是 Remotion？

Remotion 是一个开源工具，通过**编写代码**的方式制作视频，实现：

- 像素级精准控制
- 组件复用
- 批量自动化生成

传统视频剪辑软件（如 After Effects）无法做到的代码化能力。

但传统 Remotion 上手门槛高：需要懂 React 代码和 CSS 布局。

---

## Agent Skills：对话式视频生成


![Remotion Agent Skills 演示](https://cdn.jsdelivr.net/gh/maxzyma/articleread/general/remotion-agent-skills-video-generation/images/remotion-demo.png)

### 1. **发布背景**

Remotion 团队在 X 上宣布推出 **Agent Skills**，演示视频在 Claude Code 上通过简单对话创建。

- 推文浏览量：500 多万
- 社区反响：Video editors are cooked（视频剪辑师要慌了）

### 2. **实测效果**

| 案例 | 时间 | 提示词数量 | 输出 |
|------|------|-----------|------|
| 数据可视化视频 | 30 分钟 | 4-5 个 | 完整视频 |
| 产品宣传视频 | 几分钟 | 1 条 | 30 秒视频（含背景音乐、转场、品牌配色、产品演示） |

---

## 使用方式

### 前置要求

需要本地安装：
1. Remotion
2. Claude Code

### 安装命令

```bash
npx skills add remotion-dev/skills
```

安装后，即可在终端中通过对话对 Claude 发号施令生成视频。

---

## 注意事项

### 1. **渲染原理**

无论人写代码还是 AI 写代码，底层依然是**逐帧截屏合成**。

- 复杂画面：渲染吃内存
- 导出速度：不一定比专业软件快

### 2. **开源协议**

Remotion **不采用 MIT 协议**，而是公司许可证。

| 使用场景 | 授权要求 |
|---------|---------|
| 个人开发者 | 免费 ✅ |
| 非营利组织 | 免费 ✅ |
| 小团队（3 人以下） | 免费 ✅ |
| 大公司使用 | 需要商业授权 |
| 商业化视频生成服务 | 需要商业授权 |

---

## 技术启示

对于正在探索视频自动化的开发者：

1. **代码化视频 = 程序化生成**：适合批量、模板化场景，而非单次创意剪辑
2. **AI + Low Code 组合**：Agent Skills 降低门槛，但仍需编程基础
3. **许可证陷阱**：商业化前务必确认开源协议条款

---

## 参考资源

- GitHub 项目：https://github.com/remotion-dev/remotion
- Claude Code 技能：`npx skills add remotion-dev/skills`
