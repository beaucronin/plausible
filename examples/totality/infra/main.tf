provider "plausible" {
    logging = ""
}

resource "plausible_http_api" "public" {
    openapi_spec = "${var.api_home}/public/"
}

resource "plausible_data_schema" "input_observation" {
    source = "${var.data_home}/observation/"
}

resource "plausible_function" "post_observations" {
    source = "${var.code_home}/observation-validator/"

    api_route_trigger {
        api_id = plausible_http_api.public.id
        route = "/observations"
        method = "post"
        content_type = "application/json"
        request_data = plausible_data_schema.input_observation
    }

    schedule_trigger {
        cron = "5 * * * 1 * *"
    }

    datastore_trigger {

    }

    subscription_trigger {
        publisher_id = plausible_publisher.observation_events.id
    }

    function_output {
        name = "kv"
        target = plausible_keyvalue_store.observations.id
    }

    function_output {
        name = "stream"
        target = plausible_stream_analytics.observations.id
    }

    function_output {
        name = "publish"
        target = plausible_publisher.observation_events.id
    }
}

resource "plausible_stream_analytics" "observations" {
    source = "${var.code_home}/observation-stream-analytics/"

    output {
        target = plausible_publisher.observation_events
    }
}

resource "plausible_object_store" "obj" {
    name = "my-object-store"

}

resource "plausible_keyvalue_store" "observations" {
    index {
        type = "primary"
        key = "compound"
    }

    index {
        type = "secondary"
        key = "compound"
        name = "GSI1"
    }
}

resource "plausible_publisher" "observation_events" {

}

resource "plausible_graphql_api" "percepts" {

}

resource "plausible_function" "example_interpreter" {
    source = "${var.code_home}/observation-validator/"

    subscription_trigger {
        publisher = plausible_publisher.observation_events

        filter = {
            
        }
    }
}