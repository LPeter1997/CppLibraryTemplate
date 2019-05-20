#include <catch2/catch.hpp>
#include <sample_library/sample_lib.hpp>

TEST_CASE("squaring a means a*a", "[square]") {
    REQUIRE(samplib::square(1) == 1);
    REQUIRE(samplib::square(2) == 4);
    REQUIRE(samplib::square(3) == 9);
}

TEST_CASE("squaring a negative becomes positive", "[square]") {
    REQUIRE(samplib::square(-1) == 1);
    REQUIRE(samplib::square(-2) == 4);
}
