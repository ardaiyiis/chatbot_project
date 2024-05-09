import json
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from fastapi import Request
from starlette.responses import Response, PlainTextResponse
from starlette.types import ASGIApp
from core.models import ApiResponse, Error
from core.exceptions import DataException
import environment
import logging
from starlette.types import Message

class ResponseWrapper(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
    
    logger:logging.Logger = None
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            self.logger = request.app.container.logger().get_logger(__name__)
            self.show_exception_info = self.logger.level == logging.DEBUG or self.logger.level == logging.ERROR

            check_json = check_docs = False
            if environment.DEBUG:
                check_docs = f'{request.base_url}docs' == request.url
                check_json = f'{request.base_url}openapi.json' == request.url
            methods = ['GET', 'PUT', 'POST','DELETE']
            if(not check_docs and not check_json and request.method in methods):
                return await self.__wrap_response(request, call_next)
            else:
                return await call_next(request)

        except DataException as data_ex:
            return self.__handle_data_exceptions(data_ex)
        except Exception as ex:
            return self.__handle_exceptions(ex)

    async def __wrap_response(self, request:Request, call_next: RequestResponseEndpoint) -> Response:
        
        if request.url.path == '/api/message/gupshup-webhook':
            return await call_next(request)

        await self.__write_request_log(request)

        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        api_response = ApiResponse(json.loads(response_body), None).__dict__
        new_response = Response(content=json.dumps(api_response), status_code = response.status_code, headers=dict(response.headers), media_type = response.media_type)
        new_response.headers['Content-Length'] = str(new_response.body.__len__())
        
        self.logger.info(f"Response Status : {new_response.status_code }")
        return new_response
    
    def __handle_data_exceptions(self, exception:DataException) -> Response:
        api_response = ApiResponse(None, Error(exception.message, exception.error_code).__dict__).__dict__
        response = Response(content=json.dumps(api_response), status_code = 200)
        self.logger.error(f'Exception Message:{exception}',  exc_info=self.show_exception_info)
        return response
    
    def __handle_exceptions(self, exception:Exception) -> Response:
        api_response = ApiResponse(None, Error('Internal Server Error', 500).__dict__).__dict__
        response = Response(content=json.dumps(api_response), status_code = 200)
        print(exception)
        self.logger.exception(f'Exception:{exception}', exc_info=self.show_exception_info)
        return response
        #raise exception

    async def __write_request_log(self, request:Request):
        await self.set_body(request, await request.body())
        request_body = await self.get_body(request)
        
        query_params = f", PATH PARAMETERS:{request.query_params._dict}" if request.query_params.__len__()>0 else ""
        path_params  =  f", QUERY PARAMETERS:{request.path_params}" if request.path_params.__len__()>0 else ""
        self.logger.info(f'{request.url}, {request.method}, BODY:{json.loads(request_body)}{path_params}{query_params}, CLIENT: {request.client.host}')

        
    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {"type": "http.request", "body": body}
        request._receive = receive
    
    async def get_body(self, request: Request) -> bytes:
        body = await request.body()
        await self.set_body(request, body)
        return body