from langchain_tavily import TavilySearch
import pprint  # 导入美观打印模块

tool = TavilySearch(max_results=2,tavily_api_key="")
tools = [tool]
result= tool.invoke("武汉烧烤")

# 创建美观打印对象
pp = pprint.PrettyPrinter(indent=2, width=80, depth=3, compact=False)

print("结果为:")
pp.pprint(result)  # 使用美观打印输出结果