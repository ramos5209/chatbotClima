import requests # Biblioteca  para fazer requisições HTTP
from typing import Any, Text, Dict, List # Tipagem para facilitar a leitira do codigo
from rasa_sdk import Action, Tracker # Iportaçao de classes para criar a custom action
from rasa_sdk.executor import CollectingDispatcher # Classe que permite enviar resposta ao usuario

class ActionInformaClima(Action):
    def name(self) -> Text:
        """
        Define o nome da Action. Esse nome deve ser o mesmo registrado no domain.yml .
        """
        return "action_informa_clima"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        Este método é chamado quando a action é executada. Ele:
        - Obtém a cidade da mensagem do usuario
        - Consulta a API de clima
        - Envia a resposta para o usuario
        """

        # Captura o nome da cidade a partir da mensagem mais recente do usuario
        city = tracker.latest_message['text']

        # Chama a API para obter os dados do clima 
        weather_data =  self.get_weather(city)

        print(f"City: {city}")
        print(f"Weather Data: {weather_data}")

        if weather_data:
            # Se os dados fore recebidos, formata a resposta com a temperatura 
            response = f"O clima na cidade de {city} esta em: {weather_data['current']['temp_c']} °C."
        else:
            # Se não conseguir buscar os dados, informa o erro
            response = f"Me desculpe, mas não consegui obter a situação do clima da cidade {city}."

        # Envia a resposta ao usuario
        dispatcher.utter_message(text=response)
        return []
    
    @staticmethod
    def get_weather(city: str) -> Dict[Text, Any]:
        """
        Método responsavel por consultar a API de clima e retornar os dados.
        """
        api_key = "4c333c51ebb04ad3b2b01859252603" # Chave da API (substitua pela sua!)
        base_url = "http://api.weatherapi.com/v1/current.json"
        params= {
            "q": city,  # Parametro da cidade a ser consultada
            "aqi": "no",    # Não incluir dados de qualidade do ar
            "key": api_key  # Chave de acesso a API
        }

        try:
            # Faz a requisição GET para a API 
            print(f"API Request URL: {base_url}?{params}")
            response = requests.get(base_url, params=params)
            response.raise_for_status() # Verifica se houve erro na requisição
            api_response = response.json() # Converte a resposta para JSON
            print(f"API Response: {api_response}")
            return api_response
        except requests.exceptions.RequestException as e:
            # Captura erros na requisição e imprime no console 
            print(f"API Request Error: {e}")
            return None