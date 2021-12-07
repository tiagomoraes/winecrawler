from fastapi import FastAPI
from starlette import status

from pre_processing.index import SearchField, get_documents_for_query


def main():
    main_app = FastAPI(title="Wine Google")

    @main_app.get('/search/', status_code=status.HTTP_200_OK)
    def search(query: str, field: SearchField):
        docs = get_documents_for_query(query, field)
        pass

    @main_app.on_event('startup')
    async def startup():
        pass

    @main_app.on_event('shutdown')
    async def shutdown():
        pass

    return main_app


app = main()
