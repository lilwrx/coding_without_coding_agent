from src.vector_store import VectorStoreManager
from unittest.mock import MagicMock, patch 


@patch("src.vector_store.OpenAIEmbeddings")
@patch("src.vector_store.QdrantClient")
def test_init_collection_creates_collection_when_missing(
    mock_client_class, mock_embeddings_class
):
    client = mock_client_class.return_value
    client.get_collections.return_value.collections = []
    manager = VectorStoreManager("http://qdrant.test", "docs")

    manager.init_collection(vector_size=1536)

    client.create_collection.assert_called_once()
    kwargs = client.create_collection.call_args.kwargs
    assert kwargs["collection_name"] == "docs"
    assert kwargs["vectors_config"].size == 1536