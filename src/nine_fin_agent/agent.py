from src.nine_fin_agent.graph import graph
import logging
import uuid
import sys

# -------------------
# Logging
# -------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("agent")


def run_agent():
    logger.info("Starting Financial Agent (type 'exit' to quit)")
    print("Financial Agent Ready (type 'exit' to quit)")
    thread_id = str(uuid.uuid4())
    CONFIG = {"configurable": {"thread_id": thread_id}}
    logger.info(f"New session started with thread_id={thread_id}")
    while True:
        try:
            query = input("\n> ")
            if query.lower() in ["exit", "quit"]:
                print("Goodbye")
                thread_id = str(uuid.uuid4())
                CONFIG = {"configurable": {"thread_id": thread_id}}
                logger.info(f"Prepared with thread_id={thread_id}")
                break

            logger.info(f"User query: {query}")

            for step in graph.stream(
                {"messages": [{"role": "user", "content": query}]},
                stream_mode="values",
                config = CONFIG
            ):
                step["messages"][-1].pretty_print()

        except KeyboardInterrupt:
            print("\nGoodbye")
            sys.exit(0)

if __name__ == "__main__":
    run_agent()
