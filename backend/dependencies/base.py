from ..services.Email import EmailService
from ..services.Parser import ParserService
from ..services.ProjectIo import ProjectIoService
from ..services.instagram.instagram_service import InstagramService
from ..services.openai.Prompter import PrompterService


def __init__():
    pass


def get_email_service():
    return EmailService()


def get_parser_service():
    return ParserService()


def get_project_io_service():
    return ProjectIoService()


def get_prompter_service():
    return PrompterService()


def get_instagram_service():
    return InstagramService()
