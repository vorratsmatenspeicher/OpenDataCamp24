import textwrap

from openai import OpenAI
import dotenv

dotenv.load_dotenv()

def convert_location(location):
    response_shema = textwrap.dedent('''
    {
        "function": "function_name",
        "parameters": [
            "param1",
            "param2":
        ]
        }
    }
    ''')

    instructions = textwrap.dedent(f"""
    Deine einzige Aufgabe ist es, die konkreten Koordinaten eines Ortes aus einer generellen Beschreibung zu ermitteln.
    Dafür kannst du GENAU EINE der nachfolgenden Funktionen nutzen.
    Gebe immer AUSSCHLIESLICH in folgender Form zurück:
    {response_shema}
    Du hast folgende Funktionen zur Verfügung:
    - intersection(street name, street name)  # z. B. "Hauptstraße Ecke Nebenstraße"
    - closestPoint(query a, query b)  # z. B. "Lidl in der Nähe der Albertbrücke"
    - getCoords(query)  # z. B. "Rathaus Dresden", "Hauptstraße 5"
    Du kannst irrelevante Informationen weglassen und die Anfragen auf das wesentliche reduzieren.
    """)

    prompt = textwrap.dedent(f"""
    Konvertiere folgende Ortsangaben zu Inputs der vordefinierten Funktionen:
    "{location}"
    """)
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# Beispiel zur Nutzung der Funktion
if __name__ == "__main__":
    locations = [
        # "Eisenstuckstraße Ecke Liebigstraße",
        "Lidl in der Nähe der Albertbrücke",
        # "Ich befinde mich am Rathaus"
    ]

    # Verarbeite jede Eingabe
    for location in locations:
        result = convert_location(location)
        print(result)
