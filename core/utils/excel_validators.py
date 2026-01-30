import re
import pandas as pd

INDEX_PATTERN = re.compile(r'^\d+(\.\d+)*$')


def validate_work_items_excel(df):
    errors = []
    index_set = set()

    for i, row in df.iterrows():
        row_num = i + 2  # Excel bắt đầu từ dòng 2

        # --- CHỈ MỤC ---
        index_raw = row.get('Chỉ mục')

        if pd.isna(index_raw):
            errors.append(f"Dòng {row_num}: Chỉ mục bị trống")
            continue

        index_code = str(index_raw).rstrip('.0').strip()

        if not INDEX_PATTERN.match(index_code):
            errors.append(f"Dòng {row_num}: Chỉ mục '{index_code}' sai format")
            continue

        if index_code in index_set:
            errors.append(f"Dòng {row_num}: Trùng chỉ mục '{index_code}'")

        index_set.add(index_code)

        # --- TÊN CÔNG VIỆC ---
        name = row.get('Tên công việc')

        if pd.isna(name) or not str(name).strip():
            errors.append(f"Dòng {row_num}: Tên công việc bị trống")

        # --- KHỐI LƯỢNG ---
        qty = row.get('Khối lượng')

        if not pd.isna(qty):
            try:
                qty = float(qty)
                if qty < 0:
                    errors.append(f"Dòng {row_num}: Khối lượng < 0")
            except ValueError:
                errors.append(f"Dòng {row_num}: Khối lượng không phải số")

        # --- KIỂM TRA CHA ---
        if '.' in index_code:
            parent_index = '.'.join(index_code.split('.')[:-1])
            if parent_index not in index_set:
                errors.append(
                    f"Dòng {row_num}: Chưa có chỉ mục cha '{parent_index}'"
                )

    return errors
