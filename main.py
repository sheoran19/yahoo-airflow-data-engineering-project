from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from typing import Annotated
import os
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from pydantic import BaseModel, validator
from fastapi.responses import HTMLResponse

load_dotenv()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class YahooData(BaseModel):

    id: int
    affiliate: str
    domain: str
    date: date
    hour: int
    partner: str
    market: str
    source_tag: str
    device: str
    type_tag: str
    searches: int
    bidded_clicks: int
    est_revenue: float
    mq_revenue: float
    revenue: float
    tq_score: int


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

SECRET_KEY = os.getenv("SECRET_KEY")


@app.get("/", summary="API Homepage", response_class=HTMLResponse)
async def read_home():
    html_content = """
    <html>
        <head>
            <title>Yahoo Hourly Data API</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    background-color: #FAFAFA;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1, h2 {
                    color: #0277BD; /* Consistent blue for headings */
                }
                .title-status, .status {
                    padding: 5px 10px;
                    border-radius: 5px;
                    display: inline-block;
                    margin-bottom: 10px;
                }
                .title-status {
                    background-color: #E1F5FE; /* Very light blue */
                    color: #01579B; /* Dark blue */
                    font-size: 24px;
                }
                .status {
                    background-color: #FFF3E0; /* Very light orange */
                    color: #FF9800; /* Orange */
                    font-size: 16px; /* Smaller font size for a minimalist look */
                    padding: 3px 8px; /* Reduced padding */
                }
                .live {
                    background-color: #E8F5E9; /* Very light green */
                    color: #4CAF50; /* Green */
                }
                a {
                    color: #0277BD;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin-bottom: 5px;
                }
                .under-development {
                    font-weight: bold;
                }
                p, li {
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <h1 class="title-status">Yahoo Hourly Data API</h1>
            <p>Welcome to the Yahoo Hourly Data API.  Current version: 1.0.1</p>
            
            <h2>Available Endpoints:</h2>
            <ul>
                <li>/api/daily: Fetch hourly data for a specific date. <span class="live">(Live)</span></li>
                <li>/api/dates: Fetch data within a specific date range. <span class="live">(Live)</span></li>
            </ul>

            <h2>Docs:</h2>
            <ul>
                <li>Use the API documentation for detailed information about each endpoint.</li>
                <li>Ensure to pass the correct 'secret_key' as a query param for authentication.</li>
                <li>Check the date and hour formats when making requests to the endpoints.</li>
                <li>Visit <a href="/docs">/docs</a> or <a href="/redoc">/redoc</a> for interactive API documentation.</li>
            </ul>
            
             <h2>Report Issues:</h2>
            <p>If you encounter any issues or have feedback, please don't hesitate to contact us at <a href="mailto:deepak@mquestgroup.com">deepak@mquestgroup.com</a>.</p>
            
            <h2 class="status">Status: Under Development</h2>
            <p>This API is currently under development. Features and endpoints may change. Please check back for updates.</p>
                   
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/dates", summary="Fetch data within a date range")

async def fetch_data_within_date_range(secret_key: str,start_date: date, end_date: date, db: db_dependency):
    """
    Fetches data from YahooHourly model within a specified date range.
    The date range should be within the last 14 days and the start date
    should be before the end date.

    - secret_key: str - A secret key for API authentication
    - start_date: date - The start date of the date range
    - end_date: date - The end date of the date range
    """
    if secret_key != SECRET_KEY:
        return {"error": "Unauthenticated: Access Token Expired or Invalid!"}

    result = db.query(models.YahooHourly).filter(
        models.YahooHourly.date >= start_date,
        models.YahooHourly.date <= end_date
    ).all()

    if not result:
        raise HTTPException(status_code=404, detail="No records found for the specified date range.")

    return result


@app.get("/api/daily", summary="Fetch hourly data for a specific date")
async def fetch_data(
        secret_key: str,date: date,hour: int, db: db_dependency):
    """
    Fetches hourly data from the YahooHourly model for a specific date and hour.

    - secret_key: str - A secret key for API authentication provided in the header.
    - date: date - The date for which to fetch the data.
    - hour: int - The hour for which to fetch the data (0-23).
    """
    if secret_key != SECRET_KEY:
        return {"error": "Unauthenticated: Access Token Expired or Invalid!"}

    result = db.query(models.YahooHourly).filter(
        models.YahooHourly.date == date,
        models.YahooHourly.hour == hour
    ).all()

    if not result:
        raise HTTPException(status_code=404, detail="No records found for the specified date and hour.")

    return result
