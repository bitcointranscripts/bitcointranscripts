---
title: CAmount
tags:
  - bitcoin-core
  - refactoring
date: 2026-05-07
---

AKA: F---ing with people's money.
(Too see if we can catch bugs before they get released).

```c++
typedef int64_t CAmount;
```

## Inspiration

Recent bugfix mixing boolean values with `CAmount`

(Abbreviated version of diff).

```diff
- if (CAmount total = available.GetTotalAmount() - total_discarded < value_to_select) {
+ if (CAmount total = available.GetTotalAmount() - total_discarded;
+     total < value_to_select) {
```

## Approach being explored

```diff
- typedef int64_t CAmount;
+ class Amount
```

## Benefits

Making amounts a `class` allows imposing more rigor:

- Disallowing direct operations involving boolean/floating point
- Enforcing always specifying an initial value
- Making the constructor `explicit`
- Typed operations:

```c++
Amount a = true; // <- No longer compiles
Amount * int64_t -> Amount  // Increases magnitude
Amount / Amount  -> int64_t // Returns untyped ratio
```

## C++ Quiz (1/2)

What is wrong with the following `Amount` implementation?

```c++
// Compressed version of function on master - /src/util/overflow.h
template <class T>
[[nodiscard]] T SaturatingAdd(const T i, const T j) noexcept
{
    if constexpr (std::numeric_limits<T>::is_signed) {
        if (i > 0 && j > std::numeric_limits<T>::max() - i) return std::numeric_limits<T>::max();
        if (i < 0 && j < std::numeric_limits<T>::min() - i) return std::numeric_limits<T>::min();
    } else {
        if (std::numeric_limits<T>::max() - i < j) return std::numeric_limits<T>::max();
    }
    return i + j;
}

struct Amount {
    int64_t inner;
    Amount operator+(Amount other) const { return Amount{.inner = inner + other.inner}; }
    Amount operator-(Amount other) const { return Amount{.inner = inner - other.inner}; }
    constexpr auto operator<=>(const Amount& other) const noexcept = default;
};

int main() {
    Amount a{.inner = 1};
    Amount b{.inner = 2};
    printf("1 + 2 = %ld\n", SaturatingAdd(a, b).inner);
}
```

Full version with `#include`s and execution: https://godbolt.org/z/odnhsTEPr

```
1 + 2 = 0
```

Takeaway - `std::numeric_limits` default implementation sucks, returning zero
for `min()` & `max()` rather than compile errors. - Tread lightly when
implementing numeric-ish types.

## Making incorrect things impossible

```C++
class TxOut
{
public:
    CAmount nValue;
    ...
```

## Making incorrect things impossible

```C++
class TxOut
{
public:
    UAmount nValue;
    ...
```

## C++ Quiz (2/2)

Behavior with types on master - what is the printed string?

```C++
#include <cstdint>
#include <iostream>
#include <vector>

typedef int64_t CAmount;

int main() {
    std::vector<int> a{1, 2, 3};
    CAmount b{-2};
    auto c = a.size() * b;
    std::cout << "c = " << c << '\n';
    return 0;
}
```

Answer: It depends - https://godbolt.org/z/cbev8avK5

Multiplying unsigned size_t by CAmount on master will result in a signed integer
on 32-bit platforms (`-6`), but a very large unsigned integer on 64-bit
platforms.

By having separate signed `Amount` and unsigned `UAmount` we can avoid weird
results like what happened in the quiz.

- `UAmount` simply only allows mul/div/mod with unsigned integer types.

- `Amount` only allows these operations with *smaller* unsigned integer types,
  or equally sized signed integers.

Current approach:

```C++
UAmount + UAmount -> UAmount
UAmount - UAmount -> Amount

(UAmount - UAmount).AssertToUnsigned() -> UAmount
(UAmount - UAmount).TruncateToUnsigned() -> UAmount
(UAmount - UAmount).TryToUnsigned() -> std::optional<UAmount>
```

Also possibly:

```C++
// Making conversions to signed explicit, probably don't need all.
UAmount.AssertToSigned() -> Amount
UAmount.TruncateToSigned() -> Amount
UAmount.TryToSigned() -> std::optional<Amount>
```

## In the same vein as `"deadf00d"_hex`

What if we introduce C++11 User Defined Literals for amounts?

```C++
// From master - /src/test/miniminer_tests.cpp
const CAmount low_fee{CENT/2000}; // 500 ṩ
const CAmount med_fee{CENT/200}; // 5000 ṩ
const CAmount high_fee{CENT/10}; // 100_000 ṩ
```

Becomes:

```C++
const Amount low_fee{     500_sats};
const Amount med_fee{   5'000_sats};
const Amount high_fee{100'000_sats};
```

Possibly even:

```C++
constexpr UAmountLiteral low_fee{     500_sats};
constexpr UAmountLiteral med_fee{   5'000_sats};
constexpr UAmountLiteral high_fee{100'000_sats};
```

Allow `_BTC` for tests *only*:

```diff
- auto result = AttemptSelection(wallet.chain(), 1002.99 * COIN, group, ...);
+ auto result = AttemptSelection(wallet.chain(), 1002.99_BTC, ...);
```

Float-type UDLs are represented as `long double`. `double` itself *commonly* is
an IEEE 754 64-bit type with ~53 bits for the mantissa, we only need 50 bits to
represent 21 * 10^6 * 10^8 satoshis. Possible reason we have 21M BTC?

Potentially even stricter:

```C++
Amount modified_fee{-10_sats};
Amount modified_fee{-10}; // No longer allowed
// Requires more explicit conversion from runtime-determined integers.
Amount modified_fee{Amount::From(-10)};
```

## Pain point

- `PrioritizeTransaction()`-RPC - Allows modifying the fee of a transaction to
  be treated as negative.
- `CFeeRate::GetFee()` can be negative which needs to be explicitly converted in
  some places.

```C++
class CTxMemPoolEntry {
	const UAmount nFee;
	mutable Amount m_modified_fee;
	...
```

## Pain point

- Adding `U`-suffixes all over:

```diff
-    t1.vout[0].nValue = 90 * COIN;
+    t1.vout[0].nValue = 90U * COIN;
```

## Fin

Assigning boolean value to CAmount (int64_t)

Alternative solution to implementing a class could be to lean more on compiler
warnings and/or Clang-tidy. Doesn't need to be an either/or thing.

## Real Fin

UBSAN & friends along with tests perform a remarkable job already.

This aspect of the code appears to be in quite good shape.
Haven't uncovered anything major, *yet*.

Similar work:
https://github.com/purpleKarrot/std-bitcoin/blob/master/0-PRIMITIVES.md#bitcoinamount-class-amount

## Feedback on presentation

- Java got it right - only having signed integers. (Some) C++ committee members
  regret returning unsigned sizes for containers.

- Mixing signed and unsigned types is problematic due to the resulting type
  becoming unsigned for equally sized types. Instead of having UAmount with
  constraints on multiplication with large signed types, we should have a signed
  type which ensures keeping within the valid range: `0 <= amount <= 21M BTC`

- Gradual rollout, still using old name, first making some operations like
  multiplying two amounts illegal, disallowing operations with unexpected types,
  then requiring explicit construction later.

- Maybe fall back to plain int64_t when negative values are required, like for
  modified fees.

- The reason for 21M BTC is correctly due to wanting to enable JavaScript to
  represent numeric values of BTC. It uses `double` for all numbers.

- Would be good to catch invalid IPC amount values before even calling the
  operation taking them.
