# AI编码实践：从Vibe Coding到SDD

> 来源：微信公众号 阿里云开发者，2026-01-23
> 作者：式遂
> 原文链接：https://mp.weixin.qq.com/s/W6-e-uSPcGCqQAXxx_PDgA

## 核心观点

**淘特导购团队系统性回顾AI编程实践演进历程**——从代码智能补全到Agentic Coding（代理编程），再到Rules约束和SDD（规格驱动开发）。实践中发现SDD理念先进但落地门槛高，最终采用融合策略：以轻量级技术方案模板为输入 + Rules严格约束 + Agent Coding高效实现 + AI自动汇总架构文档，形成兼顾规范性、效率与可维护性的AI辅助编程最佳实践。

---

## 一、背景

### 1.1 业务背景

生成式AI（Generative AI）技术的范式突破正驱动智能开发工具进入超线性演进阶段，主流代码生成工具的迭代周期已从季度级压缩至周级，智能体（Agent）架构创新推动开发效能持续提升。

淘特导购系统承载着商品推荐、会场投放、活动营销等多样化的业务场景，技术团队面临着需求迭代频繁、代码腐化及团队协作度高的问题，如何提升开发效率、保证代码质量、降低维护成本成为我们面临的重要挑战。正是在这样的背景下，我们开始尝试将AI技术融入到日常开发流程中，探索从传统编码到AI辅助编程的转变之路。

### 1.2 AI编程工具的引入

2024年初，团队开始探索AI编程工具，希望通过AI提升开发效率和代码质量。最初接触的是Aone Copilot（阿里内部AI工具）的代码智能补全功能，后来逐步尝试Agentic Coding、Rules约束、SDD（Specification Driven Development，规格驱动开发）等多种AI编程模式。本文将详细记录我们的探索历程、实践经验以及对AI编程未来的思考。

---

## 二、代码智能补全与单方法改写

### 2.1 初识AI编程

**场景1：代码自动补全**

```java
// 开发者输入：
public List<ItemCardVO> buildItemCards(List<ContentEntity> entities) {
    List<ItemCardVO> result = new ArrayList<>();
    // AI自动补全以下代码
    for (ContentEntity entity : entities) {
        ItemCardVO itemCard = new ItemCardVO();
        itemCard.setItemId(entity.getItemId());
        itemCard.setItemTitle(entity.getTitle());
        itemCard.setItemImg(entity.getPicUrl());
        result.add(itemCard);
    }
    return result;
}
```

**场景2：单方法重构**

```java
// 原始代码（冗长难读）
public String getDiscountText(Long finalPrice, Long nnPrice) {
    if (finalPrice == null || nnPrice == null) {
        return "";
    }
    if (finalPrice <= nnPrice) {
        return "";
    }
    Long discount = finalPrice - nnPrice;
    if (discount <= 0) {
        return "";
    }
    String discountYuan = String.valueOf(discount / 100.0);
    return discountYuan + "元";
}

// AI重构后（简洁优雅）
public String getDiscountText(Long finalPrice, Long nnPrice) {
    if (finalPrice == null || nnPrice == null || finalPrice <= nnPrice) {
        return "";
    }
    Money discount = Money.ofFen(finalPrice).subtract(Money.ofFen(nnPrice));
    if (discount.getCent() <= 0) {
        return "";
    }
    return String.format("%s元", discount.getYuan());
}
```

### 2.2 初步收益

- **效率提升**：代码补全在对象构建、模型转换中减少70-80%的键盘输入；单方法重构速度提升50%
- **体验优化**：减少查找API文档的时间，避免拼写错误和语法错误，让开发者更专注于业务逻辑

### 2.3 遇到的问题

1. **局限于局部优化**：只能帮助完成单个方法或代码片段，无法理解整体业务逻辑
2. **缺乏上下文理解**：不了解项目的架构规范和代码风格
3. **无法应对复杂需求**：对于跨多个类、多个模块的需求无能为力

---

## 三、Agentic Coding的探索与挑战

### 3.1 Agentic Coding的尝试

通过编写详细的提示词（Prompt），让AI一次性实现整个功能。

**典型的Prompt结构**：

```
需求：实现NN页面红包模块

背景：
- 需要展示用户可用的红包列表
- 红包按门槛从小到大排序

实现要求：
1. 创建数据服务类 NnRedPacketDataService，查询用户红包
2. 创建模块VO NnRedPacketVO，包含红包列表、总金额等字段
3. 创建模块构建器 NnRedPacketModuleBuilder，组装数据

技术细节：
- 数据服务需要实现 DataService<List<FundQueryDTO>> 接口
- 数据服务实现类需要依赖FpProvider，并执行红包查询
- 模块构建器需要继承 BaseModuleBuilder<NnRedPacketVO>
- 使用 @Component 注解标记为Spring Bean
- 遵循项目代码规范

请生成完整的代码。
```

