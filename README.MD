\documentclass{article}
\usepackage{hyperref}
\usepackage{listings}

\title{Authentication Application}
\date{}

\begin{document}

\maketitle

\section*{Overview}
This project is a Flask-based authentication application that supports user registration, login, and Two-Factor Authentication (2FA) using Time-based One-Time Passwords (TOTP). Additionally, it allows users to manage TOTP secret keys and generate TOTP codes.

\tableofcontents

\newpage

\section{Project Structure}
\begin{verbatim}
authentication_application/
│
├── app.py                    # Main application file
├── users.csv                 # Stores registered users
├── keys.csv                  # Stores TOTP keys
├── templates/
│   ├── index.html            # Main page for signing in and validating TOTPs
│   └── authenticate.html     # Page for adding secret keys and generating TOTPs
├── static/
│   └── styles.css            # (Optional) Stylesheet for your HTML templates
├── backend.py                # Backend logic for handling TOTP (LM_TOTP class)
└── README.md                 # This README file
\end{verbatim}

\section{Setup}
\begin{enumerate}
    \item \textbf{Clone the repository:}
    \begin{lstlisting}[language=bash]
git clone https://github.com/yourusername/authentication_application.git
cd authentication_application
    \end{lstlisting}

    \item \textbf{Create a virtual environment and activate it:}
    \begin{lstlisting}[language=bash]
python3 -m venv venv
source venv/bin/activate
    \end{lstlisting}

    \item \textbf{Install the required dependencies:}
    \begin{lstlisting}[language=bash]
pip install -r requirements.txt
    \end{lstlisting}

    \item \textbf{Run the application:}
    \begin{lstlisting}[language=bash]
python app.py
    \end{lstlisting}
\end{enumerate}

The application should now be running on \url{http://127.0.0.1:5000}.

\section{Usage}

\subsection{Registration and Login}
\begin{enumerate}
    \item \textbf{Register a new user:}
    \begin{itemize}
        \item Send a POST request to \texttt{/register} with \texttt{username}, \texttt{password}, \texttt{totp}, and \texttt{secret}.
    \end{itemize}
    
    \item \textbf{Login:}
    \begin{itemize}
        \item Send a POST request to \texttt{/login} with \texttt{username} and \texttt{password}.
    \end{itemize}
    
    \item \textbf{Verify TOTP:}
    \begin{itemize}
        \item Send a POST request to \texttt{/verify\_totp} with \texttt{username} and \texttt{totp\_code}.
    \end{itemize}
\end{enumerate}

\subsection{Managing TOTP Keys}
\begin{enumerate}
    \item \textbf{Get all keys:}
    \begin{itemize}
        \item Send a GET request to \texttt{/keys}.
    \end{itemize}

    \item \textbf{Add a new key:}
    \begin{itemize}
        \item Send a POST request to \texttt{/add-key} with \texttt{name} and \texttt{secret}.
    \end{itemize}

    \item \textbf{Delete a key:}
    \begin{itemize}
        \item Send a DELETE request to \texttt{/delete-key/\{index\}} with the index of the key to be deleted.
    \end{itemize}

    \item \textbf{Generate TOTP code:}
    \begin{itemize}
        \item Send a GET request to \texttt{/generate-totp/\{index\}} with the index of the key.
    \end{itemize}
\end{enumerate}

\section{Endpoints}

\subsection{User Management}
\begin{itemize}
    \item \texttt{GET /generate-secret}
    \begin{itemize}
        \item Generates a new TOTP secret.
    \end{itemize}
    
    \item \texttt{POST /register}
    \begin{itemize}
        \item Registers a new user with \texttt{username}, \texttt{password}, \texttt{totp}, and \texttt{secret}.
    \end{itemize}
    
    \item \texttt{POST /login}
    \begin{itemize}
        \item Logs in a user with \texttt{username} and \texttt{password}.
    \end{itemize}
    
    \item \texttt{POST /verify\_totp}
    \begin{itemize}
        \item Verifies a TOTP code with \texttt{username} and \texttt{totp\_code}.
    \end{itemize}
\end{itemize}

\subsection{Key Management}
\begin{itemize}
    \item \texttt{GET /keys}
    \begin{itemize}
        \item Retrieves all stored TOTP keys.
    \end{itemize}
    
    \item \texttt{POST /add-key}
    \begin{itemize}
        \item Adds a new TOTP key with \texttt{name} and \texttt{secret}.
    \end{itemize}
    
    \item \texttt{DELETE /delete-key/\{index\}}
    \begin{itemize}
        \item Deletes a TOTP key at the specified index.
    \end{itemize}
    
    \item \texttt{GET /generate-totp/\{index\}}
    \begin{itemize}
        \item Generates a TOTP code for the key at the specified index.
    \end{itemize}
\end{itemize}

\section{License}
This project is licensed under the MIT License. See the LICENSE file for more details.

\end{document}
