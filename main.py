from config import DIRETORIO_PROJETOS, DIAS_ANALISADOS, ANGULOS
from coletor import (encontrar_repositorios, buscar_commits,
                     ler_readmes_alterados, montar_material)
from extrator import extrair_fatos
from redator import redigir_post
from saida import salvar_rascunho
from datetime import datetime

print(f"\n=== Execução {datetime.now():%Y-%m-%d %H:%M} ===")

fatos_por_repo = {}
for repo in encontrar_repositorios(DIRETORIO_PROJETOS):
    commits = buscar_commits(repo, DIAS_ANALISADOS)
    if not commits:
        continue
    readmes = ler_readmes_alterados(repo, commits)
    material = montar_material(repo, commits, readmes)
    fatos_por_repo[repo.name] = extrair_fatos(material)
    print(f"{repo.name}: {len(fatos_por_repo[repo.name])} fato(s) extraído(s)")

if fatos_por_repo:
    posts = [redigir_post(fatos_por_repo, angulo) for angulo in ANGULOS]
    arquivo = salvar_rascunho(posts, fatos_por_repo)
    print(f"{len(posts)} versões salvas em {arquivo}")
else:
    print("Nenhuma atividade nos projetos esta semana.")