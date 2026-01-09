# 文件: elf_level_config
# 作者: bao0
# 创建日期: 2024/12/6
# 描述: 这是一个变更精灵级别的配置文件
class ElfLevelData:
    """精灵等级数据枚举
    -- 精灵升级所需的经验值
    SELECT sum(upgrade_exp) FROM `talkplatform_game`.`elf_level_config` where level <=7;
    """

    LEVEL_DATA = {
        1: {'elf_total_exp': 590, 'elf_level_exp': 590, 'elf_style_code': 'elf_egg_001'},
        2: {'elf_total_exp': 630, 'elf_level_exp': 30, 'elf_style_code': 'elf_baby_001'},
        3: {'elf_total_exp': 1260, 'elf_level_exp': 60, 'elf_style_code': 'elf_baby_002'},
        4: {'elf_total_exp': 1890, 'elf_level_exp': 90, 'elf_style_code': 'elf_baby_003'},
        5: {'elf_total_exp': 4000, 'elf_level_exp': 400, 'elf_style_code': 'elf_baby_004'},
        6: {'elf_total_exp': 6500, 'elf_level_exp': 500, 'elf_style_code': 'elf_child_002'},
        7: {'elf_total_exp': 13198, 'elf_level_exp': 3598, 'elf_style_code': 'elf_child_003'},
        8: {'elf_total_exp': 13203, 'elf_level_exp': 3, 'elf_style_code': 'elf_young_001'},
        9: {'elf_total_exp': 19249, 'elf_level_exp': 3549, 'elf_style_code': 'elf_young_001'},
        10: {'elf_total_exp': 27500, 'elf_level_exp': 7100, 'elf_style_code': 'elf_young_001'},
        # 继续添加其他等级的数据
    }

    @staticmethod
    def get_level_data(elf_level):
        """根据精灵等级获取相应的数据"""
        return ElfLevelData.LEVEL_DATA.get(elf_level, None)


# # 示例调用
# if __name__ == "__main__":
#     level = 7
#     level_data = ElfLevelData.get_level_data(level)
#     if level_data:
#         print(f"Level {level} data: {level_data}")
#     else:
#         print(f"No data found for level {level}")
