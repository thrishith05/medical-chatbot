import os
import pickle
import threading
from pathlib import Path
from typing import Dict, List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.vectorstores import FAISS as FAISS_V2
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
                loader = PyPDFLoader(str(pdf_file))
                docs = loader.load()
                # Add source metadata
                for doc in docs:
                    doc.metadata['source'] = pdf_file.name
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
            # Load existing to get count
            existing_store = FAISS(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            # Get current collection count
            try:
                existing_chunks_count = existing_store._collection.count()
            except:
                pass
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
                
                # Load single PDF
                loader = PyPDFLoader(str(pdf_file))
                docs = loader.load()
                
                # Add source metadata
                for doc in docs:
                    doc.metadata['source'] = pdf_file.name
                
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
            existing_vectorstore = FAISS(
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
            self.vectorstore = FAISS.from_documents(
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
            self.vectorstore = FAISS(
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
        Get answer and relevant contexts for a query
        
        Args:
            query: User question
            top_k: Number of relevant contexts to return
            
        Returns:
            Dictionary with 'answer' and 'contexts' keys
        """
        # If vector store doesn't exist yet, return a helpful message
        if self.vectorstore is None:
            return {
                "answer": "The medical knowledge base is currently being initialized. Please try again in a few minutes. This is a one-time process that takes approximately 10-15 minutes.",
                "contexts": []
            }
        
        try:
            # Get relevant documents directly from vector store
            docs = self.vectorstore.similarity_search_with_score(query, k=top_k)
            
            # Extract the most relevant information as the answer
            if docs:
                # Try to build answer from multiple documents for better context
                answer_parts = []
                query_lower = query.lower()
                query_words = [w for w in query_lower.split() if len(w) > 3]
                
                # Process up to 3 top documents
                for doc_idx, (doc, score) in enumerate(docs[:3]):
                    page_content = doc.page_content
                    
                    # Extract sentences
                    sentences = [s.strip() for s in page_content.split(".") if s.strip()]
                    
                    # Score sentences by relevance
                    scored_sentences = []
                    for sentence in sentences:
                        sentence_lower = sentence.lower()
                        # Require substantial sentences (not headers or very short)
                        # Exclude headers, page numbers, and very short sentences
                        is_header = (sentence.isupper() or 
                                   any(char.isdigit() for char in sentence[:5]) or
                                   len(sentence) < 30 or
                                   all(c in sentence[:20] for c in "  ") or  # Multiple spaces = likely header
                                   sentence.startswith(('   ', 'Fig', 'Box')))
                        
                        if not is_header and len(sentence) > 25:
                            # Count matching keywords
                            score_count = sum(1 for word in query_words if word in sentence_lower)
                            if score_count > 0:
                                scored_sentences.append((score_count, sentence))
                    
                    # Add top sentences from this document
                    scored_sentences.sort(reverse=True)
                    for score_val, sentence in scored_sentences[:3]:
                        if len(". ".join(answer_parts)) > 300:
                            break
                        answer_parts.append(sentence)
                    
                    # If we have enough content, stop
                    if len(". ".join(answer_parts)) > 300:
                        break
                
                # If still not enough content, take sentences without scoring
                if len(". ".join(answer_parts)) < 100:
                    for doc, score_val in docs[:2]:
                        sentences = [s.strip() for s in doc.page_content.split(".") if s.strip()]
                        # Take substantial sentences (avoid headers)
                        for sentence in sentences:
                            is_header = (sentence.isupper() or len(sentence) < 30 or
                                       any(char.isdigit() for char in sentence[:5]))
                            if not is_header and len(sentence) > 30:
                                answer_parts.append(sentence)
                                if len(". ".join(answer_parts)) > 150:
                                    break
                            if len(". ".join(answer_parts)) > 150:
                                break
                        if len(". ".join(answer_parts)) > 150:
                            break
                
                # Build the answer
                if answer_parts:
                    answer = ". ".join(answer_parts) + "."
                else:
                    # Fallback: use first document content
                    top_doc = docs[0][0].page_content
                    sentences = [s.strip() for s in top_doc.split(".") if s.strip()]
                    if sentences:
                        filtered = [s for s in sentences if len(s) > 25 and not s.isupper()][:3]
                        answer = ". ".join(filtered) + "." if filtered else top_doc[:400] + "..."
                    else:
                        answer = "Based on the medical literature, this information is relevant."
                
                # Ensure answer is between 150-500 chars for best quality
                if len(answer) > 500:
                    # Truncate intelligently at sentence boundary
                    truncated = answer[:500]
                    last_period = truncated.rfind(".")
                    if last_period > 300:
                        answer = truncated[:last_period + 1]
                    else:
                        answer = truncated[:497] + "..."
                elif len(answer) < 100:
                    # If too short, try to add context from other docs with better filtering
                    for doc, _ in docs[1:3]:
                        if len(answer) > 150:
                            break
                        sentences = [s.strip() for s in doc.page_content.split(".") if s.strip()]
                        # Filter out headers
                        for sentence in sentences:
                            is_header = (sentence.isupper() or len(sentence) < 40 or
                                       any(char.isdigit() for char in sentence[:5]))
                            if not is_header and len(sentence) > 40:
                                extra = sentence + "."
                                answer = answer + " " + extra
                                if len(answer) > 150:
                                    break
                            if len(answer) > 150:
                                break
            else:
                answer = "No relevant information found in the medical literature."
            
            # Prepare source documents for contexts
            source_docs = [doc[0] for doc in docs] if docs else []
            
            # Prepare contexts (limit to top_k)
            contexts = []
            seen_sources = set()
            
            for doc in source_docs[:top_k]:
                page_content = doc.page_content
                source = doc.metadata.get('source', 'unknown')
                page = doc.metadata.get('page', '')
                
                # Truncate long contexts
                if len(page_content) > 500:
                    page_content = page_content[:497] + "..."
                
                context_entry = f"[{source}"
                if page:
                    context_entry += f" p.{page}"
                context_entry += "] " + page_content
                
                # Avoid duplicates
                context_key = (source, page)
                if context_key not in seen_sources:
                    contexts.append(page_content)
                    seen_sources.add(context_key)
                
                if len(contexts) >= top_k:
                    break
            
            return {
                "answer": answer,
                "contexts": contexts
            }
        
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "answer": f"I encountered an error processing your question. Please try rephrasing it.",
                "contexts": []
            }

