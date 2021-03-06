import logging
from bisect_b2g.repository import Rev

log = logging.getLogger(__name__)


def make_revision_linked_list(project):
    _rev_list = reversed(project.rev_list())
    head = None

    for hash, date in _rev_list:
        head = Rev(hash, project, date, head)

    return head


def create_line(exhausted_heads, heads):
    line = sorted(exhausted_heads + heads, key=lambda x: x.date)
    oldest_head = line[0]
    oldest_head_i = heads.index(oldest_head)
    if oldest_head.next_rev is None:
        log.debug("Exhausted %s", oldest_head.prj.name)
        exhausted_heads.append(oldest_head)
        del heads[oldest_head_i]
    else:
        log.debug("Moving %s to next revision", oldest_head.prj.name)
        heads[oldest_head_i] = heads[oldest_head_i].next_rev
    line.sort(key=lambda x: x.prj.name)
    log.debug("Generated a line of history: %s", [x.tag() for x in line])
    return sorted(line, key=lambda x: x.prj.name)


def build_history(projects):
    history = []
    exhausted_heads = []
    heads = [make_revision_linked_list(x) for x in projects]

    while len(heads) > (len(heads) + len(exhausted_heads) - 1):
        history.append(create_line(exhausted_heads, heads))

    log.debug("Global History:")
    for line in history:
        log.debug(["%s@%s" % (x.prj.name, x.tag()) for x in line])
    return history


def validate_history(history):
    pass
