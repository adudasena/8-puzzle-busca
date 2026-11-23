from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em profundidade com limite de profundidade.

    Cada estado é expandido no máximo uma vez. Nós além de depth_limit
    não geram filhos. A solução encontrada não é necessariamente a mais curta.
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        frontier = [initial]
        seen = {initial}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            node = frontier.pop()
            nodes_expanded += 1

            if node.cost >= self.depth_limit:
                continue

            for child in node.neighbors():
                if child in seen:
                    continue
                nodes_generated += 1
                seen.add(child)
                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max(max_frontier_size, len(frontier) + 1),
                        depth=child.cost,
                    )
                if child.cost < self.depth_limit:
                    frontier.append(child)
                    max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
