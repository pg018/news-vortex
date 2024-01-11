import asyncio
from dotenv import load_dotenv
from vortexmodel.processing.processing_main import Processing
from vortexmodel.model.GenerateTfIdf import GenerateTfIdf
from vortexmodel.model.GenerateTrainingData import GenerateTrainingData

load_dotenv()

if __name__ == "__main__":
    print("\nWelcome to NewsVortex!")
    print("Summarized News => Enter 1")
    print("Generate Training Data => Enter 2")
    print("Generate TF-IDF Json => Enter 3")
    user_input = int(input("Enter your input: "))
    if user_input == 3:
        data_obj = GenerateTfIdf()
        data_obj.generate_tfidf()
    else:
        query = input("Enter the query: ")
        if user_input == 1:
            data_obj = Processing(query)
            asyncio.run(data_obj.processing_main())
        else:
            data_obj = GenerateTrainingData(query)
            asyncio.run(data_obj.generate_data())
