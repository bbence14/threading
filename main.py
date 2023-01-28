import time

from multiprocessing import Queue

from workers.WikiWorker import WikiWorker
from workers.YahooFinancePriceWorker import YahooFinancePriceScheduler
from workers.PostgresWorker import PostgresMasterScheduler

from yaml_reader import YamlPipelineExecutor


def main():
    pipeline_location = 'pipelines/wiki_yahoo_scraper_pipeline.yaml'
    scraper_start_time = time.time()
    yamlPipelineExecutor = YamlPipelineExecutor(pipeline_location=pipeline_location)
    yamlPipelineExecutor.process_pipeline()

    print('Extracting time took: ', round(time.time() - scraper_start_time))


if __name__ == '__main__':
    main()
