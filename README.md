# 🚀 RAG Pipeline Project Roadmap (Production-Grade)

> **Mục tiêu:** Xây dựng một hệ thống **RAG (Retrieval-Augmented Generation)** chuẩn sản phẩm, không sử dụng Coding Agent, tối ưu hóa độ chính xác bằng **Hybrid Search + Reranking**, có khả năng mở rộng (Scale) và cung cấp API Streaming thời gian thực bằng FastAPI.

---

## 🛠️ Kiến trúc Hệ thống (Target Architecture)

```text
[Documents] ➔ [Loader] ➔ [Recursive Splitter] ➔ [OpenAI Embeddings] ➔ [Qdrant Vector DB]
                                                                            │
[User Query] ➔ [Query Rewriter] ───────────────────────────────────────────┼──> [Hybrid Search: Dense + BM25]
                                                                            │                 │
                                                                            ▼                 ▼
                                                                [Reranker (Cohere/Cross-Encoder)]
                                                                                              │
                                                                                              ▼
User Response ◄── [SSE Streaming] ◄── [FastAPI Server] ◄── [GPT-4o / Prompt] ◄── [Top Chunks]