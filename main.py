from fastapi import Depends, FastAPI, status
from fastapi.responses import HTMLResponse

from settings import Settings
from stockly.backend.dependencies.base import (
    get_aws_service,
    get_briefing_email_service,
    get_instagram_service,
    get_project_io_service,
    get_prompter_service,
    get_tnc_service,
)
from stockly.backend.errors.base import StocklyError
from stockly.backend.errors.project_io import ProjectIOError
from stockly.backend.services.aws.s3 import AWSService
from stockly.backend.services.instagram.instagram_service import InstagramService
from stockly.backend.services.openai.Prompter import PrompterService
from stockly.backend.services.ProjectIo import ProjectIoService
from stockly.backend.services.send_briefing_email_service import BriefingEmailService
from stockly.backend.terms_and_conditions import TermsAndConditionsService
from stockly.objects.api.response import ErrorResponse, SuccessResponse
from stockly.objects.models.aws_service import S3Object
from stockly.objects.requests.aws_service import DeleteImageRequest, UploadImageRequest
from stockly.objects.requests.generate_image import GenerateImageRequest
from stockly.objects.requests.send_briefing_email import SendEmailRequest

URL = "https://www.google.com/finance/quote/"


app = FastAPI()
settings = Settings().get_settings()


@app.get("/")
def home():
    """
    Default landing page for API.

    Returns
    -------
    SuccessResponse[str]
        hello world string.
    """
    return SuccessResponse(data="Stockly API is running.")


@app.post(
    path="/send_email",
    dependencies=[
        Depends(get_briefing_email_service),
    ],
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
    },
)
def send_email(
    param: SendEmailRequest,
    briefing_email_service: BriefingEmailService = Depends(get_briefing_email_service),
):
    """
    Send an email to the user with the stock analysis.

    Parameters
    ----------
    param : SendEmailRequest
        The request object containing the user requests.
    briefing_email_service : BriefingEmailService
        The briefing email service dependency, auto inject by FastAPI.

    Returns
    -------
    SuccessResponse[str]
        Email sent successfully.
    """
    try:
        briefing_email_service.send_briefing_email(param)

        return SuccessResponse(data="Email sent successfully.")
    except StocklyError as e:
        return ErrorResponse(error_code=e.error_code, error_message=str(e))


@app.post(
    path="/generate_image",
    dependencies=[
        Depends(get_prompter_service),
    ],
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
    },
)
def generate_image(
    param: GenerateImageRequest,
    prompter_service: PrompterService = Depends(get_prompter_service),
) -> SuccessResponse[str] | ErrorResponse:
    """
    Generate an image based on the text prompt.

    Parameters
    ----------
    param : GenerateImageRequest
        The request object containing the text prompt.
    prompter_service : PrompterService
        The prompter service dependency, auto inject by FastAPI.

    Returns
    -------
    SuccessResponse[str] | ErrorResponse
        Image generated.
    """
    try:
        image_url = prompter_service.generate_image_prompt(param)
        return SuccessResponse(data=image_url)
    except StocklyError as e:
        return ErrorResponse(error_code=e.error_code, error_message=str(e))


@app.post(
    path="/save_image",
    dependencies=[
        Depends(get_project_io_service),
    ],
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
    },
)
def save_image(
    url: str, project_io_service: ProjectIoService = Depends(get_project_io_service)
) -> SuccessResponse[str] | ErrorResponse:
    """
    Save an image to the project directory.

    Parameters
    ----------
    url : str
        The url of the image to save.
    project_io_service : ProjectIoService
        The project io service dependency, auto inject by FastAPI.
    """
    try:
        filename = project_io_service.download_image(url)
        return SuccessResponse(data=filename)
    except ProjectIOError as e:
        return ErrorResponse(error_code=e.error_code, error_message=str(e))


@app.post(
    path="/s3_image",
    dependencies=[
        Depends(get_aws_service),
    ],
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
    },
)
def upload_s3_image(
    param: UploadImageRequest, aws_service: AWSService = Depends(get_aws_service)
) -> SuccessResponse[S3Object] | ErrorResponse:
    """
    Upload an image to an S3 bucket.
    """
    try:
        s3_object = aws_service.upload_file(param)
        return SuccessResponse(data=s3_object)
    except Exception as e:
        return ErrorResponse(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_message=str(e)
        )


@app.delete(
    path="/s3_image",
    dependencies=[
        Depends(get_aws_service),
    ],
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
    },
)
def delete_s3_image(
    param: DeleteImageRequest, aws_service: AWSService = Depends(get_aws_service)
) -> SuccessResponse[str] | ErrorResponse:
    """
    Delete an image from an S3 bucket.
    """
    try:
        aws_service.delete_file(param)
        return SuccessResponse(data="Image deleted.")
    except Exception as e:
        return ErrorResponse(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_message=str(e)
        )


@app.post(
    path="/instagram_image",
    dependencies=[
        Depends(get_instagram_service),
    ],
    responses={
        200: {"model": SuccessResponse},
        400: {"model": ErrorResponse},
    },
)
def upload_instagram_image(
    url: str, instagram_service: InstagramService = Depends(get_instagram_service)
) -> SuccessResponse[str] | ErrorResponse:
    """
    Upload an image to Instagram.
    """
    try:
        instagram_service.publish_image(url)
        return SuccessResponse(data="Image uploaded to Instagram.")
    except Exception as e:
        return ErrorResponse(
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_message=str(e)
        )


@app.get(
    path="/privacy_policy",
    dependencies=[Depends(get_tnc_service)],
    response_class=HTMLResponse,
)
def get_privacy_policy(
    tnc_service: TermsAndConditionsService = Depends(get_tnc_service),
):
    """
    Get the privacy policy.
    """
    return HTMLResponse(
        status_code=status.HTTP_200_OK, content=tnc_service.get_privacy_policy()
    )


@app.get(
    path="/terms_of_service",
    dependencies=[Depends(get_tnc_service)],
    response_class=HTMLResponse,
)
def get_terms_of_service(
    tnc_service: TermsAndConditionsService = Depends(get_tnc_service),
):
    """
    Get the privacy policy.
    """
    return HTMLResponse(
        status_code=status.HTTP_200_OK, content=tnc_service.get_terms_of_service()
    )
