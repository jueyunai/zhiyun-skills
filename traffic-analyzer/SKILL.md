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
6. **专业报告** - 生成图文并茂的 PDF 研究报告

## 快速开始

### 生成完整报告（推荐）

```bash
python scripts/generate_report.py <csv_file> [output_dir]

# 示例
python scripts/generate_report.py SEMrush-data.csv ./outputs
```

**输出文件：**
- `report.html` / `report_*.pdf` - 报告（艾瑞/艾媒风格）
- `01_traffic_distribution.png` - 流量分布图
- `02_top20_sources.png` - TOP20 来源图
- `03_ai_tools_comparison.png` - AI 工具对比图
- `04_growth_quadrant.png` - 增长象限图
- `05_high_growth_opportunities.png` - 高增长机会图

**依赖安装：**
```bash
pip install pandas matplotlib seaborn jinja2 playwright
playwright install chromium
```

### 常见用户目标

| 用户请求 | 推荐操作 |
|---------|---------|
| "帮我分析这个流量数据" | `generate_report.py` |
| "生成一份专业研报" | `generate_report.py` |
| "找 AI 工具创业机会" | `analyze_traffic.py ai_tools` + `opportunities` |
| "谁是增长领导者？" | `analyze_traffic.py growth` |
| "对比 AI 编程工具" | 筛选并对比特定工具 |

## 脚本使用

### analyze_traffic.py（数据分析）

```bash
python scripts/analyze_traffic.py <csv_file> <analysis_type>
```

| 分析类型 | 说明 |
|----------|------|
| `growth` | 高增长来源排行（流量>50K，按增长率排序） |
| `by_type` | 按流量类型统计 |
| `ai_tools` | AI 相关工具分析 |
| `segments` | 各细分市场头部玩家 |
| `opportunities` | 中等流量 + 高增长机会 |
| `all` | 运行所有分析 |

### visualize_traffic.py（可视化）

```bash
python scripts/visualize_traffic.py <csv_file> <chart_type>
```

| 图表类型 | 说明 |
|----------|------|
| `top_sources` | TOP 流量来源柱状图 |
| `growth` | 流量 vs 增长率散点图 |
| `type_dist` | 流量类型分布图 |
| `ai_tools` | AI 工具流量对比 |
| `all` | 生成所有图表 |

## 数据格式要求

CSV 文件需包含以下列：

| 列名 | 说明 |
|------|------|
| `type` | 流量类型（direct/referral/search/social/ai_assistants） |
| `target` | 来源域名 |
| `traffic` | 当前流量 |
| `prev_traffic` | 上期流量 |
| `traffic_diff` | 增长率（-1到∞，0=无变化） |
| `traffic_share` | 流量占比 |

## 详细参考

完整的分析方法论、场景示例、代码模式和最佳实践，见 [references/guide.md](references/guide.md)。

在以下情况加载该参考：
- 用户需要帮助解读结果
- 解释分析方法论
- 提供战略建议
- 自定义报告模板
- 用户是流量分析新手

## 重要说明

- 数据来自支付页面（Stripe），不是产品总流量
- 高流量 ≠ 高收入（需考虑转化率、定价）
- 短期峰值可能来自营销活动
- 建议结合其他数据源获得完整图景

## 目录结构

```
traffic-analyzer/
├── SKILL.md                 # 本文档
├── scripts/
│   ├── analyze_traffic.py   # 数据分析
│   ├── visualize_traffic.py # 可视化
│   └── generate_report.py   # 报告生成
├── assets/
│   └── report_template.html # HTML 报告模板
└── references/
    └── guide.md             # 完整参考指南
```
