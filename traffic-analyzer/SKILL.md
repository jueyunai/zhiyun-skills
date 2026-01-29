---
name: traffic-analyzer
description: Analyze web traffic and market data from SEMrush, SimilarWeb, and similar sources. Use when the user wants to analyze traffic data, find market opportunities, perform competitor analysis, discover AI tool trends, identify growth leaders, analyze market segments, or evaluate business opportunities from CSV traffic data. Triggers include requests to "analyze traffic data", "find AI tool opportunities", "compare competitors", "find growth leaders", "analyze market trends", or any request involving traffic/market analysis CSV files.
---

# Traffic Analyzer

分析网站流量和市场数据，发现商业机会、理解市场趋势、进行竞争分析。

## 核心能力

1. **增长分析** - 识别高增长流量来源和新兴市场
2. **市场细分** - 按类型、分类和行业垂直分析流量
3. **AI工具发现** - 专门分析 AI/ML 产品机会
4. **竞争分析** - 对比类似产品的流量表现
5. **机会发现** - 发现"甜点"市场（中等流量+高增长）
6. **数据可视化** - 生成图表和图形展示洞察
7. **专业报告** - 生成图文并茂的 PDF 研究报告

## 快速开始

### 生成完整报告（推荐）

一键生成包含数据分析、可视化图表和专业排版的 PDF 报告：

```bash
python scripts/generate_report.py <csv_file> [output_dir]
```

**示例：**
```bash
python scripts/generate_report.py SEMrush-data.csv ./outputs
```

**输出：**
- `report.html` - HTML 版本报告
- `report_20260129.pdf` - PDF 版本报告（艾瑞/艾媒风格）
- `01_traffic_distribution.png` - 流量分布图
- `02_top20_sources.png` - TOP20 来源图
- `03_ai_tools_comparison.png` - AI 工具对比图
- `04_growth_quadrant.png` - 增长象限图
- `05_high_growth_opportunities.png` - 高增长机会图

### 基础分析工作流

1. **理解数据结构** - 检查列名和数据类型
2. **选择分析类型** - 根据用户目标（见下方常见场景）
3. **运行分析脚本** - 使用适当参数
4. **生成可视化** - 创建图表
5. **提供洞察** - 总结发现和可操作建议

### 常见用户目标

| 用户请求 | 推荐操作 |
|---------|---------|
| "帮我分析这个流量数据" | 运行 `generate_report.py` 生成完整报告 |
| "生成一份专业研报" | 运行 `generate_report.py` |
| "找 AI 工具创业机会" | 运行 AI 工具分析 + 机会分析 |
| "谁是增长领导者？" | 运行增长分析 |
| "对比 AI 编程工具" | 筛选并对比特定工具 |
| "发现市场机会" | 运行机会分析 |

## 使用分析脚本

### generate_report.py（完整报告）

生成完整的 PDF 研究报告，包含：
- 封面（艾瑞/艾媒专业风格）
- 核心摘要与指标
- 市场全景分析
- AI 工具赛道深度分析
- 机会赛道与标的
- 风险提示
- 配置方向参考

```bash
python scripts/generate_report.py <csv_file> [output_dir]
```

**依赖安装：**
```bash
pip install pandas matplotlib seaborn jinja2 playwright
playwright install chromium  # 或使用系统 Chrome
```

### analyze_traffic.py（数据分析）

主分析脚本，支持多种分析类型：

```bash
python scripts/analyze_traffic.py <csv_file> <analysis_type>
```

**分析类型：**
- `growth` - 高增长来源排行（过滤流量 > 50K，按增长率排序）
- `by_type` - 按流量类型统计（referral、search、social 等）
- `ai_tools` - AI 相关工具分析（按 AI 关键词和分类筛选）
- `segments` - 各细分市场头部玩家
- `opportunities` - 中等流量 + 高增长机会
- `all` - 运行所有分析

**输出：** JSON 格式结果，可进一步处理或展示

### visualize_traffic.py（可视化）

生成可视化图表：

```bash
python scripts/visualize_traffic.py <csv_file> <chart_type>
```

**图表类型：**
- `top_sources` - TOP 流量来源水平柱状图（按增长着色）
- `growth` - 流量 vs 增长率散点图
- `type_dist` - 流量类型分布饼图和柱状图
- `ai_tools` - AI 工具流量对比柱状图
- `all` - 生成所有图表

## 数据理解

### 期望数据格式

