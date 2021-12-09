import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Query
from starlette import status

from pre_processing.index import SearchField, get_documents_for_query, rank_documents, retrieve_docs_information, \
    SearchResponse, has_next_page


def main():
    main_app = FastAPI(title="Wine Google")

    @main_app.get('/search/', response_model=SearchResponse, status_code=status.HTTP_200_OK, tags=['Wine'])
    def search(query: str, field: SearchField, use_tf_idf: bool = False, page: int = Query(1, gt=0),
               page_size: int = Query(10, gt=0, le=10)):
        docs_with_frequency = get_documents_for_query(query, field)
        total_number_of_docs = len(docs_with_frequency)

        ranked_docs = rank_documents(docs_with_frequency, use_tf_idf)
        result = retrieve_docs_information(ranked_docs, page_size, page)
        return {
            'total_number_of_docs': total_number_of_docs,
            'has_next_page': has_next_page(total_number_of_docs, page_size, page),
            'docs_information': result
        }

    @main_app.on_event('startup')
    async def startup():
        pass

    @main_app.on_event('shutdown')
    async def shutdown():
        pass

    return main_app


if __name__ == '__main__':
    uvicorn.run(main(), host='0.0.0.0')
