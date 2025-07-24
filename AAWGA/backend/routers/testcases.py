from fastapi import APIRouter
router = APIRouter()
@router.post("", response_model=TestcaseDefinitionOutput)  # 등등
async def create_testcases(...):
    ...
