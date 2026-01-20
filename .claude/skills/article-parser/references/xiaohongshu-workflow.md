| 知道标题 | 直接搜索标题关键词 | `Claude Code 工作流` |
| 按时间排序 | 找到最新发布的文章 | 搜狗支持时间筛选 |
| 技术文章 | 优先搜微信公众号 | `site:mp.weixin.qq.com "技术关键词"` |

**跨平台搜索优先级**：

1. **搜狗微信搜索**（最推荐）
   - https://weixin.sogou.com/
   - 覆盖最全
   - 更新及时

2. **Google/Bing 高级搜索**
   ```
   site:mp.weixin.qq.com "作者名" "标题关键词"
   "作者名" "标题关键词" 公众号
   ```

3. **微信 APP 搜一搜**
   - 最准确
   - 需要手动操作
   - 适合验证

4. **第三方聚合平台**
   - 新榜：https://www.newrank.cn/
   - 清博：https://www.gsdata.cn/

#### 0.3 备选搜索方案

如果搜狗搜索没有找到，尝试：

1. **Google/Bing 高级搜索**：
   ```
   site:mp.weixin.qq.com "关键词"
   site:mp.weixin.qq.com "作者名" "关键词"
   ```

2. **直接在微信中搜索**：
   - 打开微信 APP
   - 点击"搜一搜"
   - 输入关键词
   - 选择"文章"分类

3. **其他文字友好的平台**：
   - 个人博客/官网
   - Medium/Dev.to（英文）
   - 知乎/简书
   - Medium/Dev.to（英文技术文章）
   - 知乎、简书等

#### 0.4 何时使用小红书流程

只有在以下情况才使用小红书提取流程：
- ❌ 微信公众号没有该文章
- ❌ 其他平台也没有完整版本
- ✅ 用户明确要求从小红书提取
- ✅ 内容是小红书原创（如独家图文/视频笔记）

#### 0.5 小红书访问绕过方法

**问题**：直接访问小红书链接经常被封锁（404, error_code=300031）

**解决方案**：通过首页搜索结果访问（自动添加 xsec_token）

```bash
# 步骤 1：访问小红书首页
navigate_page -> https://www.xiaohongshu.com/

# 步骤 2：使用搜索框搜索
fill -> 搜索框
value: "<作者名> <标题关键词>"

# 步骤 3：按 Enter 执行搜索
press_key -> "Enter"

# 步骤 4：从搜索结果中点击目标文章
click -> <文章标题链接>

# 步骤 5：页面会自动包含 xsec_token 参数，成功访问
```

**关键原理**：
- 直接访问：`https://www.xiaohongshu.com/explore/69698507000000001a0335b1` ❌ 被封锁
- 搜索访问：`https://www.xiaohongshu.com/explore/69698507000000001a0335b1?xsec_token=xxx&xsec_source=pc_search` ✅ 成功

**URL 参数说明**：
- `xsec_token`: 小红书安全令牌，通过搜索结果页面自动生成
- `xsec_source`: 来源标识（如 `pc_search`）

**提取流程调整**：
1. 优先尝试通过首页搜索找到目标文章
2. 点击搜索结果链接（自动带 token）
3. 如果搜索未找到，再尝试直接访问原始链接
4. 如果仍然被封锁，建议寻找其他平台的版本

---

## 内容类型识别
