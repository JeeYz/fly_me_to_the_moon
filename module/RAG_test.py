
import global_variables as gv
from vector_store_setting import VectorStoreSetting
from langchain_community.vectorstores.sklearn import SKLearnVectorStoreException

config_setting = {
    "absolute_path": gv.absolute_path,
    "vector_store_path": gv.absolute_vector_store_path,
    "model_name": gv.ollama_models[0],
    "temperature": 0.0,
    "embedding_model_name": gv.ollama_embedding_models[2],
    "retriever_top_k": 3,
    "batch_size": 32,  # 임베딩 생성 시 배치 크기 설정
}

import logging

def main():
    # VectorStoreSetting 클래스 인스턴스 생성
    vector_store_setting = VectorStoreSetting(
        **config_setting
    )

    try:
        # VectorStoreSetting 인스턴스 초기화 세팅 -> vector db 생성
        vectorstore = vector_store_setting.initialize()
        
        # 벡터 저장소에서 검색기 생성
        retriever = vector_store_setting._create_retriever(vectorstore)
        print(f"검색기 생성 완료 (top_k={config_setting['retriever_top_k']})")
        
        # 질의 실행
        query = "무역 보험 약관에 대한 정보를 알려줘."
        print(f"\n질의: {query}")
        response_invoke = retriever.invoke(query)

        print("\n검색 결과:")
        for i, doc in enumerate(response_invoke):
            print(f"\n[문서 {i+1}]")
            print(f"출처: {doc.metadata.get('source_file', '알 수 없음')}")
            print(f"내용: {doc.page_content[:150]}...")
    
    except ValueError as e:
        print(f"\n오류 발생: {e}")
        print("\n벡터 저장소를 생성하기 위해 문서를 먼저 로드해야 합니다.")
        print("예시: PyMuPDFLoader를 사용하여 PDF 파일을 로드하고 벡터 저장소를 생성하세요.")
    
    except SKLearnVectorStoreException as e:
        print(f"\n벡터 저장소 오류 발생: {e}")
        print("\n벡터 저장소에 데이터가 없습니다.")
        print("벡터 저장소를 생성하기 위해 문서를 먼저 로드해야 합니다.")
        print("예시: PyMuPDFLoader를 사용하여 PDF 파일을 로드하고 벡터 저장소를 생성하세요.")
    
    except Exception as e:
        print(f"\n예상치 못한 오류 발생: {e}")





if __name__ == "__main__":
    main()