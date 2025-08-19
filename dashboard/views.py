from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io, urllib, base64
from sklearn.datasets import load_iris


def home(request):
    return render(request, "dashboard/home.html")


def upload(request):
    preview = None
    img_tag = None

    if request.method == "POST":
        uploaded_file = request.FILES['file']

        # 파일 크기 제한 (10MB)
        max_size = 10 * 1024 * 1024
        if uploaded_file.size > max_size:
            return HttpResponse("⚠️ 파일이 10MB를 초과했습니다.")

        # 확장자 제한
        if not uploaded_file.name.endswith('.csv'):
            return HttpResponse("❌ CSV 파일만 업로드 가능합니다!")

        # CSV 읽기
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8", on_bad_lines="skip")
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="cp949", on_bad_lines="skip")

        # 데이터 미리보기
        preview = df.head().to_html()

        # 첫 번째 숫자형 컬럼으로 그래프 생성
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            plt.figure(figsize=(6, 4))
            df[numeric_cols[0]].head(20).plot(kind="bar")
            plt.title(f"예시 그래프: {numeric_cols[0]} (상위 20개)")

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            img_tag = f'<img src="data:image/png;base64,{uri}" />'
            plt.close()

    return render(request, "dashboard/upload.html", {
        "preview": preview,
        "img_tag": img_tag,
    })


def visualize(request):
    """🌸 독립 테스트용: iris 데이터셋 산점도 시각화"""
    iris = load_iris(as_frame=True)
    df = iris.frame

    plt.figure(figsize=(6, 4))
    sns.scatterplot(x="sepal length (cm)", y="sepal width (cm)",
                    hue="target", data=df, palette="Set2")
    plt.title("Iris Dataset (샘플 시각화)")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    img_tag = f'<img src="data:image/png;base64,{uri}" />'
    plt.close()

    return render(request, "dashboard/visualize.html", {
        "img_tag": img_tag
    })




# =========================================
# 🔽 보관용: 확장형 업로드 (엑셀, 텍스트, 이미지 지원)
# 👉 필요 시 함수 이름 바꿔서 사용 (예: upload_flex)
# =========================================
"""
def upload(request):
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        ext = os.path.splitext(uploaded_file.name)[1].lower()

        if ext == ".csv":
            df = pd.read_csv(uploaded_file)
            preview = df.head().to_html()
            return HttpResponse(f"✅ CSV 업로드 성공!<br>{preview}")

        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(uploaded_file)
            preview = df.head().to_html()
            return HttpResponse(f"✅ 엑셀 업로드 성공!<br>{preview}")

        elif ext == ".txt":
            content = uploaded_file.read().decode("utf-8")[:500]
            return HttpResponse(f"📄 TXT 업로드 성공!<br><pre>{content}</pre>")

        elif ext in [".jpg", ".png"]:
            return HttpResponse("🖼️ 이미지 업로드 성공! (미리보기 기능은 추후 구현)")

        else:
            return HttpResponse("❌ 지원하지 않는 파일 형식입니다!")

    return render(request, "dashboard/upload.html")
"""
