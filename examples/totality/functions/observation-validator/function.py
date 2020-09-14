from typing import Dict, Any, List
import plausible as pbl
from plausible.util.json import JSON


@pbl.resource("plausible_function.post_observations")
@pbl.http.validate_json_schema
def handler():
    trigger = pbl.function.current_trigger
    assert trigger.trigger_type == "http"
    assert trigger.http.content_type == "application/json"
    assert trigger.http.method == "post"

    observations = extract_observations(trigger.payload)

    for observation in observations:
        # stream_analytics: pbl.types.StreamAnalytics = pbl.resource.plausible_stream_analytics.observations
        sa_output: pbl.types.StreamAnalytics = pbl.function.output.stream
        sa_output.put(observation)

        kv_output: pbl.types.KeyValue = pbl.function.output.kv
        kv_output.put(get_observation_key(observation["nodeId"]), observation)


def extract_observations(payload_: Dict[str, Any]) -> List[Dict]:
    """Multiple observations can be posted in a single json doc; this 
    method breaks those into separate objects.

    Args:
        payload_ (Dict[str, Any]): The payload in the post body

    Returns:
        List[Dict]: A list of the observations, as separated out
    """
    jp = "$.nodes"
    payload = JSON(payload_)
    items = payload.read(jp)
    outer = payload.delete(jp)
    return [outer.clone().insert("$.node", item).to_dict() for item in items]


def get_observation_key(node_id):
    """Serialize the node_id dictionary that is provided with an observation into
    a pipe-delimited string. Only identifiers whose numerical id ends in 0 will be 
    included in the serialized string; other identifiers are skipped

    Args:
        node_id (Dict[str, str]): The dict containing the various identifiers of the observation

    Returns:
        str: The pipe-delimited id serialization
    """
    return "|".join(
        [node_id[k] for k in sorted(node_id.keys()) if k.split(" ")[0].endswith("0")]
    )
