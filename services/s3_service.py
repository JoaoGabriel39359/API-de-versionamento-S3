import boto3
import os

class S3Service:
    def __init__(self):
        endpoint = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
        )
        self.bucket_name = "meu-balde-versionado"

    def setup_bucket(self):
        try:
            self.client.create_bucket(Bucket=self.bucket_name)
            self.client.put_bucket_versioning(
                Bucket=self.bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
        except Exception as e:
            print(f"Bucket pronto ou erro: {e}")

    def upload(self, filename, content):
        return self.client.put_object(Bucket=self.bucket_name, Key=filename, Body=content)

    def list_versions(self, filename):
        return self.client.list_object_versions(Bucket=self.bucket_name, Prefix=filename)
    
    def restore_version(self, filename, version_id):
    # O S3 faz o restore através de uma cópia interna
        return self.client.copy_object(
            Bucket=self.bucket_name,
            Key=filename,
            CopySource={'Bucket': self.bucket_name, 'Key': filename, 'VersionId': version_id},
            MetadataDirective="REPLACE"
        )
    
    def buscar_arquivo(self, filename: str, version_id: str = None):
        """Busca o conteúdo de um arquivo. Se version_id for passado, busca aquela versão específica."""
        try:
            if version_id:
                response = self.client.get_object(Bucket=self.bucket_name, Key=filename, VersionId=version_id)
            else:
                response = self.client.get_object(Bucket=self.bucket_name, Key=filename)
            
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            print(f"Erro ao buscar arquivo: {e}")
            return None
        
    def delete_file(self, filename: str):
        """Deleta um arquivo, criando uma nova versão de deleção."""
        return self.client.delete_object(Bucket=self.bucket_name, Key=filename)