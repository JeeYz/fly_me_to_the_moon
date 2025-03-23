from re import search
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import os
import faiss

# Rich 라이브러리 임포트
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED


class FaissVectorStore:
    """
    FAISS 벡터 저장소를 관리하는 클래스
    PDF 문서를 로드하고 벡터화하여 유사도 검색을 수행합니다.
    """
    def __init__(self, 
                 vector_db_path: str = "./.cache/faiss_vectorstore",
                 source_document_path: str = "./.text_data/",
                 embedding_model_name: str = "nomic-embed-text",
                 chunk_size: int = 1000,  # 더 작은 값으로 조정
                 chunk_overlap: int = 100):
        """
        초기화 함수
        
        Args:
            vector_db_path: 벡터 저장소 파일 경로
            source_document_path: 원본 문서 경로
            embedding_model_name: 임베딩 모델 이름
            chunk_size: 텍스트 청크 크기
            chunk_overlap: 텍스트 청크 오버랩 크기
        """
        self.vector_db_path = vector_db_path
        self.source_document_path = source_document_path
        
        # 임베딩 모델 초기화
        self.embedding_model = OllamaEmbeddings(
            model=embedding_model_name,
            temperature=0.0
        )
        
        # 텍스트 분할기 초기화
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            keep_separator=True,  # 구분자 유지
        )
        
        self.vectorstore = None
    
    def initialize(self) -> FAISS:
        """
        벡터 저장소 초기화
        기존 저장소가 있으면 로드하고, 없으면 새로 생성합니다.
        
        Returns:
            FAISS: 초기화된 FAISS 벡터 저장소
        """
        if os.path.exists(self.vector_db_path):
            self.vectorstore = self._load_vectorstore(self.vector_db_path)
            # print(f"self.vectorstore.index_to_docstore_id: {self.vectorstore.index_to_docstore_id}")
        else:
            self.vectorstore = self._create_vectorstore()
            self._save_vectorstore(self.vector_db_path)
        
        return self.vectorstore
    
    def _create_vectorstore(self) -> FAISS:
        """
        새로운 벡터 저장소 생성
        
        Returns:
            FAISS: 생성된 FAISS 벡터 저장소
        """
        # PDF 파일 찾기
        pdf_files = self._find_files(self.source_document_path)
        
        # 문서 로드
        documents = []
        for pdf_file in pdf_files:
            loader = PyMuPDFLoader(pdf_file)
            loaded_docs = loader.load()
            print(f"PDF 파일: {pdf_file} - 로드된 페이지 수: {len(loaded_docs)}개")
            # 처음 몇 개 페이지의 길이 출력
            for i, doc in enumerate(loaded_docs[:3]):
                print(f"  - 페이지 {i+1} 길이: {len(doc.page_content)} 글자")
            documents.extend(loaded_docs)
        
        print(f"총 로드된 문서 수: {len(documents)}개")
        
        # 문서 분할 - 각 페이지를 적절한 크기로 분할
        texts = []
        for doc in documents:
            # 페이지 내용이 너무 짧은지 확인
            if len(doc.page_content.strip()) < 100:  # 너무 짧은 페이지는 건너뛀
                continue
                
            # 각 문서를 청크로 분할
            chunks = self.text_splitter.split_text(doc.page_content)
            
            # 너무 짧은 청크는 합치기
            merged_chunks = []
            current_chunk = ""
            
            for chunk in chunks:
                # 청크가 너무 짧으면 합치기
                if len(chunk.strip()) < 100 and current_chunk:
                    current_chunk += " " + chunk
                else:
                    if current_chunk:  # 이전 청크 저장
                        merged_chunks.append(current_chunk)
                    current_chunk = chunk
            
            if current_chunk:  # 마지막 청크 저장
                merged_chunks.append(current_chunk)
            
            # 메타데이터 유지하면서 새 Document 객체 생성
            for chunk in merged_chunks:
                texts.append(Document(page_content=chunk, metadata=doc.metadata))
        
        # 디버그 정보 출력
        print(f"분할된 텍스트 청크 수: {len(texts)}개")
        if texts:
            print(f"첫 번째 청크 길이: {len(texts[0].page_content)} 글자")
            print(f"두 번째 청크 길이: {len(texts[1].page_content) if len(texts) > 1 else 0} 글자")
            print(f"첫 번째 청크 내용 일부: {texts[0].page_content[:100]}...")
        
        # 임베딩 차원 크기 계산
        dimension_size = len(self.embedding_model.embed_query("hello world"))
        
        # FAISS 벡터 저장소 생성
        vectorstore = FAISS(
            embedding_function=self.embedding_model,
            docstore=InMemoryDocstore(),
            index=faiss.IndexFlatL2(dimension_size),
            index_to_docstore_id={},
        )
        
        # 문서 추가
        vectorstore.add_documents(texts)
        
        return vectorstore
    
    def _save_vectorstore(self, db_file: str) -> None:
        """
        벡터 저장소 저장
        
        Args:
            db_file: 저장할 파일 경로
        """
        if self.vectorstore:
            self.vectorstore.save_local(db_file)
    
    def _load_vectorstore(self, db_file: str) -> FAISS:
        """
        벡터 저장소 로드
        
        Args:
            db_file: 로드할 파일 경로
            
        Returns:
            FAISS: 로드된 FAISS 벡터 저장소
        """
        return FAISS.load_local(
            db_file, 
            self.embedding_model, 
            allow_dangerous_deserialization=True
        )
    
    @staticmethod
    def _find_files(directory: str) -> List[str]:
        """
        디렉토리에서 PDF 파일 찾기
        
        Args:
            directory: 검색할 디렉토리 경로
            
        Returns:
            List[str]: PDF 파일 경로 목록
        """
        pdf_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        유사도 검색 수행
        
        Args:
            query: 검색 쿼리
            k: 반환할 결과 수
            
        Returns:
            List[Document]: 검색 결과 문서 목록
        """
        if not self.vectorstore:
            self.initialize()
        
        # 검색 수행
        results = self.vectorstore.similarity_search(query, k=k)
        
        # 검색 결과 길이 확인
        print(f"검색 쿼리: '{query}', 결과 {len(results)}개 받음")
        for i, doc in enumerate(results):
            print(f"  - 결과 {i+1} 길이: {len(doc.page_content)} 글자, 페이지: {doc.metadata.get('page', '?')}")
        
        return results


    def _test(self):
        # 캠시 파일 삭제
        import shutil
        if os.path.exists("./.cache/faiss_vectorstore"):
            print("캠시된 벡터 저장소 삭제 중...")
            shutil.rmtree("./.cache/faiss_vectorstore")
        
        # FAISS 벡터 저장소 초기화 - 적절한 청크 크기 사용
        vector_store = FaissVectorStore(chunk_size=1500, chunk_overlap=150)
        vector_store.initialize()

        # retriever = vector_store.vectorstore.as_retriever(search_kwargs={"k": 2})

        # 유사도 검색 수행
        # results = retriever.invoke("근로 시간")
        results = vector_store.similarity_search("근로 시간", k=3)

        # 결과 출력
        # Rich 콘솔 생성
        console = Console()
            
        # 검색 결과 헤더 출력
        console.print("\n")
        console.print(Panel("[bold cyan]검색 결과[/bold cyan]", border_style="cyan"))
        console.print("\n")
        
        # 각 결과 출력
        for i, doc in enumerate(results):
            # 결과 정보 테이블 생성
            table = Table(title=f"[bold]결과 {i+1}[/bold]", box=ROUNDED)
            table.add_column("항목", style="cyan")
            table.add_column("내용", style="white")
            
            # 출처 파일 경로 처리 - 파일명만 추출
            source = doc.metadata.get('source', '알 수 없음')
            file_name = os.path.basename(source) if source != '알 수 없음' else '알 수 없음'
            
            # 테이블에 데이터 추가
            table.add_row("파일", f"[blue]{file_name}[/blue]")
            table.add_row("페이지", f"[green]{doc.metadata.get('page', '알 수 없음')}[/green]")
            
            # 내용 처리
            content = doc.page_content
            
            # 디버그 정보 출력
            console.print(f"[bold yellow]디버그 정보:[/bold yellow]")
            console.print(f"문서 내용 길이: {len(doc.page_content)} 글자")
            
            # 결과 출력
            console.print(table)
            console.print(Panel(content, title=f"[bold green]문서 내용 ({len(doc.page_content)} 글자)[/bold green]", border_style="green"))
            console.print("\n" + "-" * 80 + "\n")
        





if __name__ == "__main__":
    vector_store = FaissVectorStore()
    vector_store._test()
