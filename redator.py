# redator.py
import ollama
from config import MODELO_REDACAO, CONTEXTO, DIRETORIO_ESTILO, MAX_EXEMPLOS
from extrator import Fato
from config import MODELO_REDACAO, CONTEXTO, DIRETORIO_ESTILO

PROMPT = """Você escreve posts de LinkedIn em português do Brasil para um desenvolvedor
que estuda IA e compartilha o que constrói. Você recebe os fatos da semana dele,
agrupados por projeto e classificados por tipo.

Escreva UM post-resumo da semana:
- Primeira pessoa, com tom de quem conta o que aprendeu, e não de quem se vende.
- Primeira linha curta e concreta, que desperte curiosidade. Nada de "Animado em compartilhar".
- Destaque as descobertas mais surpreendentes, com os exemplos concretos.
- Parágrafos curtos, de 1 a 3 frases.
- Termine com o próximo passo ou com uma pergunta genuína para a comunidade.
- No máximo 2 emojis e 3 hashtags (as hashtags no final).
- Escolha no máximo 3 fatos que sustentem o ângulo pedido. Não é preciso usar todos.
- Entre 180 e 280 palavras.
- Nada de perguntas retóricas ("O resultado?"), metáforas ou frases de efeito isoladas.
- Preserve os fatos e os termos técnicos, mas reescreva com naturalidade. Não copie as frases dos fatos.
- Explique os exemplos para quem não conhece o projeto. Nada de "ex:" entre parênteses.
- Use apenas os fatos fornecidos. Não invente resultados, números ou opiniões.
- Revise a ortografia e a acentuação antes de responder.
"""

def formatar_fatos(fatos_por_repo: dict[str, list[Fato]]) -> str:
    partes = []
    for repo, fatos in fatos_por_repo.items():
        partes.append(f"## Projeto: {repo}")
        for f in fatos:
            partes.append(f"- [{f.tipo}] {f.descricao}")
        partes.append("")
    return "\n".join(partes)

def redigir_post(fatos_por_repo: dict[str, list[Fato]], angulo: str) -> str:
    prompt = montar_prompt() + f"\n\nÂngulo deste post: {angulo}"
    resposta = ollama.chat(
        model=MODELO_REDACAO,
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": formatar_fatos(fatos_por_repo)}],
        think=False,
        options={"temperature": 0.7, "num_ctx": CONTEXTO},
    )
    return resposta["message"]["content"]

def carregar_exemplos() -> str:
    arquivos = sorted(DIRETORIO_ESTILO.glob("*.md"), reverse=True)[:MAX_EXEMPLOS]
    return "\n\n---\n\n".join(a.read_text(encoding="utf-8") for a in arquivos)

def montar_prompt() -> str:
    exemplos = carregar_exemplos()
    if not exemplos:
        return PROMPT
    return (PROMPT + "\n\nA seguir, textos escritos pelo próprio desenvolvedor, "
            "que podem ser de outros gêneros (e-mails, mensagens). Imite o tom, "
            "o ritmo e o vocabulário deles, adaptando ao formato de post. "
            "NÃO imite o conteúdo:\n\n" + exemplos)
