import requests
from config import Config

def get_jobs(search="Python Developer", location="India"):

    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": Config.ADZUNA_APP_ID,
        "app_key": Config.ADZUNA_APP_KEY,
        "results_per_page": 20,
        "what": search,
        "where": location,
        "content-type": "application/json"
    }

    try:

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

        jobs = []

        for job in data.get("results", []):

            jobs.append({
                "title": job.get("title", "Not Available"),
                "company": job.get("company", {}).get("display_name", "Unknown Company"),
                "location": job.get("location", {}).get("display_name", "Not Mentioned"),
                "salary": job.get("salary_is_predicted", "Not Mentioned"),
                "description": job.get("description", "")[:250],
                "redirect_url": job.get("redirect_url")
            })

        return jobs

    except Exception as e:
        print(e)
        return []