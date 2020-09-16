provider "plausible" {}

resource "plausible_keyvalue_store" "observations" {
    primary_index {
        partition_key = "PartKey"
        row_key = "RowKey"
    }

    secondary_index {
        name = "SI1"
        partition_key = "SIPartKey"
        row_key = "SIRowKey"
    }
}
