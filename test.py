import requests


client_id = "FC9336B97B1963431231C00E109D93161688183C582ECF1DC66D62CFDF7CF171"
redirect_url = "https://t.me/ExlossiveNeuroBot"
response = requests.post(f"https://yoomoney.ru/oauth/authorize?client_id={client_id}&redirect_url={redirect_url}&scope=")