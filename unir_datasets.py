from sparkutil import *

dataset_1 = ler_csv("/home/cnmoro/Projetos/etl_projeto/dataset.csv")
dataset_1.createOrReplaceTempView('DATASET_1')

dataset_2 = ler_csv("/home/cnmoro/Projetos/etl_projeto/asteroid_dataset/Asteroid_Updated.csv")
dataset_2.createOrReplaceTempView('DATASET_2')

dataset_1 = sql_context.sql(
    """
        SELECT a,e,i,om,w,q,per_y,H,neo,pha,diameter,albedo,moid,n,per,ma
        FROM DATASET_1
    """
)

dataset_2 = sql_context.sql(
    """
        SELECT a,e,i,om,w,q,per_y,H,neo,pha,diameter,albedo,moid,n,per,ma
        FROM DATASET_2
    """
)

dataset_unido = dataset_1.union(dataset_2)

dataset_unido.show()

escrever_csv(dataset_unido, "asteroide_unido")