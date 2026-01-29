#!/usr/bin/env python3
"""
流量数据分析工具 - 用于分析 SEMrush 等流量数据源
支持多种分析模式：趋势分析、分类统计、增长排名等
"""

import pandas as pd
import json
import sys
from pathlib import Path


def load_traffic_data(filepath):
    """加载流量数据文件"""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_growth_leaders(df, top_n=20, min_traffic=50000):
    """
    分析高增长的流量来源
    
    Args:
        df: 数据框
        top_n: 返回前N个结果
        min_traffic: 最小流量阈值，过滤掉流量太小的来源
    """
    # 过滤掉流量太小的
    df_filtered = df[df['traffic'] >= min_traffic].copy()
    
    # 按增长率排序
    df_sorted = df_filtered.sort_values('traffic_diff', ascending=False)
    
    results = []
    for _, row in df_sorted.head(top_n).iterrows():
        results.append({
            'source': row['target'],
            'type': row['type'],
            'traffic': int(row['traffic']),
            'growth_rate': f"{row['traffic_diff'] * 100:.1f}%",
            'prev_traffic': int(row['prev_traffic']),
            'traffic_share': f"{row['traffic_share'] * 100:.2f}%"
        })
    
    return results


def analyze_by_type(df):
    """按流量类型分类统计"""
    type_stats = df.groupby('type').agg({
        'traffic': 'sum',
        'traffic_share': 'sum',
        'target': 'count'
    }).reset_index()
    
    type_stats.columns = ['type', 'total_traffic', 'total_share', 'source_count']
    type_stats = type_stats.sort_values('total_traffic', ascending=False)
    
    results = []
    for _, row in type_stats.iterrows():
        results.append({
            'type': row['type'],
            'total_traffic': int(row['total_traffic']),
            'share': f"{row['total_share'] * 100:.2f}%",
            'source_count': int(row['source_count'])
        })
    
    return results


def analyze_ai_tools(df, min_traffic=10000):
    """
    专门分析 AI 工具相关的流量
    识别包含 AI 相关关键词或分类的来源
    """
    ai_keywords = ['ai', 'gpt', 'claude', 'openai', 'anthropic', 'midjourney', 
                   'stable', 'diffusion', 'chatbot', 'assistant', 'copilot',
                   'cursor', 'lovable', 'windsurf', 'suno', 'elevenlabs',
                   'runway', 'turboscribe', 'undetectable']
    
    # 筛选 AI 相关的来源
    ai_mask = (
        df['type'].str.contains('ai', case=False, na=False) |
        df['target'].str.contains('|'.join(ai_keywords), case=False, na=False)
    )
    
    df_ai = df[ai_mask & (df['traffic'] >= min_traffic)].copy()
    df_ai = df_ai.sort_values('traffic', ascending=False)
    
    results = []
    for _, row in df_ai.iterrows():
        results.append({
            'tool': row['target'],
            'type': row['type'],
            'traffic': int(row['traffic']),
            'growth_rate': f"{row['traffic_diff'] * 100:.1f}%",
            'traffic_share': f"{row['traffic_share'] * 100:.3f}%"
        })
    
    return results


def analyze_market_segments(df, top_n_per_type=5):
    """分析各个细分市场的头部玩家"""
    segments = {}
    
    for type_name in df['type'].unique():
        df_type = df[df['type'] == type_name].copy()
        df_type = df_type.sort_values('traffic', ascending=False).head(top_n_per_type)
        
        segments[type_name] = []
        for _, row in df_type.iterrows():
            segments[type_name].append({
                'source': row['target'],
                'traffic': int(row['traffic']),
                'growth_rate': f"{row['traffic_diff'] * 100:.1f}%",
                'share': f"{row['traffic_share'] * 100:.3f}%"
            })
    
    return segments


def find_opportunities(df, 
                      min_traffic=100000, 
                      max_traffic=1000000,
                      min_growth=0.2):
    """
    寻找机会赛道：中等流量 + 高增长
    这些可能是值得关注的新兴市场
    """
    df_opportunity = df[
        (df['traffic'] >= min_traffic) &
        (df['traffic'] <= max_traffic) &
        (df['traffic_diff'] >= min_growth)
    ].copy()
    
    df_opportunity = df_opportunity.sort_values('traffic_diff', ascending=False)
    
    results = []
    for _, row in df_opportunity.iterrows():
        results.append({
            'source': row['target'],
            'type': row['type'],
            'traffic': int(row['traffic']),
            'growth_rate': f"{row['traffic_diff'] * 100:.1f}%",
            'market_position': 'emerging'
        })
    
    return results


def main():
    """主函数 - 支持命令行调用"""
    if len(sys.argv) < 3:
        print("Usage: python analyze_traffic.py <csv_file> <analysis_type>")
        print("\nAnalysis types:")
        print("  growth       - 高增长来源排行")
        print("  by_type      - 按类型统计")
        print("  ai_tools     - AI 工具分析")
        print("  segments     - 细分市场分析")
        print("  opportunities - 寻找机会赛道")
        print("  all          - 运行所有分析")
        sys.exit(1)
    
    filepath = sys.argv[1]
    analysis_type = sys.argv[2]
    
    df = load_traffic_data(filepath)
    
    result = {}
    
    if analysis_type in ['growth', 'all']:
        result['growth_leaders'] = analyze_growth_leaders(df)
    
    if analysis_type in ['by_type', 'all']:
        result['by_type'] = analyze_by_type(df)
    
    if analysis_type in ['ai_tools', 'all']:
        result['ai_tools'] = analyze_ai_tools(df)
    
    if analysis_type in ['segments', 'all']:
        result['segments'] = analyze_market_segments(df)
    
    if analysis_type in ['opportunities', 'all']:
        result['opportunities'] = find_opportunities(df)
    
    # 输出 JSON 格式结果
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
