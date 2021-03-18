import os
from os import listdir
from os.path import isfile, join
import shutil
from pyspark.sql import SQLContext, SparkSession

ss = SparkSession.builder\
    .appName("Projeto") \
    .getOrCreate()


sql_context = SQLContext(ss)


def ler_csv(fpath):
    return sql_context.read \
        .options(header='True', inferSchema='True', delimiter="^") \
        .csv(fpath)


def escrever_csv(dataset, outputpath):
    # Padroniza headers maiusculos
    for col in dataset.columns:
        if not col.isupper():
            dataset = dataset.withColumnRenamed(col, col.upper())

    dataset.repartition(1).write \
            .format("com.databricks.spark.csv") \
            .option("header", "true") \
            .option("delimiter", "^") \
            .option("dateFormat", "yyyy-MM-dd") \
            .option("timestampFormat", "yyyy-MM-dd") \
            .mode('overwrite') \
            .save(outputpath)

    # Renomeia o csv da particao do spark, e move uma pasta para cima
    # deletando a pasta transitoria
    handle_spark_csv_output(outputpath)


def handle_spark_csv_output(path):
    try:
        for f in listdir(path):
            if isfile(join(path, f)) and f.endswith(".csv"):
                os.rename(join(path, f), f'{path}.csv')
                remove_buggy_chars(f'{path}.csv')
            else:
                os.remove(join(path, f))

        shutil.rmtree(path)
    except Exception as e:
        print(e)

    
def remove_buggy_chars(filepath):
    with open(filepath) as fp:
        with open(filepath.replace('.csv', '.csv.fix'), 'a') as new_file:
            line = fp.readline()
            while line:
                fixed_line = line.replace('\\\\', '').replace('"', '').replace('\n', '')
                new_file.write(f'{fixed_line}\n')
                line = fp.readline()

    os.remove(filepath)
    os.rename(filepath.replace('.csv', '.csv.fix'), filepath.replace('.fix', ''))


def fix_folder_path(fpath):
    return fpath if fpath.endswith('/') else f'{fpath}/'