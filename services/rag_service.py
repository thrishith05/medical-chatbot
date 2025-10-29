import os
import pickle
import threading
from pathlib import Path
from typing import Dict, List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self, data_path: str = None, persist_directory: str = "./chroma_db"):
        """
        Initialize the RAG service with document loading and retrieval
        
        Args:
            data_path: Path to medical documents
            persist_directory: Directory to store vector database
        """
        # Default data path if not provided
        if data_path is None:
            # Try multiple possible paths
            possible_paths = [
                Path("/Users/thrishithreddy/Desktop/Dataset"),
                Path("../Dataset"),
                Path("Dataset"),
                Path("./Dataset")
            ]
            for path in possible_paths:
                if path.exists():
                    self.data_path = path
                    break
            else:
                self.data_path = Path("/Users/thrishithreddy/Desktop/Dataset")
        else:
            self.data_path = Path(data_path)
            
        self.persist_directory = persist_directory
        self.vectorstore = None
        self.qa_chain = None
        self.initialization_started = False
        self.initialization_complete = False
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize LLM
        self.llm = self._init_llm()
        
        # Initialize or load vector store (try to load sync if exists, otherwise async)
        if Path(self.persist_directory).exists() and any(Path(self.persist_directory).iterdir()):
            # Load existing vector store synchronously (should be fast)
            self._initialize_vectorstore()
        else:
            # Start background initialization for new vector store
            self._initialize_vectorstore_in_background()
    
    def _init_llm(self):
        """Initialize LLM - use OpenAI if available, otherwise extract from context"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return OpenAI(openai_api_key=api_key, temperature=0)
        else:
            print("Warning: No OpenAI API key. Using simple context extraction.")
            
            class SimpleContextLLM:
                def __call__(self, prompt):
                    # Return a summary of the first context found
                    # The RetrievalQA chain will provide context
                    return "Based on the retrieved medical literature."
                
                def __init__(self):
                    self.temperature = 0
                
                def generate(self, prompts, **kwargs):
                    return [[self(p) for p in prompts]]
                
                def __getattr__(self, name):
                    # Proxy any other method calls
                    return lambda *args, **kwargs: ""
            
            return SimpleContextLLM()
    
    def _load_documents(self) -> List:
        """Load all PDF documents from the dataset directory"""
        documents = []
        
        if not self.data_path.exists():
            raise ValueError(f"Dataset path {self.data_path} does not exist. Please check the path.")
        
        pdf_files = list(self.data_path.glob("*.pdf"))
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in {self.data_path}")
        
        print(f"Loading {len(pdf_files)} PDF files...")
        
        for pdf_file in pdf_files:
            try:
                # Load PDF without metadata extraction to avoid subprocess errors
                loader = PyPDFLoader(str(pdf_file))
                docs = loader.load()
                # Add source metadata manually
                for doc in docs:
                    doc.metadata['source'] = str(pdf_file.name)
                documents.extend(docs)
                print(f"Loaded {pdf_file.name}: {len(docs)} pages")
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")
                continue
        
        print(f"Total documents loaded: {len(documents)}")
        return documents
    
    def _create_vectorstore_with_incremental_loading(self):
        """Create vector store by processing PDFs one by one"""
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        # Get PDF files
        pdf_files = list(self.data_path.glob("*.pdf"))
        
        # TEMPORARY: Use only 8 smallest PDFs for faster testing
        # Comment this out for full dataset
        pdf_files = sorted(pdf_files, key=lambda x: x.stat().st_size)[:8]
        
        total_files = len(pdf_files)
        print(f"⚠️  Using {total_files} PDFs (can increase to 9 for full dataset)")
        
        print(f"Processing {total_files} PDF files individually...")
        
        # Check if vectorstore already exists - if so, we'll add to it
        existing_chunks_count = 0
        if Path(self.persist_directory).exists() and any(Path(self.persist_directory).iterdir()):
            print("ℹ️  Existing vector store found. Will add new documents to it.")
            # Load existing ChromaDB store
            try:
                existing_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                existing_chunks_count = existing_store._collection.count() if hasattr(existing_store, '_collection') else 0
            except Exception as e:
                print(f"Could not load existing store: {e}")
            if existing_chunks_count > 0:
                print(f"ℹ️  Current chunks in store: {existing_chunks_count}")
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Start with empty vector store (will add to it incrementally)
        all_splits = []
        
        for idx, pdf_file in enumerate(pdf_files, 1):
            try:
                print(f"\n[{idx}/{total_files}] Processing {pdf_file.name}...")
                
                # Load single PDF - handle any metadata errors gracefully
                try:
                    loader = PyPDFLoader(str(pdf_file))
                    docs = loader.load()
                except Exception as pdf_error:
                    # If PDF loading fails, try without metadata
                    print(f"Warning: Error loading PDF metadata, continuing anyway: {pdf_error}")
                    # Fallback: skip this file
                    continue
                
                # Add source metadata manually
                for doc in docs:
                    doc.metadata['source'] = str(pdf_file.name)
                
                # Split into chunks
                splits = text_splitter.split_documents(docs)
                all_splits.extend(splits)
                
                print(f"✅ {pdf_file.name} processed: {len(docs)} pages, {len(splits)} chunks")
                
            except Exception as e:
                print(f"❌ Error processing {pdf_file.name}: {e}")
                continue
        
        if not all_splits:
            raise ValueError("No documents were successfully processed")
        
        print(f"\n📊 Total chunks created: {len(all_splits)}")
        
        # Check if we should add to existing or create new
        vectorstore_path = Path(self.persist_directory)
        if existing_chunks_count > 0:
            print(f"Adding {len(all_splits)} new chunks to existing store ({existing_chunks_count} existing)...")
            # Load existing
            existing_vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            # Add new documents
            existing_vectorstore.add_documents(all_splits)
            self.vectorstore = existing_vectorstore
            print(f"✅ Added to existing store. Total: {existing_chunks_count + len(all_splits)} chunks")
        else:
            print("Creating new vector store and generating embeddings...")
            print("⏳ This may take 5-10 minutes for embedding generation...")
            
            # Create vector store with all chunks
            self.vectorstore = Chroma.from_documents(
                documents=all_splits,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            print("✅ Vector store created and persisted")
        
        print("🎉 Initialization complete! API is ready.")
    
    def _initialize_vectorstore_in_background(self):
        """Start vector store initialization in background thread"""
        if self.initialization_started:
            return
        
        self.initialization_started = True
        thread = threading.Thread(target=self._initialize_vectorstore_thread, daemon=True)
        thread.start()
    
    def _initialize_vectorstore_thread(self):
        """Initialize vector store in background thread"""
        try:
            print("Starting vector store initialization in background...")
            self._initialize_vectorstore()
            self.initialization_complete = True
            print("Vector store initialization complete!")
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            self.vectorstore = None
            self.qa_chain = None
    
    def _initialize_vectorstore(self):
        """Initialize or load the vector store"""
        vectorstore_path = Path(self.persist_directory)
        
        # Check if vector store already exists
        if vectorstore_path.exists() and any(vectorstore_path.iterdir()):
            print(f"Loading existing vector store from {self.persist_directory}")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print("Vector store loaded successfully")
        else:
            print("Creating new vector store...")
            self._create_vectorstore_with_incremental_loading()
        
        # Note: We don't use QA chain anymore - we extract answers directly from contexts
        # This allows us to provide precise answers without OpenAI
        self.qa_chain = None
    
    def get_answer(self, query: str, top_k: int = 5) -> Dict[str, List[str]]:
        """
        Get a SINGLE, PRECISE answer from ChromaDB
        Returns answer from ONLY the best matching document - ONE reliable source
        """
        # If vector store doesn't exist yet, return a helpful message
        if self.vectorstore is None:
            return {
                "answer": "The medical knowledge base is currently being initialized. Please try again in a few minutes. This is a one-time process that takes approximately 10-15 minutes.",
                "contexts": []
            }
        
        try:
            # Get ONLY the single best matching document (k=1 for one source)
            docs = self.vectorstore.similarity_search_with_score(query, k=1)
            
            if not docs:
                return {
                    "answer": "No relevant information found in the medical literature.",
                    "contexts": []
                }
            
            # Get the SINGLE best matching document (lowest score = best match)
            best_doc, best_score = docs[0]
            
            # Extract the most precise answer from the best document
            page_content = best_doc.page_content
            
            # Find the most relevant sentences within the document
            sentences = [s.strip() for s in page_content.split(".") if s.strip()]
            
            query_lower = query.lower()
            query_words = [w for w in query_lower.split() if len(w) > 3]
            
            # Score each sentence for relevance
            scored_sentences = []
            for sentence in sentences:
                # Skip headers, figures, short fragments
                is_header = (
                    sentence.isupper() or
                    len(sentence) < 50 or
                    sentence.startswith(('Fig', 'Box', 'Table', 'Chapter', '   ')) or
                    sentence.count('  ') > 2
                )
                
                if not is_header:
                    sentence_lower = sentence.lower()
                    # Count query word matches
                    matches = sum(1 for word in query_words if word in sentence_lower)
                    
                    # Prioritize longer, more complete sentences
                    score = matches * 10 + min(len(sentence), 100)
                    
                    scored_sentences.append((score, sentence))
            
            # Sort by relevance score
            scored_sentences.sort(reverse=True)
            
            # Select the top 2-3 most relevant sentences for a complete answer
            selected_sentences = []
            for score, sentence in scored_sentences[:3]:
                selected_sentences.append(sentence)
                # Stop when we have a good amount of content
                if len(". ".join(selected_sentences)) > 250:
                    break
            
            # If we don't have enough, take sentences in order (avoiding headers)
            if len(selected_sentences) < 2:
                for sentence in sentences:
                    is_header = (sentence.isupper() or len(sentence) < 50 or 
                                sentence.startswith(('Fig', 'Box', 'Table')))
                    if not is_header:
                        selected_sentences.append(sentence)
                        if len(". ".join(selected_sentences)) > 300:
                            break
            
            # Build the answer
            answer = ". ".join(selected_sentences) + "."
            
            # Trim to optimal length (200-400 characters)
            if len(answer) > 500:
                # Truncate at sentence boundary
                truncated = answer[:500]
                last_period = truncated.rfind(".")
                answer = truncated[:last_period + 1] if last_period > 200 else truncated + "..."
            elif len(answer) < 100:
                # If too short, use the full document excerpt
                answer = page_content[:300] + "..." if len(page_content) > 300 else page_content
            
            # Return empty contexts - user doesn't want to see sources
            return {
                "answer": answer,
                "contexts": []  # No sources displayed
            }
        
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "answer": "I encountered an error processing your question. Please try rephrasing it.",
                "contexts": []
            }
