from fastapi import APIRouter
from services.pdfcreator import create_pdf
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/metrics",
    tags=["metrics", "pandas"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{chat_id}")
def metrics(chat_id):
    pdf = create_pdf()
    print("PDF: ", pdf)
    return StreamingResponse(pdf, media_type="application/pdf")

