from bs4 import BeautifulSoup
import requests

def find_jobs():
    html_text = requests.get(
        'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords=java&cboWorkExp1=-1&txtLocation=').text

    soup = BeautifulSoup(html_text, 'lxml')
    job_list = soup.find('ul', id='jobsListULid')
    jobs_list = job_list.find_all('li')

    for job in jobs_list:
        # Get job title
        title_text = job.find('h3')
        job_title = title_text.text.strip() if title_text else 'N/A'

        # Get company name
        company = job.find('span', class_='srp-comp-name')
        company_name = company.text.strip() if company else 'N/A'

        # Get location
        location_name = job.find('div', class_='srp-loc')
        location = location_name.text.strip() if location_name else 'N/A'

        # Get experience
        exp_text = job.find('div', class_='srp-exp')
        experience = exp_text.text.strip() if exp_text else 'N/A'

        # Get skills - find the skills div
        skills_div = job.find('div', class_='srp-keyskills')

        job_title_link = job.find('h3').find('a') if job.find('h3') else None
        job_url = job_title_link['href'] if job_title_link else 'N/A'

        if job_title == 'N/A' and company_name == 'N/A':
            continue

        if skills_div:
            # Get all skill links inside
            skill_tags = skills_div.find_all('a', class_='srphglt')
            # Extract text from each skill
            skills_text = [skill.text.strip() for skill in skill_tags]
            skills = ', '.join(skills_text)
        else:
            continue
            skills_text = 'N/A'

        print(f"Title: {job_title}")
        print(f"Company: {company_name}")
        print(f"Location: {location}")
        print(f"Experience: {experience}")
        print(f"Skills: {skills}")
        print(f"URL: {job_url}")
        print("-" * 400)


if __name__ == "__main__":
    find_jobs()
    print("Done")
    print("Done")