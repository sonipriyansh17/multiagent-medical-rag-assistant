## 🩺 MedAssist RAG Assistant
An intelligent AI medical assistant that helps you understand your symptoms using the power of Retrieval-Augmented Generation (RAG).

<br>

<br>

Ever felt lost in a sea of medical jargon online? MedAssist is here to help. Instead of just guessing, it uses a real medical knowledge base to give you grounded, context-aware information about potential conditions related to your symptoms.

(Pro-tip: Record a quick GIF of your frontend in action and replace the link above to make your README pop!)

## 💡 The Core Idea
This isn't just another chatbot. MedAssist is built on a Retrieval-Augmented Generation (RAG) architecture.

Think of it like having a super-smart medical librarian.

You ask a question (your symptoms).

The system retrieves relevant documents from a specialized medical vector database.

It then uses a powerful Large Language Model (LLM) to generate a human-friendly answer based only on the facts it found.

This approach dramatically reduces AI "hallucinations" and provides responses that are grounded in a curated knowledge base.

## ✨ Features
AI-Powered Symptom Analysis: Get potential diagnoses based on your input.

Grounded Responses: Built with a RAG pipeline to ensure answers are based on a real knowledge base.

Blazing Fast: Powered by FastAPI on the backend and Groq for near-instant LLM inference.

Persistent Memory: Saves conversation history to a PostgreSQL database (NeonDB).

Ready to Deploy: Comes with a Dockerfile for easy containerization and deployment.

## 🛠️ Tech Stack
Backend: FastAPI

LLM: Groq (Llama 3)

Embedding Model: SentenceTransformers (BioBERT)

Vector Database: ChromaDB

Relational Database: NeonDB (PostgreSQL)

Deployment: Docker

## 🚀 Getting Started
Ready to run your own instance of MedAssist? Let's dive in.

Prerequisites

Git

Python 3.10+

An IDE like VS Code
