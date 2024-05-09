from dependency_injector import containers, providers
from data.database import Database, DatabaseOptions
from data.repositories import CompanyRepository, CompanySettingRepository, FileRepository, MessageHistoryRepository, RequirementRepository
from services import CompanyService, ConfigService, FileService, LibraryReaderService, Chatbot, FunctionService, RequirementService
from services.message_service import MessageService
from services.gupshup_service import GupshupService
from services.assistant_service import AssistantService
from services.single_request_service import SingleRequestService
import os
from core.logging.solomind_logger import SolomindLogger, SolomindLoggerOptions
class Container(containers.DeclarativeContainer):
    folder_path = os.path.dirname(os.path.abspath(__file__))
    path_to_config = os.path.join(folder_path, '..', 'app_settings.yml')
    config = providers.Configuration(yaml_files=[path_to_config])

    log_file_path = config.logging.file_path 
    log_level = config.logging.log_level

    logger = providers.Singleton(SolomindLogger, options = SolomindLoggerOptions(log_file_path=log_file_path, log_level = log_level))
 
    db = providers.Singleton(Database, solomind_logger = logger, options = DatabaseOptions(config.db.url, config.db.echo))

# register repositories
    company_repository = providers.Factory(CompanyRepository, session_factory = db.provided.session, logger=logger)
    company_setting_repository = providers.Factory(CompanySettingRepository , session_factory = db.provided.session, logger=logger)
    file_repository = providers.Factory(FileRepository, session_factory = db.provided.session, logger=logger)
    requirement_repository = providers.Factory(RequirementRepository, session_factory = db.provided.session, logger=logger)
    message_history_repository = providers.Factory(MessageHistoryRepository, session_factory = db.provided.session, logger=logger)
# register services
    config_service = providers.Factory(ConfigService)
    company_service = providers.Factory(CompanyService
                                        , company_repository = company_repository              
                                        , company_setting_repository = company_setting_repository)
    
    file_service = providers.Factory(FileService, file_repository = file_repository)
    library_reader_service = providers.Factory(LibraryReaderService, file_repository = file_repository)
    chat_service = providers.Factory(Chatbot, config_service=config_service, library_reader_service = library_reader_service, logger=logger)
    function_service = providers.Factory(FunctionService)
    requirement_service = providers.Factory(RequirementService, requirement_repository = requirement_repository)
    assistant_service = providers.Factory(AssistantService, logger=logger)
    single_request_service = providers.Factory(SingleRequestService, company_service=company_service, logger=logger, config_service=config_service)

    message_service = providers.Factory(MessageService, company_service=company_service 
                                        ,message_history_repository=message_history_repository
                                        ,config_service=config_service
                                        ,assistant_service=assistant_service)
    gupshup_service = providers.Factory(GupshupService, message_service=message_service, config_service=config_service, logger=logger)
