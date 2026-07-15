import json
import sys
from pathlib import Path
from openpyxl import Workbook
from datetime import datetime
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

TARGET_TEMPLATE_CODES = {
    "SUMMARY_V1",
    "SUMMARY_PERSON",
    "PRE_POST_SETTLE",
    "SUMMARY_V2",
    "SUMMARY_PERFECT",
}

fills = [
    PatternFill(fill_type="solid", fgColor="DDEBF7"),
    PatternFill(fill_type="solid", fgColor="E2F0D9"),
    PatternFill(fill_type="solid", fgColor="FFF2CC"),
    PatternFill(fill_type="solid", fgColor="FCE4D6"),
    PatternFill(fill_type="solid", fgColor="E4DFEC"),
    PatternFill(fill_type="solid", fgColor="D9EAD3"),
    PatternFill(fill_type="solid", fgColor="F4CCCC"),
    PatternFill(fill_type="solid", fgColor="D0E0E3"),
]

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "6种课型的接口返回json"

        
def run(suffix=None):
    """
    suffix:
        None -> 处理所有json
        moderate_mastery -> 只处理 *moderate_mastery.json
    """
   

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if suffix:
        json_files = sorted(INPUT_DIR.glob(f"*{suffix}.json"))
        output_file = BASE_DIR / f"{suffix}_sunchuan_result_{timestamp}.xlsx"
    else:
        json_files = sorted(INPUT_DIR.glob("*.json"))
        output_file = BASE_DIR / f"sunchuan_result_{timestamp}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "result"

    ws.append([
        "文件名",
        "template_code",
        "knowledge_key",
        "knowledge_name",
        "knowledge_id",
        "knowledge_type",
        "OUTPUT-SPEAK",
        "INPUT-LISTEN"
    ])

    # 根据suffix决定读取哪些文件
    if suffix:
        json_files = sorted(INPUT_DIR.glob(f"*{suffix}.json"))
    else:
        json_files = sorted(INPUT_DIR.glob("*.json"))

    if not json_files:
        print(f"未找到符合条件的json文件 suffix={suffix}")
        return

    for json_file in json_files:

        print(f"处理：{json_file.name}")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data.get("res", []):

            if item.get("template_code") not in TARGET_TEMPLATE_CODES:
                continue

            template_code = item.get("template_code")

            data_obj = item.get("data") or {}
            knowledges = data_obj.get("knowledges")

            if not knowledges:
                ws.append([
                    json_file.stem,
                    template_code,
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ])
                continue

            for knowledge_key, value in knowledges.items():

                if knowledge_key == "video":
                    continue

                if not value:
                    continue

                if isinstance(value, list):

                    for x in value:
                        ability = x.get("ability_level") or {}

                        ws.append([
                            json_file.stem,
                            template_code,
                            knowledge_key,
                            x.get("knowledge_name"),
                            x.get("knowledge_id"),
                            x.get("knowledge_type"),
                            ability.get("OUTPUT-SPEAK"),
                            ability.get("INPUT-LISTEN"),
                        ])

                elif isinstance(value, dict):

                    ability = value.get("ability_level") or {}

                    ws.append([
                        json_file.stem,
                        template_code,
                        knowledge_key,
                        value.get("knowledge_name"),
                        value.get("knowledge_id"),
                        value.get("knowledge_type"),
                        ability.get("OUTPUT-SPEAK"),
                        ability.get("INPUT-LISTEN"),
                    ])

    # 自动列宽
    for column_cells in ws.columns:

        max_length = 0
        column = column_cells[0].column

        for cell in column_cells:

            if cell.value is not None:
                value = str(cell.value)
                length = sum(2 if ord(ch) > 127 else 1 for ch in value)
                max_length = max(max_length, length)

        ws.column_dimensions[get_column_letter(column)].width = min(max_length + 2, 60)

    # 相同文件名使用同一种颜色
    file_fill_map = {}
    fill_index = 0

    for row in ws.iter_rows(min_row=2):

        file_name = row[0].value

        if file_name not in file_fill_map:
            file_fill_map[file_name] = fills[fill_index % len(fills)]
            fill_index += 1

        fill = file_fill_map[file_name]

        for cell in row:
            cell.fill = fill

    wb.save(output_file)

    print("=" * 60)
    print(f"处理完成，共处理 {len(json_files)} 个文件")
    print(f"Excel已生成：{output_file}")
    print("=" * 60)


if __name__ == "__main__":

    suffix = sys.argv[1] if len(sys.argv) > 1 else None

    run(suffix)