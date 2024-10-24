from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import minitorch
import minitorch.scalar  # Ensure scalar is imported if it's a submodule

from . import operators
from .autodiff import Context

if TYPE_CHECKING:
    from typing import Tuple

    from .scalar import Scalar, ScalarLike


def wrap_tuple(x: object) -> Tuple:  # type: ignore
    """Turn a possible value into a tuple."""
    if isinstance(x, tuple):
        return x
    return (x,)


def unwrap_tuple(x: Tuple) -> object:  # type: ignore
    """Turn a singleton tuple into a value."""
    if len(x) == 1:
        return x[0]
    return x


class ScalarFunction:
    """A wrapper for a mathematical function that processes and producesScalar variables."""

    @classmethod
    def _backward(cls, ctx: Context, d_out: float) -> Tuple[float, ...]:
        return wrap_tuple(cls.backward(ctx, d_out))  # type: ignore

    @classmethod
    def _forward(cls, ctx: Context, *inps: float) -> float:
        return cls.forward(ctx, *inps)  # type: ignore

    @classmethod
    def apply(cls, *vals: "ScalarLike") -> Scalar:
        """Apply the scalar function to the input values."""
        raw_vals = []
        scalars = []
        for v in vals:
            if isinstance(v, minitorch.scalar.Scalar):
                scalars.append(v)
                raw_vals.append(v.data)
            else:
                scalars.append(minitorch.scalar.Scalar(v))
                raw_vals.append(v)

        # Create the context.
        ctx = Context(False)

        # Call forward with the variables.
        c = cls._forward(ctx, *raw_vals)
        assert isinstance(c, float), "Expected return type float got %s" % (type(c))

        # Create a new variable from the result with a new history.
        back = minitorch.scalar.ScalarHistory(cls, ctx, scalars)
        return minitorch.scalar.Scalar(c, back)


# Examples
class Add(ScalarFunction):
    """Addition function $f(x, y) = x + y$."""

    @staticmethod
    def forward(ctx: Context, a: float, b: float) -> float:
        """Forward pass."""
        return a + b

    @staticmethod
    def backward(ctx: Context, d_output: float) -> Tuple[float, ...]:
        """Backward pass."""
        return d_output, d_output


class Log(ScalarFunction):
    """Log function $f(x) = log(x)$."""

    @staticmethod
    def forward(ctx: Context, a: float) -> float:
        """Forward pass."""
        ctx.save_for_backward(a)
        return operators.log(a)

    @staticmethod
    def backward(ctx: Context, d_output: float) -> float:
        """Backward pass."""
        (a,) = ctx.saved_values
        return operators.log_back(a, d_output)


# To implement.


class Mul(ScalarFunction):
    """Multiplication function."""

    @staticmethod
    def forward(ctx: Context, a: float, b: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        ctx.save_for_backward(a, b)
        return operators.mul(a, b)

    @staticmethod
    def backward(ctx: Context, d_output: float) -> Tuple[float, float]:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        # The derivative of x * y with respect to x is y and with respect to y is x.
        (a, b) = ctx.saved_values
        return b * d_output, a * d_output


class Inv(ScalarFunction):
    """Inverse function."""

    @staticmethod
    def forward(ctx: Context, a: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        ctx.save_for_backward(a)
        return operators.inv(a)

    @staticmethod
    def backward(ctx: Context, d_output: float) -> float:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        (a,) = ctx.saved_values
        return operators.inv_back(a, d_output)


class Neg(ScalarFunction):
    """Negation function."""

    @staticmethod
    def forward(ctx: Context, a: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        return operators.neg(a)

    @staticmethod
    def backward(ctx: Context, d_output: float) -> float:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        # The derivative of -x with respect to x is -1.
        return -d_output


class Sigmoid(ScalarFunction):
    """Sigmoid function."""

    @staticmethod
    def forward(ctx: Context, a: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        sig = operators.sigmoid(a)
        ctx.save_for_backward(sig)
        return sig

    @staticmethod
    def backward(ctx: Context, d_output: float) -> float:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        # The derivative of sigmoid(x) with respect to x is sigmoid(x) * (1 - sigmoid(x)).
        (sig,) = ctx.saved_values
        result: float = sig * (1 - sig) * d_output
        return result


class ReLU(ScalarFunction):
    """ReLU function."""

    @staticmethod
    def forward(ctx: Context, a: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        ctx.save_for_backward(a)
        return operators.relu(a)

    @staticmethod
    def backward(ctx: Context, d_output: float) -> float:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        # The derivative of exp(x) with respect to x is exp(x).
        (a,) = ctx.saved_values
        return operators.relu_back(a, d_output)


class Exp(ScalarFunction):
    """Exp function."""

    @staticmethod
    def forward(ctx: Context, a: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        exp = operators.exp(a)
        ctx.save_for_backward(exp)
        return exp

    @staticmethod
    def backward(ctx: Context, d_output: float) -> float:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        # The derivative of x < y with respect to x is 0 and with respect to y is 0.
        (exp,) = ctx.saved_values
        result: float = exp * d_output
        return result


class LT(ScalarFunction):
    """Less-than function $f(x) =$ 1.0 if x is less than y else 0.0."""

    @staticmethod
    def forward(ctx: Context, a: float, b: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        return operators.lt(a, b)

    @staticmethod
    def backward(ctx: Context, d_output: float) -> Tuple[float, float]:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        # The derivative of x < y with respect to x is 0 and with respect to y is 0.
        return 0.0, 0.0


class EQ(ScalarFunction):
    """Equal function $f(x) =$ 1.0 if x is equal to y else 0.0."""

    @staticmethod
    def forward(ctx: Context, a: float, b: float) -> float:
        """Forward pass."""
        # TODO: Implement for Task 1.2.
        return operators.eq(a, b)

    @staticmethod
    def backward(ctx: Context, d_output: float) -> Tuple[float, float]:
        """Backward pass."""
        # TODO: Implement for Task 1.4.
        # The derivative of x == y with respect to x is 0 and with respect to y is 0.
        return 0.0, 0.0
