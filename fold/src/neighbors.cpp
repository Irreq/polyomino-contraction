#include "neighbors.hpp"
#include "network.hpp"

class Neighbors
{
private:
    std::unordered_map<Position, Node*> neighbors;
    std::unordered_map<Node*, Position> neighbors_inverted;

public:

    Neighbors() = default;

    bool is_neighbor(Node* node)
    {
        return neighbors_inverted.find(node) != neighbors_inverted.end();
    }

    bool is_neighbor(Position position)
    {
        return neighbors.find(position) != neighbors.end();
    }

    void add(Node* node)
    {
        Position position = node->get_position();
        neighbors[position] = node;
        neighbors_inverted[node] = position;
    }

    void remove(Node* node) {
        Position position = neighbors_inverted[node];
        neighbors.erase(position);
        neighbors_inverted.erase(node);
    }

    /* Retrieve existing neighbors */
    std::vector<Node*> get_neighbors() {
        std::vector<Node*> neighbor_nodes;
        neighbor_nodes.reserve(neighbors.size());
        for (const auto& entry : neighbors_inverted) {
            neighbor_nodes.push_back(entry.first);
        }
        return neighbor_nodes;
    }

    /* Sync the relation between `Position` and `Node` */
    void update() {
        std::unordered_map<Node*, Position> old_neighbors = neighbors_inverted;
        neighbors.clear();
        neighbors_inverted.clear();

        for (const auto& entry : old_neighbors) {
            Node* node = entry.first;
            add(node); // Let the adder handle putting it back
        }
    }
};