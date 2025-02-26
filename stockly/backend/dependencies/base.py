from stockly.backend.services.aws.s3 import AWSService
from stockly.backend.services.Email import EmailService
from stockly.backend.services.Parser import ParserService
from stockly.backend.services.ProjectIo import ProjectIoService
from stockly.backend.services.instagram.instagram_service import InstagramService
from stockly.backend.services.openai.Prompter import PrompterService


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


def get_aws_service():
    return AWSService()
