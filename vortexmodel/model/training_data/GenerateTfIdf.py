import os
import json
from vortexmodel.processing.custom_tfidf import CustomTFIDF

class GenerateTfIdf:
    def __init__(self) -> None:
        self.script_directory = os.path.dirname(
            os.path.abspath(__file__)
        )  # Get the directory of the current script (i.e training_data)

    def get_doc_list(self):
        """Creates list of documents of the scrapped text"""
        final_doc_list = []
        data_folder = os.path.join(self.script_directory, "data", "content")
        if not os.path.exists(data_folder):
            print("Scrapped Content Folder does not exist")
            return
        # list of all the scraped files
        scrapped_files_list = [
            f
            for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f))
        ]
        for i in range(len(scrapped_files_list)):
            scrapped_file_path = os.path.join(data_folder, scrapped_files_list[i])
            print(scrapped_file_path)
            with open(scrapped_file_path, "r", encoding="utf-8") as scrap_file:
                scrap_file_content = scrap_file.read()
            final_doc_list.append(scrap_file_content)
        print("\n\n\n\n")
        # print(final_doc_list)
        return final_doc_list

    def generate_tfidf(self):
        """Generates the TFIDF of the document list as training"""
        docs_list = self.get_doc_list()
        print("DOCS List created")
        tfdif = CustomTFIDF(docs_list)
        tfidf_vector = tfdif.create_tfidf_vector()
        print("TFIDF Vector Created")
        with open(os.environ["TFIDF_SAVE_PATH"], "w") as json_file:
            json.dump(tfidf_vector, json_file)
        print("TFIDF Saved")
        return
