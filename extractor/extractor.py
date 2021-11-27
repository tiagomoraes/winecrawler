import json
import os

from bs4 import BeautifulSoup
from classifier_results.models_result import naive_bayer, mlp, svm, decision_tree, logistic_regression
import matplotlib.pyplot as plt
import pandas as pd

classifiers = [naive_bayer, mlp, svm, decision_tree, logistic_regression]


def get_classifier_name(index):
    if index == 0:
        return 'naive_bayer'
    if index == 1:
        return 'mlp'
    if index == 2:
        return 'svm'
    if index == 3:
        return 'decision_tree'
    if index == 4:
        return 'logistic_regression'


def plot_table(path, data):
    fig, ax = plt.subplots(1, 1)
    column_labels = ['Total Pages', 'Precision', 'Recall', 'Accuracy']
    df = pd.DataFrame(data, columns=column_labels)
    ax.axis('tight')
    ax.axis('off')
    ax.table(
        cellText=df.values,
        colLabels=df.columns,
        rowLabels=['naive_bayer', 'mlp', 'svm', 'decision_tree', 'logistic_regression'],
        loc="center"
    )

    plt.savefig(path)


def save_to_file(path, data):
    results_file = open(path, 'w')
    results_file.write(json.dumps(data))


def extract(domain, type, extract_function):
    classifier_index = 0
    extraction_results_metrics = []
    extraction_results = []
    negative_pages_extraction_results = []
    total_pages = 1001
    pages = [i for i in range(total_pages)]
    for classifier in classifiers:
        print(
            'running extraction from classifier {} for domain {}'.format(get_classifier_name(classifier_index), domain))
        total_pages_for_classifier = len(classifier[domain])
        total_pages_extracted_successfully = 0  # true positive
        total_negative_pages_extracted_succesfully = 0  # false negative
        positive_pages = classifier[domain]
        for index in positive_pages:
            try:
                html_file = open('../crawler/bfs_pages/{}/{}.html'.format(domain, index + 1))
                html_text = html_file.read()
                soup = BeautifulSoup(html_text, 'lxml')
                extract_result = extract_function(soup)
                extraction_results.append(extract_result)
                if extract_result['wine_type'] is not None and extract_result['wine_type'] != '':
                    total_pages_extracted_successfully += 1
            except:
                print('failed to open ../crawler/bfs_pages/{}/{}.html'.format(domain, index + 1))

        negative_pages = list(set(pages) - set(positive_pages))
        for index in negative_pages:
            try:
                html_file = open('../crawler/bfs_pages/{}/{}.html'.format(domain, index + 1))
                html_text = html_file.read()
                soup = BeautifulSoup(html_text, 'lxml')
                negative_pages_extract_result = extract_function(soup)
                negative_pages_extraction_results.append(negative_pages_extract_result)
                if negative_pages_extract_result['wine_type'] is not None and negative_pages_extract_result[
                    'wine_type'] != '':
                    total_negative_pages_extracted_succesfully += 1
            except:
                print('failed to open ../crawler/bfs_pages/{}/{}.html'.format(domain, index + 1))

        false_positive = total_pages_for_classifier - total_pages_extracted_successfully
        true_negative = total_pages - total_negative_pages_extracted_succesfully
        precision = (total_pages_extracted_successfully / total_pages_for_classifier) * 100
        recall = 0
        if total_pages_extracted_successfully + total_negative_pages_extracted_succesfully > 0:
            recall = (total_pages_extracted_successfully / (
                    total_pages_extracted_successfully + total_negative_pages_extracted_succesfully)) * 100

        accuracy = 0
        if true_negative + false_positive + total_pages_extracted_successfully + total_negative_pages_extracted_succesfully > 0:
            accuracy = ((true_negative + total_pages_extracted_successfully) / (
                    true_negative + false_positive + total_pages_extracted_successfully + total_negative_pages_extracted_succesfully)) * 100

        extraction_results_metrics.append([
            total_pages_for_classifier,
            precision,
            recall,
            accuracy,
        ])
        classifier_index += 1

    plot_table('./results/{}_{}_metrics.png'.format(domain, type), extraction_results_metrics)
    save_to_file('./results/{}_{}.json'.format(domain, type), extraction_results)
    save_to_file('./results/{}_{}_negative.json'.format(domain, type), negative_pages_extraction_results)


def is_valid_extraction(result) -> bool:
    if result['name'] is None or result['name'] == "":
        return False

    if result['grape'] is None or result['grape'] == "":
        return False

    if result['country'] is None or result['country'] == "":
        return False

    if result['alcohol_content'] is None or result['alcohol_content'] == "":
        return False

    if result['wine_type'] is None or result['wine_type'] == "":
        return False

    return True


def extract_positive_samples(domain, pages, extract_function):
    extraction_results = []
    for index in pages:
        html_file = open('../classification/samples/samples_pages/{}_{}.html'.format(domain, index))
        html_text = html_file.read()
        soup = BeautifulSoup(html_text, 'lxml')

        result = extract_function(soup)
        if is_valid_extraction(result):
            extraction_results.append(result)
        else:
            extraction_results.append(None)

    save_to_file('./results/sample_pages/{}.json'.format(domain), extraction_results)


def extract_classifier_results(domain, extract_function):
    domain_indexes = {
        'adegamais': 0,
        'divinho': 1,
        'divvino': 2,
        'evino': 3,
        'grandcru': 4,
        'mistral': 5,
        'superadega': 6,
        'viavini': 7,
        'vivavinho': 8,
        'wine': 9
    }

    extraction_results = []
    positive_pages = logistic_regression[domain]
    domain_index = domain_indexes[domain]
    for index in positive_pages:
        try:
            page_index = (1000 * domain_index) + index + 1
            html_file = open('./pages/{}.html'.format(page_index))
            html_text = html_file.read()
            soup = BeautifulSoup(html_text, 'lxml')

            result = extract_function(soup)
            if is_valid_extraction(result):
                extraction_results.append({page_index: result})
            else:
                extraction_results.append({page_index: None})
        except:
            extraction_results.append({page_index: None})

    save_to_file('./results/logistic_classifier/{}.json'.format(domain), extraction_results)


def delete_unused_pages():
    pages = [i for i in range(1001)]
    domains = ['adegamais', 'divinho', 'divvino', 'evino', 'grandcru', 'mistral', 'superadega', 'viavini', 'vivavinho',
               'wine']
    for domain in domains:
        positive_pages = logistic_regression[domain]
        negative_pages = list(set(pages) - set(positive_pages))

        for index in negative_pages:
            try:
                os.rename('./pages/{}/{}.html'.format(domain, index + 1))
            except:
                print('not found')


def rename_pages():
    domains = ['adegamais', 'divinho', 'divvino', 'evino', 'grandcru', 'mistral', 'superadega', 'viavini', 'vivavinho',
               'wine']

    domain_index = 0
    for domain in domains:
        positive_pages = logistic_regression[domain]

        for index in positive_pages:
            try:
                os.rename('./pages/{}/{}.html'.format(domain, index + 1), './pages/{}/{}.html'.format(domain, (1000 * domain_index) +index + 1))
            except:
                print('not found')

        domain_index += 1


if __name__ == '__main__':
    rename_pages()
