# 文件: details wordcloud2Svg
# 作者: bao0
# 创建日期: 2025/1/15
# 描述: 这是一个生成显示动态词云的文件
import os
import jieba
from jieba import analyse
from wordcloud import WordCloud
from opencc import OpenCC

# 获取当前脚本文件所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义目录路径和输出路径

dir_path = os.path.normpath(os.path.join(script_dir, "../../../")) #本博客对应的是/src目录

output_path = os.path.normpath(os.path.join(script_dir, "../assets/img")) #本博客对应的是/src/.vuepress/public/assets/img目录

font_path = os.path.normpath(os.path.join(script_dir, "./font.otf")) #本博客对应的是/src/.vuepress/public/scripts/font.otf

output_path_svg = os.path.normpath(os.path.join(script_dir, "../assets/img/wordcloud.svg"))  #本博客对应的是/src/.vuepress/public/assets/img/wordcloud.svg

#print(f"dir_path:{dir_path}\n\noutput_path:{output_path}\n\nfont_path:{font_path}\n\noutput_path_svg:{output_path_svg}\n\n")

contents = ""
def merge_md_contents(folder_path):
    contents = ""
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isdir(file_path):
            contents += merge_md_contents(file_path)  # 递归遍历子文件夹并将内容合并
        elif file.endswith(".md"):
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
                contents += file_content
    return contents

contents = merge_md_contents(dir_path)
#with open(r"D:\Users\ArthurFsy\Documents\python脚本\rawPic\output.md", "w", encoding="utf-8") as f:
#                f.write(contents)
#print(contents)

# 使用jieba的textrank功能提取关键词
keywords = jieba.analyse.textrank(contents, topK=150, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
#print(f"keywords={keywords}")

# 创建 OpenCC 对象，指定转换方式为简体字转繁体字
converter = OpenCC('s2t.json')

# 统计每个关键词出现的次数
keyword_counts = {}
for keyword in keywords:
    count = contents.count(keyword)
    keyword = converter.convert(keyword) #简体转繁体，如果注释掉则保留为简体的内容
    keyword_counts[keyword] = count

#print(keyword_counts)


# 创建一个WordCloud对象，并设置字体文件路径和轮廓图像

wordcloud = WordCloud(width=1600, height=800, background_color="white", font_path=font_path)


# 生成词云
wordcloud.generate_from_frequencies(keyword_counts)

# 转换为svg格式输出
svg_image = wordcloud.to_svg(embed_font=True)
with open(output_path_svg, "w+", encoding='UTF8') as f:
    f.write(svg_image)
    print(f"已保存至{output_path_svg}")