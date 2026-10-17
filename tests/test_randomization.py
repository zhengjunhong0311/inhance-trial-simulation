"""Unit tests for the randomization module."""
import pandas as pd
import pytest
import sys
import os

# 确保能导入 src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.randomization import stratified_block_randomization

def test_total_sample_size():
    """验证总样本量是否正确"""
    df = stratified_block_randomization(seed=1128)
    assert len(df) == 840, "Total sample size should be 840"

def test_group_balance():
    """验证 7 个治疗组是否每组 120 例"""
    df = stratified_block_randomization(seed=1128)
    counts = df["GroupLabel"].value_counts()
    assert (counts == 120).all(), "Each group must have exactly 120 subjects"

def test_strata_balance():
    """验证分层因素（吸烟状态）是否每层 420 例"""
    df = stratified_block_randomization(seed=1128)
    counts = df["SmokingStatus"].value_counts()
    assert (counts == 420).all(), "Each stratum must have exactly 420 subjects"

def test_block_balance():
    """验证每个区组内各治疗组的人数是否相等（1:1:1:1:1:1:1）"""
    df = stratified_block_randomization(seed=1128)
    for block_id, sub_df in df.groupby("BlockID"):
        counts = sub_df["GroupCode"].value_counts()
        assert counts.nunique() == 1, f"Block {block_id} is not balanced"

def test_reproducibility():
    """验证固定 seed 是否能生成完全相同的随机表"""
    df1 = stratified_block_randomization(seed=1128)
    df2 = stratified_block_randomization(seed=1128)
    pd.testing.assert_frame_equal(df1, df2)
