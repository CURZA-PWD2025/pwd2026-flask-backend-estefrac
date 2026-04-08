from abc import ABC, abstractmethod
from flask import Response

class ControllerInterface (ABC):
    
    @staticmethod
    @abstractmethod
    def get_all() ->tuple[Response, int]:pass
    
    @staticmethod
    @abstractmethod
    def show(id:int)->tuple[Response, int]:pass
    
    @staticmethod
    @abstractmethod
    def create(request)->tuple[Response, int]:pass
    
    @staticmethod
    @abstractmethod
    def update(request:dict, id:int)->tuple[Response, int]:pass
    
    @staticmethod
    @abstractmethod
    def destroy(id:int)->tuple[Response, int]:pass
    