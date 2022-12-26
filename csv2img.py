from csv2pdf import convert
import fitz
def saveas(source) -> None:
    if source is not None:
        name = str(source).replace(".csv",'')
        pdf = str(name) + str(".pdf")
        convert(source, pdf)
        file_path = pdf
        doc = fitz.open(file_path)
        i = 0
        for page in doc:
            i += 1
            pix = page.get_pixmap(dpi=300)
            output = str(name) + str(i) + ".png"
            pix.save(output)
        doc.close()
        return " "
