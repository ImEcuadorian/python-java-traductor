# server.py
import os

import Pyro4
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@Pyro4.expose
class PythonServer:

    def analyze_code(self, code: str) -> str:
        try:
            response = client.responses.create(
                model="gpt-4.1",
                input=f"Analiza este código Python, mejoralo y verifica que no tenga errores:\n\n{code}"
            )

            analysis = response.output_text

            java_converter = Pyro4.Proxy("PYRONAME:java.converter")
            java_code = java_converter.convert_to_java(code)

            return f"🔍 Análisis Python:\n{analysis}\n\n☕ Código Java generado:\n{java_code}"

        except Exception as e:
            return f"Error al consultar ChatGPT: {e}"

def main():
    daemon = Pyro4.Daemon()
    uri = daemon.register(PythonServer)
    print("URI del servidor:", uri)
    Pyro4.locateNS().register("chatgpt.helper", uri)
    print("Servidor Pyro4 listo.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
