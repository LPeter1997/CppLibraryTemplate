/**
 * clisquare.cpp
 *
 * Copyright (c) 2018-2019 Peter Lenkefi
 * Distributed under the MIT License.
 *
 * Example usage of the sample library, a simple Command-Line-Interface
 * application that squares the argument and prints it.
 */

#include <cstdio>
#include <cstdlib>
#include <sample_library/sample_lib.hpp>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::printf("Usage: %s <integer>\n", argv[0]);
        return 1;
    }
    int num = std::atoi(argv[1]);
    int sq = samplib::square(num);
    std::printf("%d\n", sq);
    return 0;
}
