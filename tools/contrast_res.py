import pandas as pd

# 读取两个CSV文件
df1 = pd.read_csv('../cache/personal.csv')
df2 = pd.read_csv('../cache/other.csv')

# 确保列名一致
df1.columns = ['problem_id', 'result']
df2.columns = ['problem_id', 'result']

# 使用outer合并，取problem_id的并集
merged_df = pd.merge(df1, df2, on='problem_id', how='outer', suffixes=('_file1', '_file2'))

# 标记缺失值
merged_df['result_file1'] = merged_df['result_file1'].fillna('Missing in file1')
merged_df['result_file2'] = merged_df['result_file2'].fillna('Missing in file2')

# 找出result不同的行
diff_df = merged_df[merged_df['result_file1'] != merged_df['result_file2']]

# 打印出result不同的problem_id和两个result
for index, row in diff_df.iterrows():
    print(f"problem_id: {row['problem_id']}, result_file1: {row['result_file1']}, result_file2: {row['result_file2']}")

# 将problem_id单独保存为CSV文件
diff_df[['problem_id']].to_csv('../contrast/diff_problem_ids.csv', index=False)