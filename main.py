from client import generate_answer
#our main application having an input and output
while True:
    text = input("ask a question (or type quit to exit): ")
    if text.strip().lower() == "quit":
        break
    if text.strip() == "":
        print("please enter a question")
        continue
    answer = generate_answer(text)
    print()
    print("Answer:", answer.answer)
    print("Confidence:", answer.confidence)
    print()
