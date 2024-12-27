#include <iostream>
#include <string>
#include <tuple>
#include <vector>

void readValues(int &n, int &m, int &target, std::vector<int> &seq,
                std::vector<std::vector<int>> &operations) {
   std::ios_base::sync_with_stdio(false);
   std::cin.tie(nullptr);

   std::cin >> n >> m;
   seq.resize(m);
   operations.resize(n + 1, std::vector<int>(n + 1));

   for (int i = 1; i <= n; i++) {
      for (int j = 1; j <= n; j++) {
         std::cin >> operations[i][j];
      }
   }

   for (int i = 0; i < m; i++) {
      std::cin >> seq[i];
   }

   std::cin >> target;
}

void constructTable(
    int n, int m, int target, std::vector<int> &seq, std::vector<std::vector<int>> &operations,
    std::vector<std::vector<std::vector<std::pair<int, std::tuple<int, int, int>>>>> &dp) {

   for (int i = 0; i < m; i++) {
      dp[i][i].push_back(std::make_pair(seq[i], std::make_tuple(0, 0, 0)));
   }

   for (int count = 1; count < m; count++) {
      for (int i = 0; i < m - count; i++) {
         int j    = i + count;
         int news = 0;
         std::vector<bool> s(n + 1);
         for (int k = j - 1; k >= i; k--) {
            if (news == n)
               break;
            std::vector<std::pair<int, std::tuple<int, int, int>>> left  = dp[i][k];
            std::vector<std::pair<int, std::tuple<int, int, int>>> right = dp[k + 1][j];
            for (size_t l = 0; l < left.size(); l++) {
               if (news == n)
                  break;
               for (size_t r = 0; r < right.size(); r++) {
                  if (news == n)
                     break;
                  int result = operations[left[l].first][right[r].first];
                  if (!s[result]) {
                     dp[i][j].push_back(std::make_pair(result, std::make_tuple(l, k, r)));
                     s[result] = true;
                     news++;
                  }
               }
            }
         }
      }
   }
}

std::string
getResult(std::vector<std::vector<std::vector<std::pair<int, std::tuple<int, int, int>>>>> &dp,
          int p, std::vector<int> &seq, int i, int j) {
   std::string result;
   if (i == j) {
      result = std::to_string(seq[i]);
   } else {
      int left  = std::get<0>(dp[i][j][p].second);
      int k     = std::get<1>(dp[i][j][p].second);
      int right = std::get<2>(dp[i][j][p].second);
      result =
          "(" + getResult(dp, left, seq, i, k) + " " + getResult(dp, right, seq, k + 1, j) + ")";
   }
   return result;
}

int main() {
   int n, m, target;
   std::string result;
   std::vector<int> seq;
   std::vector<std::vector<int>> operations;

   readValues(n, m, target, seq, operations);

   if (m == 1) {
      if (seq[0] == target) {
         std::cout << 1 << std::endl;
         std::cout << seq[0] << std::endl;
         return 0;
      } else {
         std::cout << 0 << std::endl;
         return 0;
      }
   }

   std::vector<std::vector<std::vector<std::pair<int, std::tuple<int, int, int>>>>> dp;
   dp.resize(m + 1, std::vector<std::vector<std::pair<int, std::tuple<int, int, int>>>>(m + 1));

   constructTable(n, m, target, seq, operations, dp);

   for (size_t p = 0; p < dp[0][m - 1].size(); p++) {
      if (dp[0][m - 1][p].first == target) {
         std::tuple<int, int, int> t = dp[0][m - 1][p].second;
         result = "(" + getResult(dp, std::get<0>(t), seq, 0, std::get<1>(t)) + " " +
                  getResult(dp, std::get<2>(t), seq, std::get<1>(t) + 1, m - 1) + ")";
         std::cout << 1 << std::endl;
         std::cout << result << std::endl;
         return 0;
      }
   }

   std::cout << 0 << std::endl;

   return 0;
}