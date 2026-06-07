#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RepoInsight-AI 单元测试
"""

import unittest
from unittest.mock import patch, MagicMock
from repoinsight import GitHubAnalyzer, RepoMetrics


class TestGitHubAnalyzer(unittest.TestCase):
    """测试GitHub分析器"""
    
    def setUp(self):
        """测试前准备"""
        self.analyzer = GitHubAnalyzer(token="test_token")
    
    def test_parse_repo_url(self):
        """测试URL解析"""
        # 测试HTTPS URL
        owner, repo = self.analyzer.parse_repo_url("https://github.com/owner/repo")
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")
        
        # 测试HTTP URL
        owner, repo = self.analyzer.parse_repo_url("http://github.com/owner/repo")
        self.assertEqual(owner, "owner")
        self.assertEqual(repo, "repo")
    
    def test_parse_repo_url_invalid(self):
        """测试无效URL"""
        with self.assertRaises(ValueError):
            self.analyzer.parse_repo_url("invalid_url")
    
    @patch('repoinsight.requests.get')
    def test_get_repo_info_success(self, mock_get):
        """测试获取仓库信息成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'test-repo',
            'full_name': 'owner/test-repo',
            'description': 'Test repository',
            'language': 'Python',
            'stargazers_count': 100,
            'forks_count': 20,
            'open_issues_count': 5,
            'watchers_count': 100,
            'created_at': '2023-01-01T00:00:00Z',
            'updated_at': '2023-06-01T00:00:00Z',
            'pushed_at': '2023-06-01T00:00:00Z',
            'size': 1024,
            'license': {'name': 'MIT License'},
            'topics': ['python', 'cli']
        }
        mock_response.headers = {'X-RateLimit-Remaining': '4999'}
        mock_get.return_value = mock_response
        
        metrics = self.analyzer.get_repo_info('owner', 'test-repo')
        
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics.name, 'test-repo')
        self.assertEqual(metrics.stars, 100)
        self.assertEqual(metrics.language, 'Python')
    
    @patch('repoinsight.requests.get')
    def test_get_repo_info_not_found(self, mock_get):
        """测试仓库不存在"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.headers = {'X-RateLimit-Remaining': '4999'}
        mock_get.return_value = mock_response
        
        metrics = self.analyzer.get_repo_info('owner', 'non-existent')
        
        self.assertIsNone(metrics)
    
    def test_calculate_metrics(self):
        """测试指标计算"""
        metrics = RepoMetrics(
            name='test',
            full_name='owner/test',
            description='Test',
            language='Python',
            stars=120,
            forks=10,
            open_issues=5,
            watchers=120,
            created_at='2023-01-01T00:00:00Z',
            updated_at='2023-06-01T00:00:00Z',
            pushed_at='2023-06-01T00:00:00Z',
            size_kb=1024,
            license='MIT License',
            topics=['python']
        )
        
        stats = {
            'contributors_count': 3,
            'top_contributor': 'user1'
        }
        
        result = self.analyzer.calculate_metrics(metrics, stats)
        
        self.assertGreater(result.star_velocity, 0)
        self.assertGreater(result.activity_score, 0)
        self.assertGreater(result.community_health, 0)
        self.assertIsNotNone(result.maintenance_status)


class TestRepoMetrics(unittest.TestCase):
    """测试RepoMetrics数据类"""
    
    def test_metrics_creation(self):
        """测试创建指标对象"""
        metrics = RepoMetrics(
            name='test-repo',
            full_name='owner/test-repo',
            description='Test',
            language='Python',
            stars=100,
            forks=20,
            open_issues=5,
            watchers=100,
            created_at='2023-01-01T00:00:00Z',
            updated_at='2023-06-01T00:00:00Z',
            pushed_at='2023-06-01T00:00:00Z',
            size_kb=1024,
            license='MIT',
            topics=['python', 'cli']
        )
        
        self.assertEqual(metrics.name, 'test-repo')
        self.assertEqual(metrics.stars, 100)
        self.assertEqual(len(metrics.topics), 2)


if __name__ == '__main__':
    unittest.main()
