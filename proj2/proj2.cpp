#include <iostream>
#include <vector>
#include <queue>

using namespace std;

typedef struct Node {
   int depth;         
   int seen;        
} Node;


// Read the input
// O(m*l), m is the number of lines, l is the number of stations
int read_input(int &n, int &l, vector<vector<int>> &lines_graph, vector<vector<int>> &lines) {
   ios::sync_with_stdio(0);
   cin.tie(0);
   int m;

   // Read the first line
   cin >> n >> m >> l;

   // If there are no lines, or the graph is not connected
   if (l == 0 || n-1 > m)
      return 1;

   // Initialize the vectors
   // O(l + n)
   lines.resize(l, vector<int>());
   lines_graph.resize(l, vector<int>(l, 0));
   vector<vector<int>> points_to_lines(n, vector<int>());

   // Read the input
   // O(m)
   for (int i = 0; i < m; i++) {
      int x, y, line;
      cin >> x >> y >> line;
      x--; y--; line--;

      // If the line is empty or the last station is different from x, we add x to the line
      if (lines[line].empty() || (lines[line].back() != x))
         lines[line].push_back(x);
      lines[line].push_back(y);


      int a = points_to_lines[x].size();
      if (a == 0) {
         points_to_lines[x].push_back(line);
      } else if (points_to_lines[x][a-1] != line) { // If the last line is different from the current line, we add the line to the station
         points_to_lines[x].push_back(line);  
         for (int i = 0; i < a; i++) {              // Connect the lines that share the station, O(l)
            lines_graph[points_to_lines[x][i]][line] = 1;
            lines_graph[line][points_to_lines[x][i]] = 1;
         }       
      }
      
      int b = points_to_lines[y].size();
      if (b == 0) {
         points_to_lines[y].push_back(line);
      } else if (points_to_lines[y][b-1] != line) {
         points_to_lines[y].push_back(line);
         for (int i = 0; i < b; i++) {
            lines_graph[points_to_lines[y][i]][line] = 1;
            lines_graph[line][points_to_lines[y][i]] = 1;      
         }
      }
   }      

   return 0;
}

// Convert the matrix to an adjency list
// O(l^2), l is the number of lines
vector<vector<int>> matrix_to_adjency_list(const vector<vector<int>>& matrix, const int l) {
   vector<vector<int>> adjency_list(l, vector<int>());

   for (int i = 0; i < l; i++)
      for (int j = 0; j < l; j++)
         if (matrix[i][j] == 1)
            adjency_list[i].push_back(j);

   return adjency_list;
}

// Breadth-first search
// O(n*l + l^2), n is the number of stations, l is the number of lines
int bfs(const vector<vector<int>> &stations_by_line, const vector<vector<int>> &adjency_list, const int n, const int l, const int start) {

   // Initialize the vectors
   // O(n + l)
   vector<Node> stations(n, {0, 0});
   vector<Node> lines(l, {0, 0});
   queue<int> q;
   int max_depth = 0;

   q.push(start);
   lines[start].seen = 1;
   // Análise separada 
   while (!q.empty()) { 
      int u = q.front();
      q.pop();

      // O(n), n is the max number of stations in one line
      for (size_t i = 0; i < stations_by_line[u].size(); i++) {  
         Node &station = stations[stations_by_line[u][i]];
         if (station.seen == 0) {
            station.seen = 1;
            station.depth = lines[u].depth;
         }
      }

      // O(l^2), l^2 is the max edges in the graph
      for (size_t i = 0; i < adjency_list[u].size(); i++) {    
         int v = adjency_list[u][i];
         Node &line = lines[v];
         if (line.seen == 0) {
            line.seen = 1;
            line.depth = lines[u].depth + 1;
            q.push(v);
         }
      }
   }

   // O(n), n is the number of stations
   for (int i = 0; i < n; i++) {
      // One of the stations is unreachable
      if (stations[i].seen == 0)
         return -1;
      if (stations[i].depth > max_depth)
         max_depth = stations[i].depth;
   }

   return max_depth;
}

// Main function
// Total complexity: O(m*l) + O(l^2) + O(n*l + l^2) * O(l) = O(m*l + n*l^2 + l^2 + l^3) = O(m*l + n*l^2 + l^3)
int main() {
   int n, l;
   vector<vector<int>> lines_graph;
   vector<vector<int>> lines; 

   // O(m*l), m is the number of lines, l is the number of stations
   if (read_input(n, l, lines_graph, lines) == 1) {
      cout << -1 << endl;
      return 0;
   }

   vector<vector<int>> adjency_list = matrix_to_adjency_list(lines_graph, l);

   int max = 0;
   for (int i = 0; i < l; i++) { // O(l)
      // If the line is empty, we skip it, would not make sense from a line with no stations
      // that means it is not connected to any other line
      if (lines[i].empty() == true)
         continue;

      // Get max deph of the bfs from the line i
      int result = bfs(lines, adjency_list, n, l, i); // O(n + l^2)
      if (result == -1 || result == 0) {
         cout << result << endl;
         return 0;
      }
      if (result > max)
         max = result;
   }

   cout << max << endl;

   return 0;
}
