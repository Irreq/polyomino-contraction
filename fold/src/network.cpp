#include <unordered_map>
#include <stdexcept>
#include <iostream>
#include <vector>

#include "neighbors.hpp"
#include "network.hpp"

enum Direction {
    UP,DOWN,RIGHT,LEFT
};

/* A Position is a collection of coordinates in space */
struct Position
{
    int x;
    int y;

    Position() = default;

    Position(int xPos, int yPos) : x(xPos), y(yPos) {}

public:
    Position convert_direction(Direction direction) {
        Position new_position(x, y);

        switch (direction) {
            case UP:    new_position.y += 1; break;
            case DOWN:  new_position.y -= 1; break;
            case LEFT:  new_position.x -= 1; break;
            case RIGHT: new_position.x += 1; break;
        }

        return new_position;
    }

     // Equality operator
    bool operator==(const Position& other) const {
        return x == other.x && y == other.y;
    }
};

// Custom hash function specialization for Position
namespace std {
    template <>
    struct hash<Position> {
        size_t operator()(const Position& pos) const {
            // Combine the hash values of x and y using a suitable hash function
            // Here's a simple example using the std::hash function
            return hash<int>()(pos.x) ^ hash<int>()(pos.y);
        }
    };
}

// class Neighbors; // Forward declaration
class Node;


class Node
{
private:
    Position position;
    Neighbors* neighbors;
public:

    Node(int x, int y) : position(x, y), neighbors(nullptr)
    {
    }

    Position get_position() {
        return this->position;
    }

    void connect(Node* node);

    std::vector<Node*> get_neighbors() {
        return this->neighbors->get_neighbors();
    }

    // void connect(Node* node) {
    //     if (!neighbors->is_neighbor(node)) {
    //         neighbors->add(node);
    //     }
    // }

    // void disconnect(Node* node) {
    //     if (neighbors->is_neighbor(node)) {
    //         neighbors->remove(node);
    //     }
    // }

    // Equality operator
    bool operator==(const Node& other) const {
        return this == &other;
    }
};

// class Neighbors
// {
// private:
//     std::unordered_map<Position, Node*> neighbors;
//     std::unordered_map<Node*, Position> neighbors_inverted;

// public:

//     Neighbors() = default;

//     bool is_neighbor(Node* node)
//     {
//         return neighbors_inverted.find(node) != neighbors_inverted.end();
//     }

//     bool is_neighbor(Position position)
//     {
//         return neighbors.find(position) != neighbors.end();
//     }

//     void add(Node* node)
//     {
//         Position position = node->get_position();
//         neighbors[position] = node;
//         neighbors_inverted[node] = position;
//     }

//     void remove(Node* node) {
//         Position position = neighbors_inverted[node];
//         neighbors.erase(position);
//         neighbors_inverted.erase(node);
//     }

//     /* Retrieve existing neighbors */
//     std::vector<Node*> get_neighbors() {
//         std::vector<Node*> neighbor_nodes;
//         neighbor_nodes.reserve(neighbors.size());
//         for (const auto& entry : neighbors_inverted) {
//             neighbor_nodes.push_back(entry.first);
//         }
//         return neighbor_nodes;
//     }

//     /* Sync the relation between `Position` and `Node` */
//     void update() {
//         std::unordered_map<Node*, Position> old_neighbors = neighbors_inverted;
//         neighbors.clear();
//         neighbors_inverted.clear();

//         for (const auto& entry : old_neighbors) {
//             Node* node = entry.first;
//             add(node); // Let the adder handle putting it back
//         }
//     }
// };

// Definition of connect member function
// void Node::connect(Node* node)
// {
//     if (neighbors && !neighbors->is_neighbor(node)) {
//         neighbors->remove(node);
//     }
// }

void Node::connect(Node* node) {
    if (neighbors && !neighbors->is_neighbor(node)) {
        neighbors->add(node);
    }
}


/*
Bi-directional map to store entries efficiently
*/
template <typename KeyType, typename ValueType>
class BiDirectionalMap
{
public:
    void insert(const KeyType &key, const ValueType &value)
    {
        forwardMap[key] = value;
        reverseMap[value] = key;
    }

    const ValueType &getValueByKey(const KeyType &key) const
    {
        auto it = forwardMap.find(key);
        if (it != forwardMap.end())
        {
            return it->second;
        }
        throw std::out_of_range("Key not found.");
    }

    const KeyType &getKeyByValue(const ValueType &value) const
    {
        auto it = reverseMap.find(value);
        if (it != reverseMap.end())
        {
            return it->second;
        }
        throw std::out_of_range("Value not found.");
    }

    bool containsKey(const KeyType &key) const
    {
        return forwardMap.find(key) != forwardMap.end();
    }

    bool containsValue(const ValueType &value) const
    {
        return reverseMap.find(value) != reverseMap.end();
    }

private:
    std::unordered_map<KeyType, ValueType> forwardMap;
    std::unordered_map<ValueType, KeyType> reverseMap;
};

int main()
{
    Node node1(1, 2); // Position: (1, 2)
    Node node2(3, 4); // Position: (3, 4)
    Node node3(5, 6); // Position: (5, 6)
    
    BiDirectionalMap<int, std::string> bimap;

    bimap.insert(1, "One");
    bimap.insert(2, "Two");
    bimap.insert(3, "Three");

    std::cout << bimap.getValueByKey(2) << std::endl;       // Output: Two
    std::cout << bimap.getKeyByValue("Three") << std::endl; // Output: 3

    if (bimap.containsKey(1))
    {
        std::cout << "Key 1 exists" << std::endl;
    }

    if (bimap.containsValue("Four"))
    {
        std::cout << "Value Four exists" << std::endl;
    }
    else
    {
        std::cout << "Value Four does not exist" << std::endl; // Output: Value Four does not exist
    }

    Position pos(0, 0);

    Position new_pos = pos.convert_direction(Direction::LEFT);

    std::cout << (node1 == node1) << std::endl;

    node1.connect(&node2);

    // node1.get_neighbors()

    for (const auto& entry : node1.get_neighbors()) {
        Node* node = entry;
        std::cout << node << std::endl;
        // add(node); // Let the adder handle putting it back
    }

    return 0;
}
