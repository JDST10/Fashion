### lets set up the system
from Features import recommendation_process 

class seacrh_from_luxury_brands:

    def __init__(self, description,vectorstore):
        self.description = description
        self.vectorstore = vectorstore

    def search_similarity_from_description(self,df_retail):

        similarity_object = recommendation_process.recommendation_process(
            description=self.description,
            vectorestore=self.vectorstore
            )
        
        returning_df = similarity_object.search_similarity_from_description(df_retail=df_retail)
        
        return returning_df





