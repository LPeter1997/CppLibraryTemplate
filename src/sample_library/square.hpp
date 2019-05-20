/**
 * square.hpp
 *
 * Copyright (c) 2019 Peter Lenkefi
 * Distributed under the MIT License.
 *
 * Performs squaring a number.
 */

#ifndef SAMPLE_LIBRARY_SQUARE_HPP
#define SAMPLE_LIBRARY_SQUARE_HPP

#include "detail/identity.hpp"

namespace samplib {

template <typename T>
T square(T const& val) {
    return detail::identity(val * val);
}

} /* namespace samplib */

#endif /* SAMPLE_LIBRARY_SQUARE_HPP */
