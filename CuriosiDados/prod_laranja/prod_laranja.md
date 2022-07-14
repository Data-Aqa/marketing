## CuriosiDados 2 - Quais cidades mais produziram laranja nos últimos 45 anos?


```python
# Importando bibliotecas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import basedosdados as bd
import geobr
```

### Avisos antes de continuar!

As próximas 6 células foram usadas apenas para baixar os dados utilizados, então não é necessário instalar a biblioteca `basedosdados` (caso queira, fique a vontade! ela é **MUITO** útil para conseguir dados) e nem rodas as próximas células.

A seção de <font color = 'blue'>Manipulação<font color = 'black'> tem um roteirinho a ser seguido. Ele não é longo, e muitas das coisas podem ser vistas em notebooks de aulas (caso não queira abrir os notebooks, eles estão todos no GitHub do grupo).

A seção de <font color = 'blue'>Visualização<font color = 'black'> já está feita, mas recomendo tentar entender o que as linhas do código mudaram na visualização, isso ajuda bastante a lembrar como fazer as alterações.


```python
# Baixando os dados de produção pela API da Base dos Dados
query_sp = """
        SELECT *
        FROM `basedosdados.br_ibge_pam.municipio_lavouras_permanentes`
        WHERE sigla_uf = 'SP'
        AND produto = 'Laranja'
        """

df = bd.read_sql(query_sp, billing_project_id = 'projeto1-311803')
```


```python
# Salvando os dados como um arquivo csv
df.to_csv('../prod_laranja_aqa/prod_laranja_sp.csv', index = False)
```


```python
bd.get_table_columns('br_bd_diretorios_brasil', 'municipio')
```


```python
# Baixando dados para liguar o id do município ao nome do município

query = """
        SELECT id_municipio, nome
        FROM `basedosdados.br_bd_diretorios_brasil.municipio`
        WHERE sigla_uf = 'SP'
"""

df_ids = bd.read_sql(query, billing_project_id = 'projeto1-311803')
```


```python
df_ids.head()
```


```python
df_ids.to_csv('../prod_laranja_aqa/relacao_id_nome.csv', index = False)
```

<br>

<br>

## Manipulação
---
Queremos encontrar os 10 municípios com maior produção de laranja ao longo da série (1974 - 2018).


```python
# Leia o arquivo 'prod_laranja_sp.csv' e armazene em uma variável
df = pd.read_csv('prod_laranja_sp.csv')
```

### `.group_by()`

Agrupe a coluna `quantidade_produzida` por município e some as produções anuais e salvar em uma nova variável. A função deve retornar um objeto `pd.DataFrame` ao invés de um objeto `pd.Series`.

<font size = 2>caso tenho dúvidas, lembre que quando queremos selecionar mais de uma coluna de um dataframe, utilizamos uma a seguinte sintaxe: `df[['coluna1', 'coluna2']]`, isso porque quando queremos ler mais de uma coluna, precisamos passa-las no formato de lista (tente selecionar duas colunas com apenas um par de colchetes, irá gerar um erro). Lembre também que as colunas de um dataframe podem ser interpretadas como listas. Dessa forma, quando usamos a notação `df[['coluna1']]` a saída é uma lista de listas, que o pandas transforma em um dataframe.


```python
df_agrupado = df.groupby('id_municipio')[['quantidade_produzida']].sum()
```


```python
df_agrupado.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>quantidade_produzida</th>
    </tr>
    <tr>
      <th>id_municipio</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3500105</th>
      <td>207910.0</td>
    </tr>
    <tr>
      <th>3500204</th>
      <td>6223134.0</td>
    </tr>
    <tr>
      <th>3500303</th>
      <td>13174686.0</td>
    </tr>
    <tr>
      <th>3500402</th>
      <td>6140.0</td>
    </tr>
    <tr>
      <th>3500501</th>
      <td>47373.0</td>
    </tr>
  </tbody>
</table>
</div>



Transforme o índice do dataframa em uma coluna.


```python
# .reset_index()
df_agrupado = df_agrupado.reset_index()
```


```python
df_agrupado.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_municipio</th>
      <th>quantidade_produzida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3500105</td>
      <td>207910.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3500204</td>
      <td>6223134.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3500303</td>
      <td>13174686.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3500402</td>
      <td>6140.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3500501</td>
      <td>47373.0</td>
    </tr>
  </tbody>
</table>
</div>



### Ordenar

Ordene o dataframe pela coluna `quantidade_produzida` de forma decrescentea e armazene os **10 maiores** em uma nova variável


```python
# .sort_values()
df_rank = df_agrupado.sort_values(by = 'quantidade_produzida', ascending = False).head(10)
```


