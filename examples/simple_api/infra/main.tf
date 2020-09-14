locals {
    apis_home = "${var.app_home}/apis"
    functions_home = "${var.app_home}/functions"
}

resource "plausible_http_api" "main" {
    spec_file = "${local.apis_home}/main/api.yaml"
}

resource "plausible_function" "post_item" {
    source = "${local.functions_home}/post-item/"

    api_route_trigger {
        api_id = plausible_http_api.main.id
        route = "/items"
        method = "POST"
    }
}

resource "plausible_object_store" "freeform" {
    key_type = "simple"
}

resource "plausible_object_store" "recursive" {
    key_type = "composite"

    key_component {
        name = "path"
        parent = "path"
    }

    key_component {
        terminal = true
        parent = "path"
    }
}

resource "plausible_object_store" "hierarchical" {
    key_type = "composite"
    
    key_component {
        name = "stage"
        enum = ["prod", "dev", "test", "meta"]
    }

    key_component {
        name = "year"
        parent = "stage"
        regex = "^\d{4}$"
    }

    key_component {
        name = "month"
        parent = "year",
        regex = "^\d{2}$"
    }

    key_component {
        name = "day"
        parent = "month",
        regex = "^\d{2}$"
    }

    key_component {
        terminal = true
        parent = "day"
    }

    key_component {
        name = "meta_entry"
        parent = "stage"
        parent_val = ["meta"]
    }
}

# resource "plausible_function" "get_item" {
#     source = "${local.functions_home}/get-item/"

#     api_route_trigger {
#         api = plausible_http_api.main.id
#         route = "/item/{}"
#         method = "get"
#         content_type = "application/json"
#     }
# }
