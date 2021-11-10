from bs4 import BeautifulSoup
from classifier_results.models_result import naive_bayer, mlp, svm, decision_tree, logistic_regression


def extract(domain, extract_function):
    results = [naive_bayer, mlp, svm, decision_tree, logistic_regression]
    for result in results:
        for index in result[domain]:
            try:
                html_file = open('../crawler/bfs_pages/{}/{}.html'.format(domain, index))
                html_text = html_file.read()
                soup = BeautifulSoup(html_text, 'lxml')
                print(index, extract_function(soup))
            except:
                print('failed to open ../crawler/bfs_pages/{}/{}.html'.format(domain, index))
