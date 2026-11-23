import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):
    """A* com distância de Manhattan (admissível e consistente no 8-puzzle)."""

    def heuristic(self, state: State) -> int:
        """Soma das distâncias de Manhattan de cada peça até a meta. O vazio não entra."""
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = tile - 1
            row, col = divmod(index, 3)
            goal_row, goal_col = divmod(goal_index, 3)
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        counter = 0
        frontier: list[tuple[int, int, State]] = [
            (self.heuristic(initial), counter, initial)
        ]
        best_cost = {initial.tiles: 0}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            _f, _tie, node = heapq.heappop(frontier)
            if node.cost > best_cost.get(node.tiles, node.cost):
                continue

            nodes_expanded += 1
            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            for child in node.neighbors():
                previous = best_cost.get(child.tiles)
                if previous is not None and child.cost >= previous:
                    continue
                nodes_generated += 1
                best_cost[child.tiles] = child.cost
                counter += 1
                priority = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (priority, counter, child))
                max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )
