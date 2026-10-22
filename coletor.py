from pathlib import Path
from dataclasses import dataclass
import subprocess

@dataclass(frozen=True)
class Commit:
    hash: str
    data: str
    mensagem: str
    arquivos: tuple[str, ...]

def eh_repositorio(pasta: Path) -> bool:
    return (pasta / ".git").exists()

def encontrar_repositorios(raiz: Path) -> list[Path]:
    if eh_repositorio(raiz):
        return [raiz]
    return [pasta for pasta in raiz.iterdir()
            if pasta.is_dir() and eh_repositorio(pasta)]


def buscar_commits(repo: Path, dias: int) -> list[Commit]:
    resultado = subprocess.run(
        ["git", "-C", str(repo), "log",
         f"--since={dias} days ago",
         "--date=short",
         "--pretty=format:%h|%ad|%s"],
        capture_output=True, text=True, check=True,
    )
    commits = []
    for linha in resultado.stdout.splitlines():
        hash_, data, mensagem = linha.split("|", 2)
        commits.append(Commit(hash_, data, mensagem, buscar_arquivos(repo, hash_)))
    return commits

def buscar_arquivos(repo: Path, hash_: str) -> tuple[str, ...]:
    resultado = subprocess.run(
        ["git", "-C", str(repo), "show",
         "--name-only", "--pretty=format:", hash_],
        capture_output=True, text=True, check=True,
    )
    return tuple(l for l in resultado.stdout.splitlines() if l.strip())

def ler_readmes_alterados(repo: Path, commits: list[Commit],
                          limite: int = 12_000) -> dict[str, str]:
    caminhos = {arq for c in commits for arq in c.arquivos
                if Path(arq).name.lower() == "readme.md"}
    readmes = {}
    vistos = set()
    for caminho in sorted(caminhos):
        arquivo = repo / caminho
        if not arquivo.exists():
            continue
        conteudo = ler_novidades(repo, commits, caminho)
        if not conteudo.strip() or conteudo in vistos:
            continue
        vistos.add(conteudo)
        readmes[caminho] = conteudo[:limite]
    return readmes

# coletor.py
def montar_material(repo: Path, commits: list[Commit],
                    readmes: dict[str, str]) -> str:
    partes = [f"# Repositório: {repo.name}", "",
              "## Commits da semana (do mais antigo ao mais recente)"]
    for c in reversed(commits):
        partes.append(f"- {c.data}: {c.mensagem}")
        partes.append(f"  arquivos: {', '.join(c.arquivos)}")
    for caminho, conteudo in readmes.items():
        partes += ["", f"## Arquivo {caminho}", conteudo]
    return "\n".join(partes)

ARVORE_VAZIA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

def ler_novidades(repo: Path, commits: list[Commit], caminho: str) -> str:
    mais_antigo = commits[-1].hash
    base = f"{mais_antigo}^"
    tem_pai = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", base],
        capture_output=True,
    ).returncode == 0
    if not tem_pai:
        base = ARVORE_VAZIA
    diff = subprocess.run(
        ["git", "-C", str(repo), "diff", base, "HEAD", "--", caminho],
        capture_output=True, text=True, check=True,
    ).stdout
    return "\n".join(l[1:] for l in diff.splitlines()
                     if l.startswith("+") and not l.startswith("+++"))

