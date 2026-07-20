import base64
import json
from openai import OpenAI
import streamlit as st

def scan_sudoku_image(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    prompt = """
    Analiza esta imagen de un Sudoku. Devuelve EXCLUSIVAMENTE una matriz de 9x9 en formato JSON.
    Usa 0 para las celdas vacías. 
    Ejemplo: [[0, 8, 0...], [5, 0, 0...], ...]
    No añadas ningún texto adicional, solo el JSON.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ]
    )
    
    result = response.choices[0].message.content
    return json.loads(result.replace("```json", "").replace("```", ""))