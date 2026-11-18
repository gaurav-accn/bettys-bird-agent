
import os

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine


def search(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> list[str]:

    client_options = (
        ClientOptions(
            api_endpoint=f"{location}-discoveryengine.googleapis.com"
        )
        if location != "global"
        else None
    )

    client = discoveryengine.SearchServiceClient(
        client_options=client_options
    )

    serving_config = (
        f"projects/{project_id}/locations/{location}"
        f"/collections/default_collection/engines/{engine_id}"
        f"/servingConfigs/default_config"
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=5,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                return_snippet=True
            ),
            extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                max_extractive_answer_count=1,
                max_extractive_segment_count=1,
            ),
        ),
    )

    response = client.search(request)

    results = []

    for result in response.results:
        data = result.document.derived_struct_data

        for item in data.get("snippets", []):
            if item.get("snippet"):
                results.append(item["snippet"])

        for item in data.get("extractive_answers", []):
            if item.get("content"):
                results.append(item["content"])

    return results


def search_store_documents(query: str) -> list[str]:

    project_id = os.environ.get(
        "DATASTORE_PROJECT_ID",
        os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
    )

    location = os.environ.get("DATASTORE_LOCATION", "global")
    engine_id = os.environ["DATASTORE_ENGINE_ID"]

    return search(
        project_id=project_id,
        location=location,
        engine_id=engine_id,
        search_query=query,
    )
