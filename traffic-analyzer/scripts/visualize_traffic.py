#!/usr/bin/env python3
"""
流量数据可视化工具
生成各类图表帮助理解数据
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")


def load_data(filepath):
    """加载数据"""
    return pd.read_csv(filepath)


def plot_top_sources(df, top_n=20, output_file='top_sources.png'):
    """绘制流量 TOP 来源"""
    df_top = df.nlargest(top_n, 'traffic')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(df_top['target'], df_top['traffic'])
    
    # 根据增长率着色
    colors = ['green' if x > 0 else 'red' for x in df_top['traffic_diff']]
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax.set_xlabel('Traffic', fontsize=12)
    ax.set_title(f'Top {top_n} Traffic Sources', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    return output_file


def plot_growth_scatter(df, output_file='growth_scatter.png'):
    """绘制流量 vs 增长率散点图"""
    # 过滤掉流量太小的
    df_filtered = df[df['traffic'] > 10000].copy()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter = ax.scatter(
        df_filtered['traffic'], 
        df_filtered['traffic_diff'] * 100,
        alpha=0.6,
        s=50,
        c=df_filtered['traffic'],
        cmap='viridis'
    )
    
    ax.set_xlabel('Traffic Volume', fontsize=12)
    ax.set_ylabel('Growth Rate (%)', fontsize=12)
    ax.set_title('Traffic Volume vs Growth Rate', fontsize=14, fontweight='bold')
    ax.set_xscale('log')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    
    plt.colorbar(scatter, ax=ax, label='Traffic')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    return output_file


def plot_type_distribution(df, output_file='type_distribution.png'):
    """绘制流量类型分布"""
    type_stats = df.groupby('type')['traffic'].sum().sort_values(ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 饼图
    ax1.pie(type_stats.values, labels=type_stats.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Traffic Distribution by Type', fontsize=14, fontweight='bold')
    
    # 柱状图
    ax2.bar(range(len(type_stats)), type_stats.values)
    ax2.set_xticks(range(len(type_stats)))
    ax2.set_xticklabels(type_stats.index, rotation=45, ha='right')
    ax2.set_ylabel('Traffic', fontsize=12)
    ax2.set_title('Traffic Volume by Type', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    return output_file


def plot_ai_tools_comparison(df, output_file='ai_tools.png'):
    """专门绘制 AI 工具对比图"""
    ai_keywords = ['ai', 'gpt', 'claude', 'openai', 'anthropic', 'midjourney', 
                   'cursor', 'lovable', 'windsurf', 'suno', 'elevenlabs',
                   'runway', 'turboscribe', 'undetectable']
    
    ai_mask = (
        df['type'].str.contains('ai', case=False, na=False) |
        df['target'].str.contains('|'.join(ai_keywords), case=False, na=False)
    )
    
    df_ai = df[ai_mask & (df['traffic'] > 50000)].copy()
    df_ai = df_ai.nlargest(15, 'traffic')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.barh(df_ai['target'], df_ai['traffic'])
    
    # 根据增长率着色
    colors = []
    for diff in df_ai['traffic_diff']:
        if diff > 0.5:
            colors.append('darkgreen')
        elif diff > 0:
            colors.append('lightgreen')
        elif diff > -0.2:
            colors.append('orange')
        else:
            colors.append('red')
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax.set_xlabel('Traffic', fontsize=12)
    ax.set_title('Top AI Tools Traffic Comparison', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    return output_file


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python visualize_traffic.py <csv_file> [chart_type]")
        print("\nChart types:")
        print("  top_sources  - TOP 流量来源")
        print("  growth       - 流量增长散点图")
        print("  type_dist    - 流量类型分布")
        print("  ai_tools     - AI 工具对比")
        print("  all          - 生成所有图表")
        sys.exit(1)
    
    filepath = sys.argv[1]
    chart_type = sys.argv[2] if len(sys.argv) > 2 else 'all'
    
    df = load_data(filepath)
    
    # 默认输出到当前目录下的 outputs 文件夹
    output_dir = Path('./outputs')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_files = []
    
    if chart_type in ['top_sources', 'all']:
        output_file = output_dir / 'top_sources.png'
        plot_top_sources(df, output_file=str(output_file))
        generated_files.append(str(output_file))
    
    if chart_type in ['growth', 'all']:
        output_file = output_dir / 'growth_scatter.png'
        plot_growth_scatter(df, output_file=str(output_file))
        generated_files.append(str(output_file))
    
    if chart_type in ['type_dist', 'all']:
        output_file = output_dir / 'type_distribution.png'
        plot_type_distribution(df, output_file=str(output_file))
        generated_files.append(str(output_file))
    
    if chart_type in ['ai_tools', 'all']:
        output_file = output_dir / 'ai_tools.png'
        plot_ai_tools_comparison(df, output_file=str(output_file))
        generated_files.append(str(output_file))
    
    print(f"\nGenerated {len(generated_files)} charts")
    for f in generated_files:
        print(f"  - {f}")


if __name__ == '__main__':
    main()
