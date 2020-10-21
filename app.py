import os
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.cnb_model import CNBDescriptionClf
from server.schemas.prediction import (
    PredictIn,
    PredictOut,
)

app = FastAPI()
clf = CNBDescriptionClf()

router = APIRouter()

if os.environ.get("PYTHON_ENV") == "production":
    @app.get("/")
    def index():
        project_path = Path(__file__).parent.resolve()
        static_root = project_path / "client/build"
        return FileResponse(str(static_root) + '/index.html', media_type='text/html')

@router.get("/")
def index():
    return {"Hello": "World"}


@router.post("/predict/", response_model=PredictOut)
async def predict(predict_in: PredictIn) -> PredictOut:
    """Predict most probable incident types from input string.

    Args:
        predict_in (PredictIn): Input text and number of predictions to return.

    Returns:
        PredictMultiOut: JSON containing input text and predictions with their
        probabilities.
    """
    input_string = predict_in.text
    num_predictions = predict_in.num_predictions
    [predictions] = clf.predict_multiple([input_string], num_predictions)
    predictions = [(pred[0].value, pred[1]) for pred in predictions]
    return PredictOut(input_text=input_string, predictions=predictions)


@router.post("/submit/")
async def submit_form(xml_file: UploadFile = File(...)):
    return {"detail": "A"}

# if (process.env.NODE_ENV === "production") {
#   const path = require("path");
#   const root = path.join(__dirname, "..", "build");
#   app.use(express.static(root));
#   app.get("*", (req, res) => {
#     res.sendFile("index.html", { root });
#   });
# }
if os.environ.get("PYTHON_ENV") == "production":
    project_path = Path(__file__).parent.resolve()
    static_root = project_path / "client/build/static"
    app.mount("/static", StaticFiles(directory=static_root), name="static")
    app.include_router(router, prefix="/api")
