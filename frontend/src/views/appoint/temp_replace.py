import sys

with open('AppointList.vue', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 删除 'unkown': '阿语课',
    if "'unkown': '阿语课'," in line:
        i += 1
        continue
    
    # 替换 getCategoryText 函数
    if line.strip() == "// 获取课程种类文本":
        output.append(line)
        output.append("const getCategoryText = (category, usePoint) => {\n")
        output.append("  // 特殊处理阿语课：根据use_point区分体验课和付费课\n")
        output.append("  if (category === 'unkown') {\n")
        output.append("    if (usePoint === 'free') return '阿语体验课'\n")
        output.append("    if (usePoint === 'buy') return '阿语付费课'\n")
        output.append("    return '阿语课'\n")
        output.append("  }\n")
        output.append("  return categoryMap[category] || category || '未知'\n")
        output.append("}\n")
        i += 4  # 跳过原来的3行函数定义
        continue
    
    # 替换 getCategoryColor 函数
    if line.strip() == "// 获取课程种类标签颜色":
        output.append(line)
        output.append("const getCategoryColor = (category, usePoint) => {\n")
        output.append("  // 特殊处理阿语课：根据use_point决定颜色\n")
        output.append("  if (category === 'unkown') {\n")
        output.append("    if (usePoint === 'buy') return 'warning'  // 阿语付费课 - 橙色\n")
        output.append("    if (usePoint === 'free') return 'success'  // 阿语体验课 - 绿色\n")
        output.append("    return 'info'\n")
        output.append("  }\n")
        output.append("\n")
        output.append("  if (category === 'ph_buy' || category === 'ea_buy' || category === 'nat_buy') {\n")
        output.append("    return 'warning'  // 付费课 - 橙色\n")
        output.append("  }\n")
        output.append("  if (category === 'ph_free' || category === 'nat_free') {\n")
        output.append("    return 'success'  // 体验课 - 绿色\n")
        output.append("  }\n")
        output.append("  return 'info'       // 其他 - 灰色\n")
        output.append("}\n")
        i += 10  # 跳过原来的9行函数定义
        continue
    
    # 修改表格列调用
    if "getCategoryColor(row.category)" in line:
        line = line.replace("getCategoryColor(row.category)", "getCategoryColor(row.category, row.use_point)")
    if "getCategoryText(row.category)" in line:
        line = line.replace("getCategoryText(row.category)", "getCategoryText(row.category, row.use_point)")
    
    # 修改详情对话框调用
    if "getCategoryColor(currentRow.category)" in line:
        line = line.replace("getCategoryColor(currentRow.category)", "getCategoryColor(currentRow.category, currentRow.use_point)")
    if "getCategoryText(currentRow.category)" in line:
        line = line.replace("getCategoryText(currentRow.category)", "getCategoryText(currentRow.category, currentRow.use_point)")
    
    output.append(line)
    i += 1

with open('AppointList.vue', 'w', encoding='utf-8') as f:
    f.writelines(output)

print("修改完成")
