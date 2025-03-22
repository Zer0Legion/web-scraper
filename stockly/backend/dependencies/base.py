from stockly.backend.services.aws.s3 import AWSService
from stockly.backend.services.Email import EmailService
from stockly.backend.services.instagram.instagram_service import InstagramService
from stockly.backend.services.openai.Prompter import PrompterService
from stockly.backend.services.Parser import ParserService
from stockly.backend.services.ProjectIo import ProjectIoService
from stockly.backend.services.send_briefing_email_service import BriefingEmailService
from stockly.backend.terms_and_conditions import TermsAndConditionsService


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


def get_briefing_email_service():
    return BriefingEmailService(
        email_service=get_email_service(),
        parser_service=get_parser_service(),
        project_io_service=get_project_io_service(),
        prompter_service=get_prompter_service(),
    )


def get_tnc_service():
    return TermsAndConditionsService()