```python
df_rank
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_municipio</th>
      <th>quantidade_produzida</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>68</th>
      <td>3506102</td>
      <td>83752164.0</td>
    </tr>
    <tr>
      <th>341</th>
      <td>3530706</td>
      <td>79968458.0</td>
    </tr>
    <tr>
      <th>257</th>
      <td>3522703</td>
      <td>58787985.0</td>
    </tr>
    <tr>
      <th>379</th>
      <td>3533908</td>
      <td>58046131.0</td>
    </tr>
    <tr>
      <th>300</th>
      <td>3526902</td>
      <td>51232119.0</td>
    </tr>
    <tr>
      <th>349</th>
      <td>3531506</td>
      <td>42437903.0</td>
    </tr>
    <tr>
      <th>36</th>
      <td>3503208</td>
      <td>41358768.0</td>
    </tr>
    <tr>
      <th>591</th>
      <td>3553708</td>
      <td>41273923.0</td>
    </tr>
    <tr>
      <th>122</th>
      <td>3510807</td>
      <td>38798969.0</td>
    </tr>
    <tr>
      <th>62</th>
      <td>3505500</td>
      <td>33807413.0</td>
    </tr>
  </tbody>
</table>
</div>



Agora que temos um dataframe contendo os 10 maiores produtores de laranja do estado, precimos da uma maneira de mapear os ids aos nomes dos municípios.

Leia o arquivo `relacao_id_nome.csv`.


```python
df_ids = pd.read_csv('relacao_id_nome.csv')
```


```python
df_ids.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_municipio</th>
      <th>nome</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3500105</td>
      <td>Adamantina</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3500204</td>
      <td>Adolfo</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3500303</td>
      <td>Aguaí</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3500402</td>
      <td>Águas da Prata</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3500501</td>
      <td>Águas de Lindóia</td>
    </tr>
  </tbody>
</table>
</div>



### `.merge()`

A função `.merge()` funciona como o **PROCV** no excel. Com ela, nós podemos juntar duas tabelas por meio de uma coluna em comum.

No nosso caso, temos dois dataframes: um contendo o o id e a produção dos 10 maiores produtores de laranja do estado e outro com o id e nome dos municipios de São Paulo. Vamos usar a função `.merge()` para junta-las.

A função recebe 4 argumentos principais: `left`, `right`, `on` e `how`. Os dois primeiros indicam quais dataframes serão utilizados. Por convenção a tabela da esquerda é a tabela que queremos adicionar a coluna, enquanto a da direita é a que vai 'ceder' a coluna.

O argumento `on` indica qual coluna dos dataframes será utilizada como *link* (coluna em comum).

**OBS**: caso as colunas tenham nomes diferentes nos dataframes, devemos utilizar os argumentos `left_on` e `right_on` para indicar os nomes em cada dataframe.

Por último, o argumento `how` indica qual será o método utilizado para realizar a junção. Por padrão este argumento é `'inner'`, que indica que queremos trazer apenas as linhas da tabela da direita que tem correspondência na tabela da direita.


```python
df_nomes = pd.merge(left = df_rank, right = df_ids, on = 'id_municipio', how = 'inner')
```


```python
df_nomes.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_municipio</th>
      <th>quantidade_produzida</th>
      <th>nome</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3506102</td>
      <td>83752164.0</td>
      <td>Bebedouro</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3530706</td>
      <td>79968458.0</td>
      <td>Mogi Guaçu</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3522703</td>
      <td>58787985.0</td>
      <td>Itápolis</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3533908</td>
      <td>58046131.0</td>
      <td>Olímpia</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3526902</td>
      <td>51232119.0</td>
      <td>Limeira</td>
    </tr>
  </tbody>
</table>
</div>



## Visualizações

### Ranking


```python
# Definindo o padrão das fontes
plt.rcParams["font.family"] = 'serif'

# Criando objetos da figura e eixo
fig, ax = plt.subplots(figsize = (9,7))

# Plotando
barras = ax.barh(y = df_nomes.index, width = df_nomes['quantidade_produzida'], color = '#1F77B4')
ax.invert_yaxis()

# Título
ax.set_title('10 maiores produtores de laranja no estado de SP (1974 - 2018)', fontsize = 15, loc = 'left')

# Eixo y
ax.set_yticks(np.arange(0,10))
ax.set_yticklabels(df_nomes['nome'])

# Eixo x
xtick_labels = np.arange(0, 90, step = 10)
ax.set_xticklabels(xtick_labels)
ax.set_xlabel('Produção (bilhões de toneladas)', fontsize = 13)

# Spines
spines = ['left', 'right', 'top']
for spine in spines:
    ax.spines[spine].set_visible(False)
    
# Valor da produção na frente da barra
for barra in barras:
    largura = barra.get_width()
    ax.text(x = largura + 1000000, y = barra.get_y() + barra.get_height()/2, s = round(largura / 1000000, 2))
    
# Coluna Araraquara
barras[6].set_color('darkorange')

plt.show()
```


    
![png](output_30_0.png)
    



```python
fig.savefig('ranking_cidades.jpg', edgecolor='none', bbox_inches = 'tight', facecolor = fig.get_facecolor())
```
