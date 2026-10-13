import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o-mini")

text = "Hi Moeez, unbelievable progress today!"
tokens = encoding.encode(text)

print("Number of tokens:", len(tokens))
print("Token IDs:", tokens)

for token_id in tokens:
    print(token_id, "->", repr(encoding.decode([token_id])))