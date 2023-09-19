from pydantic import BaseModel, PastDatetime


class MongoDBLog(BaseModel):
    created: PastDatetime
    args: dict = {}
    filename: str
    levelname: str
    func_name: str
    lineno: int
    msg: str
    name: str
    pathname: str