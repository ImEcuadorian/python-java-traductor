import os
import Pyro4
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@Pyro4.expose
class TypescriptServer:
    def convert_to_typescript(self, python_code_description: str) -> str:
        try:
            response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {"role": "system", "content": "Eres un traductor experto de código Python a Typescript."},
                    {"role": "user", "content": f"Convierte este código o descripción Python a Typescript:\n\n{python_code_description}"}
                ]
            )
            return response.output_text
        except Exception as e:
            return f"Error al convertir a Java: {e}"

def main():
    daemon = Pyro4.Daemon()
    uri = daemon.register(TypescriptServer)
    print("URI del servidor Typescript:", uri)
    Pyro4.locateNS().register("typescript.converter", uri)
    print("Servidor TypescriptServer listo.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