### 3.2 显著的效率提升

Agentic Coding实现了开发效率的显著优化，虽然Prompt设计需要额外时间，但综合效率提升效果明显。

### 3.3 快速暴露的问题

| 问题 | 现象 | 影响 |
|------|------|------|
| **代码延续性差** | 同样业务第二次生成时，代码风格完全不同 | 同一项目内类似功能实现方式五花八门，维护成本高 |
| **代码风格不一致** | AI不了解项目的代码规范 | 生成的代码风格和存量代码不一致 |
| **团队协同性差** | 不同开发者写的Prompt差异大 | 生成的代码质量参差不齐 |

**原因分析**：AI缺乏项目特定的上下文和约束
1. 没有项目规范：AI不知道项目的代码风格、架构模式、命名规范
2. 没有领域知识：AI不了解淘特导购业务的特定术语和设计模式
3. 没有历史经验：每次都是"零基础"生成代码

---

## 四、Rules约束 - 建立AI的"项目规范"

### 4.1 引入Rules文件

用Rules文件来约束AI的行为，将项目规范、架构模式、领域知识固化下来。

**文件体系**：

```
.aone_copilot/
├── rules/
│   ├── code-style.aonerule          # 代码风格规范
│   ├── project-structure.aonerule   # 项目结构规范
│   └── features.aonerule            # 功能实现规范
└── tech/
    ├── xx秒杀-技术方案.md
    └── xx红包模块-技术方案.md
```

### 4.2 Rules文件内容示例

**代码风格规范**：
- 类名使用大驼峰命名法（PascalCase）
- 方法名和变量名使用小驼峰命名法（camelCase）
- 常量使用全大写，单词间用下划线分隔（CONSTANT_CASE）
- 集合判空统一使用：`CollectionUtils.isEmpty()` 或 `isNotEmpty()`
- Service类使用 `@Component` 注解

**项目结构规范**：

```
com.alibaba.aladdin.app/
├── module/          # 模块构建器
├── domain/          # 领域对象
├── dataservice/impl/# 数据服务实现
└── provider/        # 外部服务提供者
```

### 4.3 技术方案模板

为每个需求创建技术方案文档，明确定义需要生成的代码：

| 维度 | 定义 | 说明 |
|------|------|------|
| **业务定义** | 业务背景和目标 | 1-2句话描述 |
| **业务领域对象** | BO或DTO | 是否需要新增/修改 |
| **模块领域对象** | VO对象 | 属性及类型定义 |
| **数据服务层** | 数据服务定义 | execute逻辑说明 |
| **模块构建器** | 模块构建器定义 | doBuild逻辑说明 |

### 4.4 显著改善的效果

- **代码一致性**：所有生成的代码都遵循统一的命名规范，项目结构清晰
- **开发效率**：技术方案填写时间从2小时降低到20分钟，代码实现从1天降低到2小时
- **团队协作**：技术方案成为团队共同语言，Code Review效率提升50%，新人上手时间从1周降低到2天

### 4.5 依然存在的问题

1. 需求理解不够深入：AI仍然是基于技术方案"翻译"成代码
2. 测试质量参差不齐：测试用例的通过率和覆盖度仍需人工把关
3. 文档滞后：代码变更后，文档更新容易遗漏

---

## 五、SDD探索 - 规格驱动开发

### 5.1 SDD的引入

SDD（Specification Driven Development，规格驱动开发）的核心理念：

- **规格是唯一真理源（Single Source of Truth）**
- **所有的代码、测试、文档都从规格生成**
- **规格即文档，文档永不过期**
- **设计先于实现**
- **可测试性内建**

### 5.2 Speckit执行流程

**文件体系**：

```
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   ├── scripts/
│   └── templates/
├── specs/
│   └── 001-nn-redpacket-module/
│       ├── checklists/requirements.md
│       ├── contracts/api-contract.md
│       ├── data-model.md
│       ├── plan.md
│       ├── quickstart.md
│       ├── research.md
│       └── spec.md
└── req/
    └── nn-redpacket.md
```

**核心步骤**：

1. **speckit.constitution** — 制定整个项目的原则
2. **speckit.specify** — 编写规格说明（spec.md）
3. **speckit.plan** — 制定实施计划（plan.md）
4. **speckit.tasks** — 任务分解（task.md）
5. **speckit.implement** — 实现代码

### 5.3 SDD带来的改进

