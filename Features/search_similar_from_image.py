### lets set up the system


from Features import recommendation_process, feature_extraction
import pandas as pd

class seacrh_similar_from_image:

    def __init__(self, img,vectorstore):
        self.img = img
        self.vectorstore = vectorstore
        self.description = None
        self.form = None


    def ____image_to_description(self):
        
        extractor = feature_extraction.feature_extraction(self.img)

        self.description = extractor.image_to_description()
        
        self.form = extractor.image_to_form()


    def search_similarity_from_description(self,df_retail):

        self.__image_to_description()

        description = self.description

        similarity_object = recommendation_process.recommendation_process(
            description=description,
            vectorestore=self.vectorstore
            )
        
        returning_df = similarity_object.search_similarity_from_description(df_retail=df_retail)
        
        return returning_df


