# Zhiyun Skills

志云的 Claude Skills 集合，持续更新中

## traffic-analyzer

网站流量分析和市场洞察工具，帮你从 SEMrush/SimilarWeb 数据中发现商业机会。

### 适合谁用

- 想做 AI Tool 的创业者
- 需要分析竞品的产品经理
- 做市场研究的分析师
- 寻找投资机会的投资人
- 对数据分析感兴趣的任何人

### 效果预览

#### 生成的研究报告

| | |
|:---:|:---:|
| ![报告封面](./screenshots/report_cover.png) | ![核心摘要](./screenshots/report_summary.png) |
| 专业研报封面 | 核心指标摘要 |

| | |
|:---:|:---:|
| ![AI工具分析](./screenshots/report_ai_tools.png) | ![机会矩阵](./screenshots/report_opportunities.png) |
| AI工具赛道深度分析 | 高增长机会矩阵 |

#### 数据可视化图表

| | |
|:---:|:---:|
| ![流量分布](./screenshots/01_traffic_distribution.png) | ![AI工具对比](./screenshots/03_ai_tools_comparison.png) |
| 流量类型分布 | AI 工具流量对比 |

![增长象限](./screenshots/04_growth_quadrant.png)

### 安装

#### 快速安装（推荐）

```bash
npx skills add jueyunai/zhiyun-skills
```

#### 注册插件市场

在 Claude Code 中运行：

```bash
/plugin marketplace add jueyunai/zhiyun-skills
```

#### 安装技能

**方式一：直接安装**

```bash
/plugin install traffic-analyzer@zhiyun-skills
```

**方式二：告诉 Agent**

直接告诉 Claude Code：

> 请帮我安装 github.com/jueyunai/zhiyun-skills 中的 Skills

### 使用

#### 1. 准备数据

准备一个包含流量数据的 CSV 文件，需要以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| `type` | 流量类型 | direct, referral, search, social, ai_assistants |
| `target` | 来源域名 | cursor.com, suno.com, lovable.dev |
| `traffic` | 当前流量 | 1020181 |
| `prev_traffic` | 上期流量 | 983839 |
| `traffic_diff` | 增长率 | 0.53（增长 53%），-0.17（下降 17%） |
| `traffic_share` | 流量占比 | 0.018（表示 1.8%） |

#### 2. 告诉 Claude

直接用自然语言告诉 Claude：

```
分析这份 Stripe 流量数据，找出增长最快的 AI 工具
```

```
对比 Cursor、Lovable、Bolt 的流量表现，生成竞品分析报告
```

```
筛选流量 50万+ 且增长超过 30% 的产品，按赛道分类
```

```
AI Agent 赛道表现怎么样？Manus 和 Devin 谁更强？
```

```
生成一份专业的 PDF 研究报告，包含流量分布图和增长象限图
```

### 核心功能

- **增长分析** - 识别高增长流量来源
- **AI 工具发现** - 发现 AI/ML 产品机会
- **竞争分析** - 对比产品流量表现
- **报告生成** - 生成专业 PDF 研究报告

### 典型使用场景

#### 场景 1：寻找 AI Tool 创业方向

**你的问题：** "我想做一个 AI 工具，但不知道做什么方向好？"

**如何使用：**
1. 上传流量数据 CSV 到 Claude
2. 说："帮我分析这些数据，找到适合做的 AI Tool 方向"
3. Claude 会分析热门 AI 工具、识别高增长赛道、找到"中等流量 + 高增长"的机会窗口

#### 场景 2：竞品分析

**你的问题：** "我在做 AI 代码编辑器，想了解竞争对手的情况"

**如何使用：**
1. 上传数据
2. 说："帮我分析 AI 代码编辑器的竞争格局"
3. Claude 会找出所有相关竞品、对比流量规模和增长率、分析市场份额

#### 场景 3：市场趋势发现

**你的问题：** "最近有什么新兴的 AI 应用类别在快速增长？"

**如何使用：**
1. 上传数据
2. 说："帮我找出增长最快的新兴 AI 应用"
3. Claude 会识别高增长产品、发现新兴类别、评估市场潜力

### 输出内容

**数据分析报告：**
- 增长排行榜（谁在快速增长？）
- 流量类型分布（主要从哪里来？）
- AI 工具分析（AI 产品表现如何？）
- 市场细分（各赛道的头部玩家）
- 机会发现（哪些是最好的机会？）

**可视化图表：**
- TOP 流量来源条形图
- 流量 vs 增长率散点图
- 流量类型分布饼图
- AI 工具对比图

**战略洞察：**
- 具体的产品方向建议
- 市场进入时机判断
- 竞争格局分析
- 注意事项和风险提示

### 注意事项

1. **数据来源限制** - 这些数据通常来自 Stripe 支付页面，不是产品总流量
2. **流量≠收入** - 流量大不一定收入高，还要看转化率、定价等
3. **短期波动** - 流量的短期波动可能是营销活动导致
4. **数据完整性** - 使用其他支付方式的产品不会出现在数据中

### 高级功能

在 `scripts/analyze_traffic.py` 中可以调整：
- `min_traffic`: 最小流量阈值（默认 50,000）
- `top_n`: 返回结果数量（默认 20）
- `min_growth`: 最小增长率（默认 20%）

### 相关资源

Skill 内包含的参考文档：
- `traffic-analyzer/references/analysis_methodology.md`: 详细的分析方法论
- `traffic-analyzer/references/common_scenarios.md`: 常见使用场景和案例

### 学习路径

如果你是第一次使用：
1. 先用示例数据跑一遍所有分析
2. 看看生成的图表和报告
3. 阅读参考文档理解分析方法
4. 尝试针对自己的需求定制分析
5. 结合其他数据源综合判断

> **祝你找到好的创业方向！记住："耐心看一个一个调研，熟读唐诗三百首，你一定可以做个 AI Tool 养活自己"** 🚀

---

## 贡献和反馈

如果你有改进建议或发现问题：
1. 可以基于这个 skill 创建自己的版本
2. 添加新的分析方法
3. 改进可视化效果
4. 扩展支持的数据格式

## 目录结构

```
zhiyun-skills/
├── README.md
├── LICENSE
├── screenshots/
└── traffic-analyzer/
    ├── SKILL.md          # Claude 读取的技能文档
    ├── scripts/          # Python 脚本
    ├── templates/        # 报告模板
    └── references/       # 参考文档
```

## License

MIT
