import asyncio

from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness, FactualCorrectness


async def main() -> None:
    client = AsyncOpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
    llm = llm_factory(
        "gemma3:4b", client=client, temperature=0, seed=20260902
    )
    faithfulness = await Faithfulness(llm=llm).ascore(
        user_input="What is the mean?",
        response="The mean is an average.",
        retrieved_contexts=["The arithmetic mean is an average."],
    )
    factual_correctness = await FactualCorrectness(llm=llm).ascore(
        response="The mean is an average.",
        reference="The arithmetic mean is an average.",
    )
    print({"faithfulness": faithfulness.value, "factual_correctness": factual_correctness.value})
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
