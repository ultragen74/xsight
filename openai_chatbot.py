from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pandas as pd

df = pd.read_csv("sales.csv")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
}

agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", callbacks=[StreamingStdOutCallbackHandler()], streaming=True),
    df,
    # verbose=True,
    memory=memory,
    agent_executor_kwargs=agent_kwargs,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)