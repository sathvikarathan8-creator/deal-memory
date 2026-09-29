from memory import recall_memories

memories = recall_memories(
    "Northwind Logistics",
    "What is blocking the deal?"
)

for memory in memories:
    print(memory["text"])
    print("---")