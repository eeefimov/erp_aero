import os
import fitz
from icecream import ic
from pdfminer.high_level import extract_text


class AeroPdf:
    pj_dir = os.getcwd()
    pdf_file_path = None
    elements = []
    pdf_info = {}
    template = {
        "PN:": None, "DESCRIPTION:": None, "LOCATION:": None, "RECEIVER#:": None,
        "EXP DATE:": None, "CERT SOURCE:": None, "REC.DATA:": None, "BATCH#:": None,
        "REMARK:": None, "TAGGED BY:": None, "Qty:": None, "SN:": None, "CONDITION:": None,
        "UOM:": None, "PO:": None, "MFG:": None, "DOM:": None, "LOT#:": None,
        "NOTES:": None
    }

    """ 
    This method is looking pdf file in PDF_FILES folder. 
    In this case you have to use "pdf_file_path" and "PDF_FILES" as argument
    when call the method. 
    """
    # def find_pdf(self, folder_path):
    #     path = os.path.join(os.getcwd(), aepdf.pj_dir, folder_path)
    #     items = os.listdir(path)
    #     ic(items)
    #     for item in items:
    #         self.pdf_file_path = os.path.join(path, item)
    #         if os.path.isfile(self.pdf_file_path) and item.endswith(".pdf"):
    #             return self.pdf_file_path

    def data_from_pdf(self, file_path: str) -> dict:
        """
        Get file path, extract keys and values, return Dict.
        """
        text = extract_text(file_path)
        lines = text.split('\n')
        data_list = []
        is_notes = False

        for line in lines:
            line = line.strip()

            if ':' in line:
                if is_notes:
                    data_list[-1] += line
                    is_notes = False
                key, value = line.split(':', 1)
                data_list.append(f"{key.strip()}: {value.strip()}")
                self.pdf_info[key.strip()] = value.strip()
            elif is_notes:
                self.pdf_info['NOTES'] += ' ' + line
            elif data_list and data_list[-1].startswith('NOTES:'):
                self.pdf_info['NOTES'] += ' ' + line

        return self.pdf_info

    def check_positions(self, file_path: str) -> dict:
        """
        Get pdf file. Extract keys words and position in the file.
        """
        prototype = {}
        file = fitz.open(file_path)
        for page in file:
            self.elements.append(page.get_text("words"))
        file.close()

        for element in self.elements[0]:
            word = element[4]
            if word == 'Qty:':
                prototype[word] = list(element[0:4])
            if word.isupper() and word not in self.pdf_info.values():
                prototype[word] = list(element[0:4])

        return prototype

    def check(self, etalon_dict: dict, new_dict: dict) -> bool:
        """
        Get two dict. Match word positions. Positions is a list with coordinates.
        If key and position are the same -> return TRUE.
        """
        if set(etalon_dict.keys()) == set(new_dict.keys()):
            return all(etalon_dict[key] == new_dict[key] for key in etalon_dict)
        else:
            return False


if __name__ == "__main__":
    """
    ic, uses for showing functions return and debugging. 
    """
    aepdf = AeroPdf()
    ic(aepdf.data_from_pdf("template.pdf"))                # print dict
    template = aepdf.check_positions("template.pdf")       # get template positions

    new = template.copy()                                  # create new dict for checking
    new.update({"GRIFFON": [6, 6.5, 55, 20]})              # change positions values
    ic(aepdf.check(template, template))                    # match template with correct dict
    ic(aepdf.check(template, new))                         # match template with incorrect dict
