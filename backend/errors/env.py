from .base import StocklyError


class CredentialsNotSuppliedError(StocklyError):
    """
    Error for case where credentials are not supplied.

    Parameters
    ----------
    StocklyError : stockly error
        base stockly error.
    """

    def __init__(self, missing_credentials: list[str]):
        super().__init__(errors={"missing credentials": missing_credentials}, error_code=400)


class EnvironmentVariableNotSuppliedError(StocklyError):
    """
    Error when environment variable is not supplied.

    Parameters
    ----------
    StocklyError : stockly error
        base stockly error.
    """

    def __init__(self, missing_variables: list[str]):
        super().__init__(errors={"missing variables": missing_variables}, error_code=400)
