from flask import Flask, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os, openai, markdown2


load_dotenv()

client = MongoClient(os.environ.get('MONGODB_URI'))
db=client[os.environ.get('DATABASE_NAME')]
collection_name=os.environ.get('COLLECTION_NAME')
print(collection_name)
openai.api_key = os.environ.get("OPENAI_API_KEY")
# model_engine = "davinci"


app = Flask(__name__)


# def generate_response(prompt, model_engine):
#     response = openai.Completion.create(
#         engine=model_engine,
#         prompt=prompt,
#         max_tokens=2034,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )

#     message = response.choices[0].text
#     return message.strip()




@app.route('/', methods = ['GET', 'POST'])
def prompt():
    if request.method == 'POST':
        user_text = request.form.get('leetcode_problem_number')
        ## chatgpt_text = f'Please generate an in-depth blog on LeetCode question number {user_text} in markdown format. The blog should cover the problem statement, examples, solution with multiple approaches if applicable along with code and time and space complexity analysis with explanation, edge cases, conclusion, tips, similar questions with link. Make it in about 1700 words'
        ## chatgpt_text = f'write java code with comments for leetcode problem number {user_text} in understandable format'
        ## chatgpt_text = "Write a blog post about LeetCode problem number {}.".format(user_text)
        # 
        chatgpt_text  = f'You are ChatGPT, a large language model trained by OpenAI.Can you provide me well-written problem description(wrapped under <b> tag), test-cases(in bold heading), edge-cases(in bold heading), java code(in bold heading) and code (in <pre> tag) with proper comments and time ans space complexity in proper format for leetcode question number {user_text}.'
        ## chatgpt_text = f'Can you provide me well-written problem description(wrapped under <b> tag), test-cases(in bold heading), edge-cases(in bold heading), java code(in bold heading) and code (in <pre> tag) with proper comments and time ans space complexity in proper format for leetcode question number {user_text}.'
        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt=chatgpt_text,
            max_tokens=1900,
            n=1,
            stop=None,
            temperature=0.9,
            presence_penalty = 0.6,
            top_p = 1
        )
        ## blog_text = response.choices[0].text
        blog_text = response.choices[0].text
        print(blog_text)
        html_text = markdown2.markdown(blog_text)
        print(html_text)
        return render_template('index.html', response=html_text, problem_number = user_text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)