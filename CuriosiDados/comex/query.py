import basedosdados as bd

query = """
SELECT *
FROM `basedosdados.br_me_comex_stat.municipio_exportacao`
WHERE id_municipio = '3503208'
"""

dados = bd.read_sql(query, billing_project_id = 'projeto1-311803')
dados.to_csv('dados.csv', index = False)