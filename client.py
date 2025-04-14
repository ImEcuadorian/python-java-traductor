import Pyro4


def main():
    chatgpt_helper = Pyro4.Proxy("PYRONAME:chatgpt.helper")
    print("Escribe tu código Python (termina con 'EOF'):")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "EOF":
            break
        lines.append(line)

    code = "\n".join(lines)
    print("\nEnviando a ChatGPT...\n")
    result = chatgpt_helper.analyze_code(code)
    print("\n🔍 Respuesta de ChatGPT:\n")
    print(result)


if __name__ == "__main__":
    main()