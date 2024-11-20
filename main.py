from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import requests
import os
app = FastAPI()
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not specified
    uvicorn.run(app, host="0.0.0.0", port=port)
class WorklogQuery(BaseModel):
    # api_base_url: str
    # api_token: str
    from_date: str = "2021-01-01"  # Default value if not provided
    to_date: str = "2025-01-31"    # Default value if not provided

api_token = os.getenv('API_TOKEN')
# Assume this is a dictionary mapping classification to hourly rate
# In a real application, this could come from a database or a secure config file
rate_info = {
    'Employee': 50,  # $50 per hour for employees
    'Contractor': 75  # $75 per hour for contractors
}



def fetch_worklogs(from_date, to_date):
    api_base_url = "https://api.us.tempo.io/4"
    url = f"{api_base_url}/worklogs?from={from_date}&to={to_date}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        worklogs = response.json()
        # Simulate adding classification and hours worked
        for log in worklogs.get('results', []):
            log['classification'] = 'Employee'  # or 'Contractor'
            log['hours_worked'] = log['billableSeconds']/3600  
            log['total_billing_in_$'] =log['hours_worked']*rate_info.get(log['classification'], 0)
        return worklogs.get('results', [])
    else:
        print(f"Failed to fetch worklogs. Status Code: {response.status_code}")
        return None



def calculate_accruals(worklogs):
    total_accrual = 0
    for log in worklogs:
        rate = rate_info.get(log['classification'], 0)  # Get the hourly rate based on classification
        total_accrual += rate * log['hours_worked']  # Calculate total cost
    return total_accrual



@app.post("/fetch_worklogs/")
async def post_fetch_worklogs(query: WorklogQuery):
    results = fetch_worklogs(query.from_date, query.to_date)
    print(results)
    if results is None:
        raise HTTPException(status_code=404, detail="Failed to fetch worklogs")
    total_accrual = calculate_accruals(results)
    return {"worklogs": results, "total_accrual": total_accrual}


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# Assuming the 'static' folder and 'app.py' or 'main.py' are at the same level
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('templates/index.html')



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not specified
    uvicorn.run(app, host="0.0.0.0", port=port)
