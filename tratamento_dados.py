from sparkutil import *

dataset = ler_csv("asteroide_unido.csv")
dataset.createOrReplaceTempView('DATASET')

dataset = sql_context.sql(
    """
        SELECT * FROM DATASET
        WHERE ALBEDO IS NOT NULL
        AND DIAMETER IS NOT NULL
    """
)

dataset = dataset.drop('NEO').drop('PHA')

escrever_csv(dataset, "asteroide_unido_tratado")

from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.read_csv("asteroide_unido_tratado.csv", \
    sep="^", \
    encoding="utf-8", \
    low_memory=False)

df_normalizado = StandardScaler().fit_transform(df)

df.to_csv("asteroide_unido_tratado_normalizado.csv", sep='^', index=False)

#####################
from sparkutil import *

dataset = ler_csv("arq.csv")
dataset.createOrReplaceTempView('DATASET')

dataset = sql_context.sql(
    """
        SELECT * FROM DATASET
        WHERE CAST(DIAMETER AS float) > 0.0
    """
)

dataset = dataset.drop('NEO').drop('PHA')

escrever_csv(dataset, "arq_corrigido_diametro")
