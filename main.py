from flask import Flask, render_template, request, redirect, send_file
from source.indeed import scrap_indeed_pages
from source.wwr import extract_jobs
from file import save_to_file

app = Flask("JobScrapper")


@app.route("/")
def first():
  return render_template("home.html", name="SeungMin")


db = {}  #fake database


@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword in db:  # 만약 keyword로 검색한 값이 존재한다면 db에서 저장된 값을 리턴해 줘서 다음 새로고침 때는 더빠르게 응답해 줄 수 있음
    jobs = db[keyword]
  else:  # 빈 칸이면 서칭
    indeed = scrap_indeed_pages(keyword)
    wwr = extract_jobs(keyword)
    jobs = indeed + wwr
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:  # 스킵한 경우
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])  # file이름, jobs list
  return send_file(f"{keyword}.csv",
                   as_attachment=True)  # as_attachment = 파일 다운로드 해주는 function


app.run("0.0.0.0")
