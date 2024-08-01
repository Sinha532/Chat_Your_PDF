# Generative AI Q&A Web Application

This project is a Generative AI-powered web application that prioritizes the Retrieval-Augmented Generation (RAG) pipeline. It leverages Google's `gemini-1.5-flash` model to enable question and answer functionality with custom knowledge provided by the user. The application includes customized authentication and a message retrieval option for an enhanced user experience.

## Features

- **Generative AI Model**: Utilizes Google's `gemini-1.5-flash` model for accurate and context-aware responses.
- **RAG Pipeline**: Combines retrieval and generation capabilities to provide precise answers based on provided documents.
- **Custom Knowledge Integration**: Users can upload custom documents (PDFs) that the AI will use to generate responses.
- **Web Application**: A user-friendly web interface built with Django.
- **Authentication**: Customized user authentication for secure access.
- **Message Retrieval**: Users can retrieve previous interactions and answers.

### Prerequisites

- Python 3.8 or later
- Django
- Streamlit
- LangChain
- Pandas
- FAISS
- PyPDF2
- dotenv
- Bootstrap (for front-end styling)


### Usage

1. **Sign Up / Log In**: Access the application and either sign up for a new account or log in if you already have one.
2. **Upload Document**: Navigate to the upload section and upload your PDF document.
3. **Ask Questions**: Enter your question in the input field and get answers based on the content of the uploaded document.
4. **Retrieve Messages**: View previous interactions and responses.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, feel free to contact the project maintainer at [lokeshsinha746@gmail.com].
