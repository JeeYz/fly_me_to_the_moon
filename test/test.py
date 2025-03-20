
from termcolor import colored

print(colored('빨간색 텍스트', 'red'))
print(colored('초록색 배경', 'white', 'on_green'))
print(colored('빨간색 텍스트, 초록색 배경', 'red', 'on_green'))


print('\033[31m빨간색 텍스트\033[0m')
print('\033[42m초록색 배경\033[0m')
print('\033[31;42m빨간색 텍스트, 초록색 배경\033[0m')

from rich.console import Console
from rich.table import Table

console = Console()

console.print("Hello, [bold red]World[/bold red]!", style="italic blue")

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Name", style="dim", width=12)
table.add_column("Age", justify="right")
table.add_column("City", justify="right")
table.add_row("Bill", "35", "San Francisco")
table.add_row("John", "42", "London")
table.add_row("Sarah", "28", "Tokyo")

console.print(table)

from rich.console import Console
from rich.markdown import Markdown

console = Console()

markdown_text = """
# 제목 1
## 제목 2
*기울임체*
**굵게**
- 목록 1
- 목록 2
```python
print("Hello, world!")"""

markdown = Markdown(markdown_text)
console.print(markdown)




from langchain.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama

from langchain_core.output_parsers import (
    StrOutputParser, 
    JsonOutputParser
)

import json

llm = ChatOllama(model="gemma3:4b", temperature=0.0)

template = """
{subject}에 대한 간략한 요약을 작성해주세요.
"""

prompt_template = PromptTemplate(
    input_variables=["subject"],
    template=template
)

final_prompt = prompt_template.format(subject="인공지능")
print(final_prompt)  # 출력: 인공지능에 대한 간략한 요약을 작성해주세요.


from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "당신은 유용한 챗봇 어시스턴트입니다."
    ),
    HumanMessagePromptTemplate.from_template(
        "{user_input}"
    )
])

messages = chat_template.format_messages(user_input="안녕, LangChain이 뭐야?")

print("\n기본 출력:")
print(messages)

# 방법 1: JSON으로 변환하여 예쁘게 출력
print("\n방법 1: JSON 형식으로 출력")
# 중요: messages 객체는 직접 json.dumps()로 직렬화할 수 없음
# 잘못된 방법: print(json.dumps(messages, indent=2)) # TypeError 발생!
# 올바른 방법: 먼저 딕셔너리로 변환 후 직렬화
messages_dict = [{'type': msg.type, 'content': msg.content} for msg in messages]
print(json.dumps(messages_dict, indent=2, ensure_ascii=False))

# 방법 2: rich 라이브러리 활용
print("\n방법 2: rich 라이브러리 활용")
from rich.panel import Panel
from rich import box

for msg in messages:
    color = "green" if msg.type == "system" else "blue"
    console.print(Panel(
        f"[bold]{msg.content}[/bold]", 
        title=f"[{color}]{msg.type.upper()}[/{color}]",
        border_style=color,
        box=box.ROUNDED
    ))

# 방법 3: rich 테이블 활용
print("\n방법 3: rich 테이블 활용")
msg_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
msg_table.add_column("Type", style="dim")
msg_table.add_column("Content")

for msg in messages:
    msg_table.add_row(f"[{'green' if msg.type == 'system' else 'blue'}]{msg.type}[/]", msg.content)

console.print(msg_table)


chat_chain = chat_template | llm | StrOutputParser()

# result = chat_chain.invoke({"user_input": "안녕, LangChain이 뭐야?"})

# print(result)


from langchain_ollama.embeddings import OllamaEmbeddings 

embedding_model = OllamaEmbeddings(model="snowflake-arctic-embed2")

# 임베딩 차원 크기를 계산
dimension_size = len(embedding_model.embed_query("hello world"))
print(dimension_size)
