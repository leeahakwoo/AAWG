from fastapi import APIRouter
router = APIRouter()
@router.post("", response_model=TraceabilityDefinitionOutput)
async def make_traceability(...):
    ...
