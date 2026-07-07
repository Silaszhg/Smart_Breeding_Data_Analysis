"""
数据集划分：训练集 / 测试集 / 验证集
=======================================
分层抽样，确保三个数据集中 最终结局（存栏/出售/死亡）的比例一致
比例：60% 训练 / 20% 测试 / 20% 验证
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split

# ============================================================
# 0. 设置
# ============================================================
DATA_DIR = "./data/processed"
OUTPUT_DIR = "./data/split"
os.makedirs(OUTPUT_DIR, exist_ok=True)

RANDOM_SEED = 42
TRAIN_RATIO = 0.6
TEST_RATIO = 0.2
VAL_RATIO = 0.2

# ============================================================
# 1. 加载宽表
# ============================================================
df = pd.read_csv(os.path.join(DATA_DIR, "牛只全生命周期分析宽表.csv"))
print(f"\n{'='*55}")
print(f"📊 数据集划分")
print(f"{'='*55}")
print(f"原始数据: {len(df)} 行 × {len(df.columns)} 列\n")

# ============================================================
# 2. 分层抽样划分
# ============================================================
if '最终结局' in df.columns:
    stratify_col = df['最终结局']
    print(f"分层依据: 最终结局")
    for k, v in df['最终结局'].value_counts().items():
        print(f"  {k}: {v} 头 ({v/len(df)*100:.1f}%)")
else:
    stratify_col = None
    print(f"⚠️ 未找到 '最终结局' 列，使用随机划分")

# 第一步：分出训练集 (60%)，剩余 40%
df_train, df_temp = train_test_split(
    df,
    test_size=(1 - TRAIN_RATIO),
    stratify=stratify_col,
    random_state=RANDOM_SEED
)

# 第二步：剩余 40% 均分给测试集和验证集 (各 20%)
if stratify_col is not None:
    stratify_temp = df_temp['最终结局']
else:
    stratify_temp = None

df_test, df_val = train_test_split(
    df_temp,
    test_size=0.5,  # 40% 的一半 = 20%
    stratify=stratify_temp,
    random_state=RANDOM_SEED
)

# ============================================================
# 3. 验证划分结果
# ============================================================
print(f"\n{'─'*55}")
print(f"划分结果:")
print(f"{'─'*55}")
print(f"  训练集: {len(df_train):5d} 行 ({len(df_train)/len(df)*100:.0f}%)")
print(f"  测试集: {len(df_test):5d} 行 ({len(df_test)/len(df)*100:.0f}%)")
print(f"  验证集: {len(df_val):5d} 行 ({len(df_val)/len(df)*100:.0f}%)")
print(f"  合计:   {len(df_train)+len(df_test)+len(df_val):5d} 行")

# 验证分层效果
if '最终结局' in df.columns:
    print(f"\n{'─'*55}")
    print(f"分层效果验证（最终结局占比）:")
    print(f"{'─'*55}")
    print(f"  {'':12s} {'原始数据':>10s} {'训练集':>10s} {'测试集':>10s} {'验证集':>10s}")
    for outcome in df['最终结局'].unique():
        orig = df['最终结局'].value_counts(normalize=True)[outcome] * 100
        train = df_train['最终结局'].value_counts(normalize=True).get(outcome, 0) * 100
        test = df_test['最终结局'].value_counts(normalize=True).get(outcome, 0) * 100
        val = df_val['最终结局'].value_counts(normalize=True).get(outcome, 0) * 100
        print(f"  {outcome:12s} {orig:9.1f}% {train:9.1f}% {test:9.1f}% {val:9.1f}%")

# ============================================================
# 4. 保存
# ============================================================
train_path = os.path.join(OUTPUT_DIR, "train.csv")
test_path = os.path.join(OUTPUT_DIR, "test.csv")
val_path = os.path.join(OUTPUT_DIR, "val.csv")

df_train.to_csv(train_path, index=False, encoding='utf-8-sig')
df_test.to_csv(test_path, index=False, encoding='utf-8-sig')
df_val.to_csv(val_path, index=False, encoding='utf-8-sig')

print(f"\n{'─'*55}")
print(f"✅ 已保存:")
print(f"   训练集 → {train_path}")
print(f"   测试集 → {test_path}")
print(f"   验证集 → {val_path}")
print(f"{'='*55}")