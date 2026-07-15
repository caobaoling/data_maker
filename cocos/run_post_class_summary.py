# -*- coding:utf-8 -*-

import sys

import reset_mastery
import fetch_api
import get_summary

# 六种课型
COURSE_TYPES = {
    "100": "阅读",
    "101": "词汇",
    "102": "字母",
    "103": "自拼",
    "104": "嘉年华",
    "105": "对话",
}

# 支持的掌握程度
VALID_MASTERY = {
    "not_mastered",
    "moderate_mastery",
    "excellent_mastery",
    "perfect_mastery",
}


def main():
    """
    用法：

    python run_all.py all moderate_mastery

    python run_all.py 101 moderate_mastery

    python run_all.py 100,101,103 perfect_mastery
    """

    if len(sys.argv) != 3:
        print("""
==================== 用法 ====================

全部课型：

python run_all.py all moderate_mastery

单个课型：

python run_all.py 101 moderate_mastery

多个课型：

python run_all.py 100,101,103 moderate_mastery

mastery可选：

not_mastered
moderate_mastery
excellent_mastery
perfect_mastery

==============================================
""")
        sys.exit(1)

    appoint_arg = sys.argv[1].strip()
    mastery = sys.argv[2].strip()

    # 校验掌握程度
    if mastery not in VALID_MASTERY:
        print(f"错误：不支持的 mastery：{mastery}")
        sys.exit(1)

    # 解析appoint_id
    if appoint_arg.lower() == "all":

        appoint_ids = list(COURSE_TYPES.keys())

    else:

        appoint_ids = []

        for item in appoint_arg.split(","):

            item = item.strip()

            if item not in COURSE_TYPES:
                print(f"错误：不存在课型 {item}")
                sys.exit(1)

            appoint_ids.append(item)

    print()
    print("=" * 70)
    print("【步骤1】重置掌握程度")
    print("=" * 70)

    reset_mastery.run(
        appoint_ids=appoint_ids,
        mastery=mastery
    )

    print()
    print("=" * 70)
    print("【步骤2】获取推荐接口JSON")
    print("=" * 70)

    fetch_api.run(
        appoint_ids=appoint_ids,
        suffix=mastery
    )

    print()
    print("=" * 70)
    print("【步骤3】生成Excel")
    print("=" * 70)

    get_summary.run(
        suffix=mastery
    )

    print()
    print("=" * 70)
    print("全部执行完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()