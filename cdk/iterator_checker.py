from pylint.checkers import BaseChecker
from astroid import nodes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pylint.lint import PyLinter

class IteratorMisuseChecker(BaseChecker):
    name = 'iterator-misuse'
    priority = -1
    msgs = {
        'E9901': (
            'Iterator variable used as iterable in comprehension',
            'iterator-variable-misuse',
            'Iterator variable should not be used as the iterable in the same comprehension'
        ),
    }

    def visit_listcomp(self, node: nodes.ListComp) -> None:
        for generator in node.generators:
            target_names = {name.name for name in generator.target.nodes_of_class(nodes.Name)}
            iter_names = {name.name for name in generator.iter.nodes_of_class(nodes.Name)}
            if target_names & iter_names:
                self.add_message('E9901', node=node)

def register(linter: "PyLinter") -> None:
    """Register the checker."""
    linter.register_checker(IteratorMisuseChecker(linter))
