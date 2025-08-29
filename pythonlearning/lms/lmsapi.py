import lmstudio as lms

model = lms.llm("google/gemma-3-4b")
result = model.respond("What is the meaning of life?")

print(result)