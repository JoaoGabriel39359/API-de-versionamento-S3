import pytest
import boto3
from botocore.exceptions import ClientError

@pytest.fixture
def s3_client():
    """Prepara o cliente para o LocalStack"""
    return boto3.client(
        "s3",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

@pytest.fixture
def bucket_name(s3_client):
    """Garante que o bucket de testes exista"""
    nome = "bucket-de-teste-automatizado"
    s3_client.create_bucket(Bucket=nome)
    yield nome
    # O código após o yield roda DEPOIS do teste (limpeza)
    # Dica: Você poderia deletar o bucket aqui se quisesse
    
# --- TESTE DE PUT (SUCESSO) ---
def test_s3_put_object_sucesso(s3_client, bucket_name):
    """Testa se conseguimos subir um arquivo com sucesso"""
    # ARRANGE (Organizar)
    nome_arquivo = "teste.txt"
    conteudo = b"Ola Mundo S3" # Boto3 espera bytes

    # ACT (Agir)
    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=nome_arquivo,
        Body=conteudo
    )

    # ASSERT (Afirmar)
    # Verifique se o status HTTP da resposta foi 200
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200


# --- TESTE DE GET (CAMINHO TRISTE / ERRO) ---
def test_s3_get_object_nao_existente(s3_client, bucket_name):
    """Testa se o S3 retorna erro ao buscar arquivo que não existe"""
    
    # Aqui usamos o gerenciador de contexto 'with'
    with pytest.raises(ClientError) as excinfo:
        s3_client.get_object(Bucket=bucket_name, Key="arquivo_fantasma.txt")
    
    # Opcional: Validar se o erro foi exatamente 'NoSuchKey'
    assert excinfo.value.response['Error']['Code'] == 'NoSuchKey'

def test_s3_upload_e_leitura_integra(s3_client, bucket_name):
    nome_arquivo = "teste_integra.txt"
    conteudo = b"Conteudo para teste de integracao"

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=nome_arquivo,
        Body=conteudo
    )

    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=nome_arquivo
    )

    conteudo_lido = response['Body'].read()

    assert conteudo_lido == conteudo

    
