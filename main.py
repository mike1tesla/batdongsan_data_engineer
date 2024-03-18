import requests
from bs4 import BeautifulSoup


url = "https://batdongsan.com.vn/ban-nha-rieng-ha-dong"

header = {
    'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}
# Gửi yêu cầu GET đến trang web
response = requests.get(url,headers=header)

# Kiểm tra xem yêu cầu có thành công không (status code 200 là thành công)
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích HTML của trang web
    soup = BeautifulSoup(response.content, "html.parser")

    # Tìm tất cả các thẻ <a> trong HTML có thuộc tính href
    links = soup.find_all("a", href=True)

    # Lặp qua các liên kết và in chúng
    for link in links:
        print(link['href'])
else:
    print("Yêu cầu không thành công, mã trạng thái:", response.status_code)
