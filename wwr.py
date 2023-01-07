from requests import get
from bs4 import BeautifulSoup


def extract_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
  response = get(f"{base_url}{keyword}")
  if response.status_code != 200:  # 신호 확인 = 정상 응답 신호는 200 / 여기서는 200이 아닐 경우, 즉 정상 응답 아닌 경우
    print("Can't request website")
  else:
    results = []
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all('section', class_="jobs")  # section에서 job부분만 찾기
    for job_section in jobs:
      job_posts = job_section.find_all('li')  # section 칸에서 li만 찾기
      job_posts.pop(-1)  # 마지막에 있는 View all 버튼 제거
      for post in job_posts:
        anchors = post.find_all('a')  # html내의 모든 a 태그 검색
        anchor = anchors[1]  # 0번째 a가 tool tip이기에 필요 없다 판단 후 1번째 a만 가져옴
        link = anchor['href']  # 회사 링크
        company, kind, region = anchor.find_all(
          'span', class_='company')  # span 안의 company class가 3개기에 나눠서 변수로 저장
        title = anchor.find('span', class_='title')
        job_data = {
          'link': f"https://weworkremotely.com{link}",
          'company': company.string.replace("", " "),
          'kind': kind.string.replace("", " "),
          'location': region.string.replace("", " "),
          'position': title.string.replace("", " ")  # ,(콤마를 공백으로 대체시켜 포함 X
        }
        results.append(job_data)

      return results
