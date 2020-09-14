resource "plausible_function" "enqueue" {
    source = "${local.functions_home}/enqueue/"

    schedule_trigger {
        cron = "5 * * * 1 * *"        
    }
}

resource "plausible_function" "ingest" {
    source = "${local.functions_home}/enqueue/"

    output {
        name = "kv"
        target = plausible_keyvalue_store.kv.id
    }
}

resource "plausible_keyvalue_store" "vehicles_kv" {

}

resource "plausible_keyvalue_store" "reads_kv" {

}