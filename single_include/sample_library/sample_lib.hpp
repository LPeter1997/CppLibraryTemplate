/**
 * sample_lib.hpp
 *
 * Version: 0.0.1
 *
 * This file has been merged from multiple source files.
 * Generation date: 2019-05-20T18:05:07
 *
 * Copyright (c) 2019 Peter Lenkefi
 * Distributed under the MIT License.
 *
 * A sample single-header release library template.
 */

#ifndef SAMPLE_LIBRARY
#define SAMPLE_LIBRARY

namespace samplib {
namespace detail {

template <typename T>
T identity(T val) {
    return val;
}

} /* namespace detail */
} /* namespace samplib */

namespace samplib {

/**
 * Squares the provided argument.
 * @param val A value that supports operator* with it's same kind.
 * @return The equivalent to val * val.
 */
template <typename T>
T square(T const& val) {
    return detail::identity(val * val);
}

} /* namespace samplib */

#endif /* SAMPLE_LIBRARY */