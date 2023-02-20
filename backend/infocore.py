import paddle
import zhconv
import pdfplumber
from pprint import pprint
from paddlenlp import Taskflow
import requests
import fitz
from PIL import Image
class infoextractor:
    def __init__(self):
        self.entityname=None
        self.date=None
        self.maincontent=None
        self.url=None
        self.docintelcore=None
        self.sumcore=None
    def getpdf(self):
        response = requests.get(self.url)
        with open("./cash/pdfdata.pdf", "wb") as f:
            f.write(response.content)
        f.close()
        response=None
    def pdftojpg(self):
        with fitz.open('./cash/pdfdata.pdf') as doc:
            num_pages = doc.page_count
        use_pages=min([num_pages,1])
        for page_num in range(use_pages):
            with fitz.open('./cash/pdfdata.pdf') as doc:
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                pix.save(f'./cash/page{page_num + 1}.jpg')
        img = Image.open('./cash/page1.jpg')
        img_width, img_height = img.size
        new_img = Image.new('RGB', (img_width, img_height * use_pages))
        for page_num in range(use_pages):
            img = Image.open(f'./cash/page{page_num + 1}.jpg')
            new_img.paste(img, (0, img_height * page_num))
        new_img.save('./cash/jpgdata.jpg')
    def docintel(self):
        # if not self.docintelcore:
        #     self.docintelcore = Taskflow("document_intelligence")
        # result=self.docintelcore({
        #               "doc": "./cash/jpgdata.jpg",
        #               "prompt": ["概括公告内容", "处罚决定", "处罚对象",
        #                          '处罚时间','处罚执行机构','违规行为','风险因素']})
        result = ''
        with pdfplumber.open(
                "./cash/pdfdata.pdf") as pdf:
            for page in pdf.pages:
                text = page.extract_text()  # 提取文本
                result += text
            result = result.replace('\n', '')
            result = zhconv.convert(result, 'zh-cn')
        if not self.sumcore:
            self.sumcore=Taskflow("text_summarization")
        result2 = self.sumcore(result)
        if not self.docintelcore:
            self.docintelcore = Taskflow("information_extraction", schema=[ '违规','风险','后果','时间','金额'], model="uie-x-base")
        result1=self.docintelcore({
                      "doc": "./cash/jpgdata.jpg"})
        return result1,result2
    def infoget(self,pdfurl):
        self.url=pdfurl
        self.getpdf()
        self.pdftojpg()
        result=self.docintel()
        return result

if __name__ == '__main__':
    pass





