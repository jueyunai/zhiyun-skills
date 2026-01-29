#!/usr/bin/env python3
"""
流量分析报告生成工具
整合数据分析、图表生成、HTML渲染和PDF导出的完整流程

使用方法:
    python generate_report.py <csv_file> [output_dir]

依赖:
    pip install pandas matplotlib seaborn jinja2 playwright
    playwright install chromium  # 或使用系统 Chrome
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['Heiti SC', 'PingFang SC', 'Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'sans-serif'
sns.set_style("whitegrid")

# 脚本所在目录
SCRIPT_DIR = Path(__file__).parent.absolute()
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "assets"


class TrafficAnalyzer:
    """流量数据分析类"""

    # AI 工具关键词
    AI_KEYWORDS = [
        'ai', 'gpt', 'claude', 'openai', 'anthropic', 'midjourney',
        'cursor', 'lovable', 'windsurf', 'suno', 'elevenlabs',
        'runway', 'turboscribe', 'undetectable', 'manus', 'emergent',
        'kling', 'higgsfield', 'hailuo', 'replit', 'blackbox', 'grok'
    ]

    # AI 工具分类映射
    AI_CATEGORIES = {
        'lovable': 'AI编程', 'cursor': 'AI编程', 'windsurf': 'AI编程',
        'replit': 'AI编程', 'blackbox': 'AI编程',
        'suno': 'AI音乐',
        'elevenlabs': 'AI语音', 'lalal': '音频处理',
        'midjourney': 'AI图像',
        'runway': 'AI视频', 'kling': 'AI视频', 'higgsfield': 'AI视频', 'hailuo': 'AI视频',
        'manus': 'AI Agent', 'emergent': 'AI开发',
        'undetectable': 'AI检测', 'turboscribe': 'AI转录',
        'grok': 'AI助手', 'chatgpt': 'AI助手', 'claude': 'AI助手'
    }

    def __init__(self, csv_path: str):
        """初始化分析器"""
        self.df = pd.read_csv(csv_path)
        self.total_traffic = self.df['traffic'].sum()
        self.total_sources = len(self.df)

    def get_summary_metrics(self) -> dict:
        """获取核心指标"""
        ai_traffic = self._get_ai_traffic()
        ai_ratio = ai_traffic / self.total_traffic * 100

        growth_sources = len(self.df[self.df['traffic_diff'] > 0])
        growth_ratio = growth_sources / self.total_sources * 100

        return {
            'total_traffic': self.total_traffic,
            'total_sources': self.total_sources,
            'ai_ratio': ai_ratio,
            'growth_ratio': growth_ratio
        }

    def _get_ai_traffic(self) -> int:
        """计算AI工具总流量"""
        ai_mask = (
            self.df['type'].str.contains('ai', case=False, na=False) |
            self.df['target'].str.contains('|'.join(self.AI_KEYWORDS), case=False, na=False)
        )
        return self.df[ai_mask]['traffic'].sum()

    def analyze_by_type(self) -> list:
        """按流量类型分析"""
        type_stats = self.df.groupby('type').agg({
            'traffic': 'sum',
            'traffic_share': 'sum',
            'target': 'count'
        }).reset_index()

        type_stats.columns = ['type', 'traffic', 'share', 'count']
        type_stats = type_stats.sort_values('traffic', ascending=False)

        # 类型说明映射
        type_notes = {
            'referral': '第三方SaaS产品贡献',
            'direct': '品牌认知度',
            'search': '搜索引擎入口',
            'social': '社交媒体引流',
            'ai_assistants': '快速崛起',
            'mail': '邮件营销'
        }

        results = []
        for _, row in type_stats.iterrows():
            results.append({
                'type': row['type'],
                'traffic': int(row['traffic']),
                'share': f"{row['share'] * 100:.1f}%",
                'count': int(row['count']),
                'note': type_notes.get(row['type'], '-')
            })

        return results

    def get_top_sources(self, n: int = 20) -> list:
        """获取TOP流量来源"""
        df_top = self.df.nlargest(n, 'traffic')

        # 高增长标记
        highlight_threshold = 0.3  # 30%以上增长高亮

        results = []
        for _, row in df_top.iterrows():
            results.append({
                'source': row['target'],
                'traffic': int(row['traffic']),
                'growth': row['traffic_diff'],
                'type': row['type'],
                'highlight': row['traffic_diff'] > highlight_threshold
            })

        return results

    def analyze_ai_tools(self, min_traffic: int = 50000) -> list:
        """分析AI工具"""
        ai_mask = (
            self.df['type'].str.contains('ai', case=False, na=False) |
            self.df['target'].str.contains('|'.join(self.AI_KEYWORDS), case=False, na=False)
        )

        df_ai = self.df[ai_mask & (self.df['traffic'] >= min_traffic)].copy()
        df_ai = df_ai.sort_values('traffic', ascending=False)

        results = []
        for _, row in df_ai.iterrows():
            target = row['target'].lower()

            # 确定分类
            category = 'AI工具'
            for key, cat in self.AI_CATEGORIES.items():
                if key in target:
                    category = cat
                    break

            # 确定评级
            growth = row['traffic_diff']
            traffic = row['traffic']
            if growth > 0.5 and traffic > 200000:
                rating, rating_class = 'S级', 's'
            elif growth > 0.2 or traffic > 500000:
                rating, rating_class = 'A级', 'a'
            else:
                rating, rating_class = 'B级', 'b'

            results.append({
                'tool': row['target'],
                'category': category,
                'traffic': int(row['traffic']),
                'growth': row['traffic_diff'],
                'rating': rating,
                'rating_class': rating_class
            })

        return results[:20]  # 返回前20个

    def find_opportunities(self, min_traffic: int = 50000, max_traffic: int = 1000000, min_growth: float = 0.2) -> list:
        """寻找高增长机会"""
        df_opp = self.df[
            (self.df['traffic'] >= min_traffic) &
            (self.df['traffic'] <= max_traffic) &
            (self.df['traffic_diff'] >= min_growth)
        ].copy()

        df_opp = df_opp.sort_values('traffic_diff', ascending=False)

        results = []
        for _, row in df_opp.iterrows():
            results.append({
                'source': row['target'],
                'type': row['type'],
                'traffic': int(row['traffic']),
                'growth': row['traffic_diff']
            })

        return results[:20]

    def find_risk_items(self, min_traffic: int = 100000, max_decline: float = -0.15) -> list:
        """寻找下行风险标的"""
        df_risk = self.df[
            (self.df['traffic'] >= min_traffic) &
            (self.df['traffic_diff'] <= max_decline)
        ].copy()

        df_risk = df_risk.sort_values('traffic_diff')

        results = []
        for _, row in df_risk.head(10).iterrows():
            decline = row['traffic_diff']
            if decline < -0.25:
                risk_level = '高'
            elif decline < -0.2:
                risk_level = '中等'
            else:
                risk_level = '关注'

            results.append({
                'name': row['target'],
                'traffic': int(row['traffic']),
                'growth': row['traffic_diff'],
                'risk_level': risk_level
            })

        return results


class ChartGenerator:
    """图表生成类"""

    def __init__(self, df: pd.DataFrame, output_dir: Path):
        self.df = df
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self) -> dict:
        """生成所有图表"""
        charts = {}
        charts['traffic_distribution'] = self._plot_traffic_distribution()
        charts['top20_sources'] = self._plot_top_sources()
        charts['ai_tools'] = self._plot_ai_tools()
        charts['growth_quadrant'] = self._plot_growth_quadrant()
        charts['opportunities'] = self._plot_opportunities()
        return charts

    def _plot_traffic_distribution(self) -> str:
        """流量类型分布图"""
        type_stats = self.df.groupby('type')['traffic'].sum().sort_values(ascending=False)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # 饼图
        colors = plt.cm.Blues(range(50, 250, int(200/len(type_stats))))
        ax1.pie(type_stats.values, labels=type_stats.index, autopct='%1.1f%%',
                startangle=90, colors=colors)
        ax1.set_title('流量类型分布', fontsize=14, fontweight='bold')

        # 柱状图
        bars = ax2.bar(range(len(type_stats)), type_stats.values, color=colors)
        ax2.set_xticks(range(len(type_stats)))
        ax2.set_xticklabels(type_stats.index, rotation=45, ha='right')
        ax2.set_ylabel('流量', fontsize=12)
        ax2.set_title('各类型流量规模', fontsize=14, fontweight='bold')

        # 添加数值标签
        for bar, val in zip(bars, type_stats.values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{val/1e6:.1f}M', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        output_file = self.output_dir / '01_traffic_distribution.png'
        plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        return str(output_file)

    def _plot_top_sources(self, n: int = 20) -> str:
        """TOP流量来源图"""
        df_top = self.df.nlargest(n, 'traffic')

        fig, ax = plt.subplots(figsize=(12, 10))

        colors = ['#22c55e' if x > 0 else '#ef4444' for x in df_top['traffic_diff']]
        bars = ax.barh(range(len(df_top)), df_top['traffic'].values, color=colors)

        ax.set_yticks(range(len(df_top)))
        ax.set_yticklabels(df_top['target'].values)
        ax.set_xlabel('流量', fontsize=12)
        ax.set_title(f'TOP {n} 流量来源', fontsize=14, fontweight='bold')
        ax.invert_yaxis()

        # 添加增长率标签
        for i, (bar, diff) in enumerate(zip(bars, df_top['traffic_diff'])):
            sign = '+' if diff > 0 else ''
            ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                   f' {sign}{diff*100:.1f}%', va='center', fontsize=9)

        plt.tight_layout()
        output_file = self.output_dir / '02_top20_sources.png'
        plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        return str(output_file)

    def _plot_ai_tools(self) -> str:
        """AI工具对比图"""
        ai_keywords = TrafficAnalyzer.AI_KEYWORDS

        ai_mask = (
            self.df['type'].str.contains('ai', case=False, na=False) |
            self.df['target'].str.contains('|'.join(ai_keywords), case=False, na=False)
        )

        df_ai = self.df[ai_mask & (self.df['traffic'] > 50000)].copy()
        df_ai = df_ai.nlargest(20, 'traffic')

        fig, ax = plt.subplots(figsize=(12, 10))

        # 根据增长率着色
        colors = []
        for diff in df_ai['traffic_diff']:
            if diff > 0.5:
                colors.append('#15803d')  # 深绿
            elif diff > 0:
                colors.append('#86efac')  # 浅绿
            elif diff > -0.1:
                colors.append('#fb923c')  # 橙色
            else:
                colors.append('#ef4444')  # 红色

        bars = ax.barh(range(len(df_ai)), df_ai['traffic'].values, color=colors)

        ax.set_yticks(range(len(df_ai)))
        ax.set_yticklabels(df_ai['target'].values)
        ax.set_xlabel('流量', fontsize=12)
        ax.set_title('AI 工具流量对比 TOP20', fontsize=14, fontweight='bold')
        ax.invert_yaxis()

        # 添加增长率标签
        for i, (bar, diff) in enumerate(zip(bars, df_ai['traffic_diff'])):
            sign = '+' if diff > 0 else ''
            ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                   f' {sign}{diff*100:.1f}%', va='center', fontsize=9)

        # 图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#15803d', label='>50% 增长'),
            Patch(facecolor='#86efac', label='0-50% 增长'),
            Patch(facecolor='#fb923c', label='0-10% 下跌'),
            Patch(facecolor='#ef4444', label='>10% 下跌')
        ]
        ax.legend(handles=legend_elements, loc='lower right')

        plt.tight_layout()
        output_file = self.output_dir / '03_ai_tools_comparison.png'
        plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        return str(output_file)

    def _plot_growth_quadrant(self) -> str:
        """增长象限图"""
        df_filtered = self.df[self.df['traffic'] > 30000].copy()

        fig, ax = plt.subplots(figsize=(12, 10))

        scatter = ax.scatter(
            df_filtered['traffic'],
            df_filtered['traffic_diff'] * 100,
            alpha=0.6,
            s=60,
            c=df_filtered['traffic_diff'] * 100,
            cmap='RdYlGn',
            vmin=-50,
            vmax=100
        )

        ax.set_xlabel('流量规模', fontsize=12)
        ax.set_ylabel('增长率 (%)', fontsize=12)
        ax.set_title('流量规模 vs 增长率 象限分析', fontsize=14, fontweight='bold')
        ax.set_xscale('log')
        ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=100000, color='gray', linestyle='--', alpha=0.5)

        # 标注重点产品
        highlight = df_filtered[
            (df_filtered['traffic_diff'] > 0.3) &
            (df_filtered['traffic'] > 100000)
        ].head(10)

        for _, row in highlight.iterrows():
            ax.annotate(row['target'],
                       (row['traffic'], row['traffic_diff'] * 100),
                       fontsize=8, alpha=0.8,
                       xytext=(5, 5), textcoords='offset points')

        plt.colorbar(scatter, ax=ax, label='增长率 (%)')

        # 象限标注
        ax.text(0.95, 0.95, '高流量+高增长\n(最佳机会)', transform=ax.transAxes,
               ha='right', va='top', fontsize=10, color='green', alpha=0.7)
        ax.text(0.05, 0.95, '低流量+高增长\n(潜力股)', transform=ax.transAxes,
               ha='left', va='top', fontsize=10, color='blue', alpha=0.7)

        plt.tight_layout()
        output_file = self.output_dir / '04_growth_quadrant.png'
        plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        return str(output_file)

    def _plot_opportunities(self) -> str:
        """高增长机会图"""
        df_opp = self.df[
            (self.df['traffic'] >= 50000) &
            (self.df['traffic'] <= 1500000) &
            (self.df['traffic_diff'] >= 0.2)
        ].copy()

        df_opp = df_opp.nlargest(15, 'traffic_diff')

        fig, ax = plt.subplots(figsize=(12, 8))

        bars = ax.barh(range(len(df_opp)), df_opp['traffic_diff'].values * 100,
                      color='#22c55e')

        ax.set_yticks(range(len(df_opp)))
        ax.set_yticklabels(df_opp['target'].values)
        ax.set_xlabel('增长率 (%)', fontsize=12)
        ax.set_title('高增长机会标的 (流量5万-150万)', fontsize=14, fontweight='bold')
        ax.invert_yaxis()

        # 添加流量标签
        for i, (bar, traffic) in enumerate(zip(bars, df_opp['traffic'])):
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                   f'{traffic/1000:.0f}K', va='center', fontsize=9, color='gray')

        plt.tight_layout()
        output_file = self.output_dir / '05_high_growth_opportunities.png'
        plt.savefig(output_file, dpi=200, bbox_inches='tight', facecolor='white')
        plt.close()
        return str(output_file)


class ReportGenerator:
    """报告生成类"""

    def __init__(self, analyzer: TrafficAnalyzer, output_dir: Path):
        self.analyzer = analyzer
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 加载模板
        self.env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
        self.template = self.env.get_template('report_template.html')

    def generate(self, charts: dict) -> Path:
        """生成完整报告"""
        # 准备模板数据
        data = self._prepare_data(charts)

        # 渲染 HTML
        html_content = self.template.render(**data)
        html_path = self.output_dir / 'report.html'
        html_path.write_text(html_content, encoding='utf-8')

        # 转换为 PDF
        pdf_path = self._convert_to_pdf(html_path)

        return pdf_path

    def _prepare_data(self, charts: dict) -> dict:
        """准备模板数据"""
        metrics = self.analyzer.get_summary_metrics()
        now = datetime.now()

        # 格式化流量数值
        def format_traffic(n):
            if n >= 10000000:
                return f"{n/10000000:.0f}千万"
            elif n >= 10000:
                return f"{n/10000:.0f}万"
            else:
                return f"{n:,}"

        data = {
            # 报告元信息
            'report_title': 'AI工具支付流量深度研究报告',
            'cover_title': 'AI工具支付流量<br>深度研究报告',
            'institution_name': '数据研究',
            'institution_name_en': 'DATA RESEARCH',
            'data_source': 'SEMrush',
            'analysis_target': 'checkout.stripe.com',
            'data_period': f'{now.year}年{now.month}月',
            'report_id': f'AITR-{now.year}-{now.month:03d}',
            'report_year': now.year,

            # 封面标语
            'cover_tagline_1': '基于 Stripe 支付数据的 AI 赛道市场格局分析',
            'cover_highlight': self._get_highlight_text(),

            # 核心指标
            'core_metrics': [
                {'value': format_traffic(metrics['total_traffic']), 'label': '总流量'},
                {'value': f"{metrics['total_sources']:,}", 'label': '流量来源数'},
                {'value': f"{metrics['ai_ratio']:.1f}%", 'label': 'AI工具流量占比', 'change': '↑ 上升', 'change_class': 'up'},
                {'value': f"{metrics['growth_ratio']:.1f}%", 'label': '增长型来源占比'}
            ],

            # 核心观点
            'core_points': self._get_core_points(),

            # 图表路径
            'charts': charts,

            # 流量类型分析
            'traffic_by_type': self.analyzer.analyze_by_type(),

            # TOP20 来源
            'top20_sources': self.analyzer.get_top_sources(20),

            # AI工具排行
            'ai_tools_ranking': self.analyzer.analyze_ai_tools(),

            # 赛道分析
            'track_analysis': self._get_track_analysis(),

            # 推荐标的
            's_level_recommendations': self._get_s_recommendations(),
            'a_level_recommendations': self._get_a_recommendations(),

            # 风险提示
            'risk_items': self.analyzer.find_risk_items(),

            # 数据局限性
            'data_caveats': [
                '本数据仅反映经Stripe支付的流量，不包含其他支付渠道（如PayPal、国内支付）',
                '流量数据不等于收入数据，需结合定价策略、转化率综合判断',
                '部分产品可能存在营销活动导致的短期波动',
                '建议结合其他数据源（AppAnnie、SimilarWeb）进行交叉验证'
            ],

            # 重点关注赛道
            'focus_tracks': self._get_focus_tracks(),

            # 核心结论
            'conclusions': self._get_conclusions(),

            # 免责声明
            'disclaimer': '本报告基于公开数据整理分析，仅作为信息参考之用，不构成对任何产品或服务的推荐。报告中涉及的数据均来源于第三方平台（SEMrush），我们不对数据的准确性和完整性做出保证。市场有风险，决策需谨慎。本报告中的观点仅代表分析时点的判断，可能随市场变化而调整。'
        }

        return data

    def _get_highlight_text(self) -> str:
        """获取封面高亮文本"""
        ai_tools = self.analyzer.analyze_ai_tools()
        if ai_tools:
            top_growth = max(ai_tools, key=lambda x: x['growth'])
            return f"{top_growth['tool']} +{top_growth['growth']*100:.1f}% 爆发式增长"
        return "AI赛道深度分析"

    def _get_core_points(self) -> list:
        """获取核心观点"""
        return [
            {'title': 'AI编程工具赛道出现结构性分化', 'description': '，部分产品爆发式增长冲击头部格局'},
            {'title': 'AI音乐、AI视频赛道增速放缓', 'description': '，头部产品进入存量竞争阶段'},
            {'title': '新兴AI Agent赛道', 'description': '展现强劲增长动能，是重点关注方向'}
        ]

    def _get_track_analysis(self) -> list:
        """获取赛道分析数据"""
        ai_tools = self.analyzer.analyze_ai_tools()

        # 按分类分组
        categories = {}
        for tool in ai_tools:
            cat = tool['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(tool)

        tracks = []

        # AI编程赛道
        if 'AI编程' in categories:
            coding_tools = categories['AI编程'][:5]
            data_lines = ["市场格局变化：", "产品              流量        环比       状态"]
            for t in coding_tools:
                status = '★ 爆发' if t['growth'] > 1 else ('稳增' if t['growth'] > 0 else '下滑')
                data_lines.append(f"{t['tool'][:15]:<15} {t['traffic']:>10,}    {t['growth']*100:>+.1f}%     {status}")

            tracks.append({
                'name': 'AI编程工具赛道',
                'data': '\n'.join(data_lines),
                'insight': '自然语言生成完整应用的产品模式正在冲击传统IDE模式，降低编程门槛吸引大量非技术用户。'
            })

        # AI视频赛道
        if 'AI视频' in categories:
            video_tools = categories['AI视频'][:5]
            data_lines = ["市场格局：", "产品              流量        环比       状态"]
            for t in video_tools:
                status = '★ 上升' if t['growth'] > 0.2 else ('承压' if t['growth'] < 0 else '稳定')
                data_lines.append(f"{t['tool'][:15]:<15} {t['traffic']:>10,}    {t['growth']*100:>+.1f}%     {status}")

            tracks.append({
                'name': 'AI视频生成赛道',
                'data': '\n'.join(data_lines),
                'insight': 'AI视频赛道竞争加剧，差异化产品展现增长势头。'
            })

        return tracks

    def _get_s_recommendations(self) -> list:
        """获取S级推荐"""
        ai_tools = self.analyzer.analyze_ai_tools()
        s_level = [t for t in ai_tools if t['rating'] == 'S级'][:3]

        recommendations = []
        reasons = {
            'AI编程': '自然语言生成应用，降低编程门槛',
            'AI Agent': 'Agent赛道龙头，已验证商业化能力',
            'AI视频': '高增长视频生成，差异化竞争'
        }

        for t in s_level:
            recommendations.append({
                'name': t['tool'],
                'category': t['category'],
                'traffic': f"{t['traffic']/1000:.0f}K",
                'growth': t['growth'],
                'reason': reasons.get(t['category'], '高增长潜力标的')
            })

        return recommendations

    def _get_a_recommendations(self) -> list:
        """获取A级推荐"""
        ai_tools = self.analyzer.analyze_ai_tools()
        a_level = [t for t in ai_tools if t['rating'] == 'A级'][:5]

        recommendations = []
        for t in a_level:
            recommendations.append({
                'name': t['tool'],
                'category': t['category'],
                'traffic': f"{t['traffic']/1000:.0f}K",
                'growth': t['growth'],
                'reason': f'{t["category"]}领域增长标的'
            })

        return recommendations

    def _get_focus_tracks(self) -> list:
        """获取重点关注赛道"""
        return [
            {'priority': '⭐⭐⭐⭐⭐', 'name': 'AI编程平台', 'examples': 'Lovable, Windsurf', 'logic': '降低编程门槛，市场空间大'},
            {'priority': '⭐⭐⭐⭐⭐', 'name': 'AI Agent', 'examples': 'Manus, Emergent', 'logic': '新兴赛道，爆发潜力高'},
            {'priority': '⭐⭐⭐⭐', 'name': 'AI视频生成', 'examples': 'KlingAI, Higgsfield', 'logic': '差异化竞争'},
            {'priority': '⭐⭐⭐', 'name': 'AI音乐', 'examples': 'Suno', 'logic': '赛道成熟，增速放缓'}
        ]

    def _get_conclusions(self) -> list:
        """获取核心结论"""
        return [
            {'title': 'AI编程工具赛道正在发生代际更替', 'description': '，自然语言生成应用模式冲击传统IDE模式'},
            {'title': 'AI Agent赛道进入商业化验证阶段', 'description': '，付费转化数据证明市场需求真实存在'},
            {'title': '头部AI工具普遍增速放缓', 'description': '，市场进入存量竞争期，差异化和垂直场景将成为突破口'}
        ]

    def _convert_to_pdf(self, html_path: Path) -> Path:
        """使用 Playwright 将 HTML 转换为 PDF"""
        pdf_path = self.output_dir / f'report_{datetime.now().strftime("%Y%m%d")}.pdf'

        async def convert():
            try:
                from playwright.async_api import async_playwright
            except ImportError:
                print("警告: playwright 未安装，跳过 PDF 生成")
                print("安装方法: pip install playwright && playwright install chromium")
                return None

            async with async_playwright() as p:
                # 尝试使用系统 Chrome
                try:
                    browser = await p.chromium.launch(channel="chrome", headless=True)
                except:
                    # 回退到 chromium
                    browser = await p.chromium.launch(headless=True)

                page = await browser.new_page()
                await page.goto(f'file://{html_path.absolute()}')
                await page.wait_for_timeout(1000)  # 等待渲染

                await page.pdf(
                    path=str(pdf_path),
                    format='A4',
                    print_background=True,
                    margin={'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'}
                )

                await browser.close()
                return pdf_path

        result = asyncio.run(convert())
        if result:
            print(f"PDF 报告已生成: {result}")
        return result or html_path


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("流量分析报告生成工具")
        print("\n使用方法:")
        print("  python generate_report.py <csv_file> [output_dir]")
        print("\n参数说明:")
        print("  csv_file   - SEMrush 流量数据 CSV 文件路径")
        print("  output_dir - 输出目录（可选，默认为 ./outputs）")
        print("\n示例:")
        print("  python generate_report.py traffic_data.csv")
        print("  python generate_report.py traffic_data.csv ./reports")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('./outputs')

    print(f"正在分析数据: {csv_path}")
    print(f"输出目录: {output_dir}")

    # 1. 加载数据并分析
    print("\n[1/4] 加载并分析数据...")
    analyzer = TrafficAnalyzer(csv_path)
    metrics = analyzer.get_summary_metrics()
    print(f"  - 总流量: {metrics['total_traffic']:,}")
    print(f"  - 来源数: {metrics['total_sources']:,}")
    print(f"  - AI工具占比: {metrics['ai_ratio']:.1f}%")

    # 2. 生成图表
    print("\n[2/4] 生成可视化图表...")
    chart_gen = ChartGenerator(analyzer.df, output_dir)
    charts = chart_gen.generate_all()
    print(f"  - 已生成 {len(charts)} 个图表")

    # 3. 生成报告
    print("\n[3/4] 渲染报告模板...")
    report_gen = ReportGenerator(analyzer, output_dir)

    # 4. 导出 PDF
    print("\n[4/4] 导出 PDF 报告...")
    result = report_gen.generate(charts)

    print(f"\n完成！报告已保存到: {result}")
    print(f"图表目录: {output_dir}")


if __name__ == '__main__':
    main()
