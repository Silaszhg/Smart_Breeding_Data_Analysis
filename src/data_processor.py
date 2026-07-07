import pandas as pd
import os
import glob
from pathlib import Path

def clean_and_convert_excel_to_csv(raw_dir, processed_dir):
    """
    读取 raw 目录下的所有 Excel 文件，进行基础清洗，并转换为 CSV 保存到 processed 目录。
    """
    # 确保输出目录存在
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    
    # 获取所有的 .xlsx 文件路径
    excel_files = glob.glob(os.path.join(raw_dir, "*.xlsx"))
    
    if not excel_files:
        print(f"在 {raw_dir} 目录下没有找到任何 Excel 文件。请检查文件路径。")
        return

    print(f"找到 {len(excel_files)} 个 Excel 文件，开始处理...\n")
    print("-" * 50)

    for file_path in excel_files:
        # 获取文件名（不含后缀）
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]
        
        # 为了规范化，去除文件名中可能存在的特殊字符或多余空格（例如 "喂养分组表 —"）
        clean_base_name = base_name.replace("—", "").strip()
        csv_file_name = f"{clean_base_name}.csv"
        csv_file_path = os.path.join(processed_dir, csv_file_name)
        
        try:
            print(f"正在处理: {file_name}")
            
            # 1. 读取 Excel 文件
            # 使用 openpyxl 引擎读取 xlsx
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # --- 基础数据清洗开始 ---
            
            # 2. 去除完全为空的行和列
            df.dropna(how='all', inplace=True)
            df.dropna(axis=1, how='all', inplace=True)
            
            # 3. 清理列名中的前后空格和换行符（Excel 中常见的录入问题）
            df.columns = df.columns.str.strip().str.replace('\n', '')
            
            # 4. 将所有文本类型列的数据去除前后空格
            # 针对如"智能耳标编号"、"用药名称"等关键字段的潜在格式问题
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
                
            # --- 基础数据清洗结束 ---
            
            # 5. 导出为 CSV
            # encoding='utf-8-sig' 非常重要，它可以在 Windows 的 Excel 中正确显示中文而不乱码
            df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
            
            print(f"  --> 成功导出至: {csv_file_name} (共 {df.shape[0]} 行, {df.shape[1]} 列)")
            
        except Exception as e:
            print(f"  [错误] 处理 {file_name} 时发生错误: {e}")
            
    print("-" * 50)
    print("所有文件转换与基础清洗完成！")

# 设定输入和输出目录
# 假设你在项目根目录运行此脚本
RAW_DATA_DIR = "./data/raw"
PROCESSED_DATA_DIR = "./data/processed"

if __name__ == "__main__":
    clean_and_convert_excel_to_csv(RAW_DATA_DIR, PROCESSED_DATA_DIR)