from datetime import datetime

class S3Auditor:
    def __init__(self, s3_client, bucket_name):
        self.client = s3_client
        self.bucket_name = bucket_name

    def gerar_auditoria(self, filename: str):
        """Compara a versão atual com a anterior e gera um relatório de mudanças."""
        try:
            # 1. Busca todas as versões do arquivo
            response = self.client.list_object_versions(Bucket=self.bucket_name, Prefix=filename)
            versions = response.get('Versions', [])

            if len(versions) < 1:
                return {"error": "Arquivo não encontrado."}

            # Versão atual (a primeira da lista)
            atual = versions[0]
            
            relatorio = {
                "arquivo": filename,
                "status": "Ativo",
                "versao_atual": {
                    "id": atual['VersionId'],
                    "tamanho_bytes": atual['Size'],
                    "data_modificacao": atual['LastModified'].strftime("%d/%m/%Y %H:%M:%S"),
                    "e_a_mais_recente": atual['IsLatest']
                }
            }

            # Se existir uma versão anterior, vamos comparar
            if len(versions) > 1:
                anterior = versions[1]
                diff_tamanho = atual['Size'] - anterior['Size']
                
                relatorio["comparacao_com_anterior"] = {
                    "id_anterior": anterior['VersionId'],
                    "mudanca_tamanho_bytes": diff_tamanho,
                    "alerta_de_crescimento": "Aumentou" if diff_tamanho > 0 else "Diminuiu ou igual",
                    "tempo_entre_versoes": str(atual['LastModified'] - anterior['LastModified'])
                }
            else:
                relatorio["comparacao_com_anterior"] = "Esta é a primeira versão criada. Sem histórico para comparar."

            return relatorio

        except Exception as e:
            return {"error": str(e)}