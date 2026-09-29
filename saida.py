from datetime import date
from pathlib import Path
from config import DIRETORIO_RASCUNHOS
from extrator import Fato
from redator import formatar_fatos

def salvar_rascunho(posts: list[str], fatos_por_repo: dict[str, list[Fato]]) -> Path:
    DIRETORIO_RASCUNHOS.mkdir(exist_ok=True)
    arquivo = DIRETORIO_RASCUNHOS / f"{date.today().isoformat()}.md"
    partes = []
    for i, post in enumerate(posts, start=1):
        partes += [f"# Versão {i}", "", post, "", "---", ""]
    partes += ["# Fatos usados (para conferência)", "", formatar_fatos(fatos_por_repo)]
    arquivo.write_text("\n".join(partes), encoding="utf-8")
    return arquivo