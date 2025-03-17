from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_community.vectorstores.sklearn import SKLearnVectorStoreException
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader

import os
import glob
import logging
import time
from typing import List, Any
from tqdm import tqdm

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VectorStoreSetting:
    """
    벡터 저장소 설정 및 관리를 위한 클래스
    
    PDF 문서를 로드하고 벡터화하여 저장소에 저장하거나 기존 저장소를 로드하는 기능 제공
    """

    def __init__(self, **kwargs):
        """
        VectorStoreSetting 클래스 초기화
        
        Args:
            absolute_path (str): PDF 문서가 저장된 절대 경로
            vector_store_path (str): 벡터 저장소 경로
            model_name (str): 사용할 모델 이름
            temperature (float): 모델 온도 설정
            embedding_model_name (str): 사용할 임베딩 모델 이름
            batch_size (int): 임베딩 생성 시 배치 크기
            retriever_top_k (int): 검색 시 반환할 문서 수
        """
        self.absolute_path = kwargs.get("absolute_path")
        self.vector_store_path = kwargs.get("vector_store_path")
        self.model_name = kwargs.get("model_name")
        self.temperature = kwargs.get("temperature")
        self.retriever_top_k = kwargs.get("retriever_top_k", 3)
        self.embedding_model_name = kwargs.get("embedding_model_name")
        self.batch_size = kwargs.get("batch_size", 32)  # 기본 배치 크기 32

        self.vector_db: SKLearnVectorStore = None

    def initialize(self):
        """
        벡터 저장소 초기화 함수
        
        기존 벡터 저장소가 있으면 로드하고, 없으면 새로 생성
        
        Returns:
            vectorstore 또는 retriever: 벡터 저장소 또는 검색기 객체
        """
        # 벡터 저장소 경로가 존재하는 경우 로드
        if os.path.exists(self.vector_store_path):
            return self._load_existing_vectorstore()
        else:
            # 벡터 저장소 경로가 없는 경우 새로 생성
            return self._create_new_vectorstore()

    def _load_existing_vectorstore(self):
        """
        기존 벡터 저장소 로드
        
        Returns:
            vectorstore: 로드된 벡터 저장소 객체
        """
        logger.info(f"벡터 저장소 DB를 로드합니다: {self.vector_store_path}")
        
        # 새로 구현한 로드 메서드 사용
        db_file = os.path.join(self.vector_store_path, "sklearn_vectorstore")
        vectorstore = self._load_vector_store(db_file)
        
        if vectorstore is None:
            logger.warning("벡터 저장소 로드 실패, 기존 방식으로 시도합니다.")
            # 기존 방식으로 로드 시도 (폴백)
            try:
                vectorstore = SKLearnVectorStore(
                    embedding=OllamaEmbeddings(
                        model=self.embedding_model_name
                    ),
                    persist_path=self.vector_store_path,
                    serializer="bson"  # 바이너리 JSON 형식으로 로드
                )
                logger.info("기존 방식으로 벡터 저장소 DB 로드 완료")
            except Exception as e:
                logger.error(f"벡터 저장소 로드 실패: {e}")
                return None
        
        logger.info("벡터 저장소 DB 로드 완료")
        return vectorstore

    def _create_new_vectorstore(self):
        """
        새로운 벡터 저장소 생성
        
        PDF 문서를 로드하고 분할한 후 벡터화하여 저장소에 저장
        
        Returns:
            retriever: 생성된 벡터 저장소의 검색기 객체
        """
        logger.info(f"벡터 저장소 DB를 생성합니다: {self.vector_store_path}")
        
        # 캐시 폴더 생성 (없는 경우)
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        # 벡터 저장소 파일 경로 설정
        db_file = os.path.join(self.vector_store_path, "sklearn_vectorstore")

        # 파일 탐색 및 로드
        pdf_files = self._find_pdf_files(self.absolute_path)
        docs_list = self._load_pdf_documents(pdf_files)

        # 문서가 없는 경우 처리
        if not docs_list:
            logger.warning("로드된 문서가 없습니다. 벡터 저장소 생성을 건너뜁니다.")
            return None

        # 문서 분할
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000,
            chunk_overlap=100
        )
        logger.info("문서 분할 중...")
        doc_splits = text_splitter.split_documents(docs_list)
        logger.info(f"문서를 {len(doc_splits)}개의 청크로 분할했습니다.")

        # 벡터 저장소 생성 시도
        try:
            # 새로운 벡터 저장소 생성
            vectorstore = self._create_and_save_vectorstore(self.vector_store_path, db_file, doc_splits)
            
            # 새로 구현한 저장 메서드 사용
            success = self._save_vector_store(vectorstore, db_file)
            if success:
                logger.info(f"벡터 저장소를 성공적으로 저장했습니다: {db_file}")
            else:
                logger.warning("벡터 저장소 저장에 실패했지만, 메모리에는 로드되었습니다.")
            
            # 검색기 생성
            retriever = self._create_retriever(vectorstore)
            logger.info(f"검색기 생성 완료 (top_k={self.retriever_top_k})")
            
            return retriever
            
        except Exception as e:
            # 오류 발생 시 폴백 벡터 저장소 생성 (저장 없이)
            logger.warning(f"벡터 저장소 생성 중 오류 발생: {e}")
            logger.info("폴백 벡터 저장소를 생성합니다 (메모리에만 저장)")
            
            vectorstore = self._create_fallback_vectorstore(doc_splits, e)
            
            # 검색기 생성
            retriever = self._create_retriever(vectorstore)
            logger.info(f"폴백 검색기 생성 완료 (top_k={self.retriever_top_k})")
            
            return retriever

    def _load_db_file(self, db_file):
        """
        기존 DB 파일 로드
        
        Args:
            db_file (str): 로드할 DB 파일 경로
            
        Returns:
            vectorstore: 로드된 벡터 저장소 객체
        """
        logger.info(f"기존 벡터 저장소 DB를 로드합니다: {db_file}")
        
        # 새로 구현한 로드 메서드 사용
        vectorstore = self._load_vector_store(db_file)
        
        # 로드 실패 시 기존 방식으로 시도
        if vectorstore is None:
            logger.warning("새 방식으로 로드 실패, 기존 방식으로 시도합니다.")
            try:
                # 저장된 벡터스토어 로드 (BSON 형식)
                vectorstore = SKLearnVectorStore(
                    embedding=OllamaEmbeddings(
                        model=self.embedding_model_name
                    ),
                    persist_path=db_file,
                    serializer="bson"  # 바이너리 JSON 형식으로 로드
                )
                logger.info("기존 방식으로 벡터 저장소 DB 로드 완료")
            except Exception as e:
                logger.error(f"벡터 저장소 로드 실패: {e}")
                return None
        
        logger.info("기존 벡터 저장소 DB 로드 완료")
        return vectorstore

    def _create_and_save_vectorstore(self, vectorstore_path, db_file, doc_splits):
        """
        새 벡터 저장소 생성 및 저장 (배치 처리 적용)
        
        Args:
            vectorstore_path (str): 벡터 저장소 디렉토리 경로
            db_file (str): 저장할 DB 파일 경로
            doc_splits (list): 분할된 문서 리스트
            
        Returns:
            vectorstore: 생성된 벡터 저장소 객체
        """
        logger.info("새로운 벡터 저장소 DB를 생성합니다.")
        os.makedirs(vectorstore_path, exist_ok=True)
        
        # 임베딩 모델 초기화
        embedding_model = OllamaEmbeddings(
            model=self.embedding_model_name
        )
        
        # 배치 처리를 위한 설정
        total_docs = len(doc_splits)
        batch_size = self.batch_size
        total_batches = (total_docs + batch_size - 1) // batch_size  # 올림 나눗셈
        
        logger.info(f"총 {total_docs}개 문서를 {batch_size}개씩 {total_batches}개 배치로 처리합니다.")
        print(f"\n[임베딩 벡터 생성] 총 {total_docs}개 문서, 배치 크기: {batch_size}")
        
        # 배치 처리 시작 시간 기록
        start_time = time.time()
        
        # 배치 단위로 문서 처리
        processed_docs = []
        for i in tqdm(range(0, total_docs, batch_size), desc="임베딩 벡터 생성 중"):
            batch = doc_splits[i:i+batch_size]
            batch_start_time = time.time()
            
            # 현재 배치 정보 로깅
            batch_num = i // batch_size + 1
            logger.info(f"배치 {batch_num}/{total_batches} 처리 중 ({len(batch)}개 문서)")
            
            # 배치 처리 완료 후 진행 상황 업데이트
            processed_docs.extend(batch)
            batch_end_time = time.time()
            batch_duration = batch_end_time - batch_start_time
            
            logger.info(f"배치 {batch_num} 완료: {batch_duration:.2f}초 소요 (누적: {len(processed_docs)}/{total_docs})")
            
            # 배치 처리 중간 결과 출력
            elapsed = batch_end_time - start_time
            docs_per_sec = len(processed_docs) / elapsed if elapsed > 0 else 0
            remaining = (total_docs - len(processed_docs)) / docs_per_sec if docs_per_sec > 0 else 0
            print(f"  - 진행률: {len(processed_docs)}/{total_docs} ({len(processed_docs)/total_docs*100:.1f}%) | 예상 남은 시간: {remaining:.1f}초")
        
        # 벡터 저장소 생성 및 저장
        logger.info("벡터 저장소 생성 중...")
        vectorstore = SKLearnVectorStore.from_documents(
            documents=doc_splits,
            embedding=embedding_model,
            persist_path=db_file,  # DB 파일 경로 지정
            serializer="bson"  # 바이너리 JSON 형식으로 저장
        )
        
        # 총 소요 시간 계산 및 로깅
        total_duration = time.time() - start_time
        logger.info(f"벡터 저장소를 DB 파일로 저장했습니다: {db_file}")
        logger.info(f"벡터 저장소 생성 완료: 총 {total_duration:.2f}초 소요")
        print(f"[완료] 벡터 저장소 생성 완료: 총 {total_duration:.2f}초 소요\n")
        
        return vectorstore

    def _create_fallback_vectorstore(self, doc_splits, error):
        """
        오류 발생 시 폴백 벡터 저장소 생성 (저장 없이, 배치 처리 적용)
        
        Args:
            doc_splits (list): 분할된 문서 리스트
            error (Exception): 발생한 오류
            
        Returns:
            vectorstore: 생성된 벡터 저장소 객체
        """
        logger.error(f"벡터 저장소 생성/로드 실패: {str(error)}")
        logger.warning("저장 기능 없이 벡터 저장소를 생성합니다.")
        
        # 임베딩 모델 초기화
        embedding_model = OllamaEmbeddings(
            model=self.embedding_model_name
        )
        
        # 배치 처리를 위한 설정
        total_docs = len(doc_splits)
        batch_size = self.batch_size
        total_batches = (total_docs + batch_size - 1) // batch_size  # 올림 나눗셈
        
        logger.info(f"총 {total_docs}개 문서를 {batch_size}개씩 {total_batches}개 배치로 처리합니다.")
        print(f"\n[임베딩 벡터 생성 (폴백 모드)] 총 {total_docs}개 문서, 배치 크기: {batch_size}")
        
        # 배치 처리 시작 시간 기록
        start_time = time.time()
        
        # 배치 단위로 문서 처리
        processed_docs = []
        for i in tqdm(range(0, total_docs, batch_size), desc="임베딩 벡터 생성 중"):
            batch = doc_splits[i:i+batch_size]
            batch_start_time = time.time()
            
            # 현재 배치 정보 로깅
            batch_num = i // batch_size + 1
            logger.info(f"배치 {batch_num}/{total_batches} 처리 중 ({len(batch)}개 문서)")
            
            # 배치 처리 완료 후 진행 상황 업데이트
            processed_docs.extend(batch)
            batch_end_time = time.time()
            batch_duration = batch_end_time - batch_start_time
            
            logger.info(f"배치 {batch_num} 완료: {batch_duration:.2f}초 소요 (누적: {len(processed_docs)}/{total_docs})")
            
            # 배치 처리 중간 결과 출력
            elapsed = batch_end_time - start_time
            docs_per_sec = len(processed_docs) / elapsed if elapsed > 0 else 0
            remaining = (total_docs - len(processed_docs)) / docs_per_sec if docs_per_sec > 0 else 0
            print(f"  - 진행률: {len(processed_docs)}/{total_docs} ({len(processed_docs)/total_docs*100:.1f}%) | 예상 남은 시간: {remaining:.1f}초")
        
        # 벡터 저장소 생성 (저장 없이)
        logger.info("벡터 저장소 생성 중...")
        vectorstore = SKLearnVectorStore.from_documents(
            documents=doc_splits,
            embedding=embedding_model
        )
        
        # 총 소요 시간 계산 및 로깅
        total_duration = time.time() - start_time
        logger.warning("저장 기능 없이 벡터 저장소를 생성했습니다.")
        logger.info(f"벡터 저장소 생성 완료: 총 {total_duration:.2f}초 소요")
        print(f"[완료] 벡터 저장소 생성 완료: 총 {total_duration:.2f}초 소요\n")
        
        return vectorstore

    def _create_retriever(self, vectorstore):
        """
        검색기 생성
        
        Args:
            vectorstore (SKLearnVectorStore): 벡터 저장소 객체
            
        Returns:
            retriever: 생성된 검색기 객체
            
        Raises:
            ValueError: 벡터 저장소가 None이거나 비어있는 경우 발생
        """
        if vectorstore is None:
            logger.error("벡터 저장소가 None입니다. 검색기를 생성할 수 없습니다.")
            raise ValueError("벡터 저장소가 비어 있습니다. 문서를 먼저 로드하고 벡터 저장소를 생성해주세요.")
        
        try:
            retriever = vectorstore.as_retriever(k=self.retriever_top_k)
            logger.info("검색기 생성 완료")
            return retriever
        except SKLearnVectorStoreException as e:
            logger.error(f"SKLearnVectorStore 예외 발생: {e}")
            raise ValueError("벡터 저장소에 데이터가 없습니다. 문서를 먼저 로드하고 벡터 저장소를 생성해주세요.")


    def _find_pdf_files(self, directory: str) -> List[str]:
        """
        주어진 디렉토리와 그 하위 디렉토리에서 모든 PDF 파일을 찾아 경로 리스트를 반환합니다.
        
        Args:
            directory (str): 탐색할 디렉토리 경로
            
        Returns:
            List[str]: 발견된 모든 PDF 파일의 경로 리스트
        """
        pdf_files = []
        
        # 디렉토리가 존재하는지 확인
        if not os.path.exists(directory):
            logger.error(f"디렉토리가 존재하지 않습니다: {directory}")
            return pdf_files
        
        # 모든 PDF 파일 찾기 (대소문자 구분 없이)
        pattern = os.path.join(directory, "**", "*.pdf")
        pdf_files = glob.glob(pattern, recursive=True)
        
        # 결과 로깅
        logger.info(f"총 {len(pdf_files)}개의 PDF 파일을 찾았습니다.")
        
        # 처음 5개 파일만 상세 로깅
        for pdf in pdf_files[:5]:
            logger.info(f"PDF 파일: {os.path.basename(pdf)}")
        
        if len(pdf_files) > 5:
            logger.info(f"... 외 {len(pdf_files) - 5}개 파일")
            
        return pdf_files


    def _load_pdf_documents(self, pdf_files: List[str]) -> List[Any]:
        """
        PDF 파일 목록을 로드하여 문서 객체 리스트를 반환합니다.
        
        Args:
            pdf_files (List[str]): PDF 파일 경로 리스트
            
        Returns:
            List[Any]: 로드된 문서 객체 리스트
        """
        documents = []
        
        for pdf_file in pdf_files:
            try:
                # PyMuPDFLoader를 사용하여 PDF 파일 로드
                loader = PyMuPDFLoader(pdf_file)
                docs = loader.load()
                
                # 메타데이터에 파일명 추가
                for doc in docs:
                    doc.metadata["source_file"] = os.path.basename(pdf_file)
                    
                documents.extend(docs)
                logger.info(f"로드 완료: {os.path.basename(pdf_file)} - {len(docs)}페이지")
            except Exception as e:
                logger.error(f"파일 로드 실패: {pdf_file}, 오류: {str(e)}")
        
        logger.info(f"총 {len(documents)}개의 문서 청크를 로드했습니다.")
        return documents

    def _save_vector_store(self, vectorstore, db_file):
        """
        벡터 저장소를 파일로 저장
        
        Args:
            vectorstore (SKLearnVectorStore): 저장할 벡터 저장소 객체
            db_file (str): 저장할 파일 경로
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            # 저장소 경로가 없으면 생성
            os.makedirs(os.path.dirname(db_file), exist_ok=True)
            
            # 벡터 저장소 저장
            vectorstore.save_local(db_file)
            logger.info(f"벡터 저장소를 저장했습니다: {db_file}")
            self.vector_db = vectorstore
            return True
        except Exception as e:
            logger.error(f"벡터 저장소 저장 실패: {e}")
            return False

    def _load_vector_store(self, db_file):
        """
        벡터 저장소를 파일에서 로드
        
        Args:
            db_file (str): 로드할 파일 경로
            
        Returns:
            SKLearnVectorStore or None: 로드된 벡터 저장소 객체 또는 실패 시 None
        """
        try:
            if not os.path.exists(db_file):
                logger.warning(f"벡터 저장소 파일이 없습니다: {db_file}")
                return None
                
            # 임베딩 모델 생성
            embeddings = OllamaEmbeddings(model=self.embedding_model_name)
            
            # 벡터 저장소 로드
            vectorstore = SKLearnVectorStore.load_local(
                folder_path=db_file,
                embeddings=embeddings
            )
            logger.info(f"벡터 저장소를 로드했습니다: {db_file}")
            self.vector_db = vectorstore
            return vectorstore
        except Exception as e:
            logger.error(f"벡터 저장소 로드 실패: {e}")
            return None