CSV 文件应包含以下关键列：
- `type` - 流量类型（direct、referral、search、social、ai_assistants 等）
- `target` - 来源域名/网站
- `traffic` - 当前流量
- `prev_traffic` - 上期流量
- `traffic_diff` - 增长率（-1 到无穷大，0 = 无变化）
- `traffic_share` - 流量占比

### 字段解读

**traffic_diff（增长率）：**
- 1.0 = 100% 增长（翻倍）
- 0.5 = 50% 增长
- -0.2 = 20% 下降
- 0 = 无变化

**type（流量类型）含义：**
- `direct` - 用户直接输入 URL（品牌认知度）
- `referral` - 来自其他网站（合作/生态）
- `search` - 来自搜索引擎（SEO/需求）
- `social` - 来自社交媒体（病毒传播）
- `ai_assistants` - 来自 AI 工具如 ChatGPT、Claude

## 报告模板

报告使用 Jinja2 模板引擎，模板文件位于 `templates/report_template.html`。

### 自定义报告

可以修改模板来自定义：
- 机构名称和 Logo
- 颜色主题
- 报告章节结构
- 封面样式

### 模板变量

主要变量包括：
- `report_title` - 报告标题
- `institution_name` - 机构名称
- `core_metrics` - 核心指标列表
- `traffic_by_type` - 流量类型分析
- `top20_sources` - TOP20 来源
- `ai_tools_ranking` - AI 工具排行
- `charts` - 图表路径字典

## 分析模式

### 模式 1：寻找 AI 工具机会

```python
# 1. 运行完整报告生成
python scripts/generate_report.py data.csv ./outputs

# 2. 或分步骤分析
results = run_script('analyze_traffic.py', csv_file, 'ai_tools')
opps = run_script('analyze_traffic.py', csv_file, 'opportunities')

# 3. 找出重叠 - 高增长且中等流量的 AI 工具
ai_opportunities = [tool for tool in results if tool in opps]

# 4. 按工具类型分类（编程、设计、音频、视频等）
# 5. 给出带市场背景的建议
```

### 模式 2：竞争分析

```python
# 1. 识别竞争对手（按关键词或分类筛选）
# 2. 提取流量数据
# 3. 对比流量、增长率和来源
# 4. 生成对比可视化
# 5. 提供战略洞察
```

### 模式 3：市场趋势发现

```python
# 1. 运行增长分析找出增长最快的来源
# 2. 按分类/关键词分组识别趋势
# 3. 按流量阈值筛选聚焦可行市场
# 4. 创建趋势总结和案例
```

## 方法论参考

详细的分析方法论、市场洞察和解读指南见：
- `references/analysis_methodology.md` - 分析框架和商业洞察
- `references/common_scenarios.md` - 常见用例的分步示例

在以下情况加载这些参考：
- 用户需要帮助解读结果
- 解释分析方法论
- 提供战略建议
- 用户是流量分析新手

## 最佳实践

### 数据质量
- 分析前检查缺失值
- 过滤掉流量很小的来源（< 10K）以获得更清晰的洞察
- 验证数据新鲜度和覆盖时间段

### 分析方法
- 先广泛分析，再深入感兴趣的特定领域
- 结合多种分析获得全面视角
- 始终提供背景和解读，不只是原始数字
- 考虑多个因素：增长、规模、竞争、契合度

### 展示
- 使用可视化让趋势清晰
- 突出可操作的洞察，而不只是数据
- 从数据中提供具体案例
- 包含数据局限性的说明

### 战略思考
- 中等流量 + 高增长 = 最佳机会
- 流量很高 = 难以竞争，成熟市场
- 负增长 = 避免或理解原因
- 根据用户技能和资源推荐机会

## 重要说明

- 这些数据来自结账/支付页面（Stripe），不是产品总流量
- 高流量 ≠ 高收入（需要转化率、定价等）
- 短期峰值可能来自营销活动
- 部分产品使用其他支付处理商，不会出现在此数据中
- 建议结合其他数据源获得完整图景

## 目录结构

```
traffic-analyzer/
├── SKILL.md                 # 本文档
├── scripts/
│   ├── analyze_traffic.py   # 数据分析脚本
│   ├── visualize_traffic.py # 可视化脚本
│   └── generate_report.py   # 完整报告生成脚本
├── templates/
│   └── report_template.html # HTML 报告模板
└── references/
    ├── analysis_methodology.md
    └── common_scenarios.md
```
