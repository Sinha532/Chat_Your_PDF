import os
import time
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
#from langchain.chains.question_answering import load_qa_chain
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, logout,login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from . import forms

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY,
                             temperature=0.7)

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions: {input}
    """
)
def signup(request):
    if request.method == 'POST':
        signup_form = forms.SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        signup_form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': signup_form})

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'form': login_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def index(request):
    return render(request, 'index.html')

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf = request.FILES['pdf']
        fs = FileSystemStorage()
        filename = fs.save(pdf.name, pdf)
        request.session['pdf_path'] = fs.path(filename)
        return redirect('result')
    return render(request, 'index.html')

def vector_embedding(pdf_path):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    final_documents = text_splitter.split_documents(docs[:20])  # splitting
    vectors = FAISS.from_documents(final_documents, embeddings)
    return vectors
    
@login_required
def result(request):
    if 'pdf_path' not in request.session:
        return redirect('index')

    pdf_path = request.session['pdf_path']

    if request.method == 'POST':
        question = request.POST['question']
        vectors = vector_embedding(pdf_path)
        doc_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vectors.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, doc_chain)
        start = time.process_time()
        result = retrieval_chain.invoke({'input': question})
        context = {
            'answer': result['answer'],
            'documents': result['context']
        }
        return render(request, 'result.html', context)

    return render(request, 'result.html')
