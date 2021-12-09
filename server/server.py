import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from starlette import status

from pre_processing.index import SearchField, get_documents_for_query, rank_documents, retrieve_docs_information


def main():
    main_app = FastAPI(title="Wine Google")

    @main_app.get('/search/', status_code=status.HTTP_200_OK)
    def search(query: str, field: SearchField, use_tf_idf: bool = False):
        now = datetime.now()
        docs = get_documents_for_query(query, field)
        ranked_docs = rank_documents(docs, use_tf_idf)
        result = retrieve_docs_information(ranked_docs)
        print(datetime.now() - now)
        return {'number_docs': len(docs), 'docs_information': result}

    @main_app.on_event('startup')
    async def startup():
        pass

    @main_app.on_event('shutdown')
    async def shutdown():
        pass

    return main_app


if __name__ == '__main__':
    uvicorn.run(main(), host='0.0.0.0')
