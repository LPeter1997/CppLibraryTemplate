/**
 * sample_lib.hpp
 *
 * Version: 0.0.1
 *
 * This file has been merged from multiple source files.
 * Generation date: 2019-05-26T11:29:24
 * Project home page: https://github.com/LPeter1997/CppLibraryTemplate
 *
 * Copyright (c) 2019 Peter Lenkefi
 * Distributed under the MIT License.
 *
 * A sample header-only C++ library template.
 */

#ifndef SAMPLE_LIBRARY
#define SAMPLE_LIBRARY

namespace samplib {
namespace detail {

template <typename T>
T identity(T val) noexcept {
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
T square(T const& val) noexcept {
    return detail::identity(val * val);
}

} /* namespace samplib */

#endif /* SAMPLE_LIBRARY */