| 维度 | 改进 |
|------|------|
| **一致性** | 所有代码都严格遵循规格说明，消除了理解偏差 |
| **可测试性** | 自动生成的测试用例覆盖所有正常和异常流程 |
| **可维护性** | 规格说明就是最准确的文档，任何变更都先更新规格 |
| **团队协作** | 新人通过阅读规格说明快速上手，跨团队协作时规格成为统一语言 |

### 5.4 SDD的问题与挑战

| 问题 | 现象 | 影响 |
|------|------|------|
| **规格编写门槛高** | 需要较强的抽象能力和文档编写能力 | 对于简单需求，写规格的时间超过直接写代码 |
| **工具链不成熟** | Spec Kit解析不准确、生成质量不稳定、增量更新困难 | 需要多次返工 |
| **与现有代码库集成困难** | 历史代码缺乏规格说明 | 新老代码风格混杂 |
| **学习成本高** | 写出合格的第一份规格需要3-5次迭代 | 老员工接受度较低 |

### 5.5 SDD适用场景分析

**适合使用SDD**：
- ✅ 全新的项目或模块
- ✅ 核心业务逻辑，需要长期维护
- ✅ 复杂度高，需要详细设计的功能
- ✅ 多人协作的大型需求

**不适合使用SDD**：
- ❌ 简单的工具函数或配置修改
- ❌ 快速验证的实验性功能
- ❌ 一次性的临时需求

---

## 六、当前最佳实践 - Rules + Agentic Coding + AI文档汇总

### 6.1 融合各阶段优势

核心思路：
1. 用Rules约束AI
2. 用技术方案指导实现
3. 用Agentic Coding快速迭代
4. 用AI汇总文档保持同步

### 6.2 技术方案模板优化

优化后的技术方案模板更加轻量级，编写时间从2小时降低到30分钟：

```markdown
# [需求名称]-技术方案

## 业务定义
[简要描述业务背景和目标，1-2句话]

## 业务领域对象
[如果需要新增/修改BO或DTO，在此说明]

## 模块领域对象
| 对象含义 | 实现方案 | 属性及类型 |
|---------|---------|-----------|
| [对象名] | 新增/修改 | 1. 字段1：类型 - 说明<br>2. 字段2：类型 - 说明 |

## 数据服务层
| 数据服务定义 | 实现方案 | execute逻辑 |
|------------|---------|-----------|
| [服务名] | 新增/复用 | 1. 步骤1<br>2. 步骤2 |

## 模块构建器
| 模块构建器定义 | 实现方案 | doBuild逻辑 |
|--------------|---------|-------------|
| [构建器名] | 新增/修改 | 1. 获取数据<br>2. 处理逻辑<br>3. 构建VO |
```

### 6.3 AI文档汇总机制

**流程**：完成需求开发 → 提交AI："将本次代码逻辑汇总到汇总文档" → AI分析代码 → AI更新文档

**架构文档结构**：

```markdown
# NN业务整体架构与逻辑文档

## 一、业务概述
[业务背景、目标、核心价值]

## 二、整体架构
### 2.1 技术架构
[分层架构图、技术栈]

### 2.2 模块组成
[各个模块的功能和关系]

## 三、核心模块详解
### 3.1 NN Feeds模块
#### 3.1.1 功能说明
#### 3.1.2 数据流转
#### 3.1.3 关键逻辑
#### 3.1.4 代码位置

## 四、数据服务层
[各个数据服务的功能和依赖]

## 五、关键流程
[重要的业务流程时序图]
```

---

## 七、思考总结

| 阶段 | 价值 | 局限性 |
|------|------|--------|
| **代码智能补全** | 认识到AI在编码辅助方面的潜力 | 缺乏规范指导，只能局部优化 |
| **Agentic Coding** | 提升功能实现的完整性 | 可延续性和一致性不足 |
| **Rules约束** | 解决代码规范和架构一致性问题 | 对复杂需求理解有限 |
| **SDD** | 理念先进，设计先行 | 落地门槛高，工具链不成熟 |

**当前最佳实践**：以轻量级技术方案模板为输入 + Rules严格约束 + Agent Coding高效实现 + AI自动汇总架构文档

---

## 八、团队介绍

本文作者式遂，来自淘天集团-淘特用户技术团队。团队主要负责淘宝行业&淘特C端链路的研发工作，包含：搜索推荐、互动游戏、导购、交易等基础服务及创新业务。

---

![封面图](https://mmbiz.qpic.cn/mmbiz_jpg/Z6bicxIx5naLwpaH3HGNYYR1pVvHLZpIYuia6yMJmgv6frq6zqVeKUCSKicrewAA01eDzsFa4MopK0eicbTRZHgdUQ/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)
