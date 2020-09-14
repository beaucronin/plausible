import plausible as pbl
from plausible import ObjectStoreKey

import logging

logger = logging.getLogger(__name__)


@pbl.resource("plausible_function.post_item")
def handler():
    trigger = pbl.function.current_trigger
    item_obj = trigger.payload

    obj_store = pbl.resource.object_store.hierarchical
    obj, err = obj_store.get(
        ObjectStoreKey("stage", "prod")
        .append("year", "2020")
        .append("month", "09")
        .append("day", "09")
        .append(name="some_terminal_name.txt")
    )
    if err:
        logger.error(err)
        return

    return True
