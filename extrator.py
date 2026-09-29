# extrator.py
import json
import ollama
from config import MODELO, CONTEXTO
from dataclasses import dataclass

@dataclass(frozen=True)
class Fato:
    tipo: str
    descricao: str

PROMPT = """Você analisa o trabalho semanal de um desenvolvedor: mensagens de commit e arquivos README.
Extraia os fatos que renderiam um bom post no LinkedIn, cobrindo todos estes tipos:
- construcao: o que foi implementado (os commits mostram isso)
- descoberta: resultados de experimentos e aprendizados
- problema: limitações ou dificuldades encontradas
- proximo_passo: o que o desenvolvedor pretende fazer em seguida
Escreva TODOS os fatos na primeira pessoa ("implementei", "descobri", "percebi").
Se o mesmo fato aparecer em mais de um arquivo, registre-o uma vez só.
Ignore instruções de instalação, listas de arquivos e comandos.
Use apenas informações presentes no material. 
Preserve os detalhes concretos: exemplos, perguntas testadas, nomes de modelos
e ferramentas. Um fato genérico não serve para um post.
Não invente nada.
Os commits são a fonte mais atual. Se algo listado como próximo passo no README
já aparece num commit posterior, trate-o como construcao, não como proximo_passo.
Cada fato deve aparecer uma única vez, no tipo que melhor o descreve: limitações
descobertas em experimentos são descoberta; use problema apenas para dificuldades
práticas no desenvolvimento.
"""

ESQUEMA = {
    "type": "object",
    "properties": {
        "fatos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tipo": {"type": "string",
                             "enum": ["construcao", "descoberta",
                                      "problema", "proximo_passo"]},
                    "descricao": {"type": "string"},
                },
                "required": ["tipo", "descricao"],
            },
        }
    },
    "required": ["fatos"],
}

def extrair_fatos(texto: str) -> list[Fato]:
    resposta = ollama.chat(
        model=MODELO,
        messages=[{"role": "system", "content": PROMPT},
                  {"role": "user", "content": texto}],
        format=ESQUEMA,
        think=False,
        options={"temperature": 0, "num_ctx": CONTEXTO},
    )
    dados = json.loads(resposta["message"]["content"])
    return [Fato(f["tipo"], f["descricao"]) for f in dados["fatos"]]
