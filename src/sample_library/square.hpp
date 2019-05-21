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

/**
 * Squares the provided argument.
 * @param val A value that supports operator* with it's same kind.
 * @return The equivalent to val * val.
 */
template <typename T>
T square(T const& val) noexcept {
    return detail::identity(val * val);
}

} /* namespace samplib */

#endif /* SAMPLE_LIBRARY_SQUARE_HPP */
