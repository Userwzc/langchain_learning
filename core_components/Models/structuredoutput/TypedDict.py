from typing_extensions import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os       
load_dotenv()
os.getenv("OPENAI_API_KEY")

class Movie(TypedDict):
    """A movie with details."""
    title: Annotated[str, "The title of the movie"]
    year: Annotated[int, "The year the movie was released"]
    director: Annotated[str, "The director of the movie"]   
    rating: Annotated[float, "The movie's rating out of 10"]

model = ChatOpenAI(
    model = "gpt-5.1",
    base_url="http://localhost:8317/v1"
)

model_with_structure = model.with_structured_output(Movie)
response = model_with_structure.invoke("Provide details about the movie Inception.")
print(response)
