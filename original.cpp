#include <fstream>
#include <string>
#include <iostream>
#include <queue>  
#include <vector> 
#include <unordered_map>
#include <stack> 
#include <set> 
#include <algorithm>
#include <list>
#include <boost/program_options.hpp>
using namespace std;
namespace po = boost::program_options;

struct edge {
    int source;
    int target;
    int slength;
    int tlength;
    int overlap;
    char sorient;
    char torient;
}; // struct edge

void printValues(const std::unordered_map<int, int>& mapping_components, const std::unordered_map<int, std::set<int>>& component_members) {
    std::cout << "Values in mapping_components:" << std::endl;
    for (const auto& pair : mapping_components) {
        std::cout << pair.second << " ";
    }
    std::cout << std::endl;

    std::cout << "Values in component_members:" << std::endl;
    for (const auto& pair : component_members) {
        const std::set<int>& members = pair.second;
        for (int value : members) {
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }
}

void relabel_components(int curr_read, const bool incoming, const std::list<edge>& edge_list, 
                        std::unordered_map<int, int>&  mapping_components, 
                        std::unordered_map<int, std::set<int> >&  component_members, 
                        const std::set<int>& removed_nodes) {

  // Find the minimum root id
  int min_root = mapping_components[curr_read]; 
  for(edge e : edge_list) {
    int neighbor = e.source; 
    if (!incoming) neighbor = e.target;
    int neighbor_root = mapping_components[neighbor];
    if (removed_nodes.find(neighbor_root) != removed_nodes.end()) continue;  
    if (neighbor_root < min_root) min_root = neighbor_root;
  }

  // Handle the current read 
  component_members[min_root].insert(curr_read);
  if(min_root != mapping_components[curr_read]) {
    int prev_root = mapping_components[curr_read];
    for(int member : component_members[prev_root]) {
      mapping_components[member] = min_root;
      component_members[min_root].insert(member);
    }
    component_members.erase(prev_root);
  }
  
  // Handle all of the current read's neighbors 
  for(edge e : edge_list) {
    int neighbor = e.source; 
    if (!incoming) neighbor = e.target; 
    if (mapping_components[neighbor] == min_root) continue; 
    int prev_root = mapping_components[neighbor];
    for(int member : component_members[prev_root]) {
      mapping_components[member] = min_root;
      component_members[min_root].insert(member);
    }
    component_members.erase(prev_root);
  }
}

void update_components(int curr_read, const std::list<edge>& incoming_edges, const std::list<edge>& outgoing_edges, const std::set<int>& removed_nodes, std::unordered_map<int, int>&  mapping_components, std::unordered_map<int, std::set<int> >&  component_members) {
  if (removed_nodes.find(curr_read) != removed_nodes.end()) {
    return;
  } 
  
  // The current read starts off as its own component 
  mapping_components[curr_read] = curr_read; 
  component_members[curr_read] = std::set<int>(); 
  component_members[curr_read].insert(curr_read);

  relabel_components(curr_read, true, incoming_edges, mapping_components, component_members, removed_nodes);
  relabel_components(curr_read, false, outgoing_edges, mapping_components, component_members, removed_nodes);


  // Updates nodes affected by transitive closures
  for(int removed_node : removed_nodes) {
    int root_of_removed_node = mapping_components[removed_node]; 
    if (component_members.find(root_of_removed_node) != component_members.end()) {
      component_members[root_of_removed_node].erase(removed_node);
    }

    if (component_members.find(removed_node) != component_members.end()) {
      for (auto removed_node_member : component_members[removed_node]) {
        if (removed_nodes.find(removed_node_member) == removed_nodes.end()) {
          component_members[mapping_components[curr_read]].insert(removed_node_member);
          mapping_components[removed_node_member] = mapping_components[curr_read];
        }
      }
      component_members.erase(removed_node);
    }

    mapping_components.erase(removed_node); 
  }
  printValues(mapping_components, component_members);
}

edge createEdgeFromLine(const string& line) {
    edge e;
    istringstream iss(line);
    iss >> e.source >> e.target >> e.slength >> e.tlength >> e.overlap >> e.sorient >> e.torient;
    return e;
}

list<edge> processEdges(ifstream& file) {
    string line;
    list<edge>edges;
    while (getline(file, line)) {
        if (line == "edges_end") {
            return edges; 
        }
        edges.push_back(createEdgeFromLine(line));
    }
    return edges;
}

set<int> stringToSet(const std::string& str) {
    set<int> intSet;
    stringstream iss(str);
    int num;
    while (iss >> num) {
        intSet.insert(num);
    }
    return intSet;
}

set<int> processSet(ifstream& file) {
    string line;
    getline(file, line);
    return stringToSet(line);
}

int main(int argc, char* argv[]) {
    std::ifstream file(argv[1]);
    string line;
    int curr_read;
    set<int>removed_nodes;
    list<edge>incoming_edges;
    list<edge>outgoing_edges;
    unordered_map<int, int>mapping_components;
    unordered_map<int, set<int> >component_members;
    while(getline(file, line)){
        curr_read = stoi(line);
        removed_nodes = processSet(file);
        incoming_edges = processEdges(file);
        outgoing_edges = processEdges(file);
        update_components(curr_read, incoming_edges, outgoing_edges, removed_nodes, mapping_components, component_members);
    }
}