# Importar as bibliotecas abaixo
import ftplib
import patoolib
import csv
import pandas as pd
import os

# Endereço do FTP que você tem interesse em conectar
ftp = ftplib.FTP("ftp.mtps.gov.br")

# Como este FTP não precisa de usuario e senha, basta solicitar o login sem estes parametros
ftp.login()

# Este comando indica para qual pasta você pretende navegar.
ftp.cwd('portal/fiscalizacao/seguranca-e-saude-no-trabalho/caepi')

# esses caminhos serão utilizados para salvar os arquivos baixados e extraidos.
caminho_pasta = 'C:/Projetos Python/ftp_mtps_gov/'
caminho_arquivo_txt = 'c:/Projetos Python/ftp_mtps_gov/tgg_export_caepi.txt'

# Comando usado para excluir o arquivo de texto e também o arquivo zip
try:
    os.remove(caminho_arquivo_txt)
    os.remove(caminho_pasta + 'tgg_export_caepi.zip')
except:
    # e caso eles não existam, apenas passe para o proximo comando.
    pass


# Defini uma função para pegar o arquivo que tenho interesse.
def getFile(ftp, filename):
    try:
        ftp.retrbinary("RETR " + filename, open(caminho_pasta + filename, 'wb').write)

    except:
        print("Error")


# Aqui eu chamo a função e passo os parametros FTP e o nome do arquivo que eu quero.
# Deixei em hardcod o nome do arquivo pois ele é imutavel, mas é possivel abrir um loop for para baixar varios arquivos.
getFile(ftp, 'tgg_export_caepi.zip')


# Agora será feita a extração/descompactação do arquivo
patoolib.extract_archive(caminho_pasta + "tgg_export_caepi.zip", outdir=caminho_pasta)
print("fim extração")


# Essas linhas são exclusivas para o caso de precisar converter o arquivo .txt em um arquivo .csv
# Tive que usar a lib cvs ao invés pandas pois o arquivo por algum motivo é incompativel com pandas.
with open('c:/Projetos Python/ftp_mtps_gov/tgg_export_caepi.txt') as csvfile:
    reader = csv.reader(csvfile)
    array_completo = []
    for row in reader:
        row = str(row).replace("[", '').replace(']', '').replace("'", '').split("|")
        array_completo.append(row)
    df = pd.DataFrame(array_completo)
    # Datafreme montado agora é salvar em .csv
    df.to_csv(caminho_pasta + 'tgg_export_caepi.csv', index=False, encoding='UTF-8', header=0)
