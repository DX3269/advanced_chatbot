from fastapi import FastAPI, HTTPException
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from transformers import pipeline


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-small") 
llm = HuggingFacePipeline(pipeline=llm_pipeline)


query_prompt = PromptTemplate(
    input_variables=["query"],
    template="You are a helpful assistant. Summarize this query: {query}",
)

response_prompt = PromptTemplate(
    input_variables=["data"],
    template="Summarize the following data: {data}",
)


query_chain = LLMChain(llm=llm, prompt=query_prompt)
response_chain = LLMChain(llm=llm, prompt=response_prompt)


mock_data = [
    {"name": "Yoga Laptop", "brand": "Lenovo", "price": 899.99},
    {"name": "Galaxy Phone", "brand": "Samsung", "price": 699.99},
]


@app.get("/query")
async def handle_query(user_input: str):
    """
    Processing user input through LangChain and return a response.
    """
    try:

        summarized_query = query_chain.run(query=user_input)


        if "Yoga" in summarized_query:
            data = [item for item in mock_data if "Yoga" in item["name"]]
        elif "Lenovo" in summarized_query:
            data = [item for item in mock_data if "Lenovo" in item["brand"]]
        else:
            data = mock_data


        summarized_response = response_chain.run(data=str(data))
        return {"response": summarized_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
