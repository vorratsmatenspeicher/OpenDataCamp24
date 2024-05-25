from openai import OpenAI
import dotenv

dotenv.load_dotenv()

def convert_location(location):
    response_shema = '''
    {
        "function": "function_name",
        "parameters": [
            "param1",
            "param2":
        ]
        }
    }
    '''

    instructions = f"""
    Deine einzige Aufgabe ist es zu entscheiden welche von vordefinierten Funktionen du wählen 
    würdest um Koordinaten für allgemeine Orstangaben zu bekommen. Gebe immer AUSSCHLIESLICH in folgender
    Form zurück:
    {response_shema}
    Du hast folgende Funktionen zur Verfügung:
    - intersection(street, street)
    - closestPoint(query a, query b)
    - getCoords(query)
    Du kannst irrelevante Informationen weglassen und die querys auf das wesentliche reduzieren.
    """

    prompt = f"""
    Konvertiere folgende Ortsangaben zu Inputs der vordefinierten Funktionen:
    "{location}"
    """
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
