#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RepoInsight-AI 🤖
AI驱动的GitHub仓库智能分析工具
深度洞察代码质量、社区健康度与发展趋势
"""

import os
import sys
import json
import time
import asyncio
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from dateutil import parser as date_parser

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.tree import Tree
from rich import box

console = Console()


@dataclass
class RepoMetrics:
    """仓库核心指标"""
    name: str
    full_name: str
    description: str
    language: str
    stars: int
    forks: int
    open_issues: int
    watchers: int
    created_at: str
    updated_at: str
    pushed_at: str
    size_kb: int
    license: str
    topics: List[str]
    
    # 计算指标
    star_velocity: float = 0.0  # Star增长速度
    issue_resolution_rate: float = 0.0  # Issue解决率
    community_health: float = 0.0  # 社区健康度
    activity_score: float = 0.0  # 活跃度评分
    maintenance_status: str = "unknown"  # 维护状态


class GitHubAnalyzer:
    """GitHub仓库分析器"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'RepoInsight-AI/1.0'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        
        self.base_url = 'https://api.github.com'
        self.rate_limit_remaining = 5000
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """发送API请求"""
        url = f'{self.base_url}{endpoint}'
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                console.print(f"[red]❌ 仓库未找到: {endpoint}[/red]")
                return None
            elif response.status_code == 403:
                console.print(f"[red]❌ API速率限制已用完，请稍后再试或使用Token[/red]")
                return None
            else:
                console.print(f"[red]❌ API请求失败: {response.status_code}[/red]")
                return None
        except requests.RequestException as e:
            console.print(f"[red]❌ 网络请求错误: {e}[/red]")
            return None
    
    def parse_repo_url(self, url: str) -> Tuple[str, str]:
        """解析GitHub仓库URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return path_parts[0], path_parts[1]
        raise ValueError("无效的GitHub仓库URL")
    
    def get_repo_info(self, owner: str, repo: str) -> Optional[RepoMetrics]:
        """获取仓库基本信息"""
        data = self._make_request(f'/repos/{owner}/{repo}')
        if not data:
            return None
        
        metrics = RepoMetrics(
            name=data.get('name', ''),
            full_name=data.get('full_name', ''),
            description=data.get('description', '无描述') or '无描述',
            language=data.get('language', '未知') or '未知',
            stars=data.get('stargazers_count', 0),
            forks=data.get('forks_count', 0),
            open_issues=data.get('open_issues_count', 0),
            watchers=data.get('watchers_count', 0),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', ''),
            pushed_at=data.get('pushed_at', ''),
            size_kb=data.get('size', 0),
            license=data.get('license', {}).get('name', '无') if data.get('license') else '无',
            topics=data.get('topics', [])
        )
        
        return metrics
    
    def get_repo_stats(self, owner: str, repo: str) -> Dict:
        """获取仓库统计信息"""
        stats = {}
        
        # 获取贡献者信息
        contributors = self._make_request(f'/repos/{owner}/{repo}/contributors?per_page=10')
        if contributors:
            stats['contributors_count'] = len(contributors)
            stats['top_contributor'] = contributors[0].get('login', '未知') if contributors else '无'
        else:
            stats['contributors_count'] = 0
            stats['top_contributor'] = '无'
        
        # 获取最近提交
        commits = self._make_request(f'/repos/{owner}/{repo}/commits?per_page=5')
        if commits:
            stats['recent_commits'] = [
                {
                    'message': c.get('commit', {}).get('message', '')[:50],
                    'author': c.get('commit', {}).get('author', {}).get('name', '未知'),
                    'date': c.get('commit', {}).get('author', {}).get('date', '')
                }
                for c in commits[:5]
            ]
        else:
            stats['recent_commits'] = []
        
        # 获取Release信息
        releases = self._make_request(f'/repos/{owner}/{repo}/releases?per_page=5')
        if releases:
            stats['releases_count'] = len(releases)
            stats['latest_release'] = releases[0].get('tag_name', '无') if releases else '无'
            stats['latest_release_date'] = releases[0].get('published_at', '') if releases else ''
        else:
            stats['releases_count'] = 0
            stats['latest_release'] = '无'
            stats['latest_release_date'] = ''
        
        return stats
    
    def calculate_metrics(self, metrics: RepoMetrics, stats: Dict) -> RepoMetrics:
        """计算高级指标"""
        try:
            created = date_parser.parse(metrics.created_at)
            pushed = date_parser.parse(metrics.pushed_at)
            now = datetime.now(created.tzinfo)
            
            # 计算Star增长速度 (每月)
            age_months = max((now - created).days / 30, 1)
            metrics.star_velocity = round(metrics.stars / age_months, 2)
            
            # 计算活跃度评分 (0-100)
            days_since_push = (now - pushed).days
            if days_since_push < 7:
                activity_score = 100
            elif days_since_push < 30:
                activity_score = 80
            elif days_since_push < 90:
                activity_score = 60
            elif days_since_push < 180:
                activity_score = 40
            else:
                activity_score = 20
            
            # 根据Issue和Fork调整
            if metrics.open_issues > 0:
                activity_score = min(100, activity_score + 10)
            if metrics.forks > 0:
                activity_score = min(100, activity_score + 10)
            
            metrics.activity_score = activity_score
            
            # 维护状态
            if days_since_push < 30:
                metrics.maintenance_status = "🟢 积极维护"
            elif days_since_push < 90:
                metrics.maintenance_status = "🟡 正常维护"
            elif days_since_push < 180:
                metrics.maintenance_status = "🟠 维护缓慢"
            else:
                metrics.maintenance_status = "🔴 可能弃用"
            
            # 社区健康度
            health = 50
            if stats.get('contributors_count', 0) > 5:
                health += 20
            elif stats.get('contributors_count', 0) > 1:
                health += 10
            
            if metrics.stars > 1000:
                health += 15
            elif metrics.stars > 100:
                health += 10
            
            if metrics.license != '无':
                health += 10
            
            if metrics.topics:
                health += 5
            
            metrics.community_health = min(100, health)
            
        except Exception as e:
            console.print(f"[yellow]⚠️ 计算指标时出错: {e}[/yellow]")
        
        return metrics
    
    def analyze_repo(self, repo_input: str) -> Optional[Dict]:
        """分析仓库主方法"""
        try:
            if 'github.com' in repo_input:
                owner, repo = self.parse_repo_url(repo_input)
            else:
                parts = repo_input.split('/')
                if len(parts) == 2:
                    owner, repo = parts
                else:
                    console.print("[red]❌ 请提供正确的格式: owner/repo 或 GitHub URL[/red]")
                    return None
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                
                task1 = progress.add_task("🔍 获取仓库基本信息...", total=None)
                metrics = self.get_repo_info(owner, repo)
                if not metrics:
                    return None
                progress.update(task1, completed=True)
                
                task2 = progress.add_task("📊 获取统计数据...", total=None)
                stats = self.get_repo_stats(owner, repo)
                progress.update(task2, completed=True)
                
                task3 = progress.add_task("🧮 计算高级指标...", total=None)
                metrics = self.calculate_metrics(metrics, stats)
                progress.update(task3, completed=True)
            
            return {
                'metrics': asdict(metrics),
                'stats': stats
            }
            
        except Exception as e:
            console.print(f"[red]❌ 分析失败: {e}[/red]")
            return None


def display_results(data: Dict):
    """显示分析结果"""
    metrics = data['metrics']
    stats = data['stats']
    
    console.print("\n")
    console.print(Panel.fit(
        f"[bold cyan]📊 {metrics['full_name']}[/bold cyan]\n"
        f"[dim]{metrics['description']}[/dim]",
        title="🤖 RepoInsight-AI 分析报告",
        border_style="cyan"
    ))
    
    # 基本信息表格
    basic_table = Table(title="📋 基本信息", box=box.ROUNDED)
    basic_table.add_column("指标", style="cyan", no_wrap=True)
    basic_table.add_column("数值", style="white")
    
    basic_table.add_row("🏷️ 名称", metrics['name'])
    basic_table.add_row("💻 主要语言", metrics['language'])
    basic_table.add_row("📄 开源协议", metrics['license'])
    basic_table.add_row("📦 仓库大小", f"{metrics['size_kb']} KB")
    basic_table.add_row("🏷️ 标签", ", ".join(metrics['topics'][:5]) if metrics['topics'] else '无')
    basic_table.add_row("👥 贡献者", str(stats.get('contributors_count', 0)))
    basic_table.add_row("🏆 主要贡献者", stats.get('top_contributor', '无'))
    
    console.print(basic_table)
    
    # 社区指标表格
    community_table = Table(title="📈 社区指标", box=box.ROUNDED)
    community_table.add_column("指标", style="magenta", no_wrap=True)
    community_table.add_column("数值", style="white")
    community_table.add_column("评级", style="green")
    
    stars = metrics['stars']
    star_rating = "⭐⭐⭐" if stars > 1000 else "⭐⭐" if stars > 100 else "⭐"
    
    forks = metrics['forks']
    fork_rating = "🔥🔥🔥" if forks > 500 else "🔥🔥" if forks > 50 else "🔥"
    
    community_table.add_row("⭐ Stars", f"{stars:,}", star_rating)
    community_table.add_row("🍴 Forks", f"{forks:,}", fork_rating)
    community_table.add_row("📮 Open Issues", f"{metrics['open_issues']:,}", "")
    community_table.add_row("👀 Watchers", f"{metrics['watchers']:,}", "")
    community_table.add_row("🚀 Star增速", f"{metrics['star_velocity']}/月", "")
    community_table.add_row("📦 Releases", str(stats.get('releases_count', 0)), "")
    community_table.add_row("🏷️ 最新版本", stats.get('latest_release', '无'), "")
    
    console.print(community_table)
    
    # 健康度评估
    health_table = Table(title="🏥 健康度评估", box=box.ROUNDED)
    health_table.add_column("指标", style="yellow", no_wrap=True)
    health_table.add_column("评分", style="white")
    health_table.add_column("状态", style="green")
    
    activity = metrics['activity_score']
    activity_status = "🟢 优秀" if activity >= 80 else "🟡 良好" if activity >= 60 else "🟠 一般" if activity >= 40 else "🔴 较低"
    
    health = metrics['community_health']
    health_status = "🟢 健康" if health >= 80 else "🟡 良好" if health >= 60 else "🟠 一般" if health >= 40 else "🔴 需关注"
    
    health_table.add_row("📊 活跃度评分", f"{activity}/100", activity_status)
    health_table.add_row("❤️ 社区健康度", f"{health}/100", health_status)
    health_table.add_row("🔧 维护状态", metrics['maintenance_status'], "")
    
    console.print(health_table)
    
    # 最近提交
    if stats.get('recent_commits'):
        console.print("\n[bold cyan]📝 最近提交[/bold cyan]")
        for i, commit in enumerate(stats['recent_commits'][:3], 1):
            date_str = commit['date'][:10] if commit['date'] else '未知'
            console.print(f"  {i}. [{date_str}] {commit['author']}: {commit['message']}")
    
    # 综合建议
    console.print("\n")
    suggestions = []
    
    if metrics['activity_score'] < 40:
        suggestions.append("⚠️ 项目活跃度较低，建议关注是否有替代方案")
    if metrics['community_health'] < 50:
        suggestions.append("⚠️ 社区健康度一般，贡献者较少")
    if metrics['maintenance_status'].startswith("🔴"):
        suggestions.append("🚨 项目可能已停止维护，谨慎用于生产环境")
    if metrics['license'] == '无':
        suggestions.append("⚠️ 项目未指定开源协议，使用时需注意法律风险")
    
    if not suggestions:
        suggestions.append("✅ 项目整体状况良好，适合使用或贡献")
    
    console.print(Panel(
        "\n".join(suggestions),
        title="💡 智能建议",
        border_style="green"
    ))
    
    console.print(f"\n[dim]💡 API剩余请求: {analyzer.rate_limit_remaining}/5000[/dim]")


# 全局分析器实例
analyzer = GitHubAnalyzer()


@click.group()
@click.version_option(version="1.0.0", prog_name="RepoInsight-AI")
def cli():
    """🤖 RepoInsight-AI - AI驱动的GitHub仓库智能分析工具"""
    pass


@cli.command()
@click.argument('repo')
@click.option('--token', '-t', help='GitHub Personal Access Token')
def analyze(repo: str, token: Optional[str]):
    """分析指定GitHub仓库
    
    REPO 可以是 owner/repo 格式或完整GitHub URL
    
    示例:
        repoinsight analyze facebook/react
        repoinsight analyze https://github.com/torvalds/linux
    """
    global analyzer
    if token:
        analyzer = GitHubAnalyzer(token)
    
    console.print(f"[cyan]🔍 正在分析仓库: {repo}[/cyan]")
    result = analyzer.analyze_repo(repo)
    
    if result:
        display_results(result)
    else:
        sys.exit(1)


@cli.command()
@click.argument('language')
@click.option('--limit', '-n', default=10, help='显示数量 (默认: 10)')
@click.option('--token', '-t', help='GitHub Personal Access Token')
def trending(language: str, limit: int, token: Optional[str]):
    """查看指定语言的热门仓库
    
    LANGUAGE 是编程语言名称，如 Python, JavaScript, Go 等
    
    示例:
        repoinsight trending Python
        repoinsight trending JavaScript -n 20
    """
    global analyzer
    if token:
        analyzer = GitHubAnalyzer(token)
    
    console.print(f"[cyan]🔥 正在获取 {language} 热门仓库...[/cyan]")
    
    data = analyzer._make_request(
        '/search/repositories',
        {
            'q': f'language:{language}',
            'sort': 'stars',
            'order': 'desc',
            'per_page': limit
        }
    )
    
    if not data or 'items' not in data:
        console.print("[red]❌ 获取热门仓库失败[/red]")
        sys.exit(1)
    
    table = Table(title=f"🔥 {language} 热门仓库 Top {limit}", box=box.ROUNDED)
    table.add_column("排名", style="cyan", justify="center")
    table.add_column("仓库", style="white")
    table.add_column("Stars", style="yellow", justify="right")
    table.add_column("Forks", style="magenta", justify="right")
    table.add_column("描述", style="dim")
    
    for i, repo in enumerate(data['items'], 1):
        table.add_row(
            str(i),
            repo['full_name'],
            f"⭐ {repo['stargazers_count']:,}",
            f"🍴 {repo['forks_count']:,}",
            (repo['description'] or '无描述')[:40]
        )
    
    console.print(table)


@cli.command()
@click.option('--token', '-t', help='GitHub Personal Access Token')
def config(token: Optional[str]):
    """配置GitHub Token
    
    设置环境变量 GITHUB_TOKEN 即可持久化配置
    
    示例:
        export GITHUB_TOKEN=your_token_here
        repoinsight config
    """
    if token:
        console.print("[green]✅ Token已提供[/green]")
    else:
        current = os.getenv('GITHUB_TOKEN')
        if current:
            masked = current[:4] + '*' * (len(current) - 8) + current[-4:]
            console.print(f"[green]✅ 当前Token: {masked}[/green]")
            console.print("[dim]💡 Token来自环境变量 GITHUB_TOKEN[/dim]")
        else:
            console.print("[yellow]⚠️ 未找到GitHub Token[/yellow]")
            console.print("[dim]💡 请设置环境变量: export GITHUB_TOKEN=your_token[/dim]")
            console.print("[dim]💡 获取Token: https://github.com/settings/tokens[/dim]")


@cli.command()
def version():
    """显示版本信息"""
    console.print(Panel.fit(
        "[bold cyan]RepoInsight-AI[/bold cyan] v1.0.0\n"
        "[dim]🤖 AI驱动的GitHub仓库智能分析工具[/dim]\n"
        "[dim]作者: gitstq[/dim]\n"
        "[dim]协议: MIT[/dim]",
        title="版本信息",
        border_style="cyan"
    ))


if __name__ == '__main__':
    cli()
