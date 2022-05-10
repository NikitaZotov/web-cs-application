"""
    Author Zotov Nikita
"""
from ...services.query_service import QueryService
from ...services.crud_service import CRUDService
from ...services.file_service import FileService
from ...services.rdf.searcher import RdfModelSpecificationSearcher


class RdfServiceContainer:
    @staticmethod
    def get_crud_service() -> CRUDService:
        searcher = RdfModelSpecificationSearcher()
        return CRUDService(searcher)

    @staticmethod
    def get_file_service() -> FileService:
        return FileService()

    @staticmethod
    def get_query_service() -> QueryService:
        return QueryService()
