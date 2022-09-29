
import openai
from retry import retry
import numpy as np 

model="ada:ft-TODO"

@retry(Exception, tries=3, delay=10)
def abstract_to_title(prompt, model, max_tokens=25, n=5):
  prediction = openai.Completion.create(
    model=model,     
    prompt=prompt + " \n\n###\n\n",
    max_tokens=max_tokens,
    stop=[" ###"],
    logprobs=0,
    top_p=1,
    n=n,
  )
  
  titles = [choice["text"].strip() for choice in prediction["choices"]]
#   titles_logprobs = [np.exp(np.sum(choice["logprobs"]["token_logprobs"])) for choice in prediction["choices"]]
#   predicted_reason = prediction["choices"][0]["text"].strip()
  
  return titles