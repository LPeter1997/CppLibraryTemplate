/**
 * identity.hpp
 *
 * Copyright (c) 2019 Peter Lenkefi
 * Distributed under the MIT License.
 *
 * A sample detail library file.
 */

#ifndef SAMPLE_LIBRARY_DETAIL_IDENTITY_HPP
#define SAMPLE_LIBRARY_DETAIL_IDENTITY_HPP

namespace samplib {
namespace detail {

template <typename T>
T identity(T val) {
    return val;
}

} /* namespace detail */
} /* namespace samplib */

#endif /* SAMPLE_LIBRARY_DETAIL_IDENTITY_HPP */
