from agent import ask_agent

result = ask_agent(
    company="Northwind Logistics",
    query="What's blocking this deal?",
    use_memory=True,
)

print("\nANSWER:")
print(result["answer"])

print("\nMEMORIES:")
for memory in result["memories"]:
    print("-", memory["text"])