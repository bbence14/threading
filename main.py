import os
import time

from yaml_reader import YamlPipelineExecutor


def main():
    pipeline_location = os.environ.get('PIPELINE_LOCATION')
    if pipeline_location is None:
        print('pipeline location is not defined')
        exit(1)
    scraper_start_time = time.time()
    yamlPipelineExecutor = YamlPipelineExecutor(pipeline_location=pipeline_location)
    yamlPipelineExecutor.start()
    yamlPipelineExecutor.join()
    print('Extracting time took: ', round(time.time() - scraper_start_time))


if __name__ == '__main__':
    main()
