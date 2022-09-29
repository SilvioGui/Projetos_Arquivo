from app.config import config, planilhas_dir
from app.ftp import create_ftp

ftp_pasta_planilha = 'retorno/'

results_filename = 'PESQUISA_ABATE_JBS.xlsx'
results_file = '{}/{}'.format(planilhas_dir, results_filename)

ftp = create_ftp()
ftp.upload(results_file, ftp_pasta_planilha + results_filename)

