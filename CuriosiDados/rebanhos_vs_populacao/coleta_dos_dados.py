# Script para baixar os dados utilizados nas visualizações

# Importando a biblioteca
import basedosdados as bd


# Queries

query_bovinos = """ 
                SELECT sigla_uf, id_municipio, quantidade_bovinos_total
                FROM `basedosdados.br_ibge_censo_agropecuario.municipio`
                WHERE ano = 2017 

                """

df_rebanhos = bd.read_sql(query_bovinos, billing_project_id = 'projeto1-311803')

df_rebanhos.to_csv('rebanhos.csv', index = False)

query_pop = """
            SELECT *
            FROM `basedosdados.br_ibge_populacao.municipio`
            WHERE ano = 2017 
            """

df_pop = bd.read_sql(query_pop, billing_project_id = 'projeto1-311803')

df_pop.to_csv('pop.csv', index = False